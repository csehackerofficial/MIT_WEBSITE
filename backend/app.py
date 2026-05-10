from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
import yt_dlp
import os
import shutil

app = Flask(__name__)
CORS(app)

# Absolute path setup taaki server confuse na ho
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DOWNLOAD_FOLDER = os.path.join(BASE_DIR, 'downloads')

if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "status": "Active",
        "message": "DownZero Backend is running at full capacity."
    })

@app.route('/download', methods=['POST'])
def download_video():
    url = request.form.get('url')
    
    if not url:
        return "Error: URL missing.", 400

    ydl_opts = {
        # HQ format selection
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s'),
        'noplaylist': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filepath = ydl.prepare_filename(info)
            
        # Video file ko browser mein bhejna
        response = send_file(filepath, as_attachment=True)

        # Download ke baad file delete karne ke liye (Optional but recommended for Render)
        # Note: Direct delete yahan nahi hoga kyunki send_file file ko read kar raha hota hai.
        # Aap periodic cleanup use kar sakte hain ya manually delete kar sakte hain.
        
        return response

    except Exception as e:
        return f"Error: {str(e)}", 500

if __name__ == '__main__':
    # Local testing ke liye port 5000 theek hai
    app.run(debug=True, port=5000)