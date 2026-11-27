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
TOTAL = 15
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

# 7. ネイティブアプリのE2Eテストに必要な設備（全体図）
import icons  # noqa: E402
import illustrations as il  # noqa: E402

c = d.c
JPF = "HeiseiKakuGo-W5"


def badge(x, y, n):
    c.setFillColor(MAG); c.circle(x, y, 9, fill=1, stroke=0)
    c.setFillColor(PAPER); c.setFont(JPF, 10); c.drawCentredString(x, y - 3.5, str(n))


def text(x, y, s, size=10, color=INK, align="l"):
    c.setFont(JPF, size); c.setFillColor(color)
    {"l": c.drawString, "c": c.drawCentredString, "r": c.drawRightString}[align](x, y, s)


def dashed(x, y, w, h, label):
    c.saveState(); c.setStrokeColor(CYAN); c.setLineWidth(1.2); c.setDash(4, 3)
    c.setFillColor(CYAN_S); c.roundRect(x, y, w, h, 6, fill=1, stroke=1); c.restoreState()
    text(x + w / 2, y + h - 15, label, 9.5, CYAN, "c")


def wire(x1, y1, x2, y2, color=CYAN, lw=2, dash=None):
    c.saveState(); c.setStrokeColor(color); c.setLineWidth(lw)
    if dash: c.setDash(*dash)
    c.line(x1, y1, x2, y2); c.restoreState()


y = d.slide("ネイティブアプリのE2Eテストに必要な設備", "図解：設備の全体図")
steps = ["テスト設計", "アプリを受け取る", "環境を用意・復元", "インストール", "機器をつなぐ",
         "テスト実行", "判定・原因調査", "完了・報告"]
sw = (CW - 7 * 8) / 8
for i, s in enumerate(steps):
    x = M + i * (sw + 8)
    label_box(x, y + 4, sw, 28, s, INK, size=9.5, color=PAPER)
    if i < 7:
        d.arrow(x + sw, y - 10, x + sw + 8, y - 10)
text(W - M, y - 44, "点線の枠＝シミュレーター・仮想で代替できる　　番号＝次のページの表", 9, INK3, "r")

BUS = 282; top = 372; bot = 74
wire(BUS, bot, BUS, top, CYAN, 7)
text(BUS, bot - 16, "テスト用ネットワーク", 10, CYAN, "c"); badge(BUS - 62, bot - 12, 3)

# 左：アプリの置き場、OSイメージ、AIのPC
icons.draw(c, "server", 84, 340, 40, INK2)
text(112, 346, "アプリの置き場", 11); text(112, 331, "リリースされたアプリ", 9, INK3); badge(60, 364, 1)
wire(205, 340, BUS, 340)
icons.draw(c, "server", 84, 258, 40, INK2)
text(112, 264, "OSイメージの保管", 11); text(112, 249, "版ごとのイメージ", 9, INK3); badge(60, 282, 2)
wire(205, 258, BUS, 258)
il.desktop(c, 54, 92, s=0.6, app_title="AIエージェント")
text(117, 78, "AIエージェントのPC", 10.5, INK, "c"); text(117, 64, "（司令塔）", 9, INK3, "c"); badge(56, 186, 4)
wire(180, 150, BUS, 150)
icons.draw(c, "screencheck", 215, 205, 26, CYAN); icons.draw(c, "magnify", 248, 205, 26, CYAN)
text(232, 182, "判定・原因調査", 9, CYAN, "c"); badge(205, 228, 9)

# 右上：テスト端末
RX = 330
text(RX + 22, 360, "テスト端末（実機）", 10.5); badge(RX + 8, 364, 5)
il.phone(c, RX + 14, 284, s=1.05); il.phone(c, RX + 66, 284, s=1.05)
text(RX + 30, 270, "iOS", 9, INK2, "c"); text(RX + 82, 270, "Android", 9, INK2, "c")
wire(BUS, 315, RX + 10, 315)
dashed(RX + 128, 270, 140, 100, "シミュレーター")
il.phone(c, RX + 160, 280, s=0.8); il.phone(c, RX + 214, 280, s=0.8)

