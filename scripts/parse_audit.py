import json, sys, os

repo = os.environ.get("REPO", "unknown")
path = sys.argv[1]

try:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
except Exception:
    # JSONとして読めない場合（yarnの出力形式など）
    print(f"⚠️ {repo}: 監査結果（audit.json）がJSONとして読み取れませんでした（形式が異なる可能性があります）。Actionsのログを確認してください。")
    sys.exit(0)

vulns = data.get("vulnerabilities", {})
found = False

# npm/pnpmの新形式に対応（vulnerabilities辞書）
for pkg, info in vulns.items():
    sev = info.get("severity")
    if sev in ("high", "critical"):
        found = True
        installed = info.get("installed") or info.get("version") or "不明"
        fix = info.get("fixAvailable")

        fix_str = ""
        if isinstance(fix, dict):
            fix_str = f" / 修正候補: {fix.get('name','')}@{fix.get('version','不明')}"
        elif fix is True:
            fix_str = " / 修正候補: あり"
        elif fix is False:
            fix_str = " / 修正候補: なし"

        sev_jp = "重大(high)" if sev == "high" else "致命的(critical)"
        print(f"🚨 {repo}: {pkg}@{installed}（深刻度: {sev_jp}）{fix_str}")

if not found:
    # 「今週は問題なし」を必ず出す
    print(f"✅ {repo}: 今週は重大な脆弱性（high/critical）は見つかりませんでした。")
