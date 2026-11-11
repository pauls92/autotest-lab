"""閉じたネットワーク・古いOSでのAI活用と、スクリプトの保守（一般論のスライドPDF）。

実行: python build.py  → 同じフォルダに closed_env_ai.pdf を出力
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools"))
from slidekit import (Deck, st, W, M, INK, INK2, INK3, CYAN, CYAN_S, MAG, MAG_S,  # noqa: E402
                      GRN, GRN_S, YEL, YEL_S, BG, PAPER)

OUT = os.path.join(HERE, "closed_env_ai.pdf")
FOOT = "autotest-lab ・ 閉じた環境でのAIと自動テスト 一般論のまとめ（2026-11）"
TOTAL = 7
CW = W - 2 * M

d = Deck(OUT, "閉じた環境でのAIと自動テスト", FOOT, TOTAL)

# 1. 表紙
d.cover("autotest-lab ・ 一般論",
        "閉じた環境でのAIと自動テスト",
        "ネットにつながらない・古いOSで、どうAIを活かすか",
        "インターネットにつながらない評価用の環境や、古いOSでのテストに、AIをどう組み込むか。"
        "AIで作ったスクリプトを、どう持ち込み、どう保守するか。",
        ["公開情報にもとづく一般論。実際の運用は、組織のセキュリティのルールに従うこと。",
         "関連資料：notes/gui_automation_landscape（GUI自動操作の技術の比較）"])

# 2. computer use の仕組み
y = d.slide("computer use は、3つの部品でできている", "仕組み")
bw = 250; gap = (CW - 3 * bw) / 2; by = y - 20; bh = 150
parts = [
    ("① 画面を撮る・操作する係", "テスト対象の画面を撮り、AIの指示どおりにクリックや入力をする小さなプログラム。", GRN, GRN_S),
    ("② 繰り返しを回す係（エージェント）", "「撮る → AIに聞く → 操作する → また撮る」を、目的を果たすまで繰り返す。", CYAN, CYAN_S),
    ("③ 判断するAIモデル", "画像を見て、どの部品を、どの座標で操作するかを決める。画像を理解できるモデルが必要。", MAG, MAG_S),
]
for i, (h, b, a, f) in enumerate(parts):
    x = M + i * (bw + gap)
    d.card(x, by, bw, bh, h, b, accent=a, fill=f, head_size=13.5, body_size=11.5)
    if i < 2:
        d.arrow(x + bw + 6, by - bh / 2 + 8, x + bw + gap - 6, by - bh / 2 + 8)
        d.arrow(x + bw + gap - 6, by - bh / 2 - 8, x + bw + 6, by - bh / 2 - 8)
d.box(M, by - bh - 24, CW, 96, fill=BG, accent=INK)
d.para("<b>AIエージェントの製品でなくてもよい</b>。この3つが揃えばcomputer useになり、①と②は自分で書ける"
       "（このリポジトリの macos/ の実験は①にあたる）。<br/>"
       "<b>ネットが要るかは、③の置き場所で決まる</b>。③がクラウドのAPIなら、インターネットへの接続が必要。"
       "③を手元に置けば（ローカルLLM）、閉じた環境でも動かせる。",
       M + 20, by - bh - 38, CW - 40, st(12.5, INK))
d.end()

# 3. ローカルLLMで閉じた環境でもできる？
y = d.slide("ローカルLLMなら、閉じた環境でもできる？", "Q&A")
d.box(M, y - 4, CW, 50, fill=GRN_S, accent=GRN)
d.para("<b>技術的にはできる。</b>画面を理解できる公開モデルを、閉じたネットワークの中のGPUマシンで動かせばよい。ただし条件と注意がある。",
       M + 18, y - 18, CW - 34, st(12.5, INK))
cw3 = (CW - 2 * 16) / 3
cards = [
    ("必要なもの",
     "・画面操作に使える公開モデル（例：UI-TARS、Qwen-VL系。OmniParserで画面を部品に分ける方法も）<br/>"
     "・GPUを積んだマシン1台（モデルの大きさに応じたメモリ）<br/>"
     "・動かす仕組み（Ollama、vLLMなど）", CYAN, CYAN_S),
    ("注意",
     "・精度は最先端のクラウドのモデルより低い。複雑な判断は苦手<br/>"
     "・古いOSの上ではモデルは動かない（別の新しいマシンに置く）<br/>"
     "・モデルの持ち込みは、組織の承認とライセンスの確認が要る", YEL, YEL_S),
    ("古いOSに何も入れない方法",
     "・仮想マシンなら、外側（ハイパーバイザ）から画面を撮り、入力を送れる<br/>"
     "・画面共有（VNC・リモートデスクトップ）越しに操作する<br/>"
     "・実機なら、画面キャプチャ機器＋USB入力装置で外から操作する", MAG, MAG_S),
]
for i, (h, b, a, f) in enumerate(cards):
    d.card(M + i * (cw3 + 16), y - 70, cw3, 210, h, b, accent=a, fill=f, head_size=14, body_size=11)
d.end()

# 4. 現実解：2つのゾーン
y = d.slide("現実解：AIは「作る・直す」側、閉じた環境は「動かす・証拠を取る」側", "考え方")
zw = 330; zh = 250; zy = y - 10
d.box(M, zy, zw, zh, fill=CYAN_S, accent=CYAN)
d.para("<b>開発の環境</b>（AIが使える・新しいOS）", M + 20, zy - 14, zw - 36, st(14, INK))
d.para("・AIがスクリプトを書く<br/>・新しいOSやエミュレーターで、まず動作を確かめる<br/>"
       "・持ち帰った証拠をAIが読み、原因を推定して直す<br/>・古いOSでも動く書き方か、自動で検査する",
       M + 20, zy - 48, zw - 36, st(12, INK2))
x2 = W - M - zw
d.box(x2, zy, zw, zh, fill=MAG_S, accent=MAG)
d.para("<b>閉じた評価の環境</b>（AIなし・古いOS）", x2 + 20, zy - 14, zw - 36, st(14, INK))
d.para("・決まった手順のスクリプトをそのまま動かす<br/>・実行時にAIもネットも使わない<br/>"
       "・失敗したら証拠を厚く残す（スクリーンショット、部品の木、操作ログ）<br/>・画面の棚卸しも取っておく",
       x2 + 20, zy - 48, zw - 36, st(12, INK2))
mx = M + zw + 14; mw = x2 - mx - 14
d.arrow(mx, zy - 80, mx + mw, zy - 80, color=CYAN)
d.para("持ち込む<br/>スクリプト一式", mx, zy - 40, mw, st(11, CYAN, align=1))
d.arrow(mx + mw, zy - 170, mx, zy - 170, color=MAG)
d.para("持ち出す<br/>結果と証拠", mx, zy - 180, mw, st(11, MAG, align=1))
d.para("どちらも、組織が承認した手段で受け渡す。この往復を速く回せるかが保守のしやすさを決める。",
       M, zy - zh - 16, CW, st(12, INK2))
d.end()

# 5. 保守を回す工夫
y = d.slide("閉じた環境のスクリプトを保守する工夫", "考え方")
hdr = ["工夫", "中身", "ねらい"]
wid = [190, 420, 254]
rows = [hdr,
        ["実行時にAIを使わない", "スクリプトは普通のコード。AIは作る・直すときだけ使う", "閉じた環境でも、毎回同じ結果になる"],
        ["いちばん古いOSに合わせる", "言語やライブラリの版を、古いOSで動く版に固定する（例：Windows 7で動くPythonは3.8まで）",
         "持ち込んでから動かない、を防ぐ"],
        ["丸ごと1つにまとめて持ち込む", "実行環境・ライブラリ・スクリプトを1つの包みにする（インストール不要の形）",
         "ネットからの取得が要らない。手順が短い"],
        ["開発の環境で互換性を検査", "古い版の言語で構文や動作を自動テストしてから持ち込む", "往復の回数を減らす"],
        ["失敗の証拠を厚く取る", "スクリーンショット、部品の木、操作ログ、OSの版をまとめて保存", "持ち帰ればAIが原因を推定できる"],
        ["OSごとの差を1か所に集める", "部品の指定（ロケータ）を画面ごとの定義にまとめ、OS別に切り替える",
         "直す場所が1か所で済む"],
        ["画面の棚卸しを差分で持ち帰る", "評価の環境で画面を探索し、前回との差を持ち帰る", "画面の変更を、失敗する前に知る"],
        ]
d.table(rows, M, y, wid, size=10)
d.end()

# 6. 段階案
y = d.slide("段階的に進める案", "示唆（一般論）")
steps = [
    ("段階1：AIで作り、閉じた環境で動かす", "2つの環境の往復を整える。証拠を厚く取り、AIは開発の環境で原因の推定と修正をする。"
     "追加の設備は要らない。", GRN, GRN_S),
    ("段階2：閉じた環境にローカルLLMを置く（解析だけ）", "評価の環境にGPUマシンを置き、失敗の解析や画面の比較をその場でさせる。"
     "テストの操作はまだ決まった手順のスクリプトで行う。", CYAN, CYAN_S),
    ("段階3：ローカルLLMで探索・自動修復", "部品が見つからないときにAIが代わりを探す、画面を探索して新しいテストを提案する。"
     "精度を見ながら範囲を広げる。", MAG, MAG_S),
]
for i, (h, b, a, f) in enumerate(steps):
    d.card(M, y - 4 - i * 96, CW, 84, h, b, accent=a, fill=f, head_size=14, body_size=11.5)
d.para("<b>先に確かめること</b>：閉じた環境への持ち込み・持ち出しの手段、仮想マシンで古いOSを動かしてよいか、"
       "公開モデルの持ち込みの可否。いずれも組織のルールしだい。",
       M, y - 300, CW, st(12, INK2))
d.end()

# 7. まとめ
y = d.slide("まとめ", "まとめ")
pts = [
    "computer use は「画面を撮る・操作する係」「繰り返す係」「判断するAI」の3つ。ネットが要るかはAIの置き場所で決まる。",
    "ローカルLLMなら閉じた環境でも技術的には可能。ただし精度・GPU・持ち込みの承認が課題で、古いOSの外に置く。",
    "当面の現実解は、AIは開発の環境で作る・直す、閉じた環境では決まった手順のスクリプトを動かして証拠を取る、の往復。",
    "保守の鍵は、古いOSに合わせた版の固定、丸ごと持ち込める形、厚い証拠、そして往復の速さ。",
]
for i, p in enumerate(pts):
    d.box(M, y - 4 - i * 84, CW, 70, fill=BG, accent=CYAN)
    d.para(p, M + 22, y - 26 - i * 84, CW - 44, st(13, INK))
d.end()

d.save()
print(OUT)
