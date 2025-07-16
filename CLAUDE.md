# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a single-file Discord role assignment system that automatically adds users to a Discord server and assigns them specific roles through OAuth authentication. The application consists of:

- **Flask web server** serving OAuth endpoints
- **Discord bot client** running concurrently in a separate thread
- **Direct Discord API integration** for reliable role assignment

## Architecture

The application runs two concurrent services:
1. **Flask HTTP server** (`app`) handling OAuth flow on port 5000
2. **Discord bot** (`bot`) maintaining server connection via asyncio thread

Key flow:
- User clicks "Get Role" → OAuth redirect → Discord authorization → callback with code
- Flask exchanges code for access token → fetches user info → uses Discord API to join user to guild
- Role assignment happens via direct API calls (bypassing bot cache issues)

## Development Commands

### Local Development
```bash
# Install dependencies
pip install -r requirements.txt

# Run locally (requires .env file)
python app.py
```

### Environment Setup
Required environment variables:
```bash
DISCORD_TOKEN=Bot_token_from_developer_portal
DISCORD_CLIENT_ID=Application_ID_from_developer_portal  
DISCORD_CLIENT_SECRET=OAuth2_client_secret
REDIRECT_URI=https://your-domain/callback
GUILD_ID=Target_server_ID_numeric
ROLE_ID=Target_role_ID_numeric
```

### Deployment
```bash
# Railway deployment (automatic via Procfile)
git push origin main
```

## Key Implementation Details

### Discord API Integration
- Uses **direct Discord API calls** instead of discord.py client methods for guild joining and role assignment
- Implements **dual role assignment strategy**: attempts role assignment during guild join, then separately if needed
- Handles existing members (status 200) vs new joins (status 201/204)

### Concurrent Architecture
- Flask and Discord bot run in separate threads using `threading.Thread(target=start_bot, daemon=True)`
- Discord bot maintains connection for guild/member data access
- Flask handles all HTTP endpoints and API calls

### OAuth Flow
- Scopes: `identify guilds.join` (essential for server joining)
- Uses Discord v10 API endpoints
- Implements proper error handling for each OAuth step

## Environment-Specific Notes

### Railway Deployment
- Uses `Procfile: web: python app.py`
- Environment variables managed through Railway dashboard
- No additional WSGI server needed (Flask development server acceptable for this use case)

### Discord Developer Portal Setup
- Requires Bot with "Manage Roles" and "View Channels" permissions
- Bot role must be positioned above target role in hierarchy
- OAuth2 redirect URI must match deployed URL exactly

## Common Issues and Solutions

### Role Assignment Failures
- Verify bot role hierarchy position
- Check ROLE_ID and GUILD_ID are numeric (not strings)
- Ensure bot has "Server Members Intent" enabled

### OAuth Errors
- Confirm REDIRECT_URI matches Discord Developer Portal exactly
- Verify all environment variables are set correctly
- Check Discord application has correct scopes configured

### Cache Issues
- Application uses direct API calls to avoid discord.py cache problems
- Implements fallback role assignment if initial attempt during join fails