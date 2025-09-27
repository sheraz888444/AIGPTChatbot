import os
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from openai import OpenAI, APIStatusError
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
        
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": user_query}
            ]
        )
        
        result = completion.choices[0].message.content
        return jsonify({"response": result})
    except APIStatusError as e:
        # Handle OpenAI-specific API errors (e.g., 401, 429)
        print(f"OpenAI API error: {e.status_code} - {e.response.text}")
        error_message = e.response.json().get("error", {}).get("message", "An unknown API error occurred.")
        return jsonify({"error": error_message}), e.status_code
    except Exception as e:
        # Handle other errors (e.g., network issues, invalid JSON)
        print(f"An error occurred: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)
