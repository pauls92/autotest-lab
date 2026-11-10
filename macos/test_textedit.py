"""最初のE2Eテスト: TextEdit で新規書類を作り、文字を入力して、内容を検証し、保存せずに閉じる。

ロケータはすべて identifier かラベル。画像は使わない。
実行:  ./.venv/bin/python test_textedit.py
"""
import time
from ax_driver import App, NotFound

TEXT = "自動テスト from ax_driver"


def open_new_document(app):
    """「開く」パネルが出ていれば「新規書類」を押す。出ていなければ Cmd+N 相当のメニューを押す。"""
    try:
        app.find(identifier="NewDocumentButton").press()          # ロケータ1: ID
        print("  「開く」パネル → NewDocumentButton を押した")
    except NotFound:
        app.find(role="AXMenuItem", title="新規").press()          # ロケータ2: ラベル
        print("  メニュー「ファイル > 新規」を押した")


def main():
    app = App("com.apple.TextEdit").activate()
    print("[1] 新規書類を開く")
    open_new_document(app)

    print("[2] 本文を入力する")
    area = app.wait_for(role="AXTextArea", timeout=5)
    area.set_value(TEXT)

    print("[3] 検証する")
    actual = area.value
    assert actual == TEXT, f"期待: {TEXT!r} / 実際: {actual!r}"
    print(f"  OK: 本文 == {actual!r}")

    print("[4] 保存せずに閉じる")
    win = next(w for w in app.windows() if w.find_all(role="AXTextArea"))
    win.find(role="AXButton", subrole="AXCloseButton").press()
    sheet_btn = app.wait_for(role="AXButton", title="削除", timeout=5)  # 「変更内容を保存しますか」シート
    sheet_btn.press()
    time.sleep(0.5)
    assert not any(w.find_all(role="AXTextArea") for w in app.windows()), "書類ウインドウが閉じていない"
    print("  OK: ウインドウを閉じた")
    print("\nPASS")


if __name__ == "__main__":
    main()
