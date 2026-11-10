"""スライド用のイラスト（プリンター、デスクトップPC、Excelのシート、ロボットアーム、印刷物）。
各関数は (x, y) を左下として描き、部位の座標（引き出し線の起点）を dict で返す。
"""
from reportlab.lib.colors import HexColor

BODY = HexColor("#E6E9ED"); BODY_D = HexColor("#C5CBD2"); EDGE = HexColor("#9AA3AD")
DARK = HexColor("#2E3742"); SCREEN = HexColor("#8FD0EE"); WHITE = HexColor("#FFFFFF")
PAPERC = HexColor("#FBFBF8"); LINEC = HexColor("#B9C0C8"); XL = HexColor("#1D6F42"); XL_S = HexColor("#E8F3EC")


def _rr(c, x, y, w, h, r, fill, stroke=EDGE, lw=1):
    c.setFillColor(fill); c.setLineWidth(lw)
    if stroke is not None:
        c.setStrokeColor(stroke)
    c.roundRect(x, y, w, h, r, fill=1, stroke=1 if stroke else 0)


def printer(c, x, y, s=1.0):
    """複合機（インクジェット）。幅 240*s、高さ 196*s"""
    S = lambda v: v * s
    a = {}
    # 本体
    _rr(c, x, y + S(6), S(240), S(126), S(10), BODY)
    c.setFillColor(BODY_D); c.rect(x + S(4), y + S(6), S(232), S(6), fill=1, stroke=0)
    # 給紙トレイ（カセット）
    _rr(c, x + S(16), y + S(16), S(208), S(36), S(4), BODY_D)
    c.setFillColor(PAPERC); c.setStrokeColor(LINEC); c.rect(x + S(26), y + S(44), S(188), S(5), fill=1, stroke=1)
    c.rect(x + S(26), y + S(47), S(188), S(3), fill=1, stroke=1)
    _rr(c, x + S(95), y + S(24), S(50), S(8), S(3), EDGE, stroke=None)
    a["tray"] = (x + S(120), y + S(28))
    # 排紙口と排紙トレイ・印刷物
    c.setFillColor(DARK); c.rect(x + S(50), y + S(70), S(140), S(8), fill=1, stroke=0)
    c.setFillColor(PAPERC); c.setStrokeColor(LINEC); c.rect(x + S(66), y + S(58), S(108), S(16), fill=1, stroke=1)
    c.setStrokeColor(LINEC)
    for k in range(3):
        c.line(x + S(74), y + S(70 - k * 4), x + S(150 - k * 18), y + S(70 - k * 4))
    a["output"] = (x + S(174), y + S(66))
    # 操作パネル
    _rr(c, x + S(12), y + S(96), S(112), S(28), S(4), DARK, stroke=None)
    _rr(c, x + S(18), y + S(101), S(48), S(18), S(2), SCREEN, stroke=None)
    for k in range(3):
        c.setFillColor(HexColor("#5C6875")); c.circle(x + S(80 + k * 14), y + S(110), S(4), fill=1, stroke=0)
    a["panel"] = (x + S(42), y + S(124))
    # 電源ボタン
    c.setFillColor(DARK); c.circle(x + S(222), y + S(110), S(7), fill=1, stroke=0)
    c.setStrokeColor(HexColor("#7EE2A8")); c.setLineWidth(S(1.4))
    c.arc(x + S(218), y + S(106), x + S(226), y + S(114), 120, 300); c.line(x + S(222), y + S(110), x + S(222), y + S(115))
    a["power"] = (x + S(222), y + S(117))
    # スキャナー部と原稿台・ADF
    _rr(c, x + S(6), y + S(132), S(228), S(30), S(6), BODY)
    c.setStrokeColor(EDGE); c.setLineWidth(1); c.line(x + S(12), y + S(140), x + S(228), y + S(140))
    _rr(c, x + S(30), y + S(162), S(180), S(20), S(5), BODY_D)
    c.setFillColor(PAPERC); c.setStrokeColor(LINEC)
    p = c.beginPath(); p.moveTo(x + S(56), y + S(182)); p.lineTo(x + S(184), y + S(182)); p.lineTo(x + S(176), y + S(196)); p.lineTo(x + S(64), y + S(196)); p.close()
    c.drawPath(p, fill=1, stroke=1)
    a["adf"] = (x + S(120), y + S(196))
    # 本体の中（ファームウェア）
    a["inside"] = (x + S(210), y + S(86))
    a["top"] = (x + S(120), y + S(200))
    a["left"] = (x, y + S(80)); a["right"] = (x + S(240), y + S(80))
    return a


