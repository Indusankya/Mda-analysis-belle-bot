# -*- coding: utf-8 -*-
"""
Created on Fri Apr 11 22:27:55 2025

@author: indus
"""

from flask import Flask, request, jsonify, render_template_string
import google.generativeai as genai
import socket
from werkzeug.serving import make_server

app = Flask(__name__)

# Configure Belle (Gemini AI)
genai.configure(api_key="AIzaSyCDnLPYp8uv5I2u_HMuxWQJ4gG9AKM2-UI")  # Replace with your actual key

# System instruction to focus only on malondialdehyde (MDA)
SYSTEM_INSTRUCTION = """You are Belle, an AI assistant specialized exclusively in malondialdehyde (MDA). 
You will ONLY answer questions related to:
- MDA biochemistry and chemical properties
- MDA as a biomarker of oxidative stress
- MDA measurement techniques
- Factors affecting MDA levels
- Health implications of elevated MDA
- Methods to reduce MDA levels

For any other questions not specifically about MDA, respond with:
"I'm sorry, I can only answer questions related to malondialdehyde (MDA)." """

@app.route('/')
def home():
    return render_template_string('''
<!DOCTYPE html>
<html>
<head>
    <title>Belle - MDA Specialist</title>
    <style>
        body {
            font-family: 'Segoe UI', sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f8f9fa;
        }
        .belle-container {
            background: white;
            border-radius: 12px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.08);
            padding: 25px;
        }
        #chat-area {
            height: 400px;
            border: 1px solid #e0e0e0;
            padding: 15px;
            margin-bottom: 20px;
            overflow-y: auto;
            background: #fafafa;
            border-radius: 8px;
        }
        #user-input {
            width: calc(100% - 90px);
            padding: 12px 15px;
            font-size: 16px;
            border: 1px solid #ddd;
            border-radius: 8px;
            margin-right: 10px;
            outline: none;
        }
        button {
            width: 80px;
            background: #6c5ce7;
            color: white;
            border: none;
            padding: 12px 0;
            font-size: 16px;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.2s;
        }
        button:hover {
            background: #5649c0;
            transform: translateY(-1px);
        }
        .user-msg {
            color: #5c6bc0;
            margin: 12px 0;
            padding: 10px 15px;
            background: #e8eaf6;
            border-radius: 18px 18px 0 18px;
            display: inline-block;
            max-width: 80%;
            float: right;
            clear: both;
        }
        .belle-msg {
            color: #26a69a;
            margin: 12px 0;
            padding: 10px 15px;
            background: #e0f2f1;
            border-radius: 18px 18px 18px 0;
            display: inline-block;
            max-width: 80%;
            float: left;
            clear: both;
        }
        .error-msg {
            color: #ef5350;
            margin: 12px 0;
            padding: 10px;
            background: #ffebee;
            border-radius: 8px;
            clear: both;
        }
        h1 {
            color: #6c5ce7;
            text-align: center;
            margin-bottom: 25px;
        }
        .disclaimer {
            font-size: 12px;
            color: #666;
            text-align: center;
            margin-top: 20px;
        }
    </style>
</head>
<body>
    <div class="belle-container">
        <h1>Belle - MDA Specialist 🤖</h1>
        <div id="chat-area"></div>
        <div style="display: flex;">
            <input type="text" id="user-input" placeholder="Ask about malondialdehyde (MDA)..." autofocus>
            <button onclick="sendMessage()">Send</button>
        </div>
        <p class="disclaimer">This AI specializes only in malondialdehyde (MDA) research</p>
    </div>

    <script>
        function sendMessage() {
            const input = document.getElementById('user-input');
            const message = input.value.trim();
            if (!message) return;
            
            const chatArea = document.getElementById('chat-area');
            chatArea.innerHTML += `<div class="user-msg">You: ${message}</div>`;
            input.value = '';
            
            fetch('/ask', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ question: message })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    chatArea.innerHTML += `<div class="belle-msg">Belle: ${data.response}</div>`;
                } else {
                    chatArea.innerHTML += `<div class="error-msg">Error: ${data.error}</div>`;
                }
                chatArea.scrollTop = chatArea.scrollHeight;
            })
            .catch(error => {
                chatArea.innerHTML += `<div class="error-msg">Connection Error: ${error}</div>`;
                chatArea.scrollTop = chatArea.scrollHeight;
            });
        }
        
        document.getElementById('user-input').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                sendMessage();
            }
        });
    </script>
</body>
</html>
    ''')
   
@app.route('/ask', methods=['POST'])
def ask_belle():
    try:
        data = request.get_json()
        question = data.get('question', '')
        
        # Initialize the model with system instruction
        model = genai.GenerativeModel('gemini-1.5-pro-latest',
                                    system_instruction=SYSTEM_INSTRUCTION)
        
        # Start a chat session to maintain context
        chat = model.start_chat()
        response = chat.send_message(question)
        
        return jsonify({
            "success": True,
            "response": response.text
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

def find_available_port(start_port=5000):
    port = start_port
    while True:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('localhost', port))
                return port
        except OSError:
            port += 1

if __name__ == '__main__':
    port = find_available_port()
    with make_server('localhost', port, app) as server:
        print(f"\nBelle (MDA Specialist) is running on http://localhost:{port}")
        print("Press Ctrl+C to stop\n")
        server.serve_forever()