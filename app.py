from flask import Flask, request, Response, render_template_string
import json

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>JSON Converter</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body style="margin:0;min-height:100vh;display:flex;align-items:center;justify-content:center;
             background:#111;color:white;font-family:Arial;">
    <form method="POST" enctype="multipart/form-data"
          style="background:#222;padding:30px;border-radius:10px;width:300px;text-align:center;">
        <h2>Upload JSON File</h2>

        <input type="file" name="json_file" accept=".json" required><br><br>

        <input type="number" name="limit" min="1"
               placeholder="How many accounts" required
               style="width:100%;padding:8px;"><br><br>

        <button type="submit"
                style="width:100%;padding:10px;font-weight:bold;cursor:pointer;">
            Convert & Download
        </button>
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
            return "Invalid input", 400

        try:
            limit = int(limit)
            data = json.load(file)
        except Exception:
            return "Invalid JSON file", 400

        # CLI logic match
        if not isinstance(data, list):
            data = [data]

        converted = data[:limit]
        wasted = data[limit:]

        result = {
            "converted": converted,
            "wasted": wasted
        }

        return Response(
            json.dumps(result, indent=2, ensure_ascii=False),
            mimetype="application/json",
            headers={
                "Content-Disposition": "attachment; filename=success-BD.json"
            }
        )

    return render_template_string(HTML)