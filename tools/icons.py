"""スライド用のシンプルなベクターアイコン（reportlab の canvas に直接描く）。
draw(c, kind, cx, cy, s, color) — (cx, cy) を中心に、一辺 s の正方形に収まるように描く。
"""
import math


def _setup(c, color, lw):
    c.setStrokeColor(color); c.setFillColor(color); c.setLineWidth(lw)
    c.setLineCap(1); c.setLineJoin(1)


def draw(c, kind, cx, cy, s, color, bg=None):
    u = s / 24.0  # 24単位のグリッドで描く
    X = lambda v: cx - s / 2 + v * u
    Y = lambda v: cy + s / 2 - v * u   # 上から下へ
    lw = max(0.8, 1.6 * u)
    _setup(c, color, lw)
    c.saveState()
    f = globals().get("_" + kind)
    if f:
        f(c, X, Y, u, color, bg)
    else:
        c.circle(cx, cy, s / 3, fill=0, stroke=1)
    c.restoreState()


def _rect(c, X, Y, x, y, w, h, fill=0, r=0):
    if r:
        c.roundRect(X(x), Y(y + h), w * (X(1) - X(0)), h * (X(1) - X(0)), r, fill=fill, stroke=1)
    else:
        c.rect(X(x), Y(y + h), w * (X(1) - X(0)), h * (X(1) - X(0)), fill=fill, stroke=1)


def _line(c, X, Y, x1, y1, x2, y2):
    c.line(X(x1), Y(y1), X(x2), Y(y2))


def _poly(c, X, Y, pts, fill=0, close=True):
    p = c.beginPath(); p.moveTo(X(pts[0][0]), Y(pts[0][1]))
    for a, b in pts[1:]:
        p.lineTo(X(a), Y(b))
    if close:
        p.close()
    c.drawPath(p, fill=fill, stroke=1)


def _doc(c, X, Y, u, col, bg):          # テストケース（書類）
    _poly(c, X, Y, [(5, 2), (15, 2), (19, 6), (19, 22), (5, 22)])
    _poly(c, X, Y, [(15, 2), (15, 6), (19, 6)], close=False)
    for yy in (10, 13.5, 17):
        _line(c, X, Y, 8, yy, 16, yy)


def _funnel(c, X, Y, u, col, bg):       # 回すテストの選択
    _poly(c, X, Y, [(3, 4), (21, 4), (14, 13), (14, 20), (10, 22), (10, 13)])


def _grid(c, X, Y, u, col, bg):         # 組み合わせの設計
    for i in range(3):
        for j in range(3):
            _rect(c, X, Y, 3 + i * 6.3, 3 + j * 6.3, 5, 5, fill=1 if (i + j) % 2 == 0 else 0)


def _images(c, X, Y, u, col, bg):       # テストデータ
    _rect(c, X, Y, 6, 3, 15, 12)
    _rect(c, X, Y, 3, 8, 15, 13, fill=0)
    _poly(c, X, Y, [(5, 19), (9, 14), (12, 17), (14, 15), (16, 19)])
    c.circle(X(14), Y(11), 1.3 * u, fill=1, stroke=0)


def _pc(c, X, Y, u, col, bg):           # テストPC
    _rect(c, X, Y, 2, 3, 20, 13, r=1.5 * u)
    _line(c, X, Y, 12, 16, 12, 20)
    _line(c, X, Y, 7, 21, 17, 21)
    _poly(c, X, Y, [(9, 7), (9, 12), (14, 12)], close=False)   # 復元の矢印
    _poly(c, X, Y, [(9, 7), (14, 7), (15.5, 9.5)], close=False)


def _install(c, X, Y, u, col, bg):      # ツールのインストール
    _poly(c, X, Y, [(3, 12), (12, 16), (21, 12), (21, 21), (12, 23), (3, 21)])
    _line(c, X, Y, 12, 16, 12, 23)
    _line(c, X, Y, 12, 2, 12, 11)
    _poly(c, X, Y, [(8.5, 7.5), (12, 11), (15.5, 7.5)], close=False)


def _update(c, X, Y, u, col, bg):       # 最新化
    cx, cy, r = X(12), Y(12), 8 * u
    c.arc(cx - r, cy - r, cx + r, cy + r, 30, 150)
    c.arc(cx - r, cy - r, cx + r, cy + r, 210, 150)
    _poly(c, X, Y, [(17, 4), (19.5, 7.5), (15.5, 8)], fill=1)
    _poly(c, X, Y, [(7, 20), (4.5, 16.5), (8.5, 16)], fill=1)


