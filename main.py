from flask import Flask, abort, render_template, redirect, url_for, make_response, request

from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.messaging import (
    Configuration, ApiClient, MessagingApi,
    ReplyMessageRequest, TextMessage
)

from linebot.v3.webhooks import MessageEvent, TextMessageContent

import os
import re
import psycopg2
from dotenv import load_dotenv
from loguru import logger

from app.event.basic import Basic
from app.event.crawler import Crawler
from app.event.arcaea_group import ArcaeaGroup

from app.functions.handle_Time import dateOperation
from app.functions.handle_Database import *

load_dotenv()

app = Flask(__name__)
configuration = Configuration(access_token=os.getenv("CHANNEL_ACCESS_TOKEN"))
handler = WebhookHandler(os.getenv("CHANNEL_SECRET"))


@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        app.logger.info(
            "Invalid signature. Please check your channel access token/channel secret.")
        abort(400)
    return 'OK'


@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        msg = event.message.text
        msg = msg.encode('utf-8')
        msg = []

        try:
            #     DATABASE_URL = 'postgres://seaotter:Ersl2kH5sG2IOiEzrFQLsh4kI5NDcyTi@dpg-ce7jktarrk049r63khs0-a.oregon-postgres.render.com/seaotterhimedb'
            #     database = psycopg2.connect(DATABASE_URL, sslmode='require')
            #     cursor = database.cursor()
            #     logger.success('Database is Connect ok!')
            #     cursor.execute("SELECT Input, Output from Words")
            #     rows = cursor.fetchall()
            #     for i in range(len(rows)):
            #         if event.message.text == rows[i][0]:
            #             msg.append(TextSendMessage(text=rows[i][1]))

            # # /command:
            #     # /search
            #     if re.match(r'[$]search', event.message.text, re.IGNORECASE):
            #         cursor.execute("SELECT Input, Output from Words")
            #         rows = cursor.fetchall()
            #         db1 = []
            #         db2 = []
            #         db3 = []
            #         for row in rows:
            #             db1.append(row[0])
            #             db2.append(row[1])
            #         for i in range(len(db1)):
            #             db3.append(f"{str(db1[i])} ---> {str(db2[i])}")
            #         db3 = str(db3)
            #         db3 = re.sub("\[|\'|\]", "", db3)
            #         msg.append(TextSendMessage(text=db3.replace(', ', "\n")))
            #     # /insert
            #     if re.match(r'^[$]insert[-][a-zA-Z0-9_/:.\u4e00-\u9fa5]{1,20}[-][a-zA-Z0-9__/:.\u4e00-\u9fa5]{1,40}$', event.message.text, re.IGNORECASE):
            #         messageList = event.message.text
            #         messageList = messageList.split('-')
            #         messageIN = messageList[1]
            #         messageOUT = messageList[2]
            #         timeDate = dateOperation()
            #         # insert database
            #         cursor.execute("INSERT INTO Words (Input, Output, Time, Date) VALUES (%s,%s,%s,%s)",
            #                        (messageIN, messageOUT, timeDate[0], timeDate[1]))
            #         database.commit()
            #         msg.append(TextSendMessage(
            #             text=f'輸入出組合: {messageIN}-{messageOUT} 已成功設置'))
            #     # /delete
            #     if re.match(r'^[$]delete[-][a-zA-Z0-9__/:.\u4e00-\u9fa5]{1,20}$', event.message.text, re.IGNORECASE):
            #         messageList = event.message.text
            #         messageList = messageList.split('-')
            #         messageDEL = messageList[1]
            #         cursor.execute("SELECT ID, Input, Output, Time, Date from Words")
            #         rows = cursor.fetchall()
            #         for i in range(len(rows)):
            #             if messageDEL == rows[i][1]:
            #                 y = rows[i][0]
            #                 cursor.execute("DELETE from Words where ID=(%s)", (y,))
            #                 database.commit()
            #         msg.append(TextSendMessage(text=f'{messageDEL} 已成功刪除'))

            # test message:
            if event.message.text == '$test':
                msg.append(TextMessage(text="測試webhook成功"))  # type: ignore

            # google feature
            if re.match(r'^[$][g][o][o][g][l][e][-][a-zA-Z0-9__/:.\u4e00-\u9fa5]{1,20}$', event.message.text, re.IGNORECASE):
                crawler = Crawler()
                msg.append(TextMessage(
                    text=crawler.google_search(event.message.text)))  # type: ignore

            # arcaea group feature
            if "查" in event.message.text:
                arcara_group = ArcaeaGroup()
                msg.append(TextMessage(
                    text=arcara_group.score_search()))  # type: ignore
            if "vc" in event.message.text.lower():
                arcara_group = ArcaeaGroup()
                msg.append(TextMessage(
                    text=arcara_group.snowth("VC")))  # type: ignore
            if "天堂門" in event.message.text:
                arcara_group = ArcaeaGroup()
                msg.append(TextMessage(
                    text=arcara_group.snowth("天堂門")))  # type: ignore

            # basic feature
            if "運勢" in event.message.text:
                basic = Basic()
                msg.append(TextMessage(text=basic.fortunate()))  # type: ignore
            if re.match(r'^[n][0-9]{1,6}$', event.message.text, re.IGNORECASE):
                crawler = Crawler()
                msg.append(TextMessage(
                    text=crawler.nhentai_search(event.message.text)))  # type: ignore
            if re.match(r'^[w][0-9]{1,5}$', event.message.text, re.IGNORECASE):
                crawler = Crawler()
                msg.append(TextMessage(
                    text=crawler.wancg_search(event.message.text)))  # type: ignore

            if msg != []:
                line_bot_api.reply_message_with_http_info(
                    ReplyMessageRequest(
                        replyToken=event.reply_token,
                        messages=msg[:5],
                        notificationDisabled=True
                    )
                )
            else:  # 沒有符合的回應
                pass

            # cursor.close()  # close cursor
            # database.close()  # close db

        except Exception as e:
            logger.error(e)


