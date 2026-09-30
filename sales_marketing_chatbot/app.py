import os
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from google import genai
from google.genai import types
import chatbot_config as cfg

load_dotenv()
app = Flask(__name__)

MODEL = os.getenv("GEMINI_MODEL", "gemini-3.1-flash-lite")
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


@app.route("/")
def index():
    return render_template("index.html", cfg=cfg)


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    message = (data.get("message") or "").strip()
    history = data.get("history") or []
    if not message:
        return jsonify({"reply": "Please type a question."}), 400
    if len(message) > 2000:
        return jsonify({"reply": "Your message is too long. Please shorten it."}), 400

    contents = []
    for turn in history[-12:]:
        role = "model" if turn.get("role") == "model" else "user"
        contents.append(types.Content(role=role, parts=[types.Part(text=str(turn.get("text", ""))[:4000])]))
    contents.append(types.Content(role="user", parts=[types.Part(text=message)]))

    try:
        res = client.models.generate_content(
            model=MODEL,
            contents=contents,
            config=types.GenerateContentConfig(
                system_instruction=cfg.SYSTEM_PROMPT,
                temperature=0.4,
                max_output_tokens=1500,
            ),
        )
        return jsonify({"reply": res.text or cfg.REFUSAL_MESSAGE})
    except Exception as e:
        app.logger.error("Gemini error: %s", e)
        return jsonify({"reply": "Sorry, something went wrong. Please try again."}), 500


if __name__ == "__main__":
    app.run(debug=True, port=int(os.getenv("PORT", 5000)))
