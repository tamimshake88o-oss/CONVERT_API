from flask import Flask, request, render_template_string, send_file
import json
import io

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
    <title>Tamim API - Premium JSON Converter</title>
</head>
<body style="background:#0f0c29;color:white;text-align:center;padding:40px;">
    <h1>TAMIM API</h1>

    <form method="POST" enctype="multipart/form-data">
        <input type="file" name="json_file" required><br><br>
        <input type="number" name="limit" placeholder="How many accounts" required><br><br>
        <button type="submit">Convert</button>
    </form>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
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

        selected_data = data[:limit]

        output = io.BytesIO()
        output.write(json.dumps(selected_data, indent=2, ensure_ascii=False).encode("utf-8"))
        output.seek(0)

        return send_file(
            output,
            as_attachment=True,
            download_name="success-BD.json",
            mimetype="application/json"
        )

    return render_template_string(HTML_TEMPLATE)