"""2回の実行の操作の記録を比べ、「ユーザーから見て同じテストをしたか」を判定する。

比べるもの（違ってはいけない）：画面の順番、操作の種類、対象（意味の名前）、入力した値、確認の項目と期待値、確認の数、結果
比べないもの（違ってよい）：部品の探し方（used）、スクリーンショット、時刻、スクリプトの中身
使い方: ./.venv/bin/python regen/compare.py ja-1 en-2
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
KEYS = ("no", "screen", "action", "target", "value", "expect", "result")


def load(label):
    return json.load(open(os.path.join(HERE, "runs", label, "log.json"), encoding="utf-8"))


def main():
    a, b = load(sys.argv[1]), load(sys.argv[2])
    print(f"前回: {sys.argv[1]}  ({a['lang']}, スクリプト {a['script']}, 結果 {a['result']})")
    print(f"今回: {sys.argv[2]}  ({b['lang']}, スクリプト {b['script']}, 結果 {b['result']})")
    problems = []
    if a["testcase_sha256"] != b["testcase_sha256"]:
        problems.append("テストケース（期待値）が違う")
    if b["result"] != "PASS":
        problems.append("今回の実行が合格していない")
    sa, sb = a["steps"], b["steps"]
    if len(sa) != len(sb):
        problems.append(f"手順の数が違う（前回 {len(sa)}、今回 {len(sb)}）")
    ca = sum(1 for s in sa if s["action"] == "確認"); cb = sum(1 for s in sb if s["action"] == "確認")
    if ca != cb:
        problems.append(f"確認の数が違う（前回 {ca}、今回 {cb}）")
    for x, y in zip(sa, sb):
        diff = [k for k in KEYS if x.get(k) != y.get(k)]
        if diff:
            problems.append(f"手順{x.get('no')}: " + "、".join(f"{k} が「{x.get(k)}」→「{y.get(k)}」" for k in diff))
    same_script = a["script_sha256"] == b["script_sha256"]
    loc_changes = [f"{x['target']}: {x.get('used')} → {y.get('used')}" for x, y in zip(sa, sb) if x.get("used") != y.get("used")]
    print(f"\nスクリプト: {'同じ' if same_script else '違う（作り直された）'}")
    if loc_changes:
        print("部品の探し方の違い（違ってよい）:")
        for l in loc_changes:
            print("  -", l)
    if problems:
        print("\n判定: 同じテストとは言えない（人に確認してもらう）")
        for p in problems:
            print("  ×", p)
        sys.exit(1)
    print("\n判定: 同じテストをした（ユーザーから見た操作と確認が一致）")


if __name__ == "__main__":
    main()
