#!/usr/bin/env python3
"""アプリの画面を自動で遷移しながら、各画面のUI要素とIDの有無を記録するクローラー。

出力:
  crawl/<app>/screens.json   画面ごとの要素一覧と遷移グラフ
  crawl/<app>/report.md      画面マップ・ID充足率・ID付与依頼リスト
  crawl/<app>/shots/*.png    各画面のスクリーンショット

安全ルール:
  - ラベルに BLOCK_WORDS を含むボタンは押さない（記録のみ）。ただしタイル型UI（ラベルが兄弟要素）は
    画面を開くだけの導線とみなして押す
  - ラベルもIDもないボタン、ポップアップ、チェックボックス、テキスト入力、メニューバーは触らない
  - メインウインドウ（起動時の最前面ウインドウ）は絶対に閉じない
  - 深さ MAX_DEPTH まで。復帰は キャンセル/閉じる/戻る/ホーム → Esc → (メイン以外の)ウインドウを閉じる の順
  - 既知の画面に戻ってしまった場合は、メインからの経路を再生して探索中の画面に戻る
使い方:
  ./.venv/bin/python ax_crawl.py com.brother.iprint-and-scan
"""
import argparse
import hashlib
import json
import os
import subprocess
import time

import Quartz
from ax_driver import App, NotFound

BLOCK_WORDS = ["プリント", "印刷", "スキャン", "送信", "削除", "更新", "リセット", "保存",
               "開始", "OK", "実行", "適用", "登録", "接続", "購入", "注文", "ワークフロー", "再検索",
               "取り出す", "開く", "完了", "次へ", "標準に戻す", "初期", "デフォルト", "既定"]
SAME_SCREEN_SIMILARITY = 0.85  # 操作対象の一致率がこれ以上なら同じ画面とみなす（非同期のステータス表示等を吸収）
BLOCK_ID_WORDS = ["ok", "save", "delete", "remove", "print", "scan", "start", "apply", "submit", "done"]
# macOS 標準パネル（ファイル選択など）は記録だけして中は探索しない
LEAF_WINDOW_IDS = {"open-panel", "save-panel"}
BACK_WORDS = ["キャンセル", "閉じる", "戻る", "ホーム", "Cancel", "Close", "Back", "Home"]
CLICKABLE = {"AXButton", "AXTab", "AXRadioButton", "AXLink", "AXPopUpButton", "AXMenuButton"}
SKIP_SUBROLES = {"AXCloseButton", "AXZoomButton", "AXMinimizeButton", "AXFullScreenButton",
                 "AXIncrementArrow", "AXDecrementArrow", "AXIncrementPage", "AXDecrementPage"}
IGNORE_ROLES = {"AXMenuBar"}


def key(code):
    for down in (True, False):
        Quartz.CGEventPost(Quartz.kCGHIDEventTap, Quartz.CGEventCreateKeyboardEvent(None, code, down))


def label_of(el, siblings=None):
    """要素のラベルと、それが兄弟要素由来かどうか。

    自身に title/description がなければ、兄弟の AXStaticText のうち
    直前にあるもの（フォームのラベル）を優先し、なければ直後のもの（タイルのキャプション）を使う。
    """
    if el.title or el.description:
        return (el.title or el.description), False
    before, after = "", ""
    seen_self = False
    for s in siblings or []:
        if s.ref == el.ref:
            seen_self = True
            continue
        if s.role == "AXStaticText" and s.value:
            if not seen_self:
                before = str(s.value)
            elif not after:
                after = str(s.value)
    lab = before or after
    return (lab.strip().rstrip(":：").strip(), True) if lab else ("", False)


