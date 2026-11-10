"""Brother iPrint&Scan の画面遷移テスト（印刷・スキャンは実行しない）。

メイン画面 → 「プリント」タイル → 「プリント」ダイアログ → 「PDF」→ ファイル選択パネル
→ キャンセル → メイン画面に戻る、を確認する。

ロケータの内訳:
  - SelectDeviceButton など主要ボタン: 明示ID
  - 「プリント」「スキャン」タイル: ボタン自身は _NS:179 で両方同じ。同じセル内のラベル文字列で特定する
  - 「写真」「PDF」: 自動ID _NS:61 が重複。ラベルで特定
  - ファイル選択パネル: macOS 標準の CancelButton / OKButton（明示ID）
実行:  ./.venv/bin/python test_iprintscan.py
"""
import time
from ax_driver import App, NotFound

BUNDLE = "com.brother.iprint-and-scan"


def tile(root, label):
    """タイル型UI: ラベル(AXStaticText)と同じセル(AXUnknown)にある AXButton を返す。"""
    for cell in root.find_all(role="AXUnknown"):
        kids = cell.children
        if any(k.role == "AXStaticText" and k.value == label for k in kids):
            return next(k for k in kids if k.role == "AXButton")
    raise NotFound(f"tile {label!r}")


def window(app, title, timeout=5):
    deadline = time.time() + timeout
    while time.time() < deadline:
        for w in app.windows():
            if w.title == title:
                return w
        time.sleep(0.2)
    raise NotFound(f"window {title!r}")


def main():
    app = App(BUNDLE).activate()

    print("[1] メイン画面の確認")
    main_win = window(app, "Brother iPrint&Scan")
    assert main_win.identifier == "TopViewController"
    device = main_win.find(identifier="SelectDeviceButton")           # 明示ID
    model = [t.value for t in main_win.find_all(role="AXStaticText") if t.value and str(t.value).startswith("DCP")]
    print(f"  OK: 製品選択ボタンあり / 接続中の製品 = {model}")

    print("[2] 「プリント」タイルを押す")
    tile(main_win, "プリント").press()                                  # 相対位置（ラベル→兄弟ボタン）
    dlg = window(app, "プリント")
    msg = next(t.value for t in dlg.find_all(role="AXStaticText") if t.value)
    print(f"  OK: ダイアログ表示 = {msg!r}")

    print("[3] 「PDF」を選ぶ")
    dlg.find(role="AXButton", title="PDF").press()                       # ラベル
    panel = window(app, "開く", timeout=8)
    assert panel.identifier == "open-panel"
    print("  OK: ファイル選択パネルが開いた")

    print("[4] キャンセルしてメイン画面に戻る")
    panel.find(identifier="CancelButton").press()                        # 明示ID
    time.sleep(1)
    titles = [w.title for w in app.windows()]
    assert titles == ["Brother iPrint&Scan"], f"残っているウインドウ: {titles}"
    print("  OK: メイン画面のみ")
    print("\nPASS")


if __name__ == "__main__":
    main()
