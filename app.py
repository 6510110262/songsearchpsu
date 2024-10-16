from flask import Flask, request, render_template, jsonify
from emotion_model import predict_emotion
import requests
import os
from dotenv import load_dotenv

# โหลดค่าตัวแปรจากไฟล์ .env
load_dotenv()

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search_song', methods=['POST'])
def search_song():
    data = request.get_json()
    user_input = data.get('user_input')

    if not user_input:
        return jsonify({"error": "กรุณาใส่ข้อความที่ต้องการ"}), 400

    # ตรวจจับอารมณ์จากข้อความที่ผู้ใช้พิมพ์
    emotion = predict_emotion(user_input)

    # ใช้ Client Access Token เป็น API Key จากไฟล์ .env
    api_key = os.getenv("GENIUS_API_KEY")
    base_url = "https://api.genius.com/search"
    headers = {
        "Authorization": f"Bearer {api_key}"
    }
    params = {
        'q': emotion  # ค้นหาเพลงจากอารมณ์ที่ตรวจจับได้
    }

    response = requests.get(base_url, headers=headers, params=params)

    if response.status_code == 200:
        result = response.json()
        songs = result['response']['hits']
        
        if songs:
            return jsonify(songs), 200
        else:
            return jsonify({"error": "ไม่พบเพลงที่ตรงกับอารมณ์"}), 404
    else:
        return jsonify({"error": "เกิดข้อผิดพลาดในการค้นหา"}), response.status_code

if __name__ == '__main__':
    app.run(debug=True, port=5000)  # กำหนดพอร์ตที่ต้องการ
