"""印刷ダイアログの操作テスト（印刷はしない）。

TextEdit で書類を作り、Cmd+P で印刷シートを開き、
  部数を 3 にする / 向きを「横」にする / 用紙サイズの現在値を読む
を行って値を検証し、キャンセルで閉じ、書類を保存せず閉じる。

印刷シートには明示IDがなく自動IDも重複しているため、ロケータはすべてラベル。
実行:  ./.venv/bin/python test_print_dialog.py
"""
import time
import Quartz
from ax_driver import App, NotFound


def key(code, cmd=False):
    for down in (True, False):
        ev = Quartz.CGEventCreateKeyboardEvent(None, code, down)
        if cmd:
            Quartz.CGEventSetFlags(ev, Quartz.kCGEventFlagMaskCommand)
        Quartz.CGEventPost(Quartz.kCGHIDEventTap, ev)


def main():
    app = App("com.apple.TextEdit").activate()

    print("[1] 書類を用意する")
    if not any(w.find_all(role="AXTextArea") for w in app.windows()):
        try:
            app.find(identifier="NewDocumentButton").press()
        except NotFound:
            app.find(role="AXMenuItem", title="新規").press()
    area = app.wait_for(role="AXTextArea", timeout=5)
    area.set_value("印刷ダイアログ テスト")

    print("[2] Cmd+P で印刷シートを開く")
    app.activate()
    key(35, cmd=True)  # P
    sheet = app.wait_for(role="AXSheet", timeout=10)
    app.wait_for(role="AXButton", title="プリント", timeout=10)  # 中身の描画待ち

    print("[3] 部数を 3 にする")
    copies = sheet.find(role="AXTextField", title="部数")
    copies.set_value("3")
    time.sleep(0.3)
    assert copies.value == "3", f"部数: {copies.value!r}"
    print("  OK: 部数 == 3")

    print("[4] 向きを「横」にする")
    landscape = sheet.find(role="AXRadioButton", title=" 横")
    landscape.press()
    time.sleep(0.3)
    assert landscape.value == 1, f"横: {landscape.value!r}"
    assert sheet.find(role="AXRadioButton", title=" 縦").value == 0
    print("  OK: 向き == 横")

    print("[5] 現在の用紙サイズとプリンタを読む")
    popups = sheet.find_all(role="AXPopUpButton")
    paper = next(p for p in popups if "mm" in str(p.value))
    printer = popups[-2]  # プリンタ / プリセット の順に並ぶ下段グループ
    print(f"  用紙サイズ = {paper.value!r}")
    print(f"  プリンタ   = {printer.value!r}")

    print("[6] キャンセルで閉じる")
    # 部数フィールドが編集中だと、1回目のキャンセルは編集確定＋値リセットに消費され、
    # シートが閉じないことがある（macOS 26 で観測）。閉じるまで確認しながら最大3回押す。
    def sheet_open():
        return any(c.role == "AXSheet" for w in app.windows() for c in w.children)
    for attempt in range(3):
        sheet.find(role="AXButton", title="キャンセル").press()
        deadline = time.time() + 2
        while time.time() < deadline and sheet_open():
            time.sleep(0.2)
        if not sheet_open():
            break
        print(f"  シートがまだ開いている。再試行 {attempt + 2} 回目")
    assert not sheet_open(), "シートが閉じていない"
    print("  OK: シートを閉じた")

    print("[7] 書類を保存せずに閉じる")
    win = next(w for w in app.windows() if w.find_all(role="AXTextArea"))
    win.find(role="AXButton", subrole="AXCloseButton").press()
    app.wait_for(role="AXButton", title="削除", timeout=5).press()
    time.sleep(0.5)
    print("\nPASS")


if __name__ == "__main__":
    main()
