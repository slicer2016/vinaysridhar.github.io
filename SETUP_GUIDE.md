# Tabula Rasa Setup Guide

## Overview
This system lets you add entries to your website by simply sending a message to a Telegram bot. The process takes less than 30 seconds per entry.

## What You'll Need (one-time setup)
1. A Telegram account
2. A GitHub account (you already have this)
3. A free Railway.app account (or Vercel/Render)
4. ~30 minutes for initial setup

---

## Step-by-Step Setup

### Step 1: Create a Telegram Bot (5 minutes)

1. Open Telegram and search for `@BotFather`
2. Start a chat and send `/newbot`
3. Follow the prompts:
   - Give your bot a name (e.g., "My Tabula Rasa Bot")
   - Give it a username (must end in 'bot', e.g., "vinay_tabula_bot")
4. Save the **Bot Token** you receive (looks like: `1234567890:ABCdefGHIjklMNOpqrsTUVwxyz`)
5. Send `/setcommands` to BotFather and select your bot
6. Send this command list:
   ```
   help - Show usage instructions
   ```

### Step 2: Get Your Telegram Chat ID (2 minutes)

1. Send a message to your new bot (any message)
2. Open this URL in your browser (replace YOUR_BOT_TOKEN):
   ```
   https://api.telegram.org/botYOUR_BOT_TOKEN/getUpdates
   ```
3. Look for `"chat":{"id":123456789}` in the response
4. Save this Chat ID number

### Step 3: Create GitHub Personal Access Token (3 minutes)

1. Go to GitHub Settings → Developer Settings → Personal Access Tokens → Tokens (classic)
2. Click "Generate new token (classic)"
3. Give it a name: "Tabula Rasa Bot"
4. Select these scopes:
   - ✅ `repo` (Full control of private repositories)
5. Generate token and **save it immediately** (you won't see it again)

### Step 4: Deploy to Railway (10 minutes)

1. Go to [railway.app](https://railway.app) and sign up
2. Create a new project → Deploy from GitHub repo
3. Connect your GitHub account
4. Select your website repository
5. Add environment variables (click on your service → Variables):
   ```
   GITHUB_TOKEN=your_github_token_from_step_3
   GITHUB_REPO=yourusername/yourrepo
   TELEGRAM_TOKEN=your_bot_token_from_step_1
   ALLOWED_CHAT_IDS=your_chat_id_from_step_2
   ```
6. Railway will automatically deploy your webhook service
7. Copy the public URL (looks like: `https://yourapp.railway.app`)

### Step 5: Set Telegram Webhook (2 minutes)

Open this URL in your browser (replace the values):
```
https://api.telegram.org/botYOUR_BOT_TOKEN/setWebhook?url=https://yourapp.railway.app/webhook/telegram
```

You should see: `{"ok":true,"result":true,...}`

### Step 6: Update Your Website (5 minutes)

1. Add the two files to your GitHub repo:
   - `tabula-rasa.html`
   - `tabula-rasa-data.json`

2. Update your `index.html` to add a link to Tabula Rasa:
   ```html
   <li><a href="tabula-rasa.html">Tabula Rasa</a></li>
   ```

3. Commit and push to GitHub

---

## How to Use (< 30 seconds per entry)

Just send a message to your Telegram bot in this format:

```
https://example.com/article Your thoughts here. Keep it to 1-2 lines.
```

**Examples:**

```
https://marginalrevolution.com/marginalrevolution/2025/10/ai-bubble.html Cowen's take on AI infrastructure spend is spot-on. The O-Ring model will slow diffusion more than people think.
```

```
https://www.youtube.com/watch?v=dQw4w9WgXcQ Brilliant podcast on startup psychology. The part about founder dynamics at 45:30 is gold.
```

```
https://twitter.com/pmarca/status/123456789 Marc's thread on creative destruction perfectly captures what we're seeing in media. Agree 100%.
```

The bot will:
- Extract the URL
- Use the rest as your note
- Try to extract a title from the URL
- Add it to your website automatically
- Send you a confirmation message

---

## Troubleshooting

### Bot doesn't respond
1. Check that your webhook is set correctly (Step 5)
2. Verify your Railway app is running (check dashboard)
3. Make sure your ALLOWED_CHAT_IDS includes your chat ID

### Entry didn't appear on website
1. Check that GitHub token has correct permissions
2. Verify GITHUB_REPO format is "username/repo"
3. Check Railway logs for errors

### Want to customize the title?
You can manually edit `tabula-rasa-data.json` to change titles. Format:
```json
{
  "entries": [
    {
      "date": "2025-10-28",
      "url": "https://...",
      "title": "Custom Title Here",
      "note": "Your thoughts"
    }
  ]
}
```

---

## Alternative: Use Email Instead

If you prefer email over Telegram:

1. Use a service like Zapier or Make.com
2. Set up: Email → Parse content → Update GitHub
3. Send emails to a specific address with format:
   ```
   Subject: [Tabula Rasa]
   Body: 
   URL: https://example.com
   Note: Your thoughts here
   ```

This is slightly more setup but might feel more natural if you're already processing email.

---

## Cost
- Telegram Bot: **Free**
- Railway: **Free** (generous free tier, $5/month after ~500hrs)
- GitHub: **Free**
- Total: **Free** or ~$5/month at scale

---

## Future Enhancements

Easy additions you can make later:
1. Add tags/categories to entries
2. Add search functionality to the page
3. Create a bookmarklet for even faster capture
4. Add support for Twitter/X thread links (auto-unfurl)
5. Weekly digest email of what you consumed

---

## Security Notes

- Keep your tokens secret (never commit them to GitHub)
- Only share your bot username with people you trust
- The ALLOWED_CHAT_IDS prevents unauthorized access
- All data is in your GitHub repo (you control it)
