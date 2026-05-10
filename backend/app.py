from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
import yt_dlp
import os

app = Flask(__name__)
CORS(app)

# Path setup taaki Render confusion na kare
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DOWNLOAD_FOLDER = os.path.join(BASE_DIR, 'downloads')

if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "status": "Active",
        "message": "DownZero Backend is running at full capacity.",
        "client": "Android-Bypass-Active"
    })

@app.route('/download', methods=['POST'])
def download_video():
    url = request.form.get('url')
    
    if not url:
        return "Error: URL missing.", 400

    # Professional HQ Settings with Bot-Bypass
    ydl_opts = {
        # HQ MP4 format selection
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s'),
        'noplaylist': True,
        'nocheckcertificate': True,
        'quiet': False,
        # TRICK: YouTube ko Android App dikhane ke liye
        'extractor_args': {
            'youtube': {
                'player_client': ['android'],
                'skip': ['dash', 'hls']
            }
        },
        # Mobile User Agent taaki bot detection bypass ho sake
        'user_agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36'
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filepath = ydl.prepare_filename(info)
            
        return send_file(filepath, as_attachment=True)

    except Exception as e:
        return f"Error: {str(e)}", 500

if __name__ == '__main__':
    # Local test ke liye port 5000, Render khud ka port manage kar lega
    app.run(debug=True, port=5000)