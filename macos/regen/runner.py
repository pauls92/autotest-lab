"""作り直す回帰テストの実行役（決まったプログラム。AIは入らない）。

テストケース（意図と期待値）と、AIが生成したスクリプト（画面との対応表）を受け取り、
手順を順に実行して、操作の記録（log.json）とスクリーンショットを残す。

使い方（macos/ で）:
  ./.venv/bin/python regen/runner.py --testcase regen/testcases/TE-PRINT-001.json \
      --script regen/scripts/te_print_ja.py --lang ja --label ja-1
"""
import argparse, datetime, hashlib, importlib.util, json, os, subprocess, sys, time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import Quartz
from ax_driver import App, Element, NotFound

HERE = os.path.dirname(os.path.abspath(__file__))
KEYCODES = {"p": 35, "n": 45, "w": 13}


def sha256(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


def check_approval(tc_path):
    """テストケース（期待値）が承認済みかを確かめる。承認なしの変更は実行しない。"""
    ap = os.path.join(HERE, "approvals.json")
    approvals = json.load(open(ap, encoding="utf-8")) if os.path.exists(ap) else {}
    name = os.path.basename(tc_path)
    h = sha256(tc_path)
    if approvals.get(name, {}).get("sha256") != h:
        sys.exit(f"[止めます] テストケース {name} は承認された版と違います。期待値の変更には人の承認が要ります（regen/approve.py）。")
    return h


def relaunch(bundle, lang):
    subprocess.run(["osascript", "-e", 'tell application id "%s" to quit saving no' % bundle], capture_output=True)
    time.sleep(1.5)
    # 環境の準備：前回の書類を復元せず、まっさらな状態で起動する（テストの前提）
    subprocess.run(["open", "-b", bundle, "--args", "-AppleLanguages", "(%s)" % lang, "-ApplePersistenceIgnoreState", "YES"])
    time.sleep(3)


def key(combo):
    parts = combo.split("+")
    k = KEYCODES[parts[-1]]
    flags = Quartz.kCGEventFlagMaskCommand if "cmd" in parts else 0
    for down in (True, False):
        ev = Quartz.CGEventCreateKeyboardEvent(None, k, down)
        if flags:
            Quartz.CGEventSetFlags(ev, flags)
        Quartz.CGEventPost(Quartz.kCGHIDEventTap, ev)


def roots(app, within):
    """探す範囲：'sheet' = 開いている印刷シート、'document' = 本文のある書類ウインドウ、None = アプリ全体"""
    if within == "sheet":
        return [c for w in app.windows() for c in w.children if c.role == "AXSheet"]
    if within == "document":
        return [w for w in app.windows() if w.find_all(role="AXTextArea")]
    return [app]


def locate(app, candidates, timeout=8.0):
    """対応表の候補を順に試し、見つかった要素と使った候補を返す"""
    deadline = time.time() + timeout
    while time.time() < deadline:
        for cand in candidates:
            q = {k: v for k, v in cand.items() if k in ("identifier", "title", "role", "subrole")}
            for r in roots(app, cand.get("within")):
                try:
                    return r.find(**q), cand
                except NotFound:
                    pass
        time.sleep(0.3)
    raise NotFound(candidates)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--testcase", required=True)
    ap.add_argument("--script", required=True)
    ap.add_argument("--lang", default="ja")
    ap.add_argument("--label", required=True)
    ap.add_argument("--no-shots", action="store_true", help="スクリーンショットを撮らない（操作の記録だけ残す）")
    a = ap.parse_args()

    tc_hash = check_approval(a.testcase)
    tc = json.load(open(a.testcase, encoding="utf-8"))
    spec = importlib.util.spec_from_file_location("gen", a.script)
    gen = importlib.util.module_from_spec(spec); spec.loader.exec_module(gen)

    run_dir = os.path.join(HERE, "runs", a.label)
    os.makedirs(run_dir, exist_ok=True)
    relaunch(tc["app"], a.lang)
    app = App(tc["app"], launch=False).activate()

    log = {"testcase": tc["id"], "testcase_sha256": tc_hash, "script": os.path.basename(a.script),
           "script_sha256": sha256(a.script), "lang": a.lang,
           "started": datetime.datetime.now().isoformat(timespec="seconds"), "steps": [], "result": "PASS"}
    for st in tc["steps"]:
        rec = {k: st.get(k) for k in ("no", "screen", "action", "target", "value", "expect")}
        try:
            if st["action"] == "キー":
                app.activate(); key(st["value"]); rec["used"] = st["value"]
                time.sleep(1.5)
            elif st["action"] == "確認" and st.get("expect") == "閉じている":
                time.sleep(1.0)
                cand = gen.LOCATORS[st["target"]]
                try:
                    locate(app, cand, timeout=1.5); still = True
                except NotFound:
                    still = False
                rec["actual"] = "開いている" if still else "閉じている"
            else:
                el, used = locate(app, gen.LOCATORS[st["target"]])
                rec["used"] = used
                if st["action"] == "押す":
                    el.press(); time.sleep(0.8)
                elif st["action"] == "入力":
                    el.set_value(st["value"]); time.sleep(0.3)
                elif st["action"] == "確認":
                    v = el.value
                    rec["actual"] = str(int(v)) if isinstance(v, (int, float)) and not isinstance(v, bool) else str(v)
            if "expect" in st and st.get("expect") is not None:
                rec["result"] = "OK" if rec.get("actual") == st["expect"] else "NG"
            else:
                rec["result"] = "OK"
        except Exception as e:
            rec["result"] = "ERROR"; rec["error"] = f"{type(e).__name__}: {str(e)[:160]}"
        if not a.no_shots:
            shot = os.path.join(run_dir, f"step{st['no']:02d}.png")
            subprocess.run(["screencapture", "-x", shot]); subprocess.run(["sips", "-Z", "900", shot], capture_output=True)
            rec["screenshot"] = os.path.basename(shot)
        log["steps"].append(rec)
        mark = {"OK": "OK", "NG": "NG", "ERROR": "ERR"}[rec["result"]]
        print(f"[{mark:>3}] {st['no']:>2}. {st['screen']} / {st['action']} / {st['target']}"
              + (f"  期待={st.get('expect')} 実際={rec.get('actual')}" if "expect" in st else "")
              + (f"  ({rec.get('error')})" if rec["result"] == "ERROR" else ""))
        if rec["result"] != "OK":
            log["result"] = "FAIL"
            break
    json.dump(log, open(os.path.join(run_dir, "log.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    subprocess.run(["osascript", "-e", 'tell application id "%s" to quit saving no' % tc["app"]], capture_output=True)
    print(f"\n結果: {log['result']}   記録: regen/runs/{a.label}/log.json")


if __name__ == "__main__":
    main()
