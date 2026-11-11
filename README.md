# autotest-lab

E2E自動テストの個人的な実験場。

- `macos/` — macOSのアクセシビリティAPI（AXUIElement）を Python（pyobjc）から使ったGUI自動操作の実験。画面の棚卸し（`ax_dump.py`）、操作（`ax_driver.py`）、画面遷移の探索（`ax_crawl.py`）、TextEdit・印刷ダイアログ・iPrint&Scanのテスト
- `macos/regen/` — 作り直す回帰テストの実験。テストケース（意図と期待値）を固定し、言語ごとに作り直したスクリプトが同じことを確かめているかを操作ログで比べる
- `tools/` — reportlab で16:9のスライドPDFを描くための部品（`slidekit.py`）、アイコン（`icons.py`）、イラスト（`illustrations.py`）
- `notes/` — 一般論の壁打ちをまとめたスライド（`build.py` で PDF を作り直せる）。GUI自動操作の技術の比較（`gui_automation_landscape/`）、閉じた環境でのAIと自動テスト（`closed_env_ai/`）
