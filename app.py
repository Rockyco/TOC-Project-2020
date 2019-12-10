import os
import sys

from flask import Flask, jsonify, request, abort, send_file
from dotenv import load_dotenv
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

from fsm import TocMachine
from utils import send_text_message

import sqlite3

load_dotenv()


machine = TocMachine(
    states=["user","fast","slow","roast","boxed","fastfood",\
         "dinner", "trivia","wine","shit","movie","Gan","tainan"\
            ,"exotic","steak"],
    transitions=[
        {
            "trigger": "advance",
            "source": "slow",
            "dest": "steak",
            "conditions": "is_going_to_steak",
        },
        {
            "trigger": "advance",
            "source": "slow",
            "dest": "exotic",
            "conditions": "is_going_to_exotic",
        },
        {
            "trigger": "advance",
            "source": "dinner",
            "dest": "slow",
            "conditions": "is_going_to_slow",
        },
        {
            "trigger": "advance",
            "source": "dinner",
            "dest": "fast",
            "conditions": "is_going_to_fast",
        },
        {
            "trigger": "advance",
            "source": "slow",
            "dest": "roast",
            "conditions": "is_going_to_roast",
        },
        {
            "trigger": "advance",
            "source": "fast",
            "dest": "boxed",
            "conditions": "is_going_to_boxed",
        },
        {
            "trigger": "advance",
            "source": "fast",
            "dest": "fastfood",
            "conditions": "is_going_to_fastfood",
        },
        {
            "trigger": "advance",
            "source": "wine",
            "dest": "tainan",
            "conditions": "is_going_to_tainan",
        },
        {
            "trigger": "advance",
            "source": "user",
            "dest": "Gan",
            "conditions": "is_going_to_Gan",
        },
        {
            "trigger": "advance",
            "source": "user",
            "dest": "movie",
            "conditions": "is_going_to_movie",
        },
        {
            "trigger": "advance",
            "source": "user",
            "dest": "shit",
            "conditions": "is_going_to_shit",
        },
        {
            "trigger": "advance",
            "source": "user",
            "dest": "dinner",
            "conditions": "is_going_to_dinner",
        },
        {
            "trigger": "advance",
            "source": "user",
            "dest": "trivia",
            "conditions": "is_going_to_trivia",
        },
        {
            "trigger": "advance",
            "source": "user",
            "dest": "wine",
            "conditions": "is_going_to_wine",
        },
        {"trigger": "go_back", "source": ["roast","boxed","fastfood",\
          "trivia","shit","movie","Gan","tainan"\
            ,"exotic","steak"], "dest": "user"},
    ],
    initial="user",
    auto_transitions=False,
    show_conditions=True,
)

app = Flask(__name__, static_url_path="")


# get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv("LINE_CHANNEL_SECRET", None)
channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)
if channel_secret is None:
    print("Specify LINE_CHANNEL_SECRET as environment variable.")
    sys.exit(1)
if channel_access_token is None:
    print("Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.")
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
parser = WebhookParser(channel_secret)


@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    #app.logger.info("Request body: " + body)
    print("Request body: " + body)

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue

        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=event.message.text)
        )

    return "OK"


@app.route("/webhook", methods=["POST"])
def webhook_handler():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    #app.logger.info(f"Request body: {body}")
    print("Request body: " +"{" + body + "}")

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue
        if not isinstance(event.message.text, str):
            continue
        print("\nFSM STATE: {machine.state}")
        print("REQUEST BODY: \n{body}")
        response = machine.advance(event)
        if response == False:
            send_text_message(event.reply_token, "你說啥，我資質努盹不善言辭，來談些我會的吧！\n例如：\n＊來點冷知識＊＊＊＊＊\n＊＊去哪喝酒＊＊＊＊＊\n＊＊＊晚餐吃啥＊＊＊＊\n＊＊＊＊推薦電影＊＊＊\n＊＊＊＊＊來點梗圖＊＊\n＊＊＊＊＊＊韓國語錄＊")

    return "OK"


@app.route("/show-fsm", methods=["GET"])
def show_fsm():
    machine.get_graph().draw("fsm.png", prog="dot", format="png")
    return send_file("fsm.png", mimetype="image/png")


if __name__ == "__main__":
    port = os.environ.get("PORT", 8000)
    app.run(host="127.0.0.1", port=port, debug=True)
