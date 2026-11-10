"""テストケース（意図と期待値）を人が承認する。承認した版のハッシュを approvals.json に記録する。
使い方: ./.venv/bin/python regen/approve.py regen/testcases/TE-PRINT-001.json あなたの名前
"""
import datetime, hashlib, json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
path, who = sys.argv[1], sys.argv[2]
ap = os.path.join(HERE, "approvals.json")
approvals = json.load(open(ap, encoding="utf-8")) if os.path.exists(ap) else {}
approvals[os.path.basename(path)] = {"sha256": hashlib.sha256(open(path, "rb").read()).hexdigest(),
                                     "approved_by": who, "at": datetime.datetime.now().isoformat(timespec="seconds")}
json.dump(approvals, open(ap, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("承認しました:", os.path.basename(path))
