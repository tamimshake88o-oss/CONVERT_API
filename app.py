from flask import Flask, request, render_template_string, send_file
import json
import io

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en" class="dark">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>TAMIM API - Premium Space Flight</title>

  <script src="https://cdn.tailwindcss.com"></script>
  <script>
    tailwind.config = {
      darkMode: 'class',
      theme: {
        extend: {
          fontFamily: {
            sans: ['Inter', 'sans-serif']
          }
        }
      }
    }
  </script>

  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet"/>

  <style>
    body {
      margin: 0;
      overflow: hidden;
      background: #000;
      font-family: 'Inter', sans-serif;
    }
    #bg-video {
      position: fixed;
      right: 0;
      bottom: 0;
      min-width: 100%;
      min-height: 100%;
      width: auto;
      height: auto;
      z-index: -1;
      object-fit: cover;
    }
    .overlay {
      position: relative;
      z-index: 1;
      min-height: 100vh;
      display: flex;
      align-items: center;
      justify-content: center;
      background: rgba(0, 0, 20, 0.5);
      backdrop-filter: blur(6px);
    }
    .glass {
      background: rgba(30, 30, 60, 0.4);
      backdrop-filter: blur(16px);
      border: 1px solid rgba(255,255,255,0.1);
      box-shadow: 0 8px 32px rgba(0,0,0,0.5);
      border-radius: 24px;
      padding: 3rem;
      max-width: 28rem;
      width: 90%;
    }
  </style>
</head>

<body>

  <!-- Looping Space Video Background -->
  <video id="bg-video" autoplay muted loop playsinline>
    <source src="/space-flight-loop.mp4" type="video/mp4">
    Your browser does not support video.
  </video>

  <div class="overlay">
    <div class="glass text-center text-white">

      <h1 class="text-4xl md:text-5xl font-bold mb-6
        bg-gradient-to-r from-blue-400 via-purple-500 to-pink-500
        bg-clip-text text-transparent">
        TAMIM API
      </h1>

      <p class="text-lg text-gray-300 mb-10">
        Convert accounts seamlessly in deep space elegance
      </p>

      <!-- IMPORTANT: method, enctype, name attributes kept SAME -->
      <form method="POST" enctype="multipart/form-data">

        <div class="mb-8">
          <label class="block text-lg font-medium mb-3">Choose File</label>
          <input
            type="file"
            name="json_file"
            required
            id="fileInput"
            class="w-full px-5 py-4 bg-gray-900/40 border border-gray-600 rounded-xl
                   text-white focus:outline-none focus:border-purple-500 transition"
          />
          <p id="fileName" class="mt-2 text-sm text-purple-400 hidden">
            Selected: <span id="name"></span>
          </p>
        </div>

        <div class="mb-8">
          <label class="block text-lg font-medium mb-3">How many accounts?</label>
          <input
            type="number"
            name="limit"
            required
            placeholder="Enter number"
            class="w-full px-5 py-4 bg-gray-900/40 border border-gray-600 rounded-xl
                   text-white focus:outline-none focus:border-purple-500 transition"
          />
        </div>

        <button
          type="submit"
          class="w-full py-5 bg-gradient-to-r from-purple-600 to-pink-600
                 hover:from-purple-700 hover:to-pink-700
                 text-white font-bold text-xl rounded-xl shadow-2xl
                 transform hover:scale-105 transition-all duration-300">
          Convert Now
        </button>

      </form>
    </div>
  </div>

  <script>
    document.getElementById('fileInput').addEventListener('change', (e) => {
      const file = e.target.files[0];
      if (file) {
        document.getElementById('name').textContent = file.name;
        document.getElementById('fileName').classList.remove('hidden');
      }
    });
  </script>

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