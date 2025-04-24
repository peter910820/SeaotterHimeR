from flask import Flask, abort, render_template, redirect, url_for, make_response, request

from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import *

import os
import re
import psycopg2
from dotenv import load_dotenv

from app.event.hentai_def import *
from app.event.basic_function import *
from app.event.arcaeaGroup_def import *
from app.event.spider_def import *

from app.functions.handle_Time import dateOperation
from app.functions.handle_Database import *

app = Flask(__name__)

load_dotenv()

line_bot_api = LineBotApi(os.getenv("CHANNEL_ACCESS_TOKEN"))
handler = WebhookHandler(os.getenv("4e54578529f5d566b759c7c54c8e8ae2"))


@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text
    msg = msg.encode('utf-8')
    msg = []

    DATABASE_URL = 'postgres://seaotter:Ersl2kH5sG2IOiEzrFQLsh4kI5NDcyTi@dpg-ce7jktarrk049r63khs0-a.oregon-postgres.render.com/seaotterhimedb'
    database = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = database.cursor()
    print('Database is Connect ok!')
    msg = event.message.text
    msg = msg.encode('utf-8')
    msg = []
    cursor.execute("SELECT Input, Output from Words")
    rows = cursor.fetchall()
    for i in range(len(rows)):
        if event.message.text == rows[i][0]:
            msg.append(TextSendMessage(text=rows[i][1]))

    # test message:
    if event.message.text == '$test':
        msg.append(TextSendMessage(text=test_Word()))

# /command:
    # /search
    if re.match(r'[$]search', event.message.text, re.IGNORECASE):
        cursor.execute("SELECT Input, Output from Words")
        rows = cursor.fetchall()
        db1 = []
        db2 = []
        db3 = []
        for row in rows:
            db1.append(row[0])
            db2.append(row[1])
        for i in range(len(db1)):
            db3.append(f"{str(db1[i])} ---> {str(db2[i])}")
        db3 = str(db3)
        db3 = re.sub("\[|\'|\]", "", db3)
        msg.append(TextSendMessage(text=db3.replace(', ', "\n")))
    # /insert
    if re.match(r'^[$]insert[-][a-zA-Z0-9_/:.\u4e00-\u9fa5]{1,20}[-][a-zA-Z0-9__/:.\u4e00-\u9fa5]{1,40}$', event.message.text, re.IGNORECASE):
        messageList = event.message.text
        messageList = messageList.split('-')
        messageIN = messageList[1]
        messageOUT = messageList[2]
        timeDate = dateOperation()
        # insert database
        cursor.execute("INSERT INTO Words (Input, Output, Time, Date) VALUES (%s,%s,%s,%s)",
                       (messageIN, messageOUT, timeDate[0], timeDate[1]))
        database.commit()
        msg.append(TextSendMessage(
            text=f'輸入出組合: {messageIN}-{messageOUT} 已成功設置'))
    # /delete
    if re.match(r'^[$]delete[-][a-zA-Z0-9__/:.\u4e00-\u9fa5]{1,20}$', event.message.text, re.IGNORECASE):
        messageList = event.message.text
        messageList = messageList.split('-')
        messageDEL = messageList[1]
        cursor.execute("SELECT ID, Input, Output, Time, Date from Words")
        rows = cursor.fetchall()
        for i in range(len(rows)):
            if messageDEL == rows[i][1]:
                y = rows[i][0]
                cursor.execute("DELETE from Words where ID=(%s)", (y,))
                database.commit()
        msg.append(TextSendMessage(text=f'{messageDEL} 已成功刪除'))
    # Google功能
    if re.match(r'^[$][g][o][o][g][l][e][-][a-zA-Z0-9__/:.\u4e00-\u9fa5]{1,20}$', event.message.text, re.IGNORECASE):
        msg.append(TextSendMessage(text=google_Search(event.message.text)))
# arcaea群組會用到的功能(((===============================================================
    if "查" in event.message.text:
        msg.append(TextSendMessage(text=score_Search()))
    if "vc" in event.message.text or "VC" in event.message.text or "Vc" in event.message.text:
        msg.append(TextSendMessage(text=snowth("VC")))
    if "天堂門" in event.message.text:
        msg.append(TextSendMessage(text=snowth("天堂門")))
# 群組會用到的功能(((=====================================================================
    if "運勢" in event.message.text:
        msg.append(TextSendMessage(text=fortunate()))
    if re.match(r'^[n][0-9]{1,6}$', event.message.text, re.IGNORECASE):
        msg.append(TextSendMessage(text=nhentai_Search(event.message.text)))
    if re.match(r'^[w][0-9]{1,5}$', event.message.text, re.IGNORECASE):
        msg.append(TextSendMessage(text=wancg_Search(event.message.text)))

    line_bot_api.reply_message(event.reply_token, messages=msg[:5])
    cursor.close()  # 關閉游標
    database.close()  # 關閉DB


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

# @app.route("/items/{id}", methods=['GET'])
# def read_item(id: str):
#     return render_template("item.html", id = id)


if __name__ == '__main__':
    app.run()
