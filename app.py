from flask import Flask, request, Response, render_template_string
import json

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Tamim API - Vercel</title>
</head>
<body style="background:#0f0c29;color:white;text-align:center;padding:40px;">
    <h1>TAMIM API</h1>
    <form method="POST" enctype="multipart/form-data">
        <input type="file" name="json_file" required><br><br>
        <input type="number" name="limit" min="1" placeholder="Limit" required><br><br>
        <button type="submit">Convert</button>
    </form>
</body>
</html>
"""

def merge_json(data, limit):
    if not isinstance(data, list):
        data = [data]
    return data[:limit]

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files.get("json_file")
        limit = int(request.form.get("limit", 0))

        if not file or limit < 1:
            return "Invalid input", 400

        data = json.load(file)
        merged = merge_json(data, limit)

        json_bytes = json.dumps(
            merged,
            indent=2,
            ensure_ascii=False
        ).encode("utf-8")

        return Response(
            json_bytes,
            mimetype="application/json",
            headers={
                "Content-Disposition": "attachment; filename=success-BD.json"
            }
        )

    return render_template_string(HTML_TEMPLATE)

# Vercel entry point
def handler(request):
    return app(request.environ, start_response=lambda *args: None)