class Crawler:
    def __init__(self, bundle, max_depth, out_dir, max_actions):
        self.app = App(bundle)
        self.bundle = bundle
        self.max_depth = max_depth
        self.max_actions = max_actions
        self.out = out_dir
        os.makedirs(os.path.join(out_dir, "shots"), exist_ok=True)
        self.screens = {}      # sig -> dict
        self.transitions = []
        self.actions = 0
        self.root_sig = None
        self.root_title = None
        self.path = []         # [(sig, loc)] メインからここまでの経路

    # ---------- 待機 ----------
    def wait_stable(self, timeout=20):
        """ビジーインジケータが消え、ウインドウ構成が1秒間変わらなくなるまで待つ。"""
        deadline = time.time() + timeout
        prev = None
        while time.time() < deadline:
            ws = self.app.windows()
            busy = any(w.find_all(role="AXBusyIndicator") for w in ws)
            cur = tuple((w.title, w.identifier) for w in ws)
            if not busy and cur == prev and ws:
                return ws
            prev = cur
            time.sleep(1.0)
        return self.app.windows()

    def front(self):
        ws = self.wait_stable()
        return ws[0] if ws else None

    # ---------- 画面の観測 ----------
    def snapshot(self, win):
        rows = []
        def walk(el, depth, siblings):
            if el.role in IGNORE_ROLES:
                return
            lab, tile = label_of(el, siblings)
            rows.append(dict(depth=depth, role=el.role, subrole=el.subrole, identifier=el.identifier,
                             label=lab, tile=tile, value=None if el.value is None else str(el.value)[:60]))
            kids = el.children
            for c in kids:
                walk(c, depth + 1, kids)
        walk(win, 0, [])
        keys = set((r["role"], r["identifier"], r["label"]) for r in rows if r["role"] in CLICKABLE)
        # 既知の画面と十分似ていれば、その画面として扱う
        for sig, sc in self.screens.items():
            if sc["title"] == win.title and sc.get("keys"):
                inter = len(keys & sc["keys"]); union = len(keys | sc["keys"]) or 1
                if inter / union >= SAME_SCREEN_SIMILARITY:
                    return sig, rows
        sig = hashlib.md5(repr((win.title or "", tuple(sorted(keys, key=str)))).encode()).hexdigest()[:8]
        self._last_keys = keys
        return sig, rows

    def clickables(self, win):
        out, counts = [], {}
        def walk(el, siblings):
            kids = el.children
            if el.role in CLICKABLE and (el.subrole or "") not in SKIP_SUBROLES:
                lab, tile = label_of(el, siblings)
                k = (el.role, el.identifier, lab)
                counts[k] = counts.get(k, 0) + 1
                loc = dict(role=el.role, identifier=el.identifier, label=lab, index=counts[k] - 1, tile=tile)
                blocked = (not tile) and (any(w.lower() in lab.lower() for w in BLOCK_WORDS)
                                          or any(w in (el.identifier or "").lower() for w in BLOCK_ID_WORDS))
                unknown = not lab and not el.identifier
                popup = el.role in ("AXPopUpButton", "AXMenuButton")
                out.append((loc, "禁止語" if blocked else "手がかりなし" if unknown else "ポップアップ" if popup else None))
            for c in kids:
                walk(c, kids)
        walk(win, [])
        return out

    def find_by_locator(self, win, loc):
        n = 0
        def walk(el, siblings):
            nonlocal n
            kids = el.children
            if el.role == loc["role"] and el.identifier == loc["identifier"] and label_of(el, siblings)[0] == loc["label"]:
                if n == loc["index"]:
                    return el
                n += 1
            for c in kids:
                r = walk(c, kids)
                if r is not None:
                    return r
            return None
        return walk(win, [])

    def record_screen(self, win):
        sig, rows = self.snapshot(win)
        if sig not in self.screens:
            name = f"S{len(self.screens) + 1:02d}"
            self.screens[sig] = dict(name=name, title=win.title, window_id=win.identifier, elements=rows, skipped=[],
                                     keys=set((r["role"], r["identifier"], r["label"]) for r in rows if r["role"] in CLICKABLE))
            subprocess.run(["screencapture", "-x", os.path.join(self.out, "shots", f"{name}.png")])
            print(f"  📄 新しい画面 {name}: '{win.title}' ({len(rows)} 要素)")
        return sig

    def name(self, sig):
        return self.screens[sig]["name"] if sig in self.screens else str(sig)

    # ---------- 復帰 ----------
    def current_sig(self):
        w = self.front()
        return (self.snapshot(w)[0], w) if w is not None else (None, None)

    def go_back(self, target_sig):
        """target_sig の画面に戻る。戻れたら True。メインウインドウは閉じない。"""
        for attempt in range(5):
            sig, win = self.current_sig()
            if sig == target_sig:
                return True
            if win is None:
                time.sleep(1); continue
            pressed = False
            # 0) 過去にこの画面から target へ遷移したことのあるボタン（学習した「戻る」）
            for t in self.transitions:
                if t["from"] == sig and t.get("to") == target_sig and t.get("loc"):
                    el = self.find_by_locator(win, t["loc"])
                    if el is not None:
                        el.press(); pressed = True; break
            # 1) 戻る系のラベル
            if not pressed and attempt < 2:
                for b in win.find_all(role="AXButton"):
                    if (b.title or "") in BACK_WORDS + [self.root_title]:
                        b.press(); pressed = True; break
            # 2) 画面内ナビゲーションの最後の手段: ウインドウ左上にある無害なボタン（ホーム/戻るの定位置）
            if not pressed and attempt == 2:
                cands = []
                for loc, reason in self.clickables(win):
                    if reason in ("禁止語", "ポップアップ") or loc["role"] != "AXButton":
                        continue
                    el = self.find_by_locator(win, loc)
                    pos = el.attr("AXPosition") if el is not None else None
                    if pos is not None:
                        from ax_dump import point
                        p = point(pos)
                        if p:
                            cands.append((p[0] + p[1], el))
                if cands:
                    cands.sort(key=lambda c: c[0]); cands[0][1].press(); pressed = True
            if not pressed:
                if win.identifier != self.screens[self.root_sig]["window_id"] and attempt >= 3:
                    try:
                        win.find(role="AXButton", subrole="AXCloseButton").press(); pressed = True
                    except NotFound:
                        pass
                if not pressed:
                    key(53)  # Esc
            time.sleep(1.2)
        return self.current_sig()[0] == target_sig

    def replay_path(self, target_sig):
        """メイン画面まで戻ってから、self.path の操作を順に再生して target_sig の画面に戻る。"""
        if not self.go_back(self.root_sig):
            return False
        for sig, loc in self.path:
            win = self.front()
            el = self.find_by_locator(win, loc) if win is not None else None
            if el is None:
                return False
            el.press()
            self.wait_stable()
        return self.current_sig()[0] == target_sig

    # ---------- 探索 ----------
    def crawl(self, depth=0):
        win = self.front()
        if win is None:
            return
        sig = self.record_screen(win)
        if self.root_sig is None:
            self.root_sig, self.root_title = sig, win.title
        if depth >= self.max_depth or (win.identifier in LEAF_WINDOW_IDS):
            if win.identifier in LEAF_WINDOW_IDS:
                print(f'{"  " * depth}  (標準パネルなので中は探索しない)')
            return
        screen = self.screens[sig]
        for loc, skip_reason in self.clickables(win):
            if self.actions >= self.max_actions:
                print("  操作回数の上限に達した")
                return
            via = f'{loc["role"]} id={loc["identifier"]} label={loc["label"]!r}#{loc["index"]}'
            if skip_reason:
                screen["skipped"].append(dict(loc, reason=skip_reason))
                continue
            if any(t["from"] == sig and t["via"] == via for t in self.transitions):
                continue
            cur_sig, win = self.current_sig()
            if cur_sig != sig:
                print(f'{"  " * depth}… {screen["name"]} にいないので経路を再生')
                if not self.replay_path(sig):
                    print(f'{"  " * depth}✗ {screen["name"]} に戻れない。この画面の探索を打ち切る')
                    return
                win = self.front()
            el = self.find_by_locator(win, loc)
            if el is None:
                continue
            print(f'{"  " * depth}▶ {screen["name"]} で {via} を押す')
            self.actions += 1
            el.press()
            new_sig, new_win = self.current_sig()
            if new_sig is None:
                self.transitions.append({"from": sig, "via": via, "to": None, "note": "ウインドウ消失"})
                continue
            if new_sig == sig:
                self.transitions.append({"from": sig, "via": via, "to": sig, "note": "変化なし"})
                continue
            known = new_sig in self.screens
            self.transitions.append({"from": sig, "via": via, "to": new_sig, "note": "既知の画面へ" if known else None, "loc": loc})
            if known:
                print(f'{"  " * depth}  ↩ 既知の画面 {self.name(new_sig)} へ遷移')
            else:
                self.path.append((sig, loc))
                self.crawl(depth + 1)
                self.path.pop()
            if not self.go_back(sig):
                print(f'{"  " * depth}… 直接戻れないので経路を再生')
                if not self.replay_path(sig):
                    print(f'{"  " * depth}✗ {screen["name"]} に戻れない。この画面の探索を打ち切る')
                    return

    # ---------- レポート ----------
    def report(self):
        trans = [dict(t, **{"from": self.name(t["from"]), "to": self.name(t["to"]) if t.get("to") else None}) for t in self.transitions]
        data = dict(bundle=self.bundle, screens=[{k: v for k, v in sc.items() if k != "keys"} for sc in self.screens.values()], transitions=trans)
        with open(os.path.join(self.out, "screens.json"), "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=1)
        L = [f"# 画面マップ: {self.bundle}", "",
             f"画面 {len(self.screens)} / 遷移 {len([t for t in trans if t['to']])} / 操作回数 {self.actions}", "", "## 遷移", ""]
        for t in trans:
            L.append(f"- {t['from']} --[{t['via']}]--> {t['to']}" + (f"  ({t['note']})" if t.get("note") else ""))
        L += ["", "## 画面ごとのID充足率", "", "| 画面 | タイトル | 操作対象 | 明示ID | 自動ID | ラベルのみ | 手がかりなし |", "|---|---|---|---|---|---|---|"]
        requests = []
        for s in data["screens"]:
            els = [e for e in s["elements"] if e["role"] in CLICKABLE | {"AXCheckBox", "AXTextField", "AXTextArea", "AXSlider"} and (e["subrole"] or "") not in SKIP_SUBROLES]
            ex = [e for e in els if e["identifier"] and not e["identifier"].startswith("_NS:")]
            au = [e for e in els if e["identifier"] and e["identifier"].startswith("_NS:")]
            lb = [e for e in els if not e["identifier"] and e["label"]]
            no = [e for e in els if not e["identifier"] and not e["label"]]
            L.append(f"| {s['name']} | {s['title']} | {len(els)} | {len(ex)} | {len(au)} | {len(lb)} | {len(no)} |")
            seen = {}
            for e in au + lb + no:
                k = (e["role"], e["identifier"], e["label"]); seen[k] = seen.get(k, 0) + 1
            for (role, ident, lab), n in seen.items():
                requests.append((s["name"], s["title"], role, ident, lab, n))
        L += ["", "## ID付与依頼リスト（明示IDがない操作対象）", "", "| 画面 | 要素 | ラベル | 現在のID | 同一IDの個数 |", "|---|---|---|---|---|"]
        for name, title, role, ident, lab, n in requests:
            L.append(f"| {name} {title} | {role} | {lab or '(なし)'} | {ident or '(なし)'} | {n} |")
        L += ["", "## 押さなかったボタン", ""]
        for s in data["screens"]:
            for sk in s["skipped"]:
                L.append(f"- {s['name']} {sk['role']} label={sk['label']!r} id={sk['identifier']} — {sk['reason']}")
        with open(os.path.join(self.out, "report.md"), "w", encoding="utf-8") as f:
            f.write("\n".join(L) + "\n")
        print(f"\nレポート: {os.path.join(self.out, 'report.md')}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("bundle")
    ap.add_argument("--max-depth", type=int, default=3)
    ap.add_argument("--max-actions", type=int, default=40)
    ap.add_argument("--out", default=None)
    a = ap.parse_args()
    c = Crawler(a.bundle, a.max_depth, a.out or os.path.join("crawl", a.bundle.split(".")[-1]), a.max_actions)
    c.app.activate(); time.sleep(1.5)
    try:
        c.crawl()
    finally:
        c.go_back(c.root_sig) if c.root_sig else None
        c.report()


if __name__ == "__main__":
    main()
