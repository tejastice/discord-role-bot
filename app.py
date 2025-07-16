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

# デバッグ用
print(f"CLIENT_ID: {DISCORD_CLIENT_ID}")
print(f"REDIRECT_URI: {REDIRECT_URI}")
print(f"TOKEN exists: {bool(DISCORD_TOKEN)}")
print(f"SECRET exists: {bool(DISCORD_CLIENT_SECRET)}")
print(f"GUILD_ID: {GUILD_ID}")
print(f"ROLE_ID: {ROLE_ID}")

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
    return redirect(f"https://discord.com/api/oauth2/authorize?client_id={DISCORD_CLIENT_ID}&redirect_uri={REDIRECT_URI}&response_type=code&scope=identify")

@app.route('/callback')
def callback():
    try:
        code = request.args.get('code')
        if not code:
            return "Failed", 400
        
        print(f"Received code: {code[:10]}...")
        
        # Get token
        token_resp = requests.post('https://discord.com/api/oauth2/token', data={
            'client_id': DISCORD_CLIENT_ID,
            'client_secret': DISCORD_CLIENT_SECRET,
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': REDIRECT_URI
        })
        
        print(f"Token response status: {token_resp.status_code}")
        if not token_resp.ok:
            print(f"Token error: {token_resp.text}")
            return "Token failed", 400
        
        token = token_resp.json()['access_token']
        print("Token obtained successfully")
        
        # Get user
        user_resp = requests.get('https://discord.com/api/v10/users/@me', 
                               headers={'Authorization': f'Bearer {token}'})
        
        print(f"User response status: {user_resp.status_code}")
        if not user_resp.ok:
            print(f"User error: {user_resp.text}")
            return "User failed", 400
        
        user_id = int(user_resp.json()['id'])
        username = user_resp.json().get('username', 'Unknown')
        print(f"User: {username} ({user_id})")
        
        # Add role
        guild = bot.get_guild(GUILD_ID)
        print(f"Guild found: {guild is not None}")
        
        member = guild.get_member(user_id) if guild else None
        print(f"Member found: {member is not None}")
        
        role = guild.get_role(ROLE_ID) if guild else None
        print(f"Role found: {role is not None}")
        
        if member and role:
            asyncio.create_task(member.add_roles(role))
            print(f"Role added to {username}")
            return f"Success! Welcome {username}!"
        else:
            print(f"Failed - Guild: {guild}, Member: {member}, Role: {role}")
            return "User not in server or role not found", 400
            
    except Exception as e:
        print(f"Callback error: {e}")
        return f"Error: {str(e)}", 500

def start_bot():
    asyncio.run(bot.start(DISCORD_TOKEN))

if __name__ == "__main__":
    threading.Thread(target=start_bot, daemon=True).start()
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5000)))