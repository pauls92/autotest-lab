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
TOTAL = 11
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

# 7. 操作対象の決め方
y = d.slide("操作対象の決め方：「IDマッチング」は手段の1つ", "深掘り：ロケータ")
d.box(M, y - 4, CW, 58, fill=GRN_S, accent=GRN)
d.para("<b>SeleniumやPlaywrightは「IDマッチング」？</b>　→ 正確には<b>「部品の木の属性で探す」</b>方式。IDはその属性の1つで、"
       "IDが無くても役割・表示名・テキスト・構造で探せる。Playwrightは「役割＋表示名」とテスト用IDを推奨している。",
       M + 18, y - 14, CW - 34, st(12, INK))
hdr3 = ["決め方", "例", "安定度", "注意"]
wid3 = [170, 330, 70, 294]
rows = [hdr3,
        ["テスト用のID", "Web: data-testid ／ Android: resource-id ／ iOS: accessibilityIdentifier ／ Windows: AutomationId",
         "◎", "開発者が付ける必要がある。画面に出ないので翻訳やデザイン変更に強い"],
        ["役割＋表示名", "get_by_role(\"button\", name=\"ログイン\")",
         "◎〜○", "利用者に見えるとおりに指定。アクセシビリティの質に依存"],
        ["表示テキスト", "「ログイン」と書かれた部品", "○", "言語の切り替えや文言変更で壊れる"],
        ["構造（木の中の位置）", "CSSセレクタ、XPath、「3番目のボタン」", "△", "レイアウト変更で壊れる。自動生成のidやclassも不安定"],
        ["画像マッチ＋相対座標", "正解画像を探し、その中の決まった点をクリック", "△", "木が無いアプリでも使える。解像度・テーマ・文言で壊れる"],
        ["画面の座標だけ", "(320, 480) をクリック", "×", "画面サイズが変わると即壊れる"],
        ]
d.table(rows, M, y - 74, wid3, size=9.5)
d.end()

# 8. OS別の部品の木とID
y = d.slide("OS別：部品の木と、IDの呼び名", "深掘り：ロケータ")
hdr4 = ["対象", "部品の木（取り出す仕組み）", "開発者が付けるID", "IDが無いときの代替", "木が取れない例"]
wid4 = [110, 190, 170, 200, 194]
rows = [hdr4,
        ["Web", "DOM（必ずある）", "id、data-testid", "役割＋表示名、テキスト、CSS・XPath",
         "canvasで描く画面（ゲーム・一部のグラフ）"],
        ["Android", "アクセシビリティ（UI Automator）", "resource-id", "content-desc（読み上げ用ラベル）、text、class",
         "ゲームエンジン、独自描画"],
        ["iOS", "アクセシビリティ（XCTest）", "accessibilityIdentifier", "accessibilityLabel、部品の種類",
         "ゲームエンジン、独自描画"],
        ["Windows", "UI Automation（UIA）", "AutomationId", "Name、ControlType、ClassName",
         "独自描画、UIA対応が弱い古いUI部品"],
        ["macOS", "アクセシビリティ（AX API）", "AXIdentifier", "AXRole＋AXTitle／AXDescription",
         "独自描画。AXIdentifierが無いアプリは多い"],
        ["Flutter・React Native など", "各フレームワークがOSの木に変換", "Semantics、testID など",
         "表示名", "変換の出来しだい"],
        ]
h = d.table(rows, M, y, wid4, size=9.5)
d.para("ポイント：標準の部品を使っていれば、IDが無くても「木」はある。困るのは、木そのものが無い（独自描画の）画面。",
       M, y - h - 12, CW, st(11.5, INK2))
d.end()

# 9. Webは簡単、ネイティブはIDが要る？
y = d.slide("「Webは簡単、ネイティブはIDが要る」は合っている？", "深掘り：理解の確認")
d.box(M, y - 4, CW, 50, fill=GRN_S, accent=GRN)
d.para("<b>おおむね合っている。</b>ただし「IDが無いと動かない」のではなく「IDが無いと壊れやすい」。本当に動かないのは木が無いとき。",
       M + 18, y - 18, CW - 34, st(13, INK))
bw = (CW - 20) / 2
d.card(M, y - 70, bw, 130, "Webが扱いやすい理由",
       "DOMが必ずあり、IDが無くてもCSS・テキスト・役割で特定できる。<br/>"
       "ブラウザの開発ツールで、誰でも木をすぐ確認できる。",
       accent=CYAN, fill=CYAN_S, body_size=11.5)
d.card(M + bw + 20, y - 70, bw, 130, "ただしWebにも落とし穴",
       "フレームワークがビルドのたびに変えるidやclassは不安定。<br/>"
       "canvas描画、iframe、Shadow DOM は工夫が要る。→ data-testid や役割で指定する。",
       accent=YEL, fill=YEL_S, body_size=11.5)
d.card(M, y - 216, bw, 130, "ネイティブで起きること",
       "IDが無いと、表示名や木の中の位置に頼る。多言語化やレイアウト変更で壊れやすい。<br/>"
       "ゲームなど独自描画の画面には木が無いので、画像に頼るしかない。",
       accent=MAG, fill=MAG_S, body_size=11.5)
d.card(M + bw + 20, y - 216, bw, 130, "打ち手",
       "開発チームにテスト用IDを付けてもらう。読み上げ対応（アクセシビリティ）の改善と同じ作業なので、"
       "品質向上として頼みやすい。<br/>付けられない画面だけ画像マッチを使う。",
       accent=GRN, fill=GRN_S, body_size=11.5)
d.end()

# 10. AIが画面構成をつかむ方法
y = d.slide("AIが画面の構成をつかむ方法", "深掘り：AIとスクリプト作成")
hdr5 = ["方法", "AIに渡すもの", "向き・不向き", "例"]
wid5 = [170, 210, 270, 214]
rows = [hdr5,
        ["部品の木をテキストで", "DOMやアクセシビリティのスナップショット",
         "正確で安い。IDや役割をそのままスクリプトに使える。木が無いと使えない",
         "Playwright MCP、Appiumのpage source、ax_dump.py"],
        ["スクリーンショットを見る", "画面の画像", "どの画面でも使える。座標がずれやすく、遅く、費用が高い",
         "computer use"],
        ["両方を重ねる", "画像に部品の番号を重ねたもの（Set-of-Mark）", "木の正確さと、見た目の理解を両立",
         "多くのAIエージェントが採用"],
        ["画像から部品を取り出す", "画像を解析した部品の一覧（文字認識・物体検出）", "木が無いアプリ向け。精度は画面しだい",
         "OmniParser など"],
        ["事前に探索して地図を作る", "画面ごとの棚卸し＋画面遷移図", "スクリプト作成の材料になる。画面の変更検知にも使える",
         "ax_crawl.py、アプリのクローラー"],
        ]
h = d.table(rows, M, y, wid5, size=9.5)
steps = ["探索して地図を作る", "テストの意図を渡す", "AIがスクリプトを書く", "実行する", "失敗時は木を取り直す"]
sw = (CW - 4 * 22) / 5; sy = y - h - 22
for i, s in enumerate(steps):
    x = M + i * (sw + 22)
    d.box(x, sy, sw, 40, fill=CYAN_S)
    d.para(s, x + 6, sy - 12, sw - 12, st(10.5, INK, align=1))
    if i < 4:
        d.arrow(x + sw + 3, sy - 20, x + sw + 19, sy - 20)
d.end()

# 11. 論点
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