# 右中：テストPC
text(RX + 22, 246, "テストPC（実機）", 10.5); badge(RX + 8, 250, 6)
il.desktop(c, RX + 8, 160, s=0.48, app_title="テスト対象")
wire(BUS, 200, RX + 8, 200)
dashed(RX + 128, 156, 140, 100, "仮想マシン")
for k, lab in enumerate(["版A", "版B", "版C"]):
    icons.draw(c, "pc", RX + 160 + k * 38, 200, 26, INK2)
    text(RX + 160 + k * 38, 176, lab, 8.5, INK3, "c")
text(RX + 198, 162, "イメージから復元", 8.5, CYAN, "c")

# 右下：接続機器
text(RX + 22, 134, "接続機器", 10.5); badge(RX + 8, 138, 7)
il.printer(c, RX + 10, 44, s=0.4)
wire(BUS, 100, RX + 10, 100)
wire(RX + 92, 160, RX + 92, 124, INK3, 1.5, (3, 2)); text(RX + 98, 140, "USB", 8.5, INK3)
dashed(RX + 128, 44, 140, 98, "機器のシミュレーター")
icons.draw(c, "printer", RX + 198, 82, 40, INK2)

# 最右：物理を補う道具
TX = RX + 300
c.setStrokeColor(LINE); c.setLineWidth(1); c.line(TX - 14, 60, TX - 14, 372)
text(TX, 360, "物理を補う道具", 10.5, MAG)
tools = [("power", "遠隔の電源・USBの切り替え", 312), ("install", "自動インストール・端末の管理", 252)]
for kind, lab, yy in tools:
    icons.draw(c, kind, TX + 16, yy, 30, MAG); text(TX + 38, yy - 4, lab, 9.5)
il.robot_arm(c, TX, 112, s=0.62)
text(TX + 90, 168, "ロボット", 10); text(TX + 90, 154, "（ボタン・用紙）", 9, INK3); badge(TX + 80, 182, 8)
icons.draw(c, "screencheck", TX + 16, 80, 30, MAG); text(TX + 38, 76, "カメラで表示を確認", 9.5)
d.end()

# 8. 設備と、自動化に必要な技術
y = d.slide("設備・備品と、自動化に必要な技術", "図解：設備の全体図")
hdr = ["番号", "設備・備品", "役割", "自動化に必要な技術", "代わりにできるもの"]
wid = [40, 150, 240, 270, 164]
rows = [hdr,
        ["1", "アプリの置き場", "リリースされたアプリを保管し、テスト環境に配る",
         "CI（自動ビルド）、成果物の保管、署名の管理", "—"],
        ["2", "OSイメージの保管", "OSの版ごとのイメージを保管し、必要な環境を復元する",
         "仮想化、イメージの管理、自動の復元", "—"],
        ["3", "テスト用ネットワーク", "端末・PC・接続機器をつなぐ。分けた環境との受け渡し口",
         "ネットワークの構築、有線・無線の切り替え", "仮想ネットワーク（一部）"],
        ["4", "AIエージェントのPC", "テストの設計、実行の指示、判定を回す司令塔",
         "AIエージェント、自動操作の技術（Appium、Playwrightなど）", "—"],
        ["5", "テスト端末", "iOS・Androidの実機。どの端末・どのOSで試すかを指定する",
         "自動インストール（iOSはMac＋Xcode、Androidはadb）、端末の管理", "シミュレーター・エミュレーター"],
        ["6", "テストPC", "Windows・Macの実機", "仮想化、スナップショットからの復元", "仮想マシン"],
        ["7", "接続機器", "周辺機器の実機。USB・ネットワーク・無線でつなぐ",
         "遠隔の電源、USBの切り替え器、機器の一覧（データ）", "機器のシミュレーター"],
        ["8", "ロボット", "物理ボタンを押す、用紙を置くなど、人の手の代わり", "ロボットの制御、位置合わせ",
         "人の手（手順書）"],
        ["9", "カメラ・判定", "画面・表示パネル・出力物を確かめ、失敗の原因を調べる",
         "画像の比較、文字認識、ログ解析、AIによる判定", "—"],
        ]
