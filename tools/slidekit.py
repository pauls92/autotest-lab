"""スライドPDFを reportlab で描くための小さな部品集（16:9、日本語）。"""
import math
from reportlab.pdfgen import canvas as _canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.lib.colors import HexColor
from reportlab.platypus import Paragraph, Table, TableStyle
from reportlab.lib.styles import ParagraphStyle

pdfmetrics.registerFont(UnicodeCIDFont("HeiseiKakuGo-W5"))
JP = "HeiseiKakuGo-W5"
W, H = 960, 540
M = 48

INK = HexColor("#1A222D"); INK2 = HexColor("#4A5563"); INK3 = HexColor("#7A8592")
LINE = HexColor("#D6DCE3"); BG = HexColor("#F2F4F6"); PAPER = HexColor("#FFFFFF")
CYAN = HexColor("#0B7AA3"); CYAN_S = HexColor("#E3F1F7")
MAG = HexColor("#B1306B"); MAG_S = HexColor("#F8E6EF")
GRN = HexColor("#2C7A4B"); GRN_S = HexColor("#E2F2E8")
YEL = HexColor("#9A7300"); YEL_S = HexColor("#FBF3D6")
KEY_S = HexColor("#E8EAEE")


def st(size=13, color=INK, leading=None, align=0):
    return ParagraphStyle("s", fontName=JP, fontSize=size, leading=leading or size * 1.55,
                          textColor=color, wordWrap="CJK", alignment=align)


class Deck:
    def __init__(self, path, title, footer, total):
        self.c = _canvas.Canvas(path, pagesize=(W, H))
        self.c.setTitle(title); self.c.setAuthor("自動テストチーム")
        self.footer = footer; self.total = total; self.page = 0

    def para(self, text, x, ytop, w, style):
        p = Paragraph(text, style); _, h = p.wrap(w, 1000); p.drawOn(self.c, x, ytop - h); return h

    def cover(self, kicker, title, subtitle, lede, notes):
        c = self.c; self.page += 1
        c.setFillColor(INK); c.rect(0, 0, W, H, fill=1, stroke=0)
        c.setFillColor(CYAN); c.rect(0, 0, 14, H, fill=1, stroke=0)
        c.setFont(JP, 13); c.setFillColor(HexColor("#9FB3C8")); c.drawString(80, 380, kicker)
        c.setFont(JP, 40); c.setFillColor(PAPER); c.drawString(80, 318, title)
        c.setFont(JP, 26); c.drawString(80, 276, subtitle)
        self.para(lede, 80, 236, 680, st(14, HexColor("#C9D3DE")))
        c.setFont(JP, 11); c.setFillColor(HexColor("#9FB3C8"))
        for i, n in enumerate(notes):
            c.drawString(80, 90 - i * 20, n)
        c.showPage()

    def slide(self, title, kicker=None):
        c = self.c; self.page += 1
        c.setFillColor(PAPER); c.rect(0, 0, W, H, fill=1, stroke=0)
        c.setFillColor(CYAN); c.rect(0, H - 6, W, 6, fill=1, stroke=0)
        if kicker:
            c.setFont(JP, 10); c.setFillColor(CYAN); c.drawString(M, H - 38, kicker)
        c.setFont(JP, 24); c.setFillColor(INK); c.drawString(M, H - 70, title)
        c.setStrokeColor(LINE); c.setLineWidth(1); c.line(M, H - 86, W - M, H - 86)
        c.setFont(JP, 9); c.setFillColor(INK3)
        c.drawString(M, 20, self.footer)
        c.drawRightString(W - M, 20, f"{self.page} / {self.total}")
        return H - 104

    def end(self):
        self.c.showPage()

    def box(self, x, ytop, w, h, fill=BG, stroke=None, accent=None):
        c = self.c; c.setFillColor(fill)
        if stroke: c.setStrokeColor(stroke); c.setLineWidth(1)
        c.rect(x, ytop - h, w, h, fill=1, stroke=1 if stroke else 0)
        if accent: c.setFillColor(accent); c.rect(x, ytop - h, 5, h, fill=1, stroke=0)

    def card(self, x, ytop, w, h, head, body, accent=CYAN, fill=BG, head_size=15, body_size=12):
        self.box(x, ytop, w, h, fill=fill, accent=accent)
        hh = self.para(head, x + 18, ytop - 14, w - 32, st(head_size, INK))
        self.para(body, x + 18, ytop - 22 - hh, w - 32, st(body_size, INK2))

    def table(self, data, x, ytop, widths, size=11, head_fill=INK, zebra=True, styles=()):
        rows = [[Paragraph(str(v), st(size, PAPER if ri == 0 else INK, size * 1.45)) for v in r]
                for ri, r in enumerate(data)]
        t = Table(rows, colWidths=widths)
        ts = [("BACKGROUND", (0, 0), (-1, 0), head_fill), ("GRID", (0, 0), (-1, -1), 0.6, LINE),
              ("VALIGN", (0, 0), (-1, -1), "TOP"),
              ("TOPPADDING", (0, 0), (-1, -1), 5), ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
              ("LEFTPADDING", (0, 0), (-1, -1), 7), ("RIGHTPADDING", (0, 0), (-1, -1), 7)]
        if zebra:
            ts += [("BACKGROUND", (0, i), (-1, i), BG) for i in range(2, len(data), 2)]
        ts.extend(styles); t.setStyle(TableStyle(ts))
        _, h = t.wrap(sum(widths), 1000); t.drawOn(self.c, x, ytop - h); return h

    def arrow(self, x1, y1, x2, y2, color=INK3):
        c = self.c; c.setStrokeColor(color); c.setFillColor(color); c.setLineWidth(1.4)
        c.line(x1, y1, x2, y2); a = math.atan2(y2 - y1, x2 - x1); L = 8
        p = c.beginPath(); p.moveTo(x2, y2)
        p.lineTo(x2 - L * math.cos(a - 0.4), y2 - L * math.sin(a - 0.4))
        p.lineTo(x2 - L * math.cos(a + 0.4), y2 - L * math.sin(a + 0.4))
        p.close(); c.drawPath(p, fill=1, stroke=0)

    def save(self):
        self.c.save()
