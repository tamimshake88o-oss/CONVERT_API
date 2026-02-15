
from flask import Flask, request, render_template_string, send_file
import json
import io

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Tamim API - JSON Converter</title>
    <style>
        body { font-family: Arial, sans-serif; background: linear-gradient(135deg, #ff9a9e, #fad0c4, #a1c4fd); color: #333; text-align: center; padding: 50px;}
        h1 { color: #fff; text-shadow: 2px 2px 5px #000; }
        input { padding: 10px; margin: 10px; border-radius: 5px; border: none; }
        button { padding: 10px 20px; border: none; border-radius: 5px; background: #4CAF50; color: white; cursor: pointer; font-weight: bold;}
        button:hover { background: #45a049; }
    </style>
</head>
<body>
    <h1>Tamim API - JSON Converter</h1>

    <form method="POST" enctype="multipart/form-data">
        <input type="file" name="json_file" required><br>
        <input type="number" name="limit" placeholder="How many accounts to convert" min="1" required><br>
        <button type="submit">Convert & Download</button>
    </form>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files.get("json_file")
        limit = request.form.get("limit")

        if not file or not limit:
            return "❌ File and limit required", 400

        try:
            limit = int(limit)
            data = json.load(file)
        except Exception:
            return "❌ Invalid JSON file", 400

        if not isinstance(data, list):
            data = [data]

        # ✅ OLD BEHAVIOR
        result = {
            "converted": data[:limit],
            "wasted": data[limit:]
        }

        # 🔥 In-memory file (NO static path issue)
        output = io.BytesIO()
        output.write(json.dumps(result, indent=2, ensure_ascii=False).encode("utf-8"))
        output.seek(0)

        return send_file(
            output,
            as_attachment=True,
            download_name="success-BD.json",
            mimetype="application/json"
        )

    return render_template_string(HTML_TEMPLATE)


if __name__ == "__main__":
    app.run(debug=True)