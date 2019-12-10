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
         "dinner", "trivia","wine","shit","movie","Gan","tainan","exotic"\
             ,"steak","taipei","kaohsiung","end"],
    transitions=[
        {
            "trigger": "advance",
            "source": "kaohsiung",
            "dest": "movie",
            "conditions": "is_going_to_movie",
        },
        {
            "trigger": "advance",
            "source": "kaohsiung",
            "dest": "dinner",
            "conditions": "is_going_to_dinner",
        },
        {
            "trigger": "advance",
            "source": "kaohsiung",
            "dest": "shit",
            "conditions": "is_going_to_shit",
        },
        {
            "trigger": "advance",
            "source": "kaohsiung",
            "dest": "wine",
            "conditions": "is_going_to_wine",
        },
        {
            "trigger": "advance",
            "source": "kaohsiung",
            "dest": "Gan",
            "conditions": "is_going_to_Gan",
        },
        {
            "trigger": "advance",
            "source": "kaohsiung",
            "dest": "trivia",
            "conditions": "is_going_to_trivia",
        },
        {
            "trigger": "advance",
            "source": "taipei",
            "dest": "movie",
            "conditions": "is_going_to_movie",
        },
        {
            "trigger": "advance",
            "source": "taipei",
            "dest": "dinner",
            "conditions": "is_going_to_dinner",
        },
        {
            "trigger": "advance",
            "source": "taipei",
            "dest": "shit",
            "conditions": "is_going_to_shit",
        },
        {
            "trigger": "advance",
            "source": "taipei",
            "dest": "wine",
            "conditions": "is_going_to_wine",
        },
        {
            "trigger": "advance",
            "source": "taipei",
            "dest": "Gan",
            "conditions": "is_going_to_Gan",
        },
        {
            "trigger": "advance",
            "source": "taipei",
            "dest": "trivia",
            "conditions": "is_going_to_trivia",
        },
        {
            "trigger": "advance",
            "source": "tainan",
            "dest": "movie",
            "conditions": "is_going_to_movie",
        },
        {
            "trigger": "advance",
            "source": "tainan",
            "dest": "dinner",
            "conditions": "is_going_to_dinner",
        },
        {
            "trigger": "advance",
            "source": "tainan",
            "dest": "shit",
            "conditions": "is_going_to_shit",
        },
        {
            "trigger": "advance",
            "source": "tainan",
            "dest": "wine",
            "conditions": "is_going_to_wine",
        },
        {
            "trigger": "advance",
            "source": "tainan",
            "dest": "Gan",
            "conditions": "is_going_to_Gan",
        },
        {
            "trigger": "advance",
            "source": "tainan",
            "dest": "trivia",
            "conditions": "is_going_to_trivia",
        },
        {
            "trigger": "advance",
            "source": "exotic",
            "dest": "movie",
            "conditions": "is_going_to_movie",
        },
        {
            "trigger": "advance",
            "source": "exotic",
            "dest": "dinner",
            "conditions": "is_going_to_dinner",
        },
        {
            "trigger": "advance",
            "source": "exotic",
            "dest": "shit",
            "conditions": "is_going_to_shit",
        },
        {
            "trigger": "advance",
            "source": "exotic",
            "dest": "wine",
            "conditions": "is_going_to_wine",
        },
        {
            "trigger": "advance",
            "source": "exotic",
            "dest": "Gan",
            "conditions": "is_going_to_Gan",
        },
        {
            "trigger": "advance",
            "source": "exotic",
            "dest": "trivia",
            "conditions": "is_going_to_trivia",
        },
        {
            "trigger": "advance",
            "source": "fastfood",
            "dest": "movie",
            "conditions": "is_going_to_movie",
        },
        {
            "trigger": "advance",
            "source": "fastfood",
            "dest": "dinner",
            "conditions": "is_going_to_dinner",
        },
        {
            "trigger": "advance",
            "source": "fastfood",
            "dest": "shit",
            "conditions": "is_going_to_shit",
        },
        {
            "trigger": "advance",
            "source": "fastfood",
            "dest": "wine",
            "conditions": "is_going_to_wine",
        },
        {
            "trigger": "advance",
            "source": "fastfood",
            "dest": "Gan",
            "conditions": "is_going_to_Gan",
        },
        {
            "trigger": "advance",
            "source": "fastfood",
            "dest": "trivia",
            "conditions": "is_going_to_trivia",
        },
        {
            "trigger": "advance",
            "source": "roast",
            "dest": "movie",
            "conditions": "is_going_to_movie",
        },
        {
            "trigger": "advance",
            "source": "roast",
            "dest": "dinner",
            "conditions": "is_going_to_dinner",
        },
        {
            "trigger": "advance",
            "source": "roast",
            "dest": "shit",
            "conditions": "is_going_to_shit",
        },
        {
            "trigger": "advance",
            "source": "roast",
            "dest": "wine",
            "conditions": "is_going_to_wine",
        },
        {
            "trigger": "advance",
            "source": "roast",
            "dest": "Gan",
            "conditions": "is_going_to_Gan",
        },
        {
            "trigger": "advance",
            "source": "roast",
            "dest": "trivia",
            "conditions": "is_going_to_trivia",
        },
        {
            "trigger": "advance",
            "source": "steak",
            "dest": "movie",
            "conditions": "is_going_to_movie",
        },
        {
            "trigger": "advance",
            "source": "steak",
            "dest": "dinner",
            "conditions": "is_going_to_dinner",
        },
        {
            "trigger": "advance",
            "source": "steak",
            "dest": "shit",
            "conditions": "is_going_to_shit",
        },
        {
            "trigger": "advance",
            "source": "steak",
            "dest": "wine",
            "conditions": "is_going_to_wine",
        },
        {
            "trigger": "advance",
            "source": "steak",
            "dest": "Gan",
            "conditions": "is_going_to_Gan",
        },
        {
            "trigger": "advance",
            "source": "steak",
            "dest": "trivia",
            "conditions": "is_going_to_trivia",
        },
        {
            "trigger": "advance",
            "source": "boxed",
            "dest": "movie",
            "conditions": "is_going_to_movie",
        },
        {
            "trigger": "advance",
            "source": "boxed",
            "dest": "dinner",
            "conditions": "is_going_to_dinner",
        },
        {
            "trigger": "advance",
            "source": "boxed",
            "dest": "shit",
            "conditions": "is_going_to_shit",
        },
        {
            "trigger": "advance",
            "source": "boxed",
            "dest": "wine",
            "conditions": "is_going_to_wine",
        },
        {
            "trigger": "advance",
            "source": "boxed",
            "dest": "Gan",
            "conditions": "is_going_to_Gan",
        },
        {
            "trigger": "advance",
            "source": "boxed",
            "dest": "trivia",
            "conditions": "is_going_to_trivia",
        },
        {
            "trigger": "advance",
            "source": "boxed",
            "dest": "slow",
            "conditions": "is_going_to_slow",
        },
        {
            "trigger": "advance",
            "source": "fastfood",
            "dest": "slow",
            "conditions": "is_going_to_slow",
        },
        {
            "trigger": "advance",
            "source": "exotic",
            "dest": "fast",
            "conditions": "is_going_to_fast",
        },
        {
            "trigger": "advance",
            "source": "roast",
            "dest": "fast",
            "conditions": "is_going_to_fast",
        },
        {
            "trigger": "advance",
            "source": "steak",
            "dest": "fast",
            "conditions": "is_going_to_fast",
        },
        {
            "trigger": "advance",
            "source": "fast",
            "dest": "dinner",
            "conditions": "is_going_to_backd",
        },
        {
            "trigger": "advance",
            "source": "slow",
            "dest": "dinner",
            "conditions": "is_going_to_backd",
        },
        {
            "trigger": "advance",
            "source": "boxed",
            "dest": "dinner",
            "conditions": "is_going_to_backd",
        },
        {
            "trigger": "advance",
            "source": "fastfood",
            "dest": "dinner",
            "conditions": "is_going_to_backd",
        },
        {
            "trigger": "advance",
            "source": "exotic",
            "dest": "dinner",
            "conditions": "is_going_to_backd",
        },
        {
            "trigger": "advance",
            "source": "roast",
            "dest": "dinner",
            "conditions": "is_going_to_backd",
        },
        {
            "trigger": "advance",
            "source": "steak",
            "dest": "dinner",
            "conditions": "is_going_to_backd",
        },
        {
            "trigger": "advance",
            "source": "steak",
            "dest": "end",
            "conditions": "is_going_to_end",
        },
        {
            "trigger": "advance",
            "source": "fast",
            "dest": "slow",
            "conditions": "is_going_to_slow",
        },
        {
            "trigger": "advance",
            "source": "slow",
            "dest": "fast",
            "conditions": "is_going_to_fast",
        },
        {
            "trigger": "advance",
            "source": "fastfood",
            "dest": "boxed",
            "conditions": "is_going_to_boxed",
        },
        {
            "trigger": "advance",
            "source": "boxed",
            "dest": "fastfood",
            "conditions": "is_going_to_fastfood",
        },
        {
            "trigger": "advance",
            "source": "steak",
            "dest": "exotic",
            "conditions": "is_going_to_exotic",
        },
        {
            "trigger": "advance",
            "source": "roast",
            "dest": "exotic",
            "conditions": "is_going_to_exotic",
        },
        {
            "trigger": "advance",
            "source": "exotic",
            "dest": "steak",
            "conditions": "is_going_to_steak",
        },
        {
            "trigger": "advance",
            "source": "roast",
            "dest": "steak",
            "conditions": "is_going_to_steak",
        },
        {
            "trigger": "advance",
            "source": "exotic",
            "dest": "roast",
            "conditions": "is_going_to_roast",
        },
        {
            "trigger": "advance",
            "source": "kaohsiung",
            "dest": "end",
            "conditions": "is_going_to_end",
        },
        {
            "trigger": "advance",
            "source": "kaohsiung",
            "dest": "wine",
            "conditions": "is_going_to_backw",
        },
        {
            "trigger": "advance",
            "source": "kaohsiung",
            "dest": "tainan",
            "conditions": "is_going_to_tainan",
        },
        {
            "trigger": "advance",
            "source": "kaohsiung",
            "dest": "taipei",
            "conditions": "is_going_to_taipei",
        },
        {
            "trigger": "advance",
            "source": "kaohsiung",
            "dest": "kaohsiung",
            "conditions": "is_going_to_kaohsiung",
        },
        {
            "trigger": "advance",
            "source": "taipei",
            "dest": "kaohsiung",
            "conditions": "is_going_to_kaohsiung",
        },
        {
            "trigger": "advance",
            "source": "tainan",
            "dest": "kaohsiung",
            "conditions": "is_going_to_kaohsiung",
        },
        {
            "trigger": "advance",
            "source": "wine",
            "dest": "kaohsiung",
            "conditions": "is_going_to_kaohsiung",
        },
        {
            "trigger": "advance",
            "source": "shit",
            "dest": "trivia",
            "conditions": "is_going_to_trivia",
        },
        {
            "trigger": "advance",
            "source": "shit",
            "dest": "wine",
            "conditions": "is_going_to_wine",
        },
        {
            "trigger": "advance",
            "source": "shit",
            "dest": "dinner",
            "conditions": "is_going_to_dinner",
        },
        {
            "trigger": "advance",
            "source": "shit",
            "dest": "movie",
            "conditions": "is_going_to_movie",
        },
        {
            "trigger": "advance",
            "source": "shit",
            "dest": "Gan",
            "conditions": "is_going_to_Gan",
        },
        {
            "trigger": "advance",
            "source": "Gan",
            "dest": "trivia",
            "conditions": "is_going_to_trivia",
        },
        {
            "trigger": "advance",
            "source": "Gan",
            "dest": "wine",
            "conditions": "is_going_to_wine",
        },
        {
            "trigger": "advance",
            "source": "Gan",
            "dest": "dinner",
            "conditions": "is_going_to_dinner",
        },
        {
            "trigger": "advance",
            "source": "Gan",
            "dest": "movie",
            "conditions": "is_going_to_movie",
        },
        {
            "trigger": "advance",
            "source": "Gan",
            "dest": "shit",
            "conditions": "is_going_to_shit",
        },
        {
            "trigger": "advance",
            "source": "movie",
            "dest": "trivia",
            "conditions": "is_going_to_trivia",
        },
        {
            "trigger": "advance",
            "source": "movie",
            "dest": "wine",
            "conditions": "is_going_to_wine",
        },
        {
            "trigger": "advance",
            "source": "movie",
            "dest": "dinner",
            "conditions": "is_going_to_dinner",
        },
        {
            "trigger": "advance",
            "source": "movie",
            "dest": "Gan",
            "conditions": "is_going_to_Gan",
        },
        {
            "trigger": "advance",
            "source": "movie",
            "dest": "shit",
            "conditions": "is_going_to_shit",
        },
        {
            "trigger": "advance",
            "source": "dinner",
            "dest": "trivia",
            "conditions": "is_going_to_trivia",
        },
        {
            "trigger": "advance",
            "source": "dinner",
            "dest": "wine",
            "conditions": "is_going_to_wine",
        },
        {
            "trigger": "advance",
            "source": "dinner",
            "dest": "movie",
            "conditions": "is_going_to_movie",
        },
        {
            "trigger": "advance",
            "source": "dinner",
            "dest": "Gan",
            "conditions": "is_going_to_Gan",
        },
        {
            "trigger": "advance",
            "source": "dinner",
            "dest": "shit",
            "conditions": "is_going_to_shit",
        },
        {
            "trigger": "advance",
            "source": "wine",
            "dest": "trivia",
            "conditions": "is_going_to_trivia",
        },
        {
            "trigger": "advance",
            "source": "wine",
            "dest": "dinner",
            "conditions": "is_going_to_dinner",
        },
        {
            "trigger": "advance",
            "source": "wine",
            "dest": "movie",
            "conditions": "is_going_to_movie",
        },
        {
            "trigger": "advance",
            "source": "wine",
            "dest": "Gan",
            "conditions": "is_going_to_Gan",
        },
        {
            "trigger": "advance",
            "source": "wine",
            "dest": "shit",
            "conditions": "is_going_to_shit",
        },
        {
            "trigger": "advance",
            "source": "trivia",
            "dest": "shit",
            "conditions": "is_going_to_shit",
        },
        {
            "trigger": "advance",
            "source": "trivia",
            "dest": "Gan",
            "conditions": "is_going_to_Gan",
        },
        {
            "trigger": "advance",
            "source": "trivia",
            "dest": "movie",
            "conditions": "is_going_to_movie",
        },
        {
            "trigger": "advance",
            "source": "trivia",
            "dest": "wine",
            "conditions": "is_going_to_wine",
        },
        {
            "trigger": "advance",
            "source": "trivia",
            "dest": "dinner",
            "conditions": "is_going_to_dinner",
        },
        {
            "trigger": "advance",
            "source": "taipei",
            "dest": "tainan",
            "conditions": "is_going_to_tainan",
        },
        {
            "trigger": "advance",
            "source": "tainan",
            "dest": "taipei",
            "conditions": "is_going_to_taipei",
        },
        {
            "trigger": "advance",
            "source": "fastfood",
            "dest": "fastfood",
            "conditions": "is_going_to_fastfood",
        },
        {
            "trigger": "advance",
            "source": "steak",
            "dest": "steak",
            "conditions": "is_going_to_steak",
        },
        {
            "trigger": "advance",
            "source": "exotic",
            "dest": "exotic",
            "conditions": "is_going_to_exotic",
        },
        {
            "trigger": "advance",
            "source": "steak",
            "dest": "roast",
            "conditions": "is_going_to_roast",
        },
        {
            "trigger": "advance",
            "source": "taipei",
            "dest": "taipei",
            "conditions": "is_going_to_taipei",
        },
        {
            "trigger": "advance",
            "source": "tainan",
            "dest": "tainan",
            "conditions": "is_going_to_tainan",
        },
        {
            "trigger": "advance",
            "source": "boxed",
            "dest": "boxed",
            "conditions": "is_going_to_boxed",
        },
        {
            "trigger": "advance",
            "source": "movie",
            "dest": "movie",
            "conditions": "is_going_to_movie",
        },
        {
            "trigger": "advance",
            "source": "Gan",
            "dest": "Gan",
            "conditions": "is_going_to_Gan",
        },
        {
            "trigger": "advance",
            "source": "shit",
            "dest": "shit",
            "conditions": "is_going_to_shit",
        },
        {
            "trigger": "advance",
            "source": "trivia",
            "dest": "trivia",
            "conditions": "is_going_to_trivia",
        },
        {
            "trigger": "advance",
            "source": "Gan",
            "dest": "end",
            "conditions": "is_going_to_end",
        },
        {
            "trigger": "advance",
            "source": "shit",
            "dest": "end",
            "conditions": "is_going_to_end",
        },
        {
            "trigger": "advance",
            "source": "movie",
            "dest": "end",
            "conditions": "is_going_to_end",
        },
        {
            "trigger": "advance",
            "source": "trivia",
            "dest": "end",
            "conditions": "is_going_to_end",
        },
        {
            "trigger": "advance",
            "source": "exotic",
            "dest": "end",
            "conditions": "is_going_to_end",
        },
        {
            "trigger": "advance",
            "source": "fast",
            "dest": "end",
            "conditions": "is_going_to_end",
        },
        {
            "trigger": "advance",
            "source": "slow",
            "dest": "end",
            "conditions": "is_going_to_end",
        },
        {
            "trigger": "advance",
            "source": "dinner",
            "dest": "end",
            "conditions": "is_going_to_end",
        },
        {
            "trigger": "advance",
            "source": "roast",
            "dest": "end",
            "conditions": "is_going_to_end",
        },
        {
            "trigger": "advance",
            "source": "fastfood",
            "dest": "end",
            "conditions": "is_going_to_end",
        },
        {
            "trigger": "advance",
            "source": "boxed",
            "dest": "end",
            "conditions": "is_going_to_end",
        },
        {
            "trigger": "advance",
            "source": "taipei",
            "dest": "end",
            "conditions": "is_going_to_end",
        },
        {
            "trigger": "advance",
            "source": "tainan",
            "dest": "end",
            "conditions": "is_going_to_end",
        },
        {
            "trigger": "advance",
            "source": "wine",
            "dest": "end",
            "conditions": "is_going_to_end",
        },
        {
            "trigger": "advance",
            "source": "taipei",
            "dest": "wine",
            "conditions": "is_going_to_backw",
        },
        {
            "trigger": "advance",
            "source": "tainan",
            "dest": "wine",
            "conditions": "is_going_to_backw",
        },
        {
            "trigger": "advance",
            "source": "wine",
            "dest": "taipei",
            "conditions": "is_going_to_taipei",
        },
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
        {
            "trigger": "advance",
            "source": "roast",
            "dest": "roast",
            "conditions": "is_going_to_roast",
        },
        {"trigger": "go_back", "source": ["end"], "dest": "user"},
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
            send_text_message(event.reply_token, "你說啥，我資質努盹不善言辭，來談些我會的吧！\n例如：\n＊來點冷知識＊＊＊＊＊\n＊＊推薦酒吧＊＊＊＊＊\n＊＊＊晚餐吃啥＊＊＊＊\n＊＊＊＊推薦電影＊＊＊\n＊＊＊＊＊來點梗圖＊＊\n＊＊＊＊＊＊韓國語錄＊")

    return "OK"


@app.route("/show-fsm", methods=["GET"])
def show_fsm():
    machine.get_graph().draw("fsm.png", prog="dot", format="png")
    return send_file("fsm.png", mimetype="image/png")


if __name__ == "__main__":
    port = os.environ.get("PORT", 8000)
    app.run(host="127.0.0.1", port=port, debug=True)
