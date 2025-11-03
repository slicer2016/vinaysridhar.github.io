# Tabula Rasa: Complete Implementation Guide

## TL;DR - Choose Your Method

| Method | Setup Time | Friction | Mobile | Best For |
|--------|-----------|----------|--------|----------|
| **Telegram Bot** | 30 min | ★★★★★ Lowest | ★★★★★ Excellent | Most seamless experience |
| **GitHub Issues** | 10 min | ★★★☆☆ Medium | ★★★☆☆ Good | No external dependencies |
| **Web Form** | 15 min | ★★★★☆ Low | ★★★★☆ Good | Visual interface, customizable |

---

## Method 1: Telegram Bot (Recommended)

### Why Choose This
- **Fastest input**: Open Telegram, paste URL + thought, done (<30 seconds)
- **Best mobile experience**: Telegram app is fast and reliable
- **Works everywhere**: Share from any app to Telegram
- **Confirmation feedback**: Bot replies confirming entry added

### Setup Requirements
- Telegram account
- Railway/Vercel account (free tier)
- GitHub token
- 30 minutes setup

### Usage Flow
```
1. See interesting content
2. Open Telegram bot
3. Paste: "https://url.com Your thoughts here"
4. Hit send
5. Bot confirms → Entry live on site
```

**Files needed:**
- `webhook.py` - Backend service
- `requirements.txt` - Dependencies
- `railway.json` - Deployment config
- `tabula-rasa.html` - Frontend page
- `tabula-rasa-data.json` - Data storage

See `SETUP_GUIDE.md` for detailed steps.

---

## Method 2: GitHub Issues

### Why Choose This
- **Zero external dependencies**: Everything on GitHub
- **Free forever**: No hosting costs
- **Easy editing**: Can edit/delete entries in GitHub
- **No tokens to manage**: Uses GitHub's built-in auth

### Setup Requirements
- GitHub account only
- 10 minutes setup

### Usage Flow
```
1. See interesting content
2. Go to repo → Issues → New Issue
3. Select "Tabula Rasa Entry" template
4. Fill in URL and thoughts
5. Submit → GitHub Action auto-processes
```

**Files needed:**
- `.github/workflows/add-tabula-entry.yml` - GitHub Action
- `.github/ISSUE_TEMPLATE/tabula-rasa.md` - Issue template
- `tabula-rasa.html` - Frontend page
- `tabula-rasa-data.json` - Data storage

See `GITHUB_ISSUES_METHOD.md` for detailed steps.

---

## Method 3: Web Form

### Why Choose This
- **Visual interface**: See what you're adding
- **Preview feature**: Check before submitting
- **Bookmarklet support**: One-click from any page
- **No app needed**: Works in any browser

### Setup Requirements
- GitHub Pages (or any web hosting)
- GitHub token
- 15 minutes setup

### Usage Flow
```
1. See interesting content
2. Open form (or use bookmarklet)
3. Fill in fields
4. Preview entry
5. Submit → Live on site
```

**Files needed:**
- `add-entry.html` - Form interface
- `tabula-rasa.html` - Frontend page
- `tabula-rasa-data.json` - Data storage

---

## Hybrid Approach (Best of All Worlds)

You can use **multiple methods simultaneously**! They all update the same `tabula-rasa-data.json` file.

**Recommended combination:**
1. **Telegram bot** for quick mobile captures
2. **Web form** for desktop with longer thoughts
3. **GitHub Issues** for editing/deleting entries

---

## Common Files (All Methods Need These)

### 1. `tabula-rasa.html` - The Public Page

This is what your visitors see. It reads from `tabula-rasa-data.json` and displays entries in a clean, chronological list.

**Features:**
- Auto-sorts by date (newest first)
- Clean, minimal design matching your site
- Mobile-responsive
- No JavaScript frameworks needed

### 2. `tabula-rasa-data.json` - Data Storage

Simple JSON structure:
```json
{
  "entries": [
    {
      "date": "2025-10-28",
      "url": "https://example.com",
      "title": "Article Title",
      "note": "Your thoughts here"
    }
  ]
}
```

**Why JSON instead of a database?**
- Simple
- Version controlled (in Git)
- No server needed
- Easy to backup/edit
- Fast to load

---

## Security Considerations