def _printer(c, X, Y, u, col, bg):      # プリンター
    _rect(c, X, Y, 6, 2, 12, 6)
    _rect(c, X, Y, 2, 8, 20, 9, r=1.5 * u)
    _rect(c, X, Y, 6, 14, 12, 8)
    _line(c, X, Y, 8.5, 17.5, 15.5, 17.5)
    _line(c, X, Y, 8.5, 20, 13, 20)
    c.circle(X(18.5), Y(11), 0.9 * u, fill=1, stroke=0)


def _phone(c, X, Y, u, col, bg):        # モバイル端末
    _rect(c, X, Y, 7, 2, 10, 20, r=2 * u)
    _line(c, X, Y, 10.5, 19, 13.5, 19)


def _paper(c, X, Y, u, col, bg):        # 用紙・原稿
    _rect(c, X, Y, 7, 2, 13, 16)
    _rect(c, X, Y, 4, 6, 13, 16, fill=0)
    if bg is not None:
        c.setFillColor(bg); _rect(c, X, Y, 4, 6, 13, 16, fill=1); c.setFillColor(col)


def _cursor(c, X, Y, u, col, bg):       # 画面の操作
    _rect(c, X, Y, 2, 3, 20, 15, r=1 * u)
    _line(c, X, Y, 2, 7, 22, 7)
    _poly(c, X, Y, [(11, 10), (11, 22), (14, 19), (16.5, 23.5), (18.5, 22.5), (16, 18), (20, 18)], fill=1)


def _combo(c, X, Y, u, col, bg):        # 多種多様な組み合わせの実行
    for i in range(3):
        for j in range(3):
            _rect(c, X, Y, 2 + i * 5, 2 + j * 5, 4, 4, fill=1)
    _poly(c, X, Y, [(15, 11), (23, 17), (15, 23)], fill=1)


def _power(c, X, Y, u, col, bg):        # 本体の操作（電源・パネル）
    cx, cy, r = X(12), Y(13), 8 * u
    c.arc(cx - r, cy - r, cx + r, cy + r, 125, 290)
    _line(c, X, Y, 12, 2, 12, 12)


def _robot(c, X, Y, u, col, bg):        # ロボットアーム
    _rect(c, X, Y, 3, 20, 10, 3, fill=1)
    _line(c, X, Y, 8, 20, 8, 13)
    _line(c, X, Y, 8, 13, 16, 6)
    c.circle(X(8), Y(13), 1.6 * u, fill=1, stroke=0)
    c.circle(X(16), Y(6), 1.6 * u, fill=1, stroke=0)
    _poly(c, X, Y, [(16, 6), (21, 4), (20, 2)], close=False)
    _poly(c, X, Y, [(16, 6), (21, 9), (22, 7)], close=False)


def _warning(c, X, Y, u, col, bg):      # エラー状態
    _poly(c, X, Y, [(12, 2), (22.5, 21), (1.5, 21)])
    _line(c, X, Y, 12, 8, 12, 14.5)
    c.circle(X(12), Y(17.5), 1.1 * u, fill=1, stroke=0)


def _clock(c, X, Y, u, col, bg):        # 定時・並列の実行
    c.circle(X(12), Y(12), 9.5 * u, fill=0, stroke=1)
    _line(c, X, Y, 12, 12, 12, 6)
    _line(c, X, Y, 12, 12, 16.5, 14.5)


def _screencheck(c, X, Y, u, col, bg):  # 画面の判定
    _rect(c, X, Y, 2, 3, 20, 15, r=1 * u)
    _poly(c, X, Y, [(7, 11), (10.5, 14.5), (17, 7.5)], close=False)
    _line(c, X, Y, 8, 21, 16, 21)


def _status(c, X, Y, u, col, bg):       # ジョブ・機器状態の判定
    for i, h in enumerate((5, 9, 13, 17)):
        _rect(c, X, Y, 2 + i * 4.5, 20 - h, 3, h, fill=1)
    c.circle(X(19), Y(6), 4 * u, fill=0, stroke=1)
    _poly(c, X, Y, [(17, 6), (18.5, 7.5), (21, 4.5)], close=False)


def _code(c, X, Y, u, col, bg):         # 印刷データの判定
    _poly(c, X, Y, [(4, 2), (15, 2), (20, 7), (20, 22), (4, 22)])
    _poly(c, X, Y, [(9.5, 10), (7, 13.5), (9.5, 17)], close=False)
    _poly(c, X, Y, [(14.5, 10), (17, 13.5), (14.5, 17)], close=False)


def _printcheck(c, X, Y, u, col, bg):   # 印刷物の判定（目視の代わり）
    _rect(c, X, Y, 3, 2, 13, 17)
    for yy in (6, 9, 12):
        _line(c, X, Y, 6, yy, 13, yy)
    c.circle(X(15.5), Y(15.5), 4.5 * u, fill=0, stroke=1)
    _line(c, X, Y, 18.8, 18.8, 22, 22)


