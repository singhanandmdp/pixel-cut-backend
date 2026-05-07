import os

os.environ.setdefault("NUMBA_DISABLE_JIT", "1")

from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
from rembg import remove, new_session
from PIL import Image
import io

app = Flask(__name__)
CORS(app)

# Lightweight model
u2net_session = new_session("u2netp")


@app.route('/')
def home():
    return "AJ Pixel Cut API Running 🚀"


@app.route('/remove-bg', methods=['POST'])
def remove_bg():
    try:
        if 'image' not in request.files:
            return jsonify({"error": "No image uploaded"}), 400

        file = request.files['image']

        input_image = Image.open(file.stream).convert("RGBA")

        output = remove(
            input_image,
            session=u2net_session
        )

        img_io = io.BytesIO()
        output.save(img_io, format="PNG")
        img_io.seek(0)

        return send_file(
            img_io,
            mimetype='image/png'
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/health')
def health():
    return jsonify({
        "status": "running"
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
