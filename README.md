# Discord Role Assignment Bot

1つのファイルでシンプルにロール付与するFlaskアプリ

## 概要

ユーザーがWebページのリンクをクリックすると、Discord OAuth認証を通してサーバーに自動参加し、指定されたロールが付与されるシステムです。

## セットアップ

### 1. Discord Developer Portal 設定

#### アプリケーション作成
1. [Discord Developer Portal](https://discord.com/developers/applications) にアクセス
2. 「New Application」をクリック
3. アプリケーション名を入力（例：Role Assignment Bot）
4. 「General Information」タブで以下をメモ：
   - **Application ID**（Client IDとして使用）

#### Bot作成
1. 左メニューの「Bot」をクリック
2. 「Reset Token」をクリック（初回は「Token」欄が表示される）
3. 「Copy」ボタンをクリックしてトークンをメモ（**DISCORD_TOKEN**として使用）
4. 「Privileged Gateway Intents」で以下を有効化：
   - Server Members Intent
   - Message Content Intent

#### OAuth2設定（後で設定）
1. 左メニューの「OAuth2」→「General」
2. 「Client Secret」を生成してメモ（**DISCORD_CLIENT_SECRET**として使用）
3. Redirect URIsは後で設定（Railway URL取得後）

### 2. Railway デプロイ

#### 初回デプロイ
1. [Railway](https://railway.app) にログイン
2. 「New Project」→「Deploy from GitHub repo」
3. このリポジトリ（`discord-role-bot`）を選択
4. 自動デプロイが開始される
5. 生成されたURL（例：`https://web-production-abcd.up.railway.app`）をメモ

#### 環境変数設定
Railway管理画面で「Variables」タブを開き、以下を設定：

```bash
DISCORD_TOKEN=Bot_から始まるトークン
DISCORD_CLIENT_ID=アプリケーションのClient ID
DISCORD_CLIENT_SECRET=OAuth2のClient Secret
REDIRECT_URI=https://web-production-abcd.up.railway.app/callback
GUILD_ID=サーバーID（数字）
ROLE_ID=付与するロールID（数字）
```

### 3. Discord OAuth2 設定（Railway URL確定後）

1. Discord Developer Portal → あなたのアプリ → OAuth2 → General
2. 「Redirects」セクションで「Add Redirect」をクリック
3. `https://web-production-abcd.up.railway.app/callback` を追加
4. 「Save Changes」をクリック

### 4. サーバー設定

#### Bot権限設定
1. Discord Developer Portal → あなたのアプリ → OAuth2 → URL Generator
2. 「Scopes」で以下を選択：
   - `bot`
   - `applications.commands`
3. 「Bot Permissions」で以下を選択：
   - `Manage Roles`
   - `View Channels`
4. 生成されたURLでBotをサーバーに招待

#### ロール階層確認
1. Discordサーバー → サーバー設定 → ロール
2. Botのロールが付与したいロールより**上位**にあることを確認
3. 付与したいロールを右クリック → 「IDをコピー」（**ROLE_ID**として使用）

**ロールIDとサーバーIDの取得方法:**
- Discord設定 → 詳細設定 → 開発者モードを有効化
- **サーバーID**: サーバー名を右クリック → 「サーバーIDをコピー」
- **ロールID**: ロールを右クリック → 「IDをコピー」

### 5. 再デプロイ

環境変数設定完了後、Railwayで「Deploy」をクリックして再デプロイ

## 使用方法

### エンドユーザー向け手順

1. **Webページにアクセス**
   - RailwayのURL（例：`https://web-production-abcd.up.railway.app`）にアクセス
   - 「Get Role」ボタンが表示される

2. **OAuth認証**
   - 「Get Role」ボタンをクリック
   - Discord認証画面に自動リダイレクト
   - 「認証」ボタンをクリック

3. **自動処理**
   - サーバーへの自動参加
   - 指定されたロールの自動付与
   - 完了メッセージが表示される

### 管理者向け確認事項

- ユーザーがサーバーに参加したか確認
- 正しいロールが付与されたか確認
- エラーが発生した場合はRailwayのログを確認

## トラブルシューティング

### よくある問題

1. **「Authorization failed」**
   - Discord Developer Portal の Redirect URI設定を確認
   - Railway URLが正しく設定されているか確認

2. **「Token exchange failed」**
   - DISCORD_CLIENT_ID と DISCORD_CLIENT_SECRET を確認
   - Discord Developer Portal の設定を再確認

3. **「Failed to join server」**
   - Botがサーバーに招待されているか確認
   - Bot権限で「Manage Roles」が有効か確認

4. **ロールが付与されない**
   - Botのロールが付与対象ロールより上位にあるか確認
   - ROLE_IDが正しいか確認

### ログ確認方法

Railway管理画面 → プロジェクト → Deployments → View Logs でエラー詳細を確認できます。

## セキュリティ注意事項

- DISCORD_TOKENは絶対に公開しない
- 環境変数は Railway の Variables で安全に管理される
- .env ファイルは .gitignore で除外済み

## ファイル構成

```
discord-role-bot/
├── app.py              # メインアプリケーション
├── requirements.txt    # Python依存関係
├── Procfile           # Railway設定
├── .env.example       # 環境変数例
├── .gitignore         # Git除外設定
└── README.md          # このファイル
```