def _scanimg(c, X, Y, u, col, bg):      # スキャン画像の判定
    _rect(c, X, Y, 2, 4, 20, 16, r=1 * u)
    _poly(c, X, Y, [(4, 18), (10, 11), (14, 15), (16.5, 12.5), (20, 18)])
    c.circle(X(16), Y(8), 1.6 * u, fill=1, stroke=0)
    _line(c, X, Y, 1, 12, 23, 12)


def _magnify(c, X, Y, u, col, bg):      # 失敗の切り分け
    c.circle(X(10), Y(10), 7 * u, fill=0, stroke=1)
    _line(c, X, Y, 15, 15, 22, 22)
    _line(c, X, Y, 7, 10, 13, 10)


def _chart(c, X, Y, u, col, bg):        # 結果の集計・報告
    _line(c, X, Y, 3, 2, 3, 21)
    _line(c, X, Y, 3, 21, 22, 21)
    for i, h in enumerate((7, 12, 9, 16)):
        _rect(c, X, Y, 6 + i * 4, 20 - h, 2.6, h, fill=1)


def _bug(c, X, Y, u, col, bg):          # 不具合の起票
    c.ellipse(X(7), Y(21), X(17), Y(7), fill=0, stroke=1)
    c.circle(X(12), Y(5), 2.5 * u, fill=1, stroke=0)
    for yy in (11, 15, 19):
        _line(c, X, Y, 3, yy - 1, 7, yy)
        _line(c, X, Y, 17, yy, 21, yy - 1)
    _line(c, X, Y, 12, 8, 12, 21)


def _wrench(c, X, Y, u, col, bg):       # スクリプトの修正
    c.setLineWidth(3.2 * u)
    _line(c, X, Y, 6, 18, 14, 10)
    c.setLineWidth(1.6 * u)
    c.circle(X(16.5), Y(7.5), 4.5 * u, fill=0, stroke=1)
    _poly(c, X, Y, [(5, 21), (3, 19), (5.5, 16.5), (7.5, 18.5)], fill=1)


def _golden(c, X, Y, u, col, bg):       # 正解データの更新
    cx, w = X(10), 7 * u
    c.ellipse(X(3), Y(7), X(17), Y(3), fill=0, stroke=1)
    _line(c, X, Y, 3, 5, 3, 19)
    _line(c, X, Y, 17, 5, 17, 19)
    c.arc(X(3), Y(21), X(17), Y(17), 180, 180)
    c.arc(X(3), Y(14), X(17), Y(10), 180, 180)
    pts = []
    for k in range(10):
        r = (4.5 if k % 2 == 0 else 2) * u
        a = math.pi / 2 + k * math.pi / 5
        pts.append((X(18.5) + r * math.cos(a), Y(17) + r * math.sin(a)))
    p = c.beginPath(); p.moveTo(*pts[0])
    for q in pts[1:]:
        p.lineTo(*q)
    p.close(); c.drawPath(p, fill=1, stroke=0)


def _tag(c, X, Y, u, col, bg):          # ID・文言の変更の検知
    _poly(c, X, Y, [(2, 4), (12, 4), (22, 13), (13, 22), (2, 12)])
    c.circle(X(7), Y(9), 1.6 * u, fill=0, stroke=1)
    _line(c, X, Y, 11, 13, 15, 13)


def _person(c, X, Y, u, col, bg):       # 人物
    c.circle(X(12), Y(7), 4.5 * u, fill=1, stroke=0)
    p = c.beginPath(); p.moveTo(X(3), Y(23)); p.curveTo(X(3), Y(13), X(21), Y(13), X(21), Y(23)); p.close()
    c.drawPath(p, fill=1, stroke=0)


def _server(c, X, Y, u, col, bg):       # 実行基盤
    for i in range(3):
        _rect(c, X, Y, 3, 2 + i * 7, 18, 5.5, r=1 * u)
        c.circle(X(6.5), Y(4.8 + i * 7), 0.9 * u, fill=1, stroke=0)
        _line(c, X, Y, 10, 4.8 + i * 7, 18, 4.8 + i * 7)


def _source(c, X, Y, u, col, bg):       # ソースコード
    _rect(c, X, Y, 2, 3, 20, 18, r=1 * u)
    _poly(c, X, Y, [(9, 8), (5.5, 12), (9, 16)], close=False)
    _poly(c, X, Y, [(15, 8), (18.5, 12), (15, 16)], close=False)
    _line(c, X, Y, 13.5, 7, 10.5, 17)
