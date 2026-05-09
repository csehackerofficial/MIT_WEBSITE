from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
import yt_dlp
import os

app = Flask(__name__)

# CORS enable karna zaroori hai taaki Netlify is backend ko call kar sake
CORS(app)

# Downloads folder create karna
DOWNLOAD_FOLDER = 'downloads'
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

# Base route bas check karne ke liye ki server chal raha hai ya nahi
@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "status": "Active",
        "message": "DownZero Backend is running at full capacity."
    })

@app.route('/download', methods=['POST'])
def download_video():
    # Frontend se URL receive karna
    url = request.form.get('url')
    
    if not url:
        return "Error: Koi URL nahi diya gaya.", 400

    # Max Quality Settings
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'outtmpl': f'{DOWNLOAD_FOLDER}/%(title)s.%(ext)s',
        'noplaylist': True, # Ek bar me ek hi video download ho, puri playlist nahi
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filepath = ydl.prepare_filename(info)
            
        # Video file ko direct browser me bhejna
        return send_file(filepath, as_attachment=True)

    except Exception as e:
        return f"Error: {str(e)}", 500

if __name__ == '__main__':
    # Default port 5000 par run karna
    app.run(debug=True, port=5000)