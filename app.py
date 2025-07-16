import os
import asyncio
import threading
import discord
import requests
from flask import Flask, request, redirect
from dotenv import load_dotenv

load_dotenv()

# 設定
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
DISCORD_CLIENT_ID = os.getenv('DISCORD_CLIENT_ID')
DISCORD_CLIENT_SECRET = os.getenv('DISCORD_CLIENT_SECRET')
REDIRECT_URI = os.getenv('REDIRECT_URI')
GUILD_ID = int(os.getenv('GUILD_ID', '0'))
ROLE_ID = int(os.getenv('ROLE_ID', '0'))

# Discord Bot
bot = discord.Client(intents=discord.Intents.default())
app = Flask(__name__)

@bot.event
async def on_ready():
    print(f'Bot ready: {bot.user}')

@app.route('/')
def home():
    return f'<h1>Discord Role Bot</h1><a href="/auth">Get Role</a>'

@app.route('/auth')
def auth():
    return redirect(f"https://discord.com/api/oauth2/authorize?client_id={DISCORD_CLIENT_ID}&redirect_uri={REDIRECT_URI}&response_type=code&scope=identify%20guilds.join")

@app.route('/callback')
def callback():
    code = request.args.get('code')
    if not code:
        return "Authorization failed", 400
    
    # Get token
    token_resp = requests.post('https://discord.com/api/oauth2/token', data={
        'client_id': DISCORD_CLIENT_ID,
        'client_secret': DISCORD_CLIENT_SECRET,
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': REDIRECT_URI
    })
    
    if not token_resp.ok:
        return "Token exchange failed", 400
    
    token = token_resp.json()['access_token']
    
    # Get user
    user_resp = requests.get('https://discord.com/api/v10/users/@me', 
                           headers={'Authorization': f'Bearer {token}'})
    
    if not user_resp.ok:
        return "Failed to get user info", 400
    
    user_id = int(user_resp.json()['id'])
    username = user_resp.json().get('username', 'Unknown')
    
    # Join user to guild
    join_resp = requests.put(
        f'https://discord.com/api/v10/guilds/{GUILD_ID}/members/{user_id}',
        headers={'Authorization': f'Bot {DISCORD_TOKEN}'},
        json={'access_token': token, 'roles': [str(ROLE_ID)]}
    )
    
    if join_resp.status_code in [201, 204]:
        # Try adding role separately if needed
        requests.put(
            f'https://discord.com/api/v10/guilds/{GUILD_ID}/members/{user_id}/roles/{ROLE_ID}',
            headers={'Authorization': f'Bot {DISCORD_TOKEN}'}
        )
        return f"Welcome {username}! You've joined the server."
    elif join_resp.status_code == 200:
        # User already in server, just add role
        role_resp = requests.put(
            f'https://discord.com/api/v10/guilds/{GUILD_ID}/members/{user_id}/roles/{ROLE_ID}',
            headers={'Authorization': f'Bot {DISCORD_TOKEN}'}
        )
        if role_resp.status_code == 204:
            return f"Welcome back {username}! Role assigned."
        return f"Welcome back {username}!"
    
    return "Failed to join server", 400

def start_bot():
    asyncio.run(bot.start(DISCORD_TOKEN))

if __name__ == "__main__":
    threading.Thread(target=start_bot, daemon=True).start()
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5000)))