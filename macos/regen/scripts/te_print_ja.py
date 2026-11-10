"""AIが生成したスクリプト（日本語の画面用）。テストケース TE-PRINT-001 の意味の名前を、画面の部品に結びつける。
生成: Claude（画面構造のダンプから）。テストケースの意図・期待値は含まない。
"""
LOCATORS = {
    "新規書類":   [{"identifier": "NewDocumentButton"}, {"role": "AXMenuItem", "title": "新規"}],
    "本文":       [{"role": "AXTextArea", "within": "document"}],
    "部数":       [{"role": "AXTextField", "title": "部数", "within": "sheet"}],
    "横向き":     [{"role": "AXRadioButton", "title": " 横", "within": "sheet"}],
    "縦向き":     [{"role": "AXRadioButton", "title": " 縦", "within": "sheet"}],
    "キャンセル": [{"role": "AXButton", "title": "キャンセル", "within": "sheet"}],
    "印刷シート": [{"role": "AXSheet"}],
    "閉じる":     [{"role": "AXButton", "subrole": "AXCloseButton", "within": "document"}],
    "保存しない": [{"role": "AXButton", "title": "削除"}],
}
