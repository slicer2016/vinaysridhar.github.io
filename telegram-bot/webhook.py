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
ALLOWED_CHAT_IDS = [id.strip() for id in os.environ.get('ALLOWED_CHAT_IDS', '').split(',') if id.strip()]  # Your Telegram chat ID(s)

# Debug logging
print("Starting webhook service...")
print(f"GITHUB_TOKEN exists: {bool(GITHUB_TOKEN)}")
print(f"GITHUB_REPO exists: {bool(GITHUB_REPO)}")
print(f"TELEGRAM_TOKEN exists: {bool(TELEGRAM_TOKEN)}")
print(f"ALLOWED_CHAT_IDS exists: {bool(ALLOWED_CHAT_IDS)}")

def extract_url(text):
    """Extract URL from text"""
    words = text.split()
    for word in words:
        if word.startswith('http://') or word.startswith('https://'):
            return word
    return None

def extract_title_from_url(url):
    """Try to get a readable title from URL"""
    parsed = urlparse(url)
    # Remove common suffixes and clean up
    path = parsed.path.rstrip('/')
    if path:
        title = path.split('/')[-1]
        title = title.replace('-', ' ').replace('_', ' ')
        return title.title()
    return parsed.netloc

def update_github_json(new_entry):
    """Update the JSON file in GitHub repository"""
    
    # Get current file content
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
        # File doesn't exist, create new structure
        current_content = {"entries": []}
        sha = None
    
    # Add new entry
    current_content['entries'].insert(0, new_entry)  # Add to beginning
    
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

@app.route('/webhook/telegram', methods=['POST'])
def telegram_webhook():
    """Handle incoming Telegram messages"""
    try:
        print("=== WEBHOOK CALLED ===")
        print(f"Request method: {request.method}")
        print(f"Content-Type: {request.content_type}")
        
        data = request.json
        print(f"Raw request data: {data}")
        
        if not data:
            print("ERROR: No JSON data received")
            return jsonify({'status': 'no_data'}), 400
        
        # Check if message exists
        if 'message' not in data:
            print(f"ERROR: No 'message' key in data. Keys: {list(data.keys())}")
            return jsonify({'status': 'no_message'}), 400
        
        message = data['message']
        print(f"Message data: {message}")
        
        # Check if chat exists
        if 'chat' not in message:
            print(f"ERROR: No 'chat' key in message. Keys: {list(message.keys())}")
            return jsonify({'status': 'no_chat'}), 400
            
        # Verify it's a message from allowed user
        chat_id = str(message['chat']['id'])
        print(f"Chat ID: {chat_id}")
        print(f"Allowed chat IDs: {ALLOWED_CHAT_IDS}")
        
        if not ALLOWED_CHAT_IDS:
            print("ERROR: No allowed chat IDs configured")
            return jsonify({'status': 'no_allowed_chats'}), 400
            
        if chat_id not in ALLOWED_CHAT_IDS:
            print(f"ERROR: Unauthorized chat ID {chat_id}")
            return jsonify({'status': 'unauthorized'}), 403
        
        message_text = message.get('text', '')
        print(f"Message text: {message_text}")
        
        if not message_text:
            print("ERROR: No text in message")
            return jsonify({'status': 'no_text'}), 400
        
        # Parse message format: URL + Note (rest of the message)
        url = extract_url(message_text)
        print(f"Extracted URL: {url}")
        
        if not url:
            # Send error message back
            print("Sending error message: no URL")
            send_telegram_message(
                chat_id, 
                "⚠️ No URL found. Please include a URL in your message."
            )
            return jsonify({'status': 'no_url'}), 400
        
        # Everything else is the note
        note = message_text.replace(url, '').strip()
        print(f"Note: {note}")
        
        if not note:
            print("Sending error message: no note")
            send_telegram_message(
                chat_id,
                "⚠️ Please add your thoughts about this link."
            )
            return jsonify({'status': 'no_note'}), 400
        
        # Try to extract title from URL
        title = extract_title_from_url(url)
        print(f"Title: {title}")
        
        # Create entry
        entry = {
            'date': datetime.now().strftime('%Y-%m-%d'),
            'url': url,
            'title': title,
            'note': note
        }
        print(f"Entry created: {entry}")
        
        # Update GitHub
        print("Updating GitHub...")
        if update_github_json(entry):
            print("GitHub update successful")
            send_telegram_message(
                chat_id,
                f"✅ Added to Tabula Rasa!\n\n{title}\n{note}"
            )
            return jsonify({'status': 'success', 'entry': entry})
        else:
            print("GitHub update failed")
            send_telegram_message(
                chat_id,
                "❌ Failed to add entry. Please try again."
            )
            return jsonify({'status': 'github_error'}), 500
            
    except Exception as e:
        print(f"EXCEPTION: {type(e).__name__}: {e}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
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
    app.run(debug=True, port=5000)