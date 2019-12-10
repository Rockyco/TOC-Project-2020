from transitions.extensions import GraphMachine

from utils import send_text_message,send_image_url

import sqlite3
import random

class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)

    def is_going_to_dinner(self, event):
        text = event.message.text
        return text.lower() == "晚餐吃啥"

    def is_going_to_trivia(self, event):
        text = event.message.text
        return text.lower() == "來點冷知識"

    def on_enter_dinner(self, event):
        reply_token = event.reply_token
        send_text_message(reply_token, "用餐時間多久呢？\n\n快一點、慢慢來")

    def on_enter_trivia(self, event):
        mydb=sqlite3.connect("my.db")
        cursor=mydb.cursor()
        cursor.execute("SELECT setence FROM users WHERE role_id = 2")
        Tables=cursor.fetchall()
        print(random.choice(Tables)[0])

        reply_token = event.reply_token
        send_text_message(reply_token, "你知道嗎：\n" + random.choice(Tables)[0])
    
    def is_going_to_wine(self, event):
        text = event.message.text
        return text.lower() == "推薦酒吧"

    def on_enter_wine(self, event):
        reply_token = event.reply_token
        send_text_message(reply_token, "選個地區吧:\n\n台北\n\t台南\n\t\t高雄")


    def is_going_to_movie(self, event):
        text = event.message.text
        return text.lower() == "推薦電影"

    def on_enter_movie(self, event):
        mydb=sqlite3.connect("my.db")
        cursor=mydb.cursor()
        cursor.execute("SELECT setence FROM users WHERE role_id = 5")
        Tables=cursor.fetchall()
        print(random.choice(Tables)[0])

        reply_token = event.reply_token
        send_text_message(reply_token, "推薦你看:\n" + random.choice(Tables)[0])

    def is_going_to_shit(self, event):
        text = event.message.text
        return text.lower() == "韓國語錄"

    def on_enter_shit(self, event):
        mydb=sqlite3.connect("my.db")
        cursor=mydb.cursor()
        cursor.execute("SELECT setence FROM users WHERE role_id = 4")
        Tables=cursor.fetchall()
        print(random.choice(Tables)[0])

        reply_token = event.reply_token
        send_text_message(reply_token, "韓國瑜曾說過：\n" + random.choice(Tables)[0] + "\n\n建議你少看點，會變笨啊！")


    def is_going_to_Gan(self, event):
        text = event.message.text
        return text.lower() == "來點梗圖"

    def on_enter_Gan(self, event):
        mydb=sqlite3.connect("my.db")
        cursor=mydb.cursor()
        cursor.execute("SELECT setence FROM users WHERE role_id = 6")
        Tables=cursor.fetchall()
        print(random.choice(Tables)[0])

        reply_token = event.reply_token
        send_image_url(reply_token,random.choice(Tables)[0])

    def is_going_to_tainan(self, event):
        text = event.message.text
        return text.lower() == "台南"

    def on_enter_tainan(self, event):
        mydb=sqlite3.connect("my.db")
        cursor=mydb.cursor()
        cursor.execute("SELECT setence FROM users WHERE role_id = 3")
        Tables=cursor.fetchall()
        print(random.choice(Tables)[0])

        reply_token = event.reply_token
        send_text_message(reply_token, "可以試試:\n" + random.choice(Tables)[0])


    def is_going_to_taipei(self, event):
        text = event.message.text
        return text.lower() == "台北"

    def on_enter_taipei(self, event):
        mydb=sqlite3.connect("my.db")
        cursor=mydb.cursor()
        cursor.execute("SELECT setence FROM users WHERE role_id = 11")
        Tables=cursor.fetchall()
        print(random.choice(Tables)[0])

        reply_token = event.reply_token
        send_text_message(reply_token, "可以試試:\n" + random.choice(Tables)[0])

    def is_going_to_kaohsiung(self, event):
        text = event.message.text
        return text.lower() == "高雄"

    def on_enter_kaohsiung(self, event):
        mydb=sqlite3.connect("my.db")
        cursor=mydb.cursor()
        cursor.execute("SELECT setence FROM users WHERE role_id = 12")
        Tables=cursor.fetchall()
        print(random.choice(Tables)[0])

        reply_token = event.reply_token
        send_text_message(reply_token, "可以試試:\n" + random.choice(Tables)[0])


    def is_going_to_backw(self, event):
        text = event.message.text
        return text.lower() == "再次查詢"

    def on_enter_backw(self, event):
        reply_token = event.reply_token
        send_text_message(reply_token, "選個地區吧:\n\n台北\n\t台南\n\t\t高雄")

    def is_going_to_backd(self, event):
        text = event.message.text
        return text.lower() == "再次查詢"

    def on_enter_backd(self, event):
        reply_token = event.reply_token
        send_text_message(reply_token, "用餐時間多久呢？\n\n快一點、慢慢來")

    def is_going_to_roast(self, event):
        text = event.message.text
        return text.lower() == "火鍋燒烤"

    def on_enter_roast(self, event):
        mydb=sqlite3.connect("my.db")
        cursor=mydb.cursor()
        cursor.execute("SELECT setence FROM users WHERE role_id = 1")
        Tables=cursor.fetchall()
        print(random.choice(Tables)[0])

        reply_token = event.reply_token
        send_text_message(reply_token, "去「 "+ random.choice(Tables)[0] +" 」如何？")

    def is_going_to_boxed(self, event):
        text = event.message.text
        return text.lower() == "便當快餐"

    def on_enter_boxed(self, event):
        mydb=sqlite3.connect("my.db")
        cursor=mydb.cursor()
        cursor.execute("SELECT setence FROM users WHERE role_id = 7")
        Tables=cursor.fetchall()
        print(random.choice(Tables)[0])

        reply_token = event.reply_token
        send_text_message(reply_token, "去「 "+ random.choice(Tables)[0] +" 」如何？")

    def is_going_to_exotic(self, event):
        text = event.message.text
        return text.lower() == "異國風"

    def on_enter_exotic(self, event):
        #print("I'm entering Gan")
        mydb=sqlite3.connect("my.db")
        cursor=mydb.cursor()
        cursor.execute("SELECT setence FROM users WHERE role_id = 9")
        Tables=cursor.fetchall()
        print(random.choice(Tables)[0])

        reply_token = event.reply_token
        send_text_message(reply_token, "去「 "+ random.choice(Tables)[0] +" 」如何？")

    def is_going_to_steak(self, event):
        text = event.message.text
        return text.lower() == "套餐"

    def on_enter_steak(self, event):
        #print("I'm entering Gan")
        mydb=sqlite3.connect("my.db")
        cursor=mydb.cursor()
        cursor.execute("SELECT setence FROM users WHERE role_id = 10")
        Tables=cursor.fetchall()
        print(random.choice(Tables)[0])

        reply_token = event.reply_token
        send_text_message(reply_token, "去「 "+ random.choice(Tables)[0] +" 」如何？")

    def is_going_to_fastfood(self, event):
        text = event.message.text
        return text.lower() == "速食店"

    def on_enter_fastfood(self, event):
        #print("I'm entering Gan")
        mydb=sqlite3.connect("my.db")
        cursor=mydb.cursor()
        cursor.execute("SELECT setence FROM users WHERE role_id = 8")
        Tables=cursor.fetchall()
        print(random.choice(Tables)[0])

        reply_token = event.reply_token
        send_text_message(reply_token, "去「 "+ random.choice(Tables)[0] +" 」如何？")

    def is_going_to_fast(self, event):
        text = event.message.text
        return text.lower() == "快一點"

    def on_enter_fast(self, event):
        #print("I'm entering Gan")
        reply_token = event.reply_token
        send_text_message(reply_token, "想吃什麼種類？\n\n便當快餐、速食店")

    def is_going_to_slow(self, event):
        text = event.message.text
        return text.lower() == "慢慢來"

    def on_enter_slow(self, event):
        #print("I'm entering Gan")
        reply_token = event.reply_token
        send_text_message(reply_token, "想吃什麼種類？\n\n火鍋燒烤、異國風、套餐")

    def on_exit_end(self):
        print("Leaving fastfood")

    def is_going_to_end(self, event):
        text = event.message.text
        return text.lower() == "結束"

    def on_enter_end(self, event):
        #print("I'm entering Gan")
        reply_token = event.reply_token
        send_text_message(reply_token, "我們可以聊！\n例如：\n＊來點冷知識＊＊＊＊＊\n＊＊推薦酒吧＊＊＊＊＊\n＊＊＊晚餐吃啥＊＊＊＊\n＊＊＊＊推薦電影＊＊＊\n＊＊＊＊＊來點梗圖＊＊\n＊＊＊＊＊＊韓國語錄＊")
        self.go_back()