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
        #print("I'm entering dinner")
        mydb=sqlite3.connect("my.db")
        cursor=mydb.cursor()
        cursor.execute("SELECT setence FROM users WHERE role_id = 1")
        Tables=cursor.fetchall()
        print(random.choice(Tables)[0])

        reply_token = event.reply_token
        send_text_message(reply_token, "去"+ random.choice(Tables)[0] +"如何？")
        self.go_back()

    def on_exit_dinner(self):
        print("Leaving dinner")

    def on_enter_trivia(self, event):
        #print("I'm entering trivia")
        mydb=sqlite3.connect("my.db")
        cursor=mydb.cursor()
        cursor.execute("SELECT setence FROM users WHERE role_id = 2")
        Tables=cursor.fetchall()
        print(random.choice(Tables)[0])

        reply_token = event.reply_token
        send_text_message(reply_token, "你知道嗎：\n" + random.choice(Tables)[0])
        self.go_back()

    def on_exit_trivia(self):
        print("Leaving trivia")
    
    def is_going_to_wine(self, event):
        text = event.message.text
        return text.lower() == "去哪喝酒"

    def on_enter_wine(self, event):
        #print("I'm entering wine")
        mydb=sqlite3.connect("my.db")
        cursor=mydb.cursor()
        cursor.execute("SELECT setence FROM users WHERE role_id = 3")
        Tables=cursor.fetchall()
        print(random.choice(Tables)[0])

        reply_token = event.reply_token
        send_text_message(reply_token, "可以試試:\n" + random.choice(Tables)[0])
        self.go_back()

    def on_exit_wine(self):
        print("Leaving wine")

    def is_going_to_movie(self, event):
        text = event.message.text
        return text.lower() == "推薦電影"

    def on_enter_movie(self, event):
        #print("I'm entering movie")
        mydb=sqlite3.connect("my.db")
        cursor=mydb.cursor()
        cursor.execute("SELECT setence FROM users WHERE role_id = 5")
        Tables=cursor.fetchall()
        print(random.choice(Tables)[0])

        reply_token = event.reply_token
        send_text_message(reply_token, "推薦你看:\n" + random.choice(Tables)[0])
        self.go_back()

    def on_exit_movie(self):
        print("Leaving movie")

    def is_going_to_shit(self, event):
        text = event.message.text
        return text.lower() == "韓國語錄"

    def on_enter_shit(self, event):
        #print("I'm entering shit")
        mydb=sqlite3.connect("my.db")
        cursor=mydb.cursor()
        cursor.execute("SELECT setence FROM users WHERE role_id = 4")
        Tables=cursor.fetchall()
        print(random.choice(Tables)[0])

        reply_token = event.reply_token
        send_text_message(reply_token, "韓國瑜曾說過：\n" + random.choice(Tables)[0] + "\n\n建議你少看點，會變笨啊！")
        self.go_back()

    def on_exit_Gan(self):
        print("Leaving Gan")

    def is_going_to_Gan(self, event):
        text = event.message.text
        return text.lower() == "來點梗圖"

    def on_enter_Gan(self, event):
        #print("I'm entering Gan")
        mydb=sqlite3.connect("my.db")
        cursor=mydb.cursor()
        cursor.execute("SELECT setence FROM users WHERE role_id = 6")
        Tables=cursor.fetchall()
        print(random.choice(Tables)[0])

        reply_token = event.reply_token
        send_image_url(reply_token,random.choice(Tables)[0])
        self.go_back()

