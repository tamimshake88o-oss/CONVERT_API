 from flask import Flask, request, render_template_string, url_for
import json
import os
import uuid

app = Flask(__name__)

# Output folder
OUTPUT_DIR = "static/output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

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
        }
        .container {
            max-width: 900px;
            margin: 0 auto;
            text-align: center;
        }
        h1 {
            font-family: 'Orbitron', sans-serif;
            font-size: 3.2rem;
            color: #00f0ff;
            text-shadow: 0 0 30px #00f0ff88;
            margin-bottom: 12px;
        }
        .subtitle {
            font-size: 1.3rem;
            color: #a0a0ff;
            margin-bottom: 40px;
        }
        form {
            background: rgba(20, 20, 50, 0.65);
            border-radius: 16px;
            padding: 40px 30px;
            max-width: 500px;
            margin: 0 auto;
        }
        input {
            width: 100%;
            padding: 14px;
            margin: 12px 0;
            border-radius: 10px;
            border: 1px solid #5555ff66;
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
            background: linear-gradient(90deg, #00d4ff, #7b00ff);
            color: white;
            font-weight: bold;
            cursor: pointer;
            border: none;
        }
        .download-section {
            margin-top: 40px;
        }
        .download-btn {
            padding: 16px 40px;
            background: linear-gradient(90deg, #ff006e, #ffcc00);
            color: white;
            text-decoration: none;
            border-radius: 12px;
            font-weight: bold;
            display: inline-block;
        }
    </style>
</head>
<body>

<div class="container">
    <h1>TAMIM API</h1>
    <div class="subtitle">Premium JSON Converter • Fast • Secure • BD Optimized</div>

    <form method="POST" enctype="multipart/form-data">
        <input type="file" name="json_file" required>
        <input type="number" name="limit" placeholder="How many accounts to keep" min="1" required>
        <input type="submit" value="Convert">
    </form>

    {% if output_file %}
    <div class="download-section">
        <p style="color:#00ff88;font-size:1.5rem;">✅ Conversion Completed</p>
        <a href="{{ output_file }}" download class="download-btn">
            Download JSON
        </a>
    </div>
    {% endif %}
</div>

</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    output_file = None

    if request.method == "POST":
        file = request.files.get("json_file")
        limit = request.form.get("limit")

        if not file or not limit:
            return "Invalid input", 400

        try:
            limit = int(limit)
            data = json.load(file)
        except Exception:
            return "Invalid JSON file", 400

        if not isinstance(data, list):
            data = [data]

        # ✅ EXACT BEHAVIOR YOU WANT
        selected_data = data[:limit]

        filename = f"success-{uuid.uuid4().hex}.json"
        filepath = os.path.join(OUTPUT_DIR, filename)

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(selected_data, f, indent=2, ensure_ascii=False)

        output_file = url_for("static", filename=f"output/{filename}")

    return render_template_string(HTML_TEMPLATE, output_file=output_file)


if __name__ == "__main__":
    app.run(debug=True)