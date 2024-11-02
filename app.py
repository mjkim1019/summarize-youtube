from flask import Flask, request, jsonify

from transcript import extract_video_id, get_video_info, get_video_captions

# Flask 애플리케이션 초기화
app = Flask(__name__)

# 엔드포인트: 동영상 정보 가져오기
@app.route('/video_info', methods=['GET'])
def video_info():
    url = request.args.get('url')
    video_id = extract_video_id(url)

    if not video_id:
        return jsonify({"error": "Invalid YouTube URL"}), 400

    res = get_video_info(video_id)
    if res:
        return jsonify(res)
    else:
        return jsonify({"error": "Video information could not be retrieved"}), 404

# 엔드포인트: 동영상 자막 가져오기
@app.route('/video_captions', methods=['GET'])
def video_captions():
    url = request.args.get('url')
    video_id = extract_video_id(url)

    if not video_id:
        return jsonify({"error": "Invalid YouTube URL"}), 400

    captions = get_video_captions(video_id)
    return jsonify({"captions": captions})

# 서버 실행
if __name__ == '__main__':
    app.run(debug=True, port=5000)