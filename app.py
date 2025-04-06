from flask import Flask, request, abort
from linebot.v3.webhook import WebhookHandler
from linebot.v3.messaging import MessagingApi, Configuration, ReplyMessageRequest
from linebot.v3.models import TextMessage, MessageEvent
import os

app = Flask(__name__)

# 初始化 LINE SDK 設定
channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
channel_secret = os.getenv("LINE_CHANNEL_SECRET")

configuration = Configuration(access_token=channel_access_token)
handler = WebhookHandler(channel_secret)
messaging_api = MessagingApi(configuration)

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except Exception as e:
        print(f"Webhook handle error: {e}")
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    reply = ReplyMessageRequest(
        reply_token=event.reply_token,
        messages=[TextMessage(text=event.message.text)]
    )
    messaging_api.reply_message(reply)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
