# All Chatbots (Gemini + Flask)

10 study-only chatbots, one folder each. To run any of them:

```
cd healthcare_chatbot
python -m venv venv && source venv/bin/activate   # Windows: venv\\Scripts\\activate
pip install -r requirements.txt
# put your key in .env  (GEMINI_API_KEY=...)
python app.py          # open http://127.0.0.1:5000
```
Production: `gunicorn app:app`. Edit `chatbot_config.py` to change the prompt, title, topics or theme colours.
