from flask import Flask, request, jsonify
from youtube_transcript_api import YouTubeTranscriptApi

app = Flask(__name__)

@app.route('/transcript', methods=['GET'])
def transcript():
    url = request.args.get('url')
    if not url:
        return jsonify({"error": "Please provide a YouTube URL"}), 400
        
    if "v=" in url:
        video_id = url.split("v=")[1].split("&")[0]
    elif "youtu.be/" in url:
        video_id = url.split("youtu.be/")[1].split("?")[0]
    else:
        return jsonify({"error": "Could not find video ID"}), 400
        
    try:
        api = YouTubeTranscriptApi()
        transcript_obj = api.fetch(video_id, languages=['uk', 'ru', 'en'])
        data = transcript_obj.to_raw_data() if hasattr(transcript_obj, 'to_raw_data') else transcript_obj
        text = " ".join([item['text'] if type(item) is dict else getattr(item, 'text', '') for item in data])
        return jsonify({"text": text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
