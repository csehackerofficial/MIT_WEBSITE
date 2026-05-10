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
        "message": "DownZero Pro (4K/2K Supported) is Live",
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

    api_url = "https://ytstream-download-youtube-videos.p.rapidapi.com/dl"
    
    headers = {
        "x-rapidapi-key": "ac016ebcdfmsh938111d895fed16p1d5882jsn0f080106dfc7",
        "x-rapidapi-host": "ytstream-download-youtube-videos.p.rapidapi.com"
    }
    
    querystring = {"id": video_id}

    try:
        response = requests.get(api_url, headers=headers, params=querystring)
        data = response.json()
        
        if data.get('status') == 'OK':
            formats = data.get('formats', [])
            
            # --- HIGH QUALITY PRIORITY LOGIC ---
            best_link = None
            # Hum ulti taraf se check karenge kyunki HQ links end mein hote hain
            # Priority order: 4K (2160p) > 2K (1440p) > Full HD (1080p) > HD (720p)
            
            target_qualities = ['2160p', '1440p', '1080p', '720p']
            
            for target in target_qualities:
                for f in reversed(formats):
                    # Check kar rahe hain ki kya quality match ho rahi hai aur video+audio dono hai
                    if f.get('qualityLabel') == target:
                        best_link = f.get('url')
                        break
                if best_link: break # Agar target mil gaya toh loop band karo

            # Agar koi target nahi mila, toh jo bhi best available link hai wo uthao
            if not best_link and formats:
                best_link = formats[-1].get('url')

            if best_link:
                return jsonify({"download_url": best_link})
            else:
                return jsonify({"error": "No downloadable formats found"}), 404
        
        return jsonify({"error": "API response not OK"}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)