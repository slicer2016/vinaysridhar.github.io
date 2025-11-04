"""
Tabula Rasa Webhook Service
Receives entries via Telegram bot and updates GitHub repository
"""

from flask import Flask, request, jsonify
import os
import json
from datetime import datetime
import requests
from urllib.parse import urlparse

app = Flask(__name__)

# Configuration - Set these as environment variables
GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN')
GITHUB_REPO = os.environ.get('GITHUB_REPO')  # Format: "username/repo"
TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
ALLOWED_CHAT_IDS = [id.strip() for id in os.environ.get('ALLOWED_CHAT_IDS', '').split(',') if id.strip()]

def extract_url(text):
    """Extract URL from text"""
    words = text.split()
    for word in words:
        if word.startswith('http://') or word.startswith('https://'):
            return word
    return None

def categorize_url(url):
    """Categorize URL by domain"""
    url_lower = url.lower()
    
    # Podcast platforms
    if 'spotify.com/episode' in url_lower or 'spotify.com/show' in url_lower:
        return 'podcast'
    if 'podcasts.apple.com' in url_lower:
        return 'podcast'
    if 'overcast.fm' in url_lower:
        return 'podcast'
    
    # Video platforms
    if 'youtube.com' in url_lower or 'youtu.be' in url_lower:
        return 'video'
    if 'vimeo.com' in url_lower:
        return 'video'
    
    # Social media
    if 'twitter.com' in url_lower or 'x.com' in url_lower:
        return 'tweet'
    
    # Default to article
    return 'article'

def parse_message(text):
    """
    Parse message in format: URL + Title + Note
    Returns: (url, title, note)
    """
    # Split by + sign
    parts = text.split('+')
    
    if len(parts) >= 3:
        # Format: URL + Title + Note
        url = parts[0].strip()
        title = parts[1].strip()
        note = '+'.join(parts[2:]).strip()  # Rejoin in case note has + signs
        return url, title, note
    elif len(parts) == 2:
        # Format: URL + Note (no explicit title)
        url = parts[0].strip()
        note = parts[1].strip()
        # Extract title from URL as fallback
        parsed = urlparse(url)
        path = parsed.path.rstrip('/')
        if path:
            title = path.split('/')[-1].replace('-', ' ').replace('_', ' ').title()
        else:
            title = parsed.netloc
        return url, title, note
    else:
        # Old format: URL Note (space-separated)
        url = extract_url(text)
        if url:
            note = text.replace(url, '').strip()
            # Extract title from URL
            parsed = urlparse(url)
            path = parsed.path.rstrip('/')
            if path:
                title = path.split('/')[-1].replace('-', ' ').replace('_', ' ').title()
            else:
                title = parsed.netloc
            return url, title, note
    
    return None, None, None

def update_github_json(new_entry):
    """Update the JSON file in GitHub repository"""
    
    url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/tabula-rasa-data.json"
    headers = {
        'Authorization': f'token {GITHUB_TOKEN}',
        'Accept': 'application/vnd.github.v3+json'
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        file_data = response.json()
        current_content = json.loads(
            requests.get(file_data['download_url']).text
        )
        sha = file_data['sha']
    else:
        current_content = {"entries": []}
        sha = None
    
    # Add new entry at the beginning
    current_content['entries'].insert(0, new_entry)
    
    # Update file in GitHub
    import base64
    content = json.dumps(current_content, indent=2)
    encoded_content = base64.b64encode(content.encode()).decode()
    
    data = {
        'message': f'Add entry: {new_entry["title"][:50]}',
        'content': encoded_content,
    }
    
    if sha:
        data['sha'] = sha
    
    response = requests.put(url, headers=headers, json=data)
    return response.status_code == 200 or response.status_code == 201

@app.route('/')
def root():
    return jsonify({'status': 'webhook service running', 'timestamp': datetime.now().isoformat()})

@app.route('/webhook/telegram', methods=['POST'])
def telegram_webhook():
    """Handle incoming Telegram messages"""
    try:
        data = request.json
        
        if not data or 'message' not in data:
            return jsonify({'status': 'no_data'}), 400
        
        message = data['message']
        
        if 'chat' not in message:
            return jsonify({'status': 'no_chat'}), 400
            
        chat_id = str(message['chat']['id'])
        
        if not ALLOWED_CHAT_IDS or chat_id not in ALLOWED_CHAT_IDS:
            return jsonify({'status': 'unauthorized'}), 403
        
        message_text = message.get('text', '')
        
        if not message_text:
            return jsonify({'status': 'no_text'}), 400
        
        # Parse message (supports both old and new format)
        url, title, note = parse_message(message_text)
        
        if not url:
            send_telegram_message(
                chat_id, 
                "⚠️ No URL found. Please use format:\n\nURL + Title + Your thoughts\n\nExample:\nhttps://example.com + Great Article + This is my take"
            )
            return jsonify({'status': 'no_url'}), 400
        
        if not note:
            send_telegram_message(
                chat_id,
                "⚠️ Please add your thoughts about this link."
            )
            return jsonify({'status': 'no_note'}), 400
        
        # Categorize the URL
        category = categorize_url(url)
        
        # Create entry
        entry = {
            'date': datetime.now().strftime('%Y-%m-%d'),
            'url': url,
            'title': title,
            'note': note,
            'category': category
        }
        
        # Update GitHub
        if update_github_json(entry):
            send_telegram_message(
                chat_id,
                f"✅ Added to Tabula Rasa!\n\n{title}\n{note}\n\nCategory: {category}"
            )
            return jsonify({'status': 'success', 'entry': entry})
        else:
            send_telegram_message(
                chat_id,
                "❌ Failed to add entry. Please try again."
            )
            return jsonify({'status': 'github_error'}), 500
            
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

def send_telegram_message(chat_id, text):
    """Send a message via Telegram bot"""
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {
        'chat_id': chat_id,
        'text': text
    }
    requests.post(url, json=data)

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', '5000'))
    app.run(host='0.0.0.0', port=port, debug=False)