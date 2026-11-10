"""AIが生成したスクリプト（英語の画面用）。作るモードで、英語のTextEditの画面構造をダンプして作り直したもの。
テストケース TE-PRINT-001 は変えていない（意図・期待値はそのまま）。変えたのは画面との対応表だけ。
"""
LOCATORS = {
    "新規書類":   [{"identifier": "NewDocumentButton"}, {"role": "AXMenuItem", "title": "New"}],
    "本文":       [{"role": "AXTextArea", "within": "document"}],
    "部数":       [{"role": "AXTextField", "title": "Copies", "within": "sheet"}],
    "横向き":     [{"role": "AXRadioButton", "title": " Portrait", "within": "sheet"}],
    "縦向き":     [{"role": "AXRadioButton", "title": " Portrait", "within": "sheet"}],
    "キャンセル": [{"role": "AXButton", "title": "Cancel", "within": "sheet"}],
    "印刷シート": [{"role": "AXSheet"}],
    "閉じる":     [{"role": "AXButton", "subrole": "AXCloseButton", "within": "document"}],
    "保存しない": [{"role": "AXButton", "title": "Delete"}],
}
