"""GUI自動操作の技術の一般的な比較（スライドPDF）。

実行: python build.py  → 同じフォルダに gui_automation_landscape.pdf を出力
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools"))
from slidekit import (Deck, st, W, M, INK, INK2, INK3, CYAN, CYAN_S, MAG, MAG_S,  # noqa: E402
                      GRN, GRN_S, YEL, YEL_S, BG, PAPER, LINE)

OUT = os.path.join(HERE, "gui_automation_landscape.pdf")
FOOT = "autotest-lab ・ GUI自動操作の技術 一般論のまとめ（2026-11）"
TOTAL = 7
CW = W - 2 * M  # 864

d = Deck(OUT, "GUI自動操作の技術 比較", FOOT, TOTAL)

# 1. 表紙
d.cover("autotest-lab ・ 一般論",
        "GUI自動操作の技術",
        "Web・iOS・Android・Mac・Windows を一望する",
        "主要なライブラリとツールを、対象OS・書く言語・画面の掴み方・AIエージェントとの相性で比べる。",
        ["公開情報にもとづく一般論。各ツールの最新状況は公式ドキュメントで確認すること。"])

# 2. 全体像：画面の掴み方は3通り
y = d.slide("画面の「掴み方」は3通り", "全体像")
cw = (CW - 2 * 20) / 3
cards = [
    ("A. アプリの内側から",
     "テストがアプリと同じプロセスで動き、部品を直接たどる。<br/>"
     "例：Espresso、Flutter integration_test<br/><br/>"
     "<b>強み</b> 速い・待ちが安定<br/><b>弱み</b> アプリの外（通知・設定・他アプリ）は触れない", GRN, GRN_S),
    ("B. 部品の木（DOM・アクセシビリティ）",
     "OSやブラウザが公開する部品の木から、IDや名前で探して操作する。<br/>"
     "例：Selenium、Playwright、Appium、UI Automator、XCUITest、pywinauto、macOSのAX API<br/><br/>"
     "<b>強み</b> 主流。テキストで扱えるのでAIとも相性がよい<br/><b>弱み</b> IDの付け方で安定度が決まる", CYAN, CYAN_S),
    ("C. 画像と座標",
     "スクリーンショットを見て、画像認識や座標でクリックする。<br/>"
     "例：PyAutoGUI、SikuliX、AIのcomputer use<br/><br/>"
     "<b>強み</b> どのOS・どのアプリでも動く<br/><b>弱み</b> 遅い。解像度やテーマの違いで壊れやすい", MAG, MAG_S),
]
for i, (h, b, a, f) in enumerate(cards):
    d.card(M + i * (cw + 20), y - 4, cw, 240, h, b, accent=a, fill=f, head_size=15, body_size=11.5)
d.para("<b>「1つのスクリプトで複数OS」を狙う方法</b>：Appium（OSごとのドライバを差し替え）、Maestro（YAMLのフロー）、"
       "Robot Framework（キーワードの層でライブラリを包む）、画像ベース。ただし部品の名前やIDはOSごとに違うため、"
       "共通化できるのは「手順」までで、「部品の指定」はOS別になりやすい。",
       M, y - 264, CW, st(12, INK2))
d.end()

# 3. Web とモバイル
y = d.slide("比較表 1：Web とモバイル", "主要ツール")
hdr = ["ツール", "対象", "書く言語", "仕組み", "特徴・注意"]
wid = [96, 150, 150, 210, 258]
rows = [hdr,
        ["Selenium", "Web（主要ブラウザ）", "Java, Python, C#, JS, Ruby",
         "W3C標準のWebDriver。各ブラウザのドライバ経由。WebDriver BiDiへ移行中",
         "最も歴史が長く情報が多い。待ち処理は自分で書く場面が多い"],
        ["Playwright", "Web（Chromium・Firefox・WebKit）", "TS/JS, Python, Java, .NET",
         "ブラウザを直接制御するライブラリ＋テストランナー（Microsoft）",
         "自動待機、録画からのコード生成、トレース。ネイティブアプリは対象外"],
        ["Cypress", "Web（主にChromium系・Firefox）", "JS/TS",
         "ブラウザの中でテストを実行", "開発者体験が良い。複数タブなどに制約"],
        ["Espresso", "Android（自アプリ内）", "Kotlin, Java",
         "アプリと同じプロセスで動く（掴み方A）", "速く安定。アプリの外は操作できない"],
        ["UI Automator", "Android（端末全体）", "Kotlin, Java",
         "アクセシビリティ情報（掴み方B）", "通知・設定・他アプリも操作できる"],
        ["XCUITest", "iOS（macOSも）", "Swift, Objective-C",
         "Appleの XCTest。アクセシビリティ情報", "Xcodeが必要＝Macが必要"],
        ["Appium", "iOS・Android・Mac・Windows ほか", "Java, Python, JS, C#, Ruby",
         "WebDriverの口＋OSごとのドライバ（UiAutomator2、XCUITest、Mac2、Windows）",
         "1つのAPIで複数OS。下で動くのは各OSの公式の仕組み"],
        ["Maestro", "iOS・Android・Web", "YAML",
         "宣言的なフローを書く", "書くのが簡単。複雑な分岐や計算は苦手"],
        ]
d.table(rows, M, y, wid, size=9.5)
d.end()

# 4. デスクトップと横断
y = d.slide("比較表 2：デスクトップと、OSを横断するもの", "主要ツール")
rows = [hdr,
        ["pywinauto", "Windows", "Python",
         "UI Automation（UIA）または Win32 API", "手軽。UIAは遅い部品や取りにくい部品がある"],
        ["FlaUI", "Windows", "C#（.NET）", "UIA", ".NETでの定番"],
        ["WinAppDriver", "Windows", "WebDriver対応の各言語",
         "UIAをWebDriverの口で公開（Microsoft）", "本家の開発は停滞気味。Appium経由で使われることが多い"],
        ["macOS AX API", "macOS", "Python（pyobjc）, Swift",
         "AXUIElement（アクセシビリティ）", "このリポジトリの macos/ の実験。権限の許可が必要"],
        ["Appium Mac2", "macOS", "Appiumの各言語", "XCTestを使うドライバ", "Xcodeが必要"],
        ["AppleScript / JXA", "macOS", "AppleScript, JavaScript",
         "System Events 経由でアクセシビリティ", "手軽だが遅く、壊れやすい"],
        ["Robot Framework", "ライブラリしだい", "キーワード（表形式）＋Python",
         "Selenium・Playwright・Appium などを包む層", "読みやすい。中身は包んだライブラリに依存"],
        ["PyAutoGUI / SikuliX", "Windows・Mac・Linux", "Python, Java",
         "座標・画像認識（掴み方C）", "どこでも動くが壊れやすい"],
        ["ノーコード／RPA", "製品しだい", "録画・ブロック",
         "内部は上のいずれかの仕組み", "書き手を選ばない。中身が独自形式だとAIや外部ツールと連携しにくい"],
        ]
d.table(rows, M, y, wid, size=9.5)
d.end()

# 5. AIエージェントとの相性
y = d.slide("AIエージェントとの相性", "AI")
hdr2 = ["ツール・方式", "AIがスクリプトを書く", "AIが直接操作する", "ポイント"]
wid2 = [150, 200, 230, 284]
rows = [hdr2,
        ["Playwright", "◎ 情報が多く、生成精度が高い", "◎ 公式のPlaywright MCP（部品の木をテキストで渡す）",
         "Web なら現時点でいちばん AI と相性がよい"],
        ["Selenium", "◎ 情報が最も多い", "○ コミュニティのMCPなど",
         "古い書き方が混ざりやすい点に注意"],
        ["Appium", "○ コードは書ける。部品のIDは実機の情報が必要", "○ MCPサーバーあり（公式・コミュニティ）",
         "画面の木をAIに見せる仕組みとセットで使う"],
        ["Espresso / XCUITest", "○ コードは書ける", "△ ビルドが必要で試行に時間がかかる",
         "開発者がアプリと一緒に書く用途に向く"],
        ["pywinauto / macOS AX", "○", "○ Windows向けMCPなど／AXの木をテキスト化すれば可能",
         "このリポジトリの ax_dump.py が「木のテキスト化」の例"],
        ["画像・座標", "△", "◎ computer use（画面を見てクリック）",
         "どこでも動くが遅く、費用もかかる"],
        ["非公開の独自形式", "× 学習データにない（仕様書を渡せば一部可）", "△ APIやMCPを公開すれば可",
         "AIに使わせるには、仕様を文章で渡す・口を開ける工夫が要る"],
        ]
h = d.table(rows, M, y, wid2, size=9.5)
d.para("◎ とても向いている　○ 向いている　△ 工夫が要る　× 難しい　（2026年時点の一般的な見立て）",
       M, y - h - 10, CW, st(10, INK3))
d.end()

# 6. Playwright とは
y = d.slide("Playwright とは？", "Q&A")
lw = 430
d.card(M, y - 4, lw, 96, "Pythonで書ける？　→ はい、その理解で合っています",
       "Microsoft製のブラウザ自動操作ライブラリ。TypeScript/JS、Python、Java、.NET の4言語に公式対応。",
       accent=GRN, fill=GRN_S, head_size=14, body_size=11.5)
d.card(M, y - 112, lw, 120, "ただし、言語で少し差がある",
       "テストランナー（@playwright/test、並列実行・UIモードなど）はNode.js版の機能。"
       "Python版は pytest と組み合わせる（pytest-playwright）。操作のAPIはほぼ同じ。",
       accent=YEL, fill=YEL_S, head_size=14, body_size=11.5)
d.card(M, y - 244, lw, 96, "対象はWeb（ブラウザ）だけ",
       "iOS・Android・Windows・Macのネイティブアプリは操作できない。そこはAppiumや各OSの仕組みの担当。",
       accent=MAG, fill=MAG_S, head_size=14, body_size=11.5)
cx = M + lw + 24; cwid = CW - lw - 24
d.box(cx, y - 4, cwid, 340, fill=INK)
code = [
    "# 準備",
    "pip install playwright pytest-playwright",
    "playwright install      # ブラウザを取得",
    "",
    "# 操作を録画してコードを作る",
    "playwright codegen --target python URL",
    "",
    "# test_login.py",
    "def test_login(page):",
    "    page.goto(\"https://example.com\")",
    "    page.get_by_label(\"メール\").fill(\"a@b.c\")",
    "    page.get_by_role(\"button\",",
    "                     name=\"ログイン\").click()",
    "    expect(page.get_by_text(\"ようこそ\"))\\",
    "        .to_be_visible()",
    "",
    "# 実行",
    "pytest",
]
c = d.c
for i, line in enumerate(code):
    c.setFillColor(INK3 if line.startswith("#") else PAPER)
    c.setFont("HeiseiKakuGo-W5", 11)
    c.drawString(cx + 18, y - 28 - i * 17.5, line)
d.end()

# 7. 論点
y = d.slide("壁打ちの論点：AI時代に選ばれやすい自動操作の条件", "示唆（一般論）")
pts = [
    ("1. テキストのコードで書ける", "AIが読める・直せる・差分をレビューできる。録画やブロックだけの形式は不利。"),
    ("2. 公開されていて情報が多い", "AIの生成精度は、世の中にある例の量でほぼ決まる。"),
    ("3. 画面をテキストで取り出せる", "部品の木（DOM・アクセシビリティ）をテキストで渡せると、AIが部品を正しく特定できる。"),
    ("4. AIから直接呼べる口がある", "MCPなどで「操作」と「画面の取得」をAIに開くと、探索的なテストも任せられる。"),
]
bw = (CW - 20) / 2
for i, (hd, bd) in enumerate(pts):
    r, col = divmod(i, 2)
    d.card(M + col * (bw + 20), y - 4 - r * 120, bw, 104, hd, bd, accent=CYAN, fill=CYAN_S,
           head_size=15, body_size=12)
d.box(M, y - 252, CW, 66, fill=BG, accent=INK)
d.para("<b>問い</b>：AIが「書き手」を代わるなら、ノーコードの価値は下がる。一方で、"
       "OSごとの違いを吸収する層や、安定して動かす実行基盤（端末の管理・並列実行・結果の記録）の価値は残るのでは？"
       "　──どこを自前で持ち、どこを公開の仕組みとAIに任せるか。",
       M + 20, y - 264, CW - 40, st(12.5, INK))
d.end()

d.save()
print(OUT)
