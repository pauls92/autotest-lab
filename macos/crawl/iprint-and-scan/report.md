# 画面マップ: com.brother.iprint-and-scan

画面 7 / 遷移 11 / 操作回数 11

## 遷移

- S01 --[AXButton id=_NS:179 label='プリント'#0]--> S02
- S02 --[AXButton id=_NS:61 label='写真'#0]--> S03
- S02 --[AXButton id=_NS:61 label='PDF'#0]--> S03  (既知の画面へ)
- S01 --[AXButton id=_NS:179 label='スキャン'#0]--> S04
- S04 --[AXButton id=_NS:105 label='スキャンしたい原稿を原稿台ガラスもしくは自動原稿送り装置にセットしてください'#0]--> S01  (既知の画面へ)
- S04 --[AXButton id=_NS:8 label='すべての設定'#0]--> S05
- S05 --[AXButton id=_NS:73 label='キャンセル'#0]--> S04  (既知の画面へ)
- S01 --[AXButton id=_NS:90 label='オフライン（利用できません）'#0]--> S06
- S06 --[AXButton id=_NS:105 label='Brother iPrint&Scan'#0]--> ee5014e7
- S01 --[AXButton id=SelectDeviceButton label='製品を選択'#0]--> S07
- S06 --[AXButton id=_NS:10 label='アプリケーション設定'#0]--> S06  (変化なし)

## 画面ごとのID充足率

| 画面 | タイトル | 操作対象 | 明示ID | 自動ID | ラベルのみ | 手がかりなし |
|---|---|---|---|---|---|---|
| S01 | Brother iPrint&Scan | 6 | 2 | 4 | 0 | 0 |
| S02 | プリント | 2 | 0 | 2 | 0 | 0 |
| S03 | 開く | 9 | 6 | 0 | 3 | 0 |
| S04 | Brother iPrint&Scan | 7 | 0 | 7 | 0 | 0 |
| S05 | すべての設定 | 6 | 0 | 6 | 0 | 0 |
| S06 | Brother iPrint&Scan | 3 | 0 | 3 | 0 | 0 |
| S07 | 製品選択 | 7 | 0 | 5 | 2 | 0 |

## ID付与依頼リスト（明示IDがない操作対象）

| 画面 | 要素 | ラベル | 現在のID | 同一IDの個数 |
|---|---|---|---|---|
| S01 Brother iPrint&Scan | AXButton | プリント | _NS:179 | 1 |
| S01 Brother iPrint&Scan | AXButton | スキャン | _NS:179 | 1 |
| S01 Brother iPrint&Scan | AXButton | オフライン（利用できません） | _NS:90 | 1 |
| S01 Brother iPrint&Scan | AXButton | ワークフローを作成 | _NS:126 | 1 |
| S02 プリント | AXButton | 写真 | _NS:61 | 1 |
| S02 プリント | AXButton | PDF | _NS:61 | 1 |
| S03 開く | AXButton | 戻る | (なし) | 1 |
| S03 開く | AXButton | 進む | (なし) | 1 |
| S03 開く | AXButton | 検索 | (なし) | 1 |
| S04 Brother iPrint&Scan | AXButton | スキャンしたい原稿を原稿台ガラスもしくは自動原稿送り装置にセットしてください | _NS:105 | 1 |
| S04 Brother iPrint&Scan | AXButton | スキャン | _NS:10 | 1 |
| S04 Brother iPrint&Scan | AXPopUpButton | 原稿サイズ | _NS:145 | 1 |
| S04 Brother iPrint&Scan | AXPopUpButton | カラー設定 | _NS:169 | 1 |
| S04 Brother iPrint&Scan | AXPopUpButton | 解像度 | _NS:191 | 1 |
| S04 Brother iPrint&Scan | AXButton | すべての設定 | _NS:8 | 1 |
| S04 Brother iPrint&Scan | AXButton | スキャン | _NS:92 | 1 |
| S05 すべての設定 | AXButton | OK | _NS:82 | 1 |
| S05 すべての設定 | AXPopUpButton | 解像度 | _NS:51 | 1 |
| S05 すべての設定 | AXPopUpButton | 解像度 | _NS:66 | 1 |
| S05 すべての設定 | AXPopUpButton | 解像度 | _NS:8 | 1 |
| S05 すべての設定 | AXButton | 標準に戻す | _NS:92 | 1 |
| S05 すべての設定 | AXButton | キャンセル | _NS:73 | 1 |
| S06 Brother iPrint&Scan | AXButton | Brother iPrint&Scan | _NS:105 | 1 |
| S06 Brother iPrint&Scan | AXButton | アプリケーション設定 | _NS:10 | 1 |
| S06 Brother iPrint&Scan | AXButton | ガイダンスを開く | _NS:8 | 1 |
| S07 製品選択 | AXButton | ローカルネットワーク | _NS:116 | 1 |
| S07 製品選択 | AXButton | OK | _NS:18 | 1 |
| S07 製品選択 | AXButton | キャンセル | _NS:8 | 1 |
| S07 製品選択 | AXButton | 製品選択 | _NS:51 | 1 |
| S07 製品選択 | AXButton | 製品を再検索 | _NS:36 | 1 |
| S07 製品選択 | AXRadioButton | ネットワーク | (なし) | 1 |
| S07 製品選択 | AXRadioButton | USB | (なし) | 1 |

## 押さなかったボタン

- S01 AXButton label='ワークフローを作成' id=_NS:126 — 禁止語
- S01 AXButton label='本体からのスキャン設定' id=ScanKeySettingButton — 禁止語
- S01 AXButton label='ワークフローを作成' id=_NS:126 — 禁止語
- S01 AXButton label='本体からのスキャン設定' id=ScanKeySettingButton — 禁止語
- S04 AXButton label='スキャン' id=_NS:10 — 禁止語
- S04 AXPopUpButton label='原稿サイズ' id=_NS:145 — ポップアップ
- S04 AXPopUpButton label='カラー設定' id=_NS:169 — ポップアップ
- S04 AXPopUpButton label='解像度' id=_NS:191 — ポップアップ
- S04 AXButton label='スキャン' id=_NS:92 — 禁止語
- S05 AXButton label='OK' id=_NS:82 — 禁止語
- S05 AXPopUpButton label='解像度' id=_NS:51 — ポップアップ
- S05 AXPopUpButton label='解像度' id=_NS:66 — ポップアップ
- S05 AXPopUpButton label='解像度' id=_NS:8 — ポップアップ
- S05 AXButton label='標準に戻す' id=_NS:92 — 禁止語
- S06 AXButton label='ガイダンスを開く' id=_NS:8 — 禁止語
