import os
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import openai

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/sms", methods=["POST"])
def sms_reply():
    incoming = request.form.get("Body", "").strip()
    resp = MessagingResponse()
    try:
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role":"system","content":"You’re a concise car‑dealership assistant. Reply in 2–3 sentences."},
                {"role":"user","content":incoming}
            ],
            temperature=0.2,
            max_tokens=80
        )
        reply = completion.choices[0].message.content
    except Exception:
        reply = "I appreciate the response. One of our dealership associates will reach out to you shortly."
    resp.message(reply)
    return str(resp)

if __name__=="__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)