# 網頁端 #
@app.route('/', methods=['GET'])
def root():
    template = render_template('login.html')
    response = make_response(template)
    response.delete_cookie('c_user')
    return response


@app.route("/introduce", methods=['GET'])
def introduce():
    c_user = request.cookies.get('c_user')
    if c_user:
        return render_template("introduce.html", cookie=c_user)
    return redirect(url_for('root'))


@app.route("/insert_Complete", methods=['POST'])
def insert():
    web_insert_database(request.form['Input'], request.form['Output'])
    return render_template("insert_Complete.html")


@app.route("/database", methods=['GET'])
def database():
    c_user = request.cookies.get('c_user')
    show_data = show_database()
    if c_user:
        return render_template("database.html", data=show_data, cookie=c_user)
    return redirect(url_for('root'))

# 註冊


@app.route("/register", methods=['GET'])
def register():
    return render_template('register.html')
# 註冊狀態


@app.route("/register/judge", methods=['POST'])
def register_show():
    reminderMessage = register_judge(str(request.form["account"]), str(
        request.form["password"]), str(request.form["passwordCheck"]), str(request.form["checkPwd"]))
    return render_template("register_Show.html", reminderMessage=reminderMessage)

# 登入


@app.route('/home', methods=['POST'])
def get_user():
    if str(request.form["account"]).strip() == '' or str(request.form["password"]).strip() == '':
        reminderMessage = check_login(None, None)
    else:
        reminderMessage = check_login(
            str(request.form["account"]), str(request.form["password"]))
    if reminderMessage == "pass":
        template = render_template(
            'home.html', account=request.form["account"])
        response = make_response(template)
        response.set_cookie(key="c_user", value=str(request.form["account"]))
        return response
    else:
        return render_template('submit_Fail.html', reminderMessage=reminderMessage)


@app.route('/home/change_password', methods=['GET'])
def change_password():
    c_user = request.cookies.get('c_user')
    if c_user:
        return render_template("change_Password.html", cookie=c_user)
    return redirect(url_for('root'))


@app.route('/home/change_password/judge', methods=['POST'])
def change_passwordJudge():
    c_user = request.cookies.get('c_user')
    old_password = request.form['old_password']
    new_password = request.form['new_password']
    new_password_check = request.form['new_password_check']
    if c_user:
        state = change_password_database(
            c_user, old_password, new_password, new_password_check)
        if state != None:
            return render_template('change_pwd_fail.html', state=state, cookie=c_user)
        else:
            return render_template('change_pwd_success.html', cookie=c_user)
    return render_template('login.html')

# @app.route("/items/{id}", methods=['GET'])
# def read_item(id: str):
#     return render_template("item.html", id = id)


if __name__ == '__main__':
    app.run(port=os.getenv("PORT"))  # type: ignore