### For Telegram Bot:
- Keep bot token secret (env variables)
- Whitelist only your chat ID
- Use HTTPS for webhooks

### For Web Form:
- Keep GitHub token secret
- Consider adding password protection
- Or host on private subdomain

### For GitHub Issues:
- Issues are public by default
- Consider making repo private if needed
- Use issue labels to control what gets processed

---

## Future Enhancements

Once basic system is working, you can add:

1. **Categories/Tags**
   - Add `category` field to JSON
   - Filter entries by type
   - Visual indicators

2. **Search Functionality**
   - Add search box to page
   - Filter by keyword in title or note

3. **Auto-Extract Metadata**
   - Fetch article title from URL
   - Extract author name
   - Pull preview image

4. **Weekly Digest**
   - Email yourself weekly summary
   - RSS feed generation
   - Twitter thread of week's entries

5. **Analytics**
   - Track most-shared domains
   - Your reading patterns over time
   - Word cloud of notes

6. **Bookmarklet Improvements**
   - Auto-fill current page URL
   - Pre-select text on page
   - Show form overlay

---

## Maintenance

### Zero maintenance needed:
- GitHub Pages auto-deploys
- JSON file is version controlled
- No database to maintain
- No server updates required

### Optional updates:
- Refresh styling every few months
- Add new features as needed
- Archive old entries yearly

---

## Cost Breakdown

| Component | Cost |
|-----------|------|
| GitHub Pages | Free |
| GitHub Actions | Free (plenty of minutes) |
| Railway (Telegram method) | Free tier, then $5/month |
| Telegram Bot | Free |
| Domain (if custom) | ~$12/year |
| **Total** | **$0-5/month** |

---

## My Recommendation

**Start with Method 2 (GitHub Issues)**
- Fastest setup
- Zero cost
- No dependencies
- See if you like the concept

**After 1 week, upgrade to Method 1 (Telegram Bot)**
- If you're using it regularly
- If mobile friction bothers you
- If you want fastest possible input

**Keep both methods running**
- Telegram for 90% of quick entries
- GitHub Issues for editing/deleting
- Best of both worlds

---

## Quick Start Checklist

- [ ] Add `tabula-rasa.html` to your repo
- [ ] Add `tabula-rasa-data.json` to your repo
- [ ] Link to page from `index.html`
- [ ] Choose your input method (start with GitHub Issues)
- [ ] Follow setup guide for chosen method
- [ ] Test with 2-3 entries
- [ ] Add to your daily workflow

---

## Questions?

Common issues and solutions:

**Entries not showing up?**
- Check JSON syntax is valid
- Verify file is committed to repo
- Clear browser cache

**Telegram bot not responding?**
- Verify webhook is set
- Check Railway logs
- Confirm chat ID is whitelisted

**GitHub Action failing?**
- Check workflow YAML syntax
- Verify issue has correct label
- Review Action logs in GitHub

---

## Example Entry

Here's what a complete entry looks like on your site:

```
Oct 28, 2025
Tyler Cowen's AI Take-Off Essay
Marginal Revolution | https://marginalrevolution.com/...

Cowen's O-Ring model for AI diffusion is brilliant. The 
bottleneck will shift to the slowest-moving part of each 
sector. Explains why deployment takes decades, not years.
```

Clean, scannable, useful.

---

## Files Included

All files are in `/mnt/user-data/outputs/`:

1. **Core files (all methods):**
   - `tabula-rasa.html` - Public page
   - `tabula-rasa-data.json` - Data file

2. **Method 1 - Telegram Bot:**
   - `webhook.py` - Backend service
   - `requirements.txt` - Dependencies
   - `railway.json` - Deployment config
   - `SETUP_GUIDE.md` - Detailed setup

3. **Method 2 - GitHub Issues:**
   - `GITHUB_ISSUES_METHOD.md` - Full guide with workflow YAML

4. **Method 3 - Web Form:**
   - `add-entry.html` - Form interface

5. **This file:**
   - `README.md` - Overview and comparison

---

## Next Steps

1. Read this README fully
2. Choose your method
3. Follow the setup guide
4. Test with a few entries
5. Iterate and improve

Remember: **Done is better than perfect**. Start simple, add features later.

Happy collecting! 📚
