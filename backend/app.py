import requests
import re
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Function: YouTube URL se Video ID nikalne ke liye
def extract_video_id(url):
    reg = r'(?:v=|\/)([0-9A-Za-z_-]{11}).*'
    match = re.search(reg, url)
    return match.group(1) if match else None

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "status": "Active",
        "message": "DownZero API (YTStream Edition) is Live",
        "developer": "Aayush Kumar"
    })

@app.route('/download', methods=['POST'])
def download_video():
    user_url = request.form.get('url')
    
    if not user_url:
        return jsonify({"error": "URL missing"}), 400

    video_id = extract_video_id(user_url)
    if not video_id:
        return jsonify({"error": "Invalid YouTube URL"}), 400

    # RapidAPI Details (Jo tumne screenshot mein dikhayi)
    api_url = "https://ytstream-download-youtube-videos.p.rapidapi.com/dl"
    
    headers = {
        "x-rapidapi-key": "ac016ebcdfmsh938111d895fed16p1d5882jsn0f080106dfc7",
        "x-rapidapi-host": "ytstream-download-youtube-videos.p.rapidapi.com"
    }
    
    querystring = {"id": video_id}

    try:
        # API ko call karna
        response = requests.get(api_url, headers=headers, params=querystring)
        data = response.json()
        
        # YTStream API usually 'link' ya 'formats' mein data bhejta hai
        # Hum sabse best quality link nikalne ki koshish karenge
        if data.get('status') == 'OK' or 'link' in data:
            # Agar direct 'link' hai toh wo bhejenge, varna formats check karenge
            download_url = data.get('link') or data.get('formats', [{}])[0].get('url')
            
            return jsonify({"download_url": download_url})
        else:
            return jsonify({"error": "Video processing failed on API side"}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)