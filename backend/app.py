import os
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from openai import OpenAI
from flask_cors import CORS

load_dotenv()

# Debug: Check if API key is loaded
api_key = os.environ.get("OPENAI_API_KEY")
if api_key:
    print(f"API Key loaded successfully. Length: {len(api_key)} characters. Starts with: {api_key[:8]}...")
else:
    print("Warning: OPENAI_API_KEY not found in environment.")

app = Flask(__name__)
CORS(app)

client = OpenAI(api_key=api_key)

@app.route("/ask", methods=["POST"])
def ask():
    try:
        data = request.get_json()
        user_query = data.get("question", "")
        if not user_query:
            return jsonify({"error": "No question provided"}), 400
        
        # Debug: Print the key being used in the request
        print(f"Using API key for request starting with: {client.api_key[:8]}...")
        
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": user_query}
            ]
        )
        
        result = completion.choices[0].message.content
        return jsonify({"response": result})
    except KeyError:
        return jsonify({"error": "OPENAI_API_KEY environment variable not set. Please check your .env file."}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
