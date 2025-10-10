# backend.py
from flask import Flask, request, jsonify
from flask_cors import CORS  # allows your frontend to talk to it

app = Flask(__name__)
CORS(app)  # necessary if HTML is not served by Flask

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_msg = data.get('message')
    
    # simple placeholder AI reply
    ai_reply = f"You said: {user_msg}"
    
    return jsonify({'reply': ai_reply})

if __name__ == '__main__':
    app.run(debug=True)
