from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
from rembg import remove, new_session
from PIL import Image
import io
import os

app = Flask(__name__)
CORS(app)

# =========================
# REMBG SESSION
# =========================
u2net_session = new_session("u2net")

# =========================
# HOME ROUTE
# =========================
@app.route('/')
def home():
    return "AJ Pixel Cut API Running 🚀"

# =========================
# BASIC BACKGROUND REMOVER
# =========================
@app.route('/remove-bg', methods=['POST'])
def remove_bg():
    try:
        if 'image' not in request.files:
            return jsonify({"error": "No image uploaded"}), 400

        file = request.files['image']

        input_image = Image.open(file.stream).convert("RGBA")

        output = remove(input_image, session=u2net_session)

        img_io = io.BytesIO()
        output.save(img_io, format="PNG")
        img_io.seek(0)

        return send_file(
            img_io,
            mimetype='image/png',
            as_attachment=False,
            download_name='removed-bg.png'
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# =========================
# HEALTH CHECK
# =========================
@app.route('/health')
def health():
    return jsonify({
        "status": "running",
        "service": "AJ Pixel Cut API"
    })

# =========================
# RUN SERVER
# =========================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))

    app.run(
        host="0.0.0.0",
        port=port,
        debug=False
    )