d.table(rows, M, y, wid, size=9.5)
d.end()

# 9. AIエージェントのPCから、テストPCを動かす
y = d.slide("AIエージェントのPCから、テストPCを動かす", "図解：設備の全体図（続き）")
il.desktop(c, 52, 206, s=0.75, app_title="AIエージェント")
text(131, 190, "AIエージェントのPC", 11, INK, "c")
text(131, 175, "スクリプトを動かし、AIが判断する", 9, INK3, "c")
TX = 470; BX = 640; BW = W - M - BX
targets = [
    (406, "テストPC（実機）", "操作を受け付ける係<br/>Appiumサーバー、WinAppDriver、MCPサーバーなど"),
    (300, "仮想マシン", "仮想化ソフトの操作コマンド<br/>復元・起動・中でプログラムを実行（VMwareのvmrunなど）"),
    (194, "スマホ・タブレット", "端末をつないだPCのAppiumサーバー<br/>（iOSは端末をMacにつなぐ）"),
]
for i, (ty, title, desc) in enumerate(targets):
    text(TX, ty, title, 10.5)
    if i == 0:
        il.desktop(c, TX, ty - 86, s=0.45, app_title="テスト対象")
    elif i == 1:
        dashed(TX, ty - 92, 120, 82, "")
        icons.draw(c, "pc", TX + 36, ty - 50, 30, INK2); icons.draw(c, "pc", TX + 84, ty - 50, 30, INK2)
    else:
        il.desktop(c, TX, ty - 86, s=0.38, app_title="Appium")
        il.phone(c, TX + 92, ty - 84, s=1.0)
        wire(TX + 80, ty - 60, TX + 92, ty - 60, INK3, 1.5, (2, 2))
    label_box(BX, ty + 4, BW, 58, desc, MAG_S, size=10, accent=MAG)
    d.arrow(214, 262, TX - 10, ty - 40, color=CYAN)
text(330, 350, "命令がネットワーク越しに届く", 10, CYAN, "c")
text(330, 160, "画面の部品の木・スクリーンショット・", 9.5, INK3, "c")
text(330, 146, "結果がAIのPCに戻る", 9.5, INK3, "c")
d.box(M, 96, CW, 50, fill=YEL_S, accent=YEL)
d.para("<b>条件</b>：AIのPCとテストPCが、ネットワークで通信できること。テストPCでは、ユーザーがログインした画面で「係」を常駐させる"
       "（SSHなどで裏側から実行すると画面が無く、GUIを操作できない）。画面ロックとスリープは切る。",
       M + 18, 88, CW - 34, st(10.5, INK))
d.end()

# 10. 仮想マシンのネットワークの3つの形
y = d.slide("古いOSの仮想マシンを、AIのPCで動かすと安全？", "図解：ネットワークの形")
BAR = 400
d.box(M, BAR + 22, CW, 30, fill=GRN_S, accent=GRN)
text(W / 2, BAR + 2, "組織のネットワーク（AIを使える環境）", 11, GRN, "c")
pw = (CW - 2 * 20) / 3
modes = [
    ("① ブリッジ接続", "×", "仮想マシンも組織のネットワークの一台になる。古いOSを直接つなぐのと同じ。"),
    ("② NAT接続", "×〜△", "ホストを経由して外に出られる。古いOSから組織のネットワークに届いてしまう。"),
    ("③ ホストオンリー接続", "○", "仮想マシンはホストとしか通信できない。組織のネットワークからも見えない。隔離するならこの形。"),
]
for i, (title, mark, desc) in enumerate(modes):
    px = M + i * (pw + 20)
    hx, hw, hy0, hy1 = px + 10, pw - 20, 196, 340
    c.setFillColor(BG); c.setStrokeColor(INK3); c.setLineWidth(1)
    c.roundRect(hx, hy0, hw, hy1 - hy0, 8, fill=1, stroke=1)
    text(hx + 10, hy1 - 16, "AIのPC（ホスト）", 9.5, INK2)
    up = hx + hw - 40
    wire(up, hy1, up, BAR - 8, GRN, 3)
    label_box(hx + hw - 92, hy1 - 26, 82, 30, "AIエージェント", CYAN_S, size=9)
    vx, vw, vy0, vy1 = hx + 16, 110, 212, 268
    label_box(vx, vy1, vw, vy1 - vy0, "古いOSの<br/>仮想マシン", YEL_S, size=9.5, accent=YEL)
    vtop = vx + 30
    if i == 0:
        wire(vtop, vy1, vtop, BAR - 8, MAG, 3)
        text(vtop + 6, 360, "直接参加", 9, MAG)
    elif i == 1:
        wire(vtop, vy1, vtop, 276, MAG, 2, (4, 3)); wire(vtop, 276, up, 276, MAG, 2, (4, 3)); wire(up, 276, up, 284, MAG, 2, (4, 3))
        text(vtop + 6, 280, "ホストを経由", 9, MAG)
    else:
        wire(vx + vw, 250, hx + hw - 51, 250, GRN, 2); wire(hx + hw - 51, 250, hx + hw - 51, 284, GRN, 2)
        text(vx + vw + 6, 236, "ホストとだけ", 9, GRN)
    text(px + pw / 2, 176, "%s　%s" % (title, mark), 12, INK, "c")
    d.para(desc, px + 10, 162, pw - 20, st(10, INK2))
