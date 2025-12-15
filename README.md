# Security Audit Prototype（Node.js）

複数の Node.js リポジトリを横断して依存関係の脆弱性をチェックし、
**重大度 high / critical のみを Slack に通知する**ための GitHub Actions ベースの仕組みです。

本リポジトリは PoC（個人検証用）として作成されています。

---

## 何をする仕組みか

- 複数リポジトリを巡回して依存関係を監査
- lockfile を見て npm / pnpm / yarn を自動判別
- audit を実行し、結果を JSON として保存
- high / critical の脆弱性のみ抽出
- Slack に結果を通知
- 問題がない場合も「今週は問題なし」と通知

---

## 全体の流れ

1. `repos.txt` に記載されたリポジトリを順番に処理
2. 対象リポジトリを clone
3. lockfile を判定して audit を実行
4. audit 結果を JSON として保存
5. JSON を解析して Slack 用メッセージを生成
6. まとめて Slack に通知

---

## ディレクトリ構成

```
.
├─ repos.txt                # 監査対象リポジトリ一覧
├─ scripts/
│  ├─ audit_repo.sh         # install + audit 実行
│  └─ parse_audit.py        # audit JSON を解析
└─ .github/
   └─ workflows/
      └─ weekly.yml         # GitHub Actions 定義
```

---

## 監査対象リポジトリの指定

`repos.txt` に `owner/repo` 形式で 1 行ずつ記載します。

例:

```
github-user-name/my-app
```

---

## GitHub Actions の実行方法

- 手動実行  
  Actions タブ → `weekly-security-audit` → Run workflow

- 定期実行  
  毎週月曜 09:00（JST）に自動実行されます

---

## 必要な GitHub Secrets

| Name | 説明 |
|---|---|
| `AUDIT_TOKEN` | 監査対象リポジトリを clone するための GitHub トークン |
| `SLACK_WEBHOOK_URL` | Slack Incoming Webhook URL |

---

## Slack 通知内容

- 🚨 脆弱性あり  
  - リポジトリ名  
  - パッケージ名  
  - 深刻度（high / critical）  
  - 修正候補がある場合はその内容  

- ✅ 脆弱性なし  
  - 「今週は問題ありません」と通知  

- ⚠️ 監査失敗  
  - lockfile が無い  
  - install / audit が失敗した場合  

---

## 注意点

- audit の結果は理論上の脆弱性を含みます  
  実際の影響有無は各プロジェクトで判断してください
- audit が失敗しても CI は止めません（可視化優先）
- monorepo や複数 package.json 構成は現状未対応です

---

## このリポジトリの位置づけ

- 個人検証用の PoC
- 社内提案・本番設計に向けた叩き台
