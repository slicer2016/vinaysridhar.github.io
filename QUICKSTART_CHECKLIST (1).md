# Tabula Rasa: Your Quick Start Checklist

## Files You Need to Add to Your GitHub Repo

Upload these files to your repository:

### 1. Core Website Files (add to root of repo)
- ✓ `tabula-rasa.html` - The public page
- ✓ `tabula-rasa-data.json` - Data storage

### 2. Bot Files (create a folder called `telegram-bot/` and add these)
- ✓ `webhook.py` - Python backend
- ✓ `requirements.txt` - Dependencies
- ✓ `railway.json` - Railway config

---

## Setup Checklist

### Phase 1: Create Telegram Bot (5 min)
- [ ] Open Telegram, search for `@BotFather`
- [ ] Send `/newbot`
- [ ] Name it: "Vinay's Tabula Bot" (or whatever you want)
- [ ] Username: something like `vinay_tabula_bot` (must end in `bot`)
- [ ] **SAVE THE TOKEN** - looks like: `1234567890:ABCdefGHIjklMNOpqrsTUVwxyz`
- [ ] Write it here: `_________________________________`

### Phase 2: Get Your Chat ID (2 min)
- [ ] Send any message to your new bot
- [ ] Open browser, go to: `https://api.telegram.org/bot<YOUR_TOKEN>/getUpdates`
  - Replace `<YOUR_TOKEN>` with the token from Phase 1
- [ ] Look for `"chat":{"id":123456789}`
- [ ] **SAVE THE CHAT ID** (just the number)
- [ ] Write it here: `_________________________________`

### Phase 3: GitHub Token (3 min)
- [ ] Go to GitHub.com → Settings
- [ ] Developer settings → Personal access tokens → Tokens (classic)
- [ ] Generate new token (classic)
- [ ] Name: "Tabula Rasa Bot"
- [ ] Expiration: 1 year (set calendar reminder)
- [ ] Check box: `repo` (gives full repo access)
- [ ] Generate token
- [ ] **SAVE THE TOKEN** - looks like: `ghp_xxxxxxxxxxxxxxxxxxxx`
- [ ] Write it here: `_________________________________`

### Phase 4: Railway Setup (5 min)
- [ ] Go to railway.app
- [ ] Login with GitHub
- [ ] Authorize Railway
- [ ] You're in!

### Phase 5: Deploy to Railway (10 min)

#### 5a. Upload Files to GitHub
- [ ] In your repo, add `tabula-rasa.html` to root
- [ ] In your repo, add `tabula-rasa-data.json` to root
- [ ] In your repo, create folder `telegram-bot/`
- [ ] Add `webhook.py` to `telegram-bot/`
- [ ] Add `requirements.txt` to `telegram-bot/`
- [ ] Add `railway.json` to `telegram-bot/`
- [ ] Commit and push all changes

#### 5b. Deploy on Railway
- [ ] In Railway, click "New Project"
- [ ] Choose "Deploy from GitHub repo"
- [ ] Select your website repo
- [ ] Railway will auto-detect Python and deploy
- [ ] Wait for deployment to complete (~2 min)

#### 5c. Add Environment Variables
- [ ] In Railway, click your service → "Variables" tab
- [ ] Add these 4 variables:

```
GITHUB_TOKEN = <paste token from Phase 3>
GITHUB_REPO = <yourusername/yourrepo>
TELEGRAM_TOKEN = <paste token from Phase 1>
ALLOWED_CHAT_IDS = <paste chat ID from Phase 2>
```

Replace the `<...>` parts with your actual values!

- [ ] Click "Deploy" or it will auto-redeploy

#### 5d. Get Your Railway URL
- [ ] In Railway, click "Settings"
- [ ] Look for "Domains" section
- [ ] Copy the URL (looks like: `https://yourapp.up.railway.app`)
- [ ] **SAVE THIS URL**
- [ ] Write it here: `_________________________________`

### Phase 6: Connect Telegram to Railway (2 min)
- [ ] Open a browser
- [ ] Go to this URL (fill in your values):

```
https://api.telegram.org/bot<YOUR_BOT_TOKEN>/setWebhook?url=<YOUR_RAILWAY_URL>/webhook/telegram
```

Example (don't use this, use your own):
```
https://api.telegram.org/bot1234567890:ABCdef/setWebhook?url=https://tabula-rasa.railway.app/webhook/telegram
```

- [ ] You should see: `{"ok":true,"result":true}`
- [ ] If you see this, you're connected! ✓

### Phase 7: Test! (5 min)
- [ ] Open Telegram
- [ ] Go to your bot
- [ ] Send this message:

```
https://example.com This is my first test entry
```

- [ ] Bot should respond: "✅ Added to Tabula Rasa!"
- [ ] Go to your GitHub repo
- [ ] Check `tabula-rasa-data.json` - should have new entry
- [ ] Go to your website: `yourusername.github.io/yourrepo/tabula-rasa.html`
- [ ] Should see your test entry! (may take 1-2 minutes)

---

## Link the Page from Your Homepage

Add this link to your `index.html` navigation:

```html
<li><a href="tabula-rasa.html">Tabula Rasa</a></li>
```

---

## Troubleshooting

**Bot doesn't respond?**
- Check Railway logs (Railway dashboard → Logs)
- Verify webhook is set (repeat Phase 6)
- Check environment variables are correct

**GitHub not updating?**
- Check GitHub token has `repo` permission
- Verify `GITHUB_REPO` format is `username/repo`
- Look at Railway logs for errors

**Website not updating?**
- Wait 1-2 minutes for GitHub Pages to rebuild
- Hard refresh page (Ctrl+Shift+R)
- Check JSON file is valid (jsonlint.com)

---

## Quick Reference

**Your Bot Username:** @________________
**Railway URL:** ________________
**Your Chat ID:** ________________

**To add an entry:**
1. Open Telegram
2. Find your bot
3. Send: `<URL> <your thoughts>`
4. Done!

**Time per entry:** 15-30 seconds

---

## What's Next?

After setup works:
- [ ] Add 3-5 real entries to test
- [ ] Update your `index.html` to link to Tabula Rasa
- [ ] Pin the bot in Telegram for quick access
- [ ] Start building the habit!

Month 1 goal: 100 entries
Month 2 goal: Muscle memory

---

## Need Help?

1. Check TROUBLESHOOTING.md
2. Look at Railway logs
3. Verify all tokens are correct
4. Double-check environment variables

Most issues are:
- Typo in a token or URL
- Environment variable not set
- Wrong GITHUB_REPO format

Take your time, follow each step carefully. You've got this! 🚀
