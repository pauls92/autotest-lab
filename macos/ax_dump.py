#!/usr/bin/env python3
"""macOS アクセシビリティツリーの棚卸しツール。

指定したアプリのUI要素を AXUIElement API で走査し、
各要素の Role / Title / Identifier / Value / 位置を一覧化する。
最後に「操作可能な要素のうち Identifier が付いているものの割合」を出す。
（方針メモ 第9章「コードを触らずに済む範囲を確定する」の実装）

使い方:
  python ax_dump.py "TextEdit"            # アプリ名（ローカライズ名でも可）
  python ax_dump.py com.apple.TextEdit    # バンドルID
  python ax_dump.py "TextEdit" --json out.json
"""
import argparse
import json
import sys

import AppKit
from ApplicationServices import (
    AXIsProcessTrusted,
    AXUIElementCopyAttributeValue,
    AXUIElementCreateApplication,
    kAXChildrenAttribute,
    kAXDescriptionAttribute,
    kAXEnabledAttribute,
    kAXIdentifierAttribute,
    kAXPositionAttribute,
    kAXRoleAttribute,
    kAXSizeAttribute,
    kAXSubroleAttribute,
    kAXTitleAttribute,
    kAXValueAttribute,
)

# 「操作対象」とみなすロール（テストで触る可能性が高いもの）
INTERACTIVE_ROLES = {
    "AXButton", "AXPopUpButton", "AXMenuButton", "AXCheckBox", "AXRadioButton",
    "AXTextField", "AXTextArea", "AXSecureTextField", "AXComboBox", "AXSlider",
    "AXIncrementor", "AXLink", "AXMenuItem", "AXTab", "AXRow", "AXCell",
    "AXDisclosureTriangle", "AXColorWell", "AXToolbar",
}


def attr(el, name):
    err, val = AXUIElementCopyAttributeValue(el, name, None)
    return val if err == 0 else None


def point(v):
    """AXValue(CGPoint/CGSize) を (x, y) タプルに。取れなければ None。"""
    if v is None:
        return None
    try:
        from ApplicationServices import AXValueGetValue, kAXValueCGPointType, kAXValueCGSizeType
        import Quartz
        for t, ctor in ((kAXValueCGPointType, Quartz.CGPoint), (kAXValueCGSizeType, Quartz.CGSize)):
            ok, out = AXValueGetValue(v, t, None)
            if ok and out is not None:
                return (round(out.x if hasattr(out, "x") else out.width, 1),
                        round(out.y if hasattr(out, "y") else out.height, 1))
    except Exception:
        pass
    return None


def find_app(name_or_bundle):
    ws = AppKit.NSWorkspace.sharedWorkspace()
    for app in ws.runningApplications():
        if app.bundleIdentifier() == name_or_bundle or app.localizedName() == name_or_bundle:
            return app
    return None


def walk(el, depth, out, max_depth):
    role = attr(el, kAXRoleAttribute)
    if role is None:
        return
    node = {
        "depth": depth,
        "role": role,
        "subrole": attr(el, kAXSubroleAttribute),
        "title": attr(el, kAXTitleAttribute),
        "identifier": attr(el, kAXIdentifierAttribute),
        "description": attr(el, kAXDescriptionAttribute),
        "value": _short(attr(el, kAXValueAttribute)),
        "enabled": attr(el, kAXEnabledAttribute),
        "position": point(attr(el, kAXPositionAttribute)),
        "size": point(attr(el, kAXSizeAttribute)),
    }
    out.append(node)
    if depth >= max_depth:
        return
    children = attr(el, kAXChildrenAttribute) or []
    for c in children:
        walk(c, depth + 1, out, max_depth)


def _short(v, n=40):
    if v is None or isinstance(v, (int, float, bool)):
        return v
    s = str(v).replace("\n", "⏎")
    return s if len(s) <= n else s[:n] + "…"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("app", help="アプリ名またはバンドルID")
    ap.add_argument("--max-depth", type=int, default=25)
    ap.add_argument("--json", help="結果をJSONで保存するパス")
    ap.add_argument("--all", action="store_true", help="操作可能な要素以外も表示する")
    args = ap.parse_args()

    if not AXIsProcessTrusted():
        print("このプロセスにアクセシビリティ権限がありません。\n"
              "システム設定 → プライバシーとセキュリティ → アクセシビリティ で、\n"
              "実行元（ターミナル / Claude など）を許可してから再実行してください。", file=sys.stderr)
        sys.exit(2)

    app = find_app(args.app)
    if app is None:
        print(f"起動中のアプリに '{args.app}' が見つかりません。先に起動してください。", file=sys.stderr)
        sys.exit(1)

    root = AXUIElementCreateApplication(app.processIdentifier())
    nodes = []
    walk(root, 0, nodes, args.max_depth)

    # 区切り線（タイトルも子もないメニュー項目）とスクロールバーの矢印は操作対象から外す
    def is_target(n):
        if n["role"] not in INTERACTIVE_ROLES:
            return False
        if n["role"] == "AXMenuItem" and not n["title"]:
            return False
        if (n["subrole"] or "").endswith(("Arrow", "Page")):
            return False
        return True

    # 行・セルはラベルが子の AXStaticText の value に入るので、そこから拾う
    def inherited_label(i):
        n = nodes[i]
        if n["title"] or n["description"]:
            return n["title"] or n["description"]
        for m in nodes[i + 1:]:
            if m["depth"] <= n["depth"]:
                break
            if m["role"] == "AXStaticText" and m["value"]:
                return str(m["value"])
        return ""

    def id_kind(ident):
        if not ident:
            return "なし"
        if ident.startswith("_NS:"):
            return "自動"
        return "明示"

    # 一覧表示
    for i, n in enumerate(nodes):
        if not args.all and not is_target(n):
            continue
        label = inherited_label(i)
        ident = n["identifier"] or "-"
        print(f'{"  " * n["depth"]}{n["role"]:<18} id={ident:<30} "{label}"'
              + (f'  value={n["value"]}' if n["value"] not in (None, "") else ""))

    # 集計
    targets = [(i, n) for i, n in enumerate(nodes) if is_target(n)]
    explicit = [n for _, n in targets if id_kind(n["identifier"]) == "明示"]
    auto = [n for _, n in targets if id_kind(n["identifier"]) == "自動"]
    label_only = [n for i, n in targets if not n["identifier"] and inherited_label(i)]
    nothing = [(i, n) for i, n in targets if not n["identifier"] and not inherited_label(i)]
    print("\n=== 棚卸し結果 ===")
    print(f"全要素: {len(nodes)}  操作対象: {len(targets)}")
    if targets:
        t = len(targets)
        print(f"  明示的なID あり : {len(explicit):4d} ({100*len(explicit)/t:.0f}%)  ← そのまま使える")
        print(f"  自動生成ID(_NS:): {len(auto):4d} ({100*len(auto)/t:.0f}%)  ← ビルドで変わりうる。ラベル併用が無難")
        print(f"  ラベルのみ      : {len(label_only):4d} ({100*len(label_only)/t:.0f}%)  ← テキストで探せる。言語切替に注意")
        print(f"  手がかりなし    : {len(nothing):4d} ({100*len(nothing)/t:.0f}%)  ← ID付与を依頼する候補")
        for i, n in nothing[:20]:
            print(f'      depth={n["depth"]} {n["role"]} sub={n["subrole"]} pos={n["position"]}')

    if args.json:
        with open(args.json, "w", encoding="utf-8") as f:
            json.dump(nodes, f, ensure_ascii=False, indent=1, default=str)
        print(f"\nJSON: {args.json}")


if __name__ == "__main__":
    main()
