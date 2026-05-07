import os

os.environ.setdefault("NUMBA_DISABLE_JIT", "1")

from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
from rembg import remove, new_session
from PIL import Image
import io

app = Flask(__name__)
CORS(app)

# Lazy load session for Railway free plan
session = None

def get_session():
    global session

    if session is None:
        session = new_session("u2netp")

    return session


@app.route('/')
def home():
    return "AJ Pixel Cut API Running 🚀"


@app.route('/health')
def health():
    return jsonify({
        "status": "running"
    })


@app.route('/remove-bg', methods=['POST'])
def remove_bg():
    try:
        if 'image' not in request.files:
            return jsonify({"error": "No image uploaded"}), 400

        file = request.files['image']

        input_image = Image.open(file.stream).convert("RGBA")

        output = remove(
            input_image,
            session=get_session()
        )

        img_io = io.BytesIO()

        output.save(
            img_io,
            format="PNG"
        )

        img_io.seek(0)

        return send_file(
            img_io,
            mimetype='image/png'
        )

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))

    app.run(
        host='0.0.0.0',
        port=port
    )
