# Discord Role Assignment Bot

1つのファイルでシンプルにロール付与するFlaskアプリ

## セットアップ

### 1. Discord設定（初回）

1. [Discord Developer Portal](https://discord.com/developers/applications) でアプリ作成
2. Bot作成してトークン取得
3. Client ID と Client Secret をメモ

### 2. Railway 初回デプロイ

1. このプロジェクトをRailwayにデプロイ
2. 生成されたURL（例：`https://web-production-abcd.up.railway.app`）をメモ

### 3. Discord OAuth2設定（デプロイ後）

1. Discord Developer Portal に戻る
2. OAuth2設定：
   - Redirect URI: `https://生成されたURL/callback`
   - Scopes: `bot`, `identify`
   - Permissions: `Manage Roles`

### 4. 環境変数設定

Railwayで以下を設定：
```
DISCORD_TOKEN=ボットトークン
DISCORD_CLIENT_ID=クライアントID  
DISCORD_CLIENT_SECRET=クライアントシークレット
GUILD_ID=サーバーID
ROLE_ID=付与するロールID
REDIRECT_URI=https://生成されたURL/callback
```

**ロールIDの取得方法:**
1. Discord → サーバー設定 → ロール
2. 該当ロールを右クリック → "IDをコピー"（開発者モード要有効）

### 5. 再デプロイ

環境変数設定後、Railwayで再デプロイ

### 4. 使用方法

リンクをクリック → OAuth認証 → 自動でロール付与