def desktop(c, x, y, s=1.0, app_title="印刷アプリ"):
    """デスクトップPC（モニター＋本体＋キーボード）。幅 210*s、高さ 150*s"""
    S = lambda v: v * s
    a = {}
    # 本体（タワー）
    _rr(c, x + S(162), y + S(20), S(48), S(126), S(5), BODY)
    c.setFillColor(DARK); c.rect(x + S(170), y + S(124), S(32), S(4), fill=1, stroke=0)
    c.rect(x + S(170), y + S(116), S(32), S(4), fill=1, stroke=0)
    c.setFillColor(HexColor("#4FB37A")); c.circle(x + S(186), y + S(36), S(4), fill=1, stroke=0)
    a["tower"] = (x + S(186), y + S(20))
    # モニター
    _rr(c, x, y + S(46), S(152), S(100), S(6), DARK, stroke=None)
    _rr(c, x + S(6), y + S(54), S(140), S(86), S(2), WHITE, stroke=None)
    # アプリの画面
    c.setFillColor(HexColor("#0B7AA3")); c.rect(x + S(14), y + S(122), S(124), S(12), fill=1, stroke=0)
    c.setFillColor(WHITE); c.setFont("HeiseiKakuGo-W5", S(7)); c.drawString(x + S(18), y + S(125), app_title)
    c.setFillColor(HexColor("#F2F4F6")); c.setStrokeColor(LINEC); c.rect(x + S(14), y + S(62), S(124), S(60), fill=1, stroke=1)
    c.setStrokeColor(LINEC)
    for k in range(3):
        c.line(x + S(22), y + S(110 - k * 10), x + S(96), y + S(110 - k * 10))
    _rr(c, x + S(98), y + S(68), S(34), S(12), S(2), HexColor("#0B7AA3"), stroke=None)
    c.setFillColor(WHITE); c.setFont("HeiseiKakuGo-W5", S(6.5)); c.drawCentredString(x + S(115), y + S(71.5), "印刷")
    # マウスカーソル
    c.setFillColor(DARK)
    p = c.beginPath(); px, py = x + S(118), y + S(76)
    p.moveTo(px, py); p.lineTo(px, py - S(12)); p.lineTo(px + S(3.5), py - S(9)); p.lineTo(px + S(6), py - S(14)); p.lineTo(px + S(8), py - S(13)); p.lineTo(px + S(5.5), py - S(8)); p.lineTo(px + S(9.5), py - S(8)); p.close()
    c.drawPath(p, fill=1, stroke=0)
    a["screen"] = (x + S(76), y + S(146))
    # スタンド
    c.setFillColor(BODY_D); c.rect(x + S(66), y + S(32), S(20), S(14), fill=1, stroke=0)
    _rr(c, x + S(46), y + S(26), S(60), S(7), S(3), BODY_D, stroke=None)
    # キーボード
    _rr(c, x + S(10), y, S(132), S(16), S(3), BODY, stroke=EDGE)
    c.setFillColor(BODY_D)
    for r in range(2):
        for k in range(14):
            c.rect(x + S(16 + k * 9), y + S(3 + r * 6), S(7), S(4), fill=1, stroke=0)
    a["left"] = (x, y + S(96)); a["right"] = (x + S(210), y + S(96))
    return a


def phone(c, x, y, s=1.0):
    S = lambda v: v * s
    _rr(c, x, y, S(30), S(56), S(5), DARK, stroke=None)
    _rr(c, x + S(3), y + S(6), S(24), S(44), S(2), WHITE, stroke=None)
    c.setFillColor(HexColor("#0B7AA3")); c.rect(x + S(3), y + S(44), S(24), S(6), fill=1, stroke=0)
    return {"center": (x + S(15), y + S(28)), "top": (x + S(15), y + S(56))}


