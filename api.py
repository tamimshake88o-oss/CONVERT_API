from flask import Flask, request, render_template_string, send_file, url_for
import os
import json
from pathlib import Path
from werkzeug.utils import secure_filename

app = Flask(__name__)

# ==============================
# ফোল্ডার কনফিগ
# ==============================
UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "Output"
WASTED_FOLDER = "wasted"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)
os.makedirs(WASTED_FOLDER, exist_ok=True)

# ==============================
# প্রিমিয়াম ডার্ক থিম HTML + CSS (আগের মতোই)
# ==============================
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
    <title>Tamim API - Premium JSON Converter</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@700;900&family=Roboto+Mono:wght@400;700&display=swap" rel="stylesheet">
    <style>
        * { margin:0; padding:0; box-sizing:border-box; }
        body {
            font-family: 'Roboto Mono', monospace;
            background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
            color: #e0e0ff;
            min-height: 100vh;
            padding: 30px 15px;
            background-attachment: fixed;
        }
        .container {
            max-width: 900px;
            margin: 0 auto;
            text-align: center;
        }
        .banner {
            width: 100%;
            max-width: 900px;
            border-radius: 16px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.6);
            margin: 0 auto 35px;
            border: 1px solid #4444ff33;
        }
        h1 {
            font-family: 'Orbitron', sans-serif;
            font-size: 3.2rem;
            color: #00f0ff;
            text-shadow: 0 0 30px #00f0ff88, 0 0 60px #00f0ff44;
            margin-bottom: 12px;
            letter-spacing: 2px;
        }
        .subtitle {
            font-size: 1.3rem;
            color: #a0a0ff;
            margin-bottom: 40px;
            opacity: 0.9;
        }
        form {
            background: rgba(20, 20, 50, 0.65);
            backdrop-filter: blur(10px);
            border: 1px solid #4444ff44;
            border-radius: 16px;
            padding: 40px 30px;
            box-shadow: 0 15px 35px rgba(0,0,0,0.5);
            max-width: 500px;
            margin: 0 auto;
        }
        input[type="file"],
        input[type="number"] {
            width: 100%;
            padding: 14px;
            margin: 12px 0;
            border: 1px solid #5555ff66;
            border-radius: 10px;
            background: rgba(40,40,80,0.4);
            color: #e0e0ff;
            font-size: 1.1rem;
        }
        input[type="file"]::file-selector-button {
            background: linear-gradient(90deg, #00d4ff, #7b00ff);
            color: white;
            border: none;
            padding: 10px 18px;
            border-radius: 8px;
            cursor: pointer;
            margin-right: 12px;
        }
        input[type="submit"] {
            width: 100%;
            padding: 16px;
            margin-top: 20px;
            background: linear-gradient(90deg, #00d4ff, #7b00ff);
            color: white;
            border: none;
            border-radius: 12px;
            font-size: 1.3rem;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.3s;
            box-shadow: 0 0 25px rgba(0, 212, 255, 0.5);
        }
        input[type="submit"]:hover {
            transform: translateY(-3px);
            box-shadow: 0 0 40px rgba(0, 212, 255, 0.8);
        }
        .download-section {
            margin-top: 50px;
            font-size: 1.4rem;
        }
        .download-btn {
            display: inline-block;
            padding: 16px 40px;
            background: linear-gradient(90deg, #ff006e, #ffcc00);
            color: white;
            text-decoration: none;
            border-radius: 12px;
            font-weight: bold;
            box-shadow: 0 0 30px rgba(255,0,110,0.6);
            transition: all 0.3s;
        }
        .download-btn:hover {
            transform: scale(1.08);
            box-shadow: 0 0 50px rgba(255,0,110,0.9);
        }
        .glow-text {
            text-shadow: 0 0 15px #00f0ff;
        }
    </style>
</head>
<body>
    <div class="container">
        <!-- Banner -->
        <img src="{{ url_for('static', filename='banner.png') }}" alt="Tamim API Banner" class="banner">

        <h1 class="glow-text">TAMIM API</h1>
        <div class="subtitle">Premium JSON Converter • Fast • Secure • BD Optimized</div>

        <form method="POST" enctype="multipart/form-data">
            <input type="file" name="json_file" required>
            <input type="number" name="limit" placeholder="How many accounts to convert" min="1" required>
            <input type="submit" value="Convert Now">
        </form>

        {% if output_file %}
            <div class="download-section">
                <div style="color: #00ff88; margin: 25px 0; font-size: 1.6rem;">
                    ✅ Conversion Completed Successfully!
                </div>
                <a href="{{ output_file }}" download class="download-btn">
                    Download Success JSON
                </a>
            </div>
        {% endif %}
    </div>
</body>
</html>
"""

# ==============================
# JSON মার্জ ফাংশন
# ==============================
def merge_json_file(file_path, limit):
    output_file = Path(OUTPUT_FOLDER) / "success-BD.json"
    wasted_file = Path(WASTED_FOLDER) / "wasted.json"

    merged = []
    wasted = []
    remaining = limit

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            if not isinstance(data, list):
                data = [data]

            if remaining > 0:
                take = min(len(data), remaining)
                merged.extend(data[:take])
                remaining -= take
                if remaining == 0:
                    wasted.extend(data[take:])
            else:
                wasted.extend(data)

        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(merged, f, indent=2, ensure_ascii=False)

        if wasted:
            with open(wasted_file, "w", encoding="utf-8") as f:
                json.dump(wasted, f, indent=2, ensure_ascii=False)

        return str(output_file)
    except Exception as e:
        print(f"Error processing file: {e}")
        return None

# ==============================
# Routes
# ==============================
@app.route("/", methods=["GET", "POST"])
def index():
    output_file = None
    if request.method == "POST":
        file = request.files.get("json_file")
        limit_str = request.form.get("limit")

        if not file or not limit_str:
            return "❌ File and limit are required", 400

        try:
            limit = int(limit_str)
            if limit < 1:
                return "❌ Limit must be at least 1", 400
        except ValueError:
            return "❌ Limit must be a valid number", 400

        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)

        output_file_path = merge_json_file(filepath, limit)
        if output_file_path:
            # URL তৈরি করা হচ্ছে যাতে download কাজ করে
            output_file = url_for('download_file', filename="success-BD.json")

    return render_template_string(HTML_TEMPLATE, output_file=output_file)

@app.route("/Output/<path:filename>")
def download_file(filename):
    return send_file(os.path.join(OUTPUT_FOLDER, filename), as_attachment=True)

# ==============================
# Run - debug বন্ধ করা হয়েছে
# ==============================
if __name__ == "__main__":
    print("🚀 Tamim API Premium is running! → http://127.0.0.1:5000/")
    app.run(debug=False, host="0.0.0.0", port=5000)