d.box(M, 96, CW, 50, fill=YEL_S, accent=YEL)
d.para("<b>「VMwareで動かしているから安全」ではない</b>。安全かどうかはネットワークの形で決まる。隔離するならホストオンリー接続にし、"
       "共有フォルダ・クリップボードの共有を切り、仮想化ソフトを最新に保つ。最終判断は組織のセキュリティ部門。",
       M + 18, 88, CW - 34, st(10.5, INK))
d.end()

# 11. つなぎ目の選択肢
y = d.slide("AIの環境と、古いOS・テスト用LANをつなぐ選択肢", "整理")
hdr = ["選択肢", "古いOSの隔離", "USBの機器", "ネットワークの機器", "注意"]
wid = [230, 90, 80, 110, 354]
rows = [hdr,
        ["A. AIのPCで、ホストオンリー接続の仮想マシン", "○", "○ USBを渡す", "×",
         "テスト用LANの機器には届かない。共有機能を切る"],
        ["B. テスト用LAN専用の差し口に、仮想マシンだけをつなぐ", "△", "○", "○",
         "1台が両方のネットワークにつながる形。承認のハードルが高い"],
        ["C. 管理されたつなぎ目（ファイアウォールで決まった通信だけ許可）", "○", "—", "○",
         "AIのPCからテスト用LANへ、操作に使う通信だけを通す。正攻法だが、設計と承認が要る"],
        ["D. 手動で持ち込む", "◎", "○", "○", "安全。往復に人手と時間がかかる"],
        ["E. テスト用LANの中にAIを置く", "○", "○", "○",
         "ローカルLLMなど。GPUマシンとモデルの持ち込み、精度が課題"],
        ]
h = d.table(rows, M, y, wid, size=10)
d.box(M, y - h - 16, CW, 72, fill=BG, accent=INK)
d.para("<b>セキュリティ部門に確かめる質問の例</b><br/>"
       "・ホストオンリー接続の仮想マシンは「ネットワークにつないだ」とみなすか　・2つのネットワークに足を持つPCは許されるか<br/>"
       "・区間をまたぐ決まった通信の許可を申請できるか　・AIに送る画面やログの扱い（含まれる情報の範囲）",
       M + 20, y - h - 28, CW - 40, st(11, INK))
d.end()