def excel(c, x, y, w, h, title="テストケース.xlsx"):
    """Excelのシート風"""
    a = {}
    _rr(c, x, y, w, h, 4, WHITE, stroke=EDGE)
    c.setFillColor(XL); c.roundRect(x, y + h - 16, w, 16, 4, fill=1, stroke=0); c.rect(x, y + h - 16, w, 6, fill=1, stroke=0)
    c.setFillColor(WHITE); c.setFont("HeiseiKakuGo-W5", 8.5); c.drawString(x + 18, y + h - 12, title)
    c.setFillColor(WHITE); c.rect(x + 5, y + h - 12, 9, 9, fill=1, stroke=0)
    c.setFillColor(XL); c.setFont("HeiseiKakuGo-W5", 7); c.drawCentredString(x + 9.5, y + h - 10.5, "X")
    # 表
    top = y + h - 20; cols = [x + 4, x + 18, x + w * 0.45, x + w * 0.72, x + w - 4]
    rows = 7; rh = (top - (y + 6)) / rows
    c.setFillColor(HexColor("#EEF1F4")); c.rect(x + 4, top - rh, w - 8, rh, fill=1, stroke=0)
    c.setFillColor(XL_S); c.rect(x + 4, top - rows * rh, 14, rows * rh, fill=1, stroke=0)
    c.setStrokeColor(LINEC); c.setLineWidth(0.6)
    for r in range(rows + 1):
        c.line(x + 4, top - r * rh, x + w - 4, top - r * rh)
    for cx in cols:
        c.line(cx, top, cx, top - rows * rh)
    heads = ["項目", "手順", "結果"]
    c.setFont("HeiseiKakuGo-W5", 6.5); c.setFillColor(HexColor("#4A5563"))
    for i, t in enumerate(heads):
        c.drawString(cols[i + 1] + 3, top - rh + 3, t)
    for r in range(1, rows):
        yy = top - (r + 1) * rh + rh / 2
        c.setFillColor(HexColor("#4A5563")); c.drawCentredString(x + 11, yy - 2, str(r))
        c.setStrokeColor(HexColor("#C9CED6")); c.setLineWidth(1.2)
        c.line(cols[1] + 4, yy, cols[2] - 6 - (r % 3) * 6, yy)
        c.line(cols[2] + 4, yy, cols[3] - 4 - (r % 2) * 8, yy)
        c.setFillColor(HexColor("#2C7A4B") if r != 4 else HexColor("#B1306B"))
        c.drawCentredString((cols[3] + cols[4]) / 2, yy - 2.5, "OK" if r != 4 else "NG")
    a["bottom"] = (x + w / 2, y); a["right"] = (x + w, y + h / 2)
    return a


def robot_arm(c, x, y, s=1.0, color=HexColor("#B1306B")):
    """ロボットアーム。左下 (x, y)、幅 100*s、高さ 110*s。右下へ手を伸ばす"""
    S = lambda v: v * s
    a = {}
    _rr(c, x, y, S(44), S(12), S(3), DARK, stroke=None)
    c.setFillColor(color); c.circle(x + S(22), y + S(18), S(9), fill=1, stroke=0)
    c.setStrokeColor(color); c.setLineCap(1)
    c.setLineWidth(S(10)); c.line(x + S(22), y + S(18), x + S(40), y + S(84))
    c.setLineWidth(S(8)); c.line(x + S(40), y + S(84), x + S(86), y + S(60))
    c.setFillColor(DARK); c.circle(x + S(40), y + S(84), S(7), fill=1, stroke=0)
    c.circle(x + S(86), y + S(60), S(5), fill=1, stroke=0)
    c.setStrokeColor(DARK); c.setLineWidth(S(3))
    c.line(x + S(86), y + S(60), x + S(94), y + S(46)); c.line(x + S(86), y + S(60), x + S(100), y + S(54))
    # つかんでいる用紙
    c.setFillColor(PAPERC); c.setStrokeColor(LINEC); c.setLineWidth(1)
    p = c.beginPath(); p.moveTo(x + S(92), y + S(50)); p.lineTo(x + S(118), y + S(40)); p.lineTo(x + S(110), y + S(20)); p.lineTo(x + S(84), y + S(30)); p.close()
    c.drawPath(p, fill=1, stroke=1)
    a["hand"] = (x + S(100), y + S(40)); a["top"] = (x + S(40), y + S(92))
    return a


def printout(c, x, y, w, h):
    """印刷物（写真と文字の入った用紙）"""
    _rr(c, x, y, w, h, 2, PAPERC, stroke=LINEC)
    c.setFillColor(HexColor("#BFE3F2")); c.rect(x + 6, y + h * 0.5, w - 12, h * 0.42, fill=1, stroke=0)
    c.setFillColor(HexColor("#6BBF8A"))
    p = c.beginPath(); p.moveTo(x + 6, y + h * 0.5); p.lineTo(x + w * 0.4, y + h * 0.8); p.lineTo(x + w * 0.6, y + h * 0.62); p.lineTo(x + w - 6, y + h * 0.5); p.close()
    c.drawPath(p, fill=1, stroke=0)
    c.setStrokeColor(LINEC); c.setLineWidth(1.2)
    for k in range(4):
        c.line(x + 6, y + h * 0.4 - k * h * 0.09, x + w - 6 - (k % 2) * 10, y + h * 0.4 - k * h * 0.09)
    return {"right": (x + w, y + h / 2), "left": (x, y + h / 2), "bottom": (x + w / 2, y), "top": (x + w / 2, y + h)}


def magnifier(c, x, y, r, color=HexColor("#2E3742")):
    c.setStrokeColor(color); c.setLineWidth(r * 0.28); c.setFillColor(HexColor("#FFFFFF"))
    c.circle(x, y, r, fill=0, stroke=1)
    c.setLineWidth(r * 0.42); c.setLineCap(1)
    c.line(x + r * 0.72, y - r * 0.72, x + r * 1.6, y - r * 1.6)
