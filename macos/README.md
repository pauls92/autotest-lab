# macOS 実験

macOS のアクセシビリティAPI（AXUIElement）を Python + pyobjc から直接使う実験。画像マッチングは使わない。

## セットアップ

```bash
python3 -m venv .venv
./.venv/bin/pip install pyobjc-core pyobjc-framework-Cocoa pyobjc-framework-ApplicationServices pyobjc-framework-Quartz
```

実行元（ターミナル / Claude など）に「システム設定 → プライバシーとセキュリティ → アクセシビリティ」の許可が必要。

## ファイル

| ファイル | 役割 |
|---|---|
| `ax_dump.py` | 棚卸しツール。起動中アプリのUI要素を一覧化し、明示ID / 自動ID / ラベルのみ / 手がかりなし の割合を集計する |
| `ax_driver.py` | 最小限の操作ドライバ。identifier → ラベル → role の優先順位で要素を探し、press / set_value する |
| `test_textedit.py` | 最初のE2Eテスト。TextEdit で新規書類 → 入力 → 検証 → 保存せず閉じる |
| `test_print_dialog.py` | 印刷シートの操作。Cmd+P → 部数=3 → 向き=横 → 用紙サイズ/プリンタを読む → キャンセル（印刷はしない） |
| `test_iprintscan.py` | Brother iPrint&Scan の画面遷移。プリントタイル → PDF → ファイル選択 → キャンセル（印刷はしない） |
| `inventory_textedit.json` | TextEdit（「開く」パネル表示時）の棚卸し結果 |
| `inventory_textedit_printsheet.json` | TextEdit 印刷シートの棚卸し結果 |
| `inventory_iprintscan.json` | iPrint&Scan メイン画面の棚卸し結果 |

```bash
./.venv/bin/python ax_dump.py com.apple.TextEdit
./.venv/bin/python test_textedit.py
```

## 棚卸し結果（macOS 26.5）

| 画面 | 操作対象 | 明示ID | 自動ID | ラベルのみ | 手がかりなし |
|---|---|---|---|---|---|
| TextEdit「開く」パネル＋メニュー | 308 | 38% | 40% | 22% | 0% |
| TextEdit 印刷シート | 28 | **0%** | 71%（`_NS:8` が5回など重複あり） | 7% | 21%（スクロールバー矢印等） |
| iPrint&Scan メイン画面（メニュー除く） | 7 | 3 | 4 | 0 | 0 |

- Apple は主要ボタン（`NewDocumentButton`, `CancelButton`, `OKButton`, `Search`）に意図的なIDを付けている
- **印刷シートは明示IDがなく自動IDも重複**しているため、ロケータはラベル一択。言語切替に弱い
- iPrint&Scan は `SelectDeviceButton` / `ScanKeySettingButton` / `StatusInformationButtonCell` に明示ID。
  一方 **「プリント」「スキャン」タイルのボタンは両方 `_NS:179`** で区別できず、同じセル内のラベル文字列で特定するしかない → ID付与依頼の第1候補。
  「写真」「PDF」ボタンも `_NS:61` で重複（ラベルで区別可能）

## 観測した注意点

- **AXPress が -25204 (CannotComplete) を返しても操作は実行されている**ことがある（モーダルを開く操作）。
  ドライバはこれを失敗にせず、呼び出し側が `wait_for` で結果画面を検証する
- **メニュー項目「プリント…」を AXPress で押すと、その後アプリのウインドウが AX ツリーから消え、
  代わりにアプリ要素自身が返る異常状態になった**（TextEdit を閉じるまで復旧せず）。`Cmd+P` のキー送信なら問題なし。
  印刷シートはキーボードショートカットで開くこと
- 印刷シートの「キャンセル」は、部数フィールド編集中だと 1回目が編集確定に消費されて閉じないことがある。
  閉じたことを確認しながら再試行する
- `screencapture` には「画面収録」の権限が別途必要

## クローラー（ax_crawl.py）

アプリの画面を自動で遷移しながら、各画面の要素とIDの有無を記録し、画面マップ・ID充足率・ID付与依頼リストを生成する。

```bash
./.venv/bin/python ax_crawl.py com.brother.iprint-and-scan --max-depth 3 --max-actions 60
# → crawl/iprint-and-scan/report.md, screens.json, shots/
```

安全ルール: 禁止語（プリント/印刷/スキャン/送信/削除/保存/OK/標準に戻す など）を含むボタンと `OKButton` 等のIDは押さない。
タイル型UI（ラベルが兄弟要素）は導線とみなして押す。メインウインドウは閉じない。macOS標準パネル（open-panel 等）は中を探索しない。
画面の同一判定は「操作対象の85%以上が一致」（非同期のステータス表示を吸収）。既知の画面に戻ってしまったら経路を再生して復帰。

iPrint&Scan での結果（2026-09-20）: 7〜9画面・約20遷移を無人で発見。明示IDはメイン画面の3ボタンのみで、
それ以外の画面は自動ID（`_NS:*`、重複あり）かラベルのみ。依頼リストは `crawl/iprint-and-scan/report.md`。