# 12. 接続機器との通信テストの3つの層
y = d.slide("接続機器との通信テストは、3つの層に分ける", "整理")
layers = [
    (0.50, "<b>③ 実機とのE2E（件数を絞る）</b><br/>テスト用LANの「決まった手順だけ動かす実行係」が自動で回す。"
     "結果を持ち帰り、AIが判定。出力物はカメラやスキャナーで画像にして判定", MAG, MAG_S, "テスト用LAN"),
    (0.75, "<b>② 機器のシミュレーターで通信を確かめる</b><br/>機器の検出・状態の問い合わせ・データの受け取りを真似るシミュレーターを、"
     "ホストオンリーのネットワークに置く。実機の癖は捕まえられない", CYAN, CYAN_S, "AIのPC 1台"),
    (1.00, "<b>① 出力データを確かめる（件数の大半）</b><br/>アプリやドライバが作った送信データ（印刷なら印刷データ）をファイルとして取り出し、"
     "期待どおりの正解データと比べる。実機は要らない", GRN, GRN_S, "AIのPC 1台"),
]
LW = CW - 120
for i, (ratio, body, a, f, where) in enumerate(layers):
    w = LW * ratio; x = M + (LW - w) / 2; yt = y - 4 - i * 82
    d.box(x, yt, w, 72, fill=f, accent=a)
    d.para(body, x + 16, yt - 10, w - 28, st(10.5, INK))
    label_box(M + LW + 16, yt - 16, 104, 40, where, PAPER if i else PAPER, size=10, color=a)
    c.setStrokeColor(a); c.setLineWidth(1); c.roundRect(M + LW + 16, yt - 56, 104, 40, 4, fill=0, stroke=1)
text(M + LW + 68, y + 2, "どこで動かすか", 9.5, INK3, "c")
text(M + LW / 2, y - 254, "↑ 上ほど実機に近く件数は少ない　↓ 下ほど速く安く、件数を多く回す", 9.5, INK3, "c")
d.box(M, y - 266, CW, 64, fill=YEL_S, accent=YEL)
d.para("<b>契約テストという考え方</b>：アプリと機器のあいだの「通信の約束（仕様）」を決め、アプリ側も機器側も"
       "それぞれ単独でその約束を守っているかを確かめる。両方が約束を守っていれば、実機をつなぐE2Eは代表的な確認だけで済む。",
       M + 20, y - 278, CW - 40, st(11, INK))
d.end()

# 13. 物理を技術で補う
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

# 14. 進め方の例
y = d.slide("進め方の例：小さく試し、根拠を作り、つなぎ目を整える", "進め方（一般論）")
steps6 = [
    ("1. 棚卸し", "今のテストを「OSで差が出るか」「実機が要るか」で分類する。過去の不具合を「実機でしか出なかったか」で分ける。", GRN, GRN_S),
    ("2. 小さく試す", "1つのアプリ・1つのOSで、AIのPC＋ホストオンリーの仮想マシンを使い、設計〜実行〜判定までAIに回させる。", GRN, GRN_S),
    ("3. 下の層を厚くする", "出力データの確認と、機器のシミュレーターを作る。契約テストの約束を、機器の担当と決める。", CYAN, CYAN_S),
    ("4. つなぎ目を相談する", "セキュリティ部門と、テスト用LANとの受け渡しの手段や、決まった通信の許可を相談する。", CYAN, CYAN_S),
    ("5. 実機のE2Eを自動にする", "テスト用LANに実行係を置き、件数を絞った実機のテストを自動で回す。", MAG, MAG_S),
    ("6. 役割を整える", "品質の設計・AIドリブンテスト・テストの基盤の3つの役割と、テストレベルの分担を見直す。", MAG, MAG_S),
]
cw6 = (CW - 2 * 28) / 3
for i, (hd, bd, a, f) in enumerate(steps6):
    r, col = divmod(i, 3)
    x = M + col * (cw6 + 28); yt = y - 4 - r * 140
    d.card(x, yt, cw6, 122, hd, bd, accent=a, fill=f, head_size=13.5, body_size=10.5)
    if col < 2:
        d.arrow(x + cw6 + 4, yt - 61, x + cw6 + 24, yt - 61)
d.box(M, y - 290, CW, 50, fill=BG, accent=INK)
d.para("<b>効果を測る指標の例</b>：テスト環境の準備時間、AIで回せたテストの割合、実機テストの件数、"
       "見つけた不具合の数と見逃し、1回の確認にかかる時間。",
       M + 20, y - 302, CW - 40, st(11, INK))
d.end()

# 15. まとめ：役割と必要な技術
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
