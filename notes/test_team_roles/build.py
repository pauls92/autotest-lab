"""AI時代のテストチームの役割（一般論のスライドPDF）。

実行: python build.py  → 同じフォルダに test_team_roles.pdf を出力
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools"))
from slidekit import (Deck, st, W, H, M, INK, INK2, INK3, CYAN, CYAN_S, MAG, MAG_S,  # noqa: E402
                      GRN, GRN_S, YEL, YEL_S, BG, PAPER, LINE)
from reportlab.platypus import Paragraph  # noqa: E402

OUT = os.path.join(HERE, "test_team_roles.pdf")
FOOT = "autotest-lab ・ AI時代のテストチームの役割 一般論のまとめ（2026-11）"
TOTAL = 8
CW = W - 2 * M

d = Deck(OUT, "AI時代のテストチームの役割", FOOT, TOTAL)


def label_box(x, ytop, w, h, text, fill, size=11.5, color=INK, accent=None):
    d.box(x, ytop, w, h, fill=fill, accent=accent)
    p = Paragraph(text, st(size, color, align=1))
    _, ph = p.wrap(w - 16, 1000)
    p.drawOn(d.c, x + 8, ytop - (h - ph) / 2 - ph)


# 1. 表紙
d.cover("autotest-lab ・ 一般論",
        "AI時代のテストチームの役割",
        "書く・動かす・判定するはAIへ。人とチームは何を担うか",
        "スクリプトの作成や実行、結果の判定をAIが担うようになると、テストチームの価値は"
        "「品質の設計」と「テストの基盤」に移る。その役割を図にする。",
        ["公開情報にもとづく一般論。",
         "関連資料：notes/ai_driven_testing（AIドリブンテストの適用範囲）"])

# 2. 役割の変化
y = d.slide("役割の変化：「評価部隊」から「品質を設計し、基盤を持つチーム」へ", "全体像")
bw = (CW - 70) / 2
d.card(M, y - 4, bw, 170, "これまで",
       "・開発の後工程で、まとめて評価する<br/>"
       "・テスト実行のスクリプトを書く、実行ツールを作ることに力を注ぐ<br/>"
       "・結果の判定や原因の切り分けを人が行う<br/>"
       "・テスト環境は、その都度、人が用意する",
       accent=INK3, fill=BG, head_size=15, body_size=12)
d.arrow(M + bw + 12, y - 89, M + bw + 58, y - 89, color=CYAN)
d.card(M + bw + 70, y - 4, bw, 170, "これから",
       "・要件定義から入り、単体〜受け入れまで<b>一気通貫で品質を設計</b>する<br/>"
       "・スクリプトの作成・実行・判定・原因の推定は<b>AIに任せる</b><br/>"
       "・AIが届かない物理的な部分（機器・ネットワーク・古いOS）を<b>技術で補う基盤</b>を持つ<br/>"
       "・人は目的を決め、最終的に判断する",
       accent=CYAN, fill=CYAN_S, head_size=15, body_size=12)
d.para("重心が「テストを書いて動かす」から「何をどこで確かめるかを決める」と「AIが動ける場を作る」に移る。",
       M, y - 194, CW, st(12.5, INK2))
d.end()

# 3. 3つの役割の図
y = d.slide("3つの役割と、その関係", "図解")
cx = W / 2
# 中央：品質
qw, qh = 220, 64; qy = y - 150
label_box(cx - qw / 2, qy, qw, qh, "<b>プロダクトの品質</b>", INK, size=15, color=PAPER)
roles = [
    (M, y - 4, "① 品質の設計（テストアーキテクト）",
     "要件定義から参加。単体・結合・総合・受け入れの分担を決め、何をどのレベルで確かめるかを設計する", GRN, GRN_S),
    (W - M - 300, y - 4, "② AIドリブンテスト（AIエージェント＋使いこなす人）",
     "テストの設計案、スクリプトの作成、実行、結果の判定、失敗の原因の推定を、AIが回す", CYAN, CYAN_S),
    (cx - 150, y - 250, "③ テストの基盤（テストインフラ）",
     "環境・機器・ネットワーク・流れを用意し、AIが届かない物理的な部分を技術で補う", MAG, MAG_S),
]
for x, yt, h, b, a, f in roles:
    d.card(x, yt, 300, 120, h, b, accent=a, fill=f, head_size=13, body_size=11)
# 矢印
d.arrow(M + 300 + 4, y - 64, cx - qw / 2 - 6, qy - 20, color=GRN)
d.arrow(W - M - 300 - 4, y - 64, cx + qw / 2 + 6, qy - 20, color=CYAN)
d.arrow(cx, y - 250 + 4, cx, qy - qh - 6, color=MAG)
d.c.setFont("HeiseiKakuGo-W5", 10); d.c.setFillColor(INK3)
d.c.drawRightString(M + 300, y - 150, "何を確かめるかを渡す")
d.c.drawString(W - M - 300, y - 150, "結果と判定を返す")
d.c.drawString(cx + 10, y - 232, "動ける場を用意する")
d.end()

# 4. テストレベルの分担（V字）
y = d.slide("① 品質の設計：テストレベルごとの分担を決める", "図解")
lv = [("要件定義", "受け入れテスト", "人が最終判断。AIは観点と記録を支援"),
      ("基本設計", "総合テスト", "AI＋テスト基盤。実機・実ネットワークは基盤が用意"),
      ("詳細設計", "結合テスト", "AIが中心。仮想マシン・仮想の機器で厚く回す"),
      ("実装", "単体テスト", "開発者＋AI。コードと一緒に書く")]
rowh = 62; lw = 150; gapx = 22
for i, (left, right, who) in enumerate(lv):
    yy = y - 4 - i * rowh
    inset = i * 40
    label_box(M + inset, yy, lw, 46, left, BG, size=12)
    label_box(M + inset + lw + gapx + (3 - i) * 0 + 300 - 2 * inset, yy, lw, 46, right, CYAN_S, size=12, accent=CYAN)
    rx = M + inset + lw + gapx + 300 - 2 * inset + lw + 16
    d.para(who, rx, yy - 14, W - M - rx, st(11, INK2))
    d.c.setStrokeColor(LINE); d.c.setDash(3, 3)
    d.c.line(M + inset + lw + 4, yy - 23, M + inset + lw + gapx + 300 - 2 * inset - 4, yy - 23)
    d.c.setDash()
d.box(M, y - 270, CW, 70, fill=GRN_S, accent=GRN)
d.para("<b>テストアーキテクトの仕事</b>：同じことを何度も確かめない・抜けを作らないように、各レベルの範囲を決める。"
       "OSや機器で差が出る部分だけを総合テストに残し、それ以外は下のレベル（AIで回せる場所）に寄せる。",
       M + 20, y - 282, CW - 40, st(12, INK))
d.end()

# 5. AIができること・できないこと
y = d.slide("AIができること・できないこと", "整理")
hdr = ["作業", "AI", "補足", "担い手"]
wid = [200, 50, 434, 180]
rows = [hdr,
        ["テストの設計案を作る", "◎", "要件や仕様から観点と手順を出す。人がレビューする", "AI＋品質の設計"],
        ["スクリプトを書く・直す", "◎", "公開の技術で書くほど得意", "AI"],
        ["テストを実行する", "◎〜×", "AIの環境から届けば実行できる。届かない環境は基盤が流れを作る", "AI＋テスト基盤"],
        ["結果を判定する", "○", "画面が期待どおりか、ログが正しいかを判断。あいまいな基準は人が決める", "AI"],
        ["失敗の原因を推定する", "○", "スクリーンショット、部品の木、ログがそろっているほど正確", "AI"],
        ["どの機器にどのテストを当てるか", "○", "機器の一覧（型番・機能・接続方式）がデータになっていればAIが割り当てられる",
         "AI＋テスト基盤（一覧を整える）"],
        ["環境を作る・戻す", "○", "仮想マシンのひな形と操作の口があれば、AIが手順を実行できる", "テスト基盤（口を作る）"],
        ["機器をつなぐ・電源・用紙など", "×", "物理的な作業。遠隔の電源やUSBの切り替え器で一部は自動にできる", "テスト基盤"],
        ["リリースの可否を決める", "×", "責任を伴う判断", "人"],
        ]
d.table(rows, M, y, wid, size=10)
d.end()

# 6. テストインフラチームの仕事（図）
y = d.slide("③ テストインフラチームの仕事：流れと土台を作る", "図解")
steps = [("ビルド", BG), ("環境を用意", MAG_S), ("インストール", MAG_S), ("機器・ネットに接続", MAG_S),
         ("テスト実行", CYAN_S), ("結果を回収", MAG_S), ("判定・原因の推定", CYAN_S), ("報告", BG)]
n = len(steps); sw = (CW - (n - 1) * 12) / n; sy = y - 30
d.c.setFont("HeiseiKakuGo-W5", 11); d.c.setFillColor(INK)
d.c.drawString(M, y - 14, "流れ（パイプライン）")
for i, (s, f) in enumerate(steps):
    x = M + i * (sw + 12)
    label_box(x, sy, sw, 50, s, f, size=10.5)
    if i < n - 1:
        d.arrow(x + sw + 1, sy - 25, x + sw + 11, sy - 25)
d.c.setFont("HeiseiKakuGo-W5", 9.5); d.c.setFillColor(INK3)
d.c.drawString(M, sy - 64, "■ 桃色：テスト基盤が自動化する部分　■ 水色：AIが担う部分")
# 土台
d.c.setFont("HeiseiKakuGo-W5", 11); d.c.setFillColor(INK)
d.c.drawString(M, sy - 92, "土台（テスト基盤）")
bases = [
    ("仮想マシンの置き場", "OSごとのひな形、スナップショット、すぐ作れて戻せる"),
    ("機器ラボ", "実機・周辺機器。遠隔の電源、USBの切り替え、カメラでの確認"),
    ("ネットワーク", "テスト用LAN、分けた環境との受け渡し口"),
    ("機器・環境の一覧", "型番・機能・接続方式・空き状況をデータに。AIが割り当てに使う"),
    ("ルールとの調整", "セキュリティの決まりの範囲で、流れを設計する"),
]
bw5 = (CW - 4 * 12) / 5; byt = sy - 102
for i, (h, b) in enumerate(bases):
    d.card(M + i * (bw5 + 12), byt, bw5, 112, h, b, accent=MAG, fill=MAG_S, head_size=12, body_size=10.5)
d.para("AIが「書く・動かす・判定する」を速く回せるかは、この流れと土台の出来で決まる。",
       M, byt - 128, CW, st(12, INK2))
d.end()

# 7. 物理を技術で補う
y = d.slide("物理的な部分を、技術で補う例", "テスト基盤")
tips = [
    ("遠隔の電源", "ネットワークから入切できる電源タップで、機器やPCの電源を切り替える。再起動や電源断のテストも自動にできる。"),
    ("USBの切り替え器", "プログラムで接続先を切り替えられるUSBハブで、抜き差しを再現する。どのPCにどの機器をつなぐかも切り替えられる。"),
    ("カメラで確かめる", "機器の表示パネルや出力物をカメラで撮り、AIが読み取って判定する。"),
    ("機器の一覧をデータにする", "型番・機能・接続方式・設置場所・空き状況を一覧にし、AIやテストの流れから参照できるようにする。"),
    ("予約と割り当て", "機器を複数のテストで取り合わないように、予約の仕組みを作る。"),
    ("人手の作業は手順にする", "用紙の補充、ケーブルの交換など残る作業は、チェックリストと記録にしてAIが整理する。"),
]
tw = (CW - 2 * 16) / 3
for i, (hd, bd) in enumerate(tips):
    r, col = divmod(i, 3)
    d.card(M + col * (tw + 16), y - 4 - r * 136, tw, 120, hd, bd, accent=MAG, fill=MAG_S,
           head_size=14, body_size=11)
d.end()

# 8. まとめ：役割と必要な技術
y = d.slide("まとめ：3つの役割と、必要な技術", "まとめ")
hdr = ["役割", "主な仕事", "必要な技術・知識"]
wid = [200, 340, 324]
rows = [hdr,
        ["① 品質の設計（テストアーキテクト）", "要件定義から参加し、テストレベルの分担と、どこで何を確かめるかを決める",
         "テスト設計の技法、リスクの見積もり、開発プロセス、製品の知識"],
        ["② AIドリブンテスト", "AIエージェントにテストの作成・実行・判定を任せ、結果を確かめて改善する",
         "AIエージェントの使い方、指示の書き方、公開の自動化技術（Playwright、Appiumなど）の基礎"],
        ["③ テストの基盤（テストインフラ）", "環境・機器・ネットワーク・流れを作り、AIが届かない部分を補う",
         "仮想化、ネットワーク、CI（自動で流れを回す仕組み）、機器の制御、セキュリティのルール"],
        ]
h = d.table(rows, M, y, wid, size=11)
d.box(M, y - h - 20, CW, 60, fill=YEL_S, accent=YEL)
d.para("<b>呼び名の例</b>：テストアーキテクト、SDET（テストの仕組みを作る開発者）、テストインフラ／テストプラットフォームエンジニア、"
       "DevOps、テストラボの担当。",
       M + 20, y - h - 32, CW - 40, st(11.5, INK))
d.end()

d.save()
print(OUT)
