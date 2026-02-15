from flask import Flask, request, Response, render_template_string
import json

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>TAMIM API</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {
            margin:0;
            min-height:100vh;
            display:flex;
            align-items:center;
            justify-content:center;
            background:linear-gradient(135deg,#0f0c29,#302b63,#24243e);
            font-family:Arial, Helvetica, sans-serif;
            color:white;
        }
        .card {
            background:rgba(0,0,0,0.4);
            padding:25px;
            border-radius:15px;
            width:90%;
            max-width:360px;
            text-align:center;
            box-shadow:0 0 25px rgba(0,0,0,0.6);
        }
        h1 {
            margin-bottom:5px;
            color:#00f7ff;
            letter-spacing:1px;
        }
        p {
            font-size:13px;
            opacity:0.85;
            margin-bottom:20px;
        }
        input, button {
            width:100%;
            padding:12px;
            margin-top:10px;
            border:none;
            border-radius:8px;
            font-size:14px;
        }
        input {
            background:#1e1e2e;
            color:white;
        }
        button {
            margin-top:18px;
            background:linear-gradient(90deg,#00f7ff,#7f00ff);
            color:white;
            font-weight:bold;
            cursor:pointer;
        }
        button:hover {
            opacity:0.9;
        }
    </style>
</head>
<body>
    <div class="card">
        <h1>TAMIM API</h1>
        <p>Premium JSON Converter • Fast • Secure</p>
        <form method="POST" enctype="multipart/form-data">
            <input type="file" name="json_file" required>
            <input type="number" name="limit" min="1" placeholder="How many accounts to convert" required>
            <button type="submit">Convert Now</button>
        </form>
    </div>
</body>
</html>
"""

def merge_json(data, limit):
    if isinstance(data, list):
        return data[:limit]
    return [data]

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

        result = merge_json(data, limit)

        return Response(
            json.dumps(result, indent=2, ensure_ascii=False),
            mimetype="application/json",
            headers={
                "Content-Disposition": "attachment; filename=success-BD.json"
            }
        )

    return render_template_string(HTML_TEMPLATE)

# 🔹 Vercel compatibility
def handler(event, context):
    return app