from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os, json, openai
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
CORS(app)  # allows frontend to talk to backend if served separately

# Set OpenAI API key from environment variable
openai.api_key = os.environ.get("OPENAI_API_KEY")

DATA_FILE = "loginregisterinfo.JSON"

# Ensure JSON file exists
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        json.dump({"users": {}, "chats": {}}, f, indent=2)

# Serve frontend files
@app.route("/")
def index():
    return send_from_directory(".", "index.html")

@app.route("/<path:path>")
def serve_file(path):
    return send_from_directory(".", path)

# Chat endpoint
@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_id = data.get("user_id", "guest")  # default to guest
    message = data.get("message", "")
    model = data.get("model", "gpt-3.5-turbo")

    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=[{"role": "user", "content": message}]
        )
        ai_reply = response['choices'][0]['message']['content']
    except Exception as e:
        ai_reply = f"Error: {e}"

    # Save chat history
    with open(DATA_FILE, "r") as f:
        json_data = json.load(f)
    if user_id not in json_data["chats"]:
        json_data["chats"][user_id] = []
    json_data["chats"][user_id].append({"user": message, "ai": ai_reply})
    with open(DATA_FILE, "w") as f:
        json.dump(json_data, f, indent=2)

    return jsonify({"reply": ai_reply})

# Register endpoint
@app.route("/register", methods=["POST"])
def register():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"success": False, "message": "Missing username or password"})

    with open(DATA_FILE, "r") as f:
        json_data = json.load(f)

    if username in json_data["users"]:
        return jsonify({"success": False, "message": "Username already exists"})

    json_data["users"][username] = generate_password_hash(password)
    json_data["chats"][username] = []

    with open(DATA_FILE, "w") as f:
        json.dump(json_data, f, indent=2)

    return jsonify({"success": True, "message": "Registered successfully"})

# Login endpoint
@app.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    with open(DATA_FILE, "r") as f:
        json_data = json.load(f)

    if username not in json_data["users"]:
        return jsonify({"success": False, "message": "User not found"})

    if check_password_hash(json_data["users"][username], password):
        return jsonify({"success": True, "message": "Login successful"})
    else:
        return jsonify({"success": False, "message": "Incorrect password"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)
