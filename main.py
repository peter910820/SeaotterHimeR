from flask import Flask, abort, render_template, request, redirect, url_for, send_from_directory

from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import *

# import os
import re
import psycopg2

from app.event.hentai_def import *
from app.event.basic_function import *
from app.event.arcaeaGroup_def import *
from app.event.spider_def import *

from app.functions.handle_Time import dateOperation
from app.functions.handle_Database import *

app = Flask(__name__)

line_bot_api = LineBotApi("uwxCr4T8etW4PhFQdvAQk1UcZRi5Yg+x4tiqvmUHHLdio4hZiHh/djgSoLCqYJjGl8tsbTcwRLz6xER1uhofuTPMeqqFRUH9SPEycnJKqNzkjsaF+34gJsw7JBeAkXAXPlDciEOo2s8k3tE84l6ETQdB04t89/1O/w1cDnyilFU=")
handler = WebhookHandler("4e54578529f5d566b759c7c54c8e8ae2")

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
            msg.append(TextSendMessage(text = rows[i][1]))

    #test message:        
    if event.message.text == '$test':
        msg.append(TextSendMessage(text = test_Word()))
    
# /command:
    # /search
    if re.match(r'[$]search', event.message.text,re.IGNORECASE):
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
        db3 = re.sub("\[|\'|\]","",db3)
        msg.append(TextSendMessage(text = db3.replace(', ',"\n")))
    # /insert
    if re.match(r'^[$]insert[-][a-zA-Z0-9_/:.\u4e00-\u9fa5]{1,20}[-][a-zA-Z0-9__/:.\u4e00-\u9fa5]{1,40}$', event.message.text,re.IGNORECASE):
        messageList = event.message.text
        messageList = messageList.split('-')
        messageIN = messageList[1]
        messageOUT = messageList[2]
        timeDate = dateOperation()
        #insert database
        cursor.execute("INSERT INTO Words (Input, Output, Time, Date) VALUES (%s,%s,%s,%s)", (messageIN,messageOUT,timeDate[0],timeDate[1]))
        database.commit()
        msg.append(TextSendMessage(text=f'輸入出組合: {messageIN}-{messageOUT} 已成功設置'))
    # /delete
    if re.match(r'^[$]delete[-][a-zA-Z0-9__/:.\u4e00-\u9fa5]{1,20}$', event.message.text,re.IGNORECASE):
        messageList = event.message.text
        messageList = messageList.split('-')
        messageDEL = messageList[1]
        cursor.execute("SELECT ID, Input, Output, Time, Date from Words")
        rows = cursor.fetchall()
        for i in range(len(rows)):
            if messageDEL == rows[i][1]:
                y = rows[i][0]
                cursor.execute("DELETE from Words where ID=(%s)",(y,))
                database.commit()
        msg.append(TextSendMessage(text=f'{messageDEL} 已成功刪除'))
    #Google功能
    if re.match(r'^[$][g][o][o][g][l][e][-][a-zA-Z0-9__/:.\u4e00-\u9fa5]{1,20}$', event.message.text,re.IGNORECASE):
        msg.append(TextSendMessage(text = google_Search(event.message.text)))
#arcaea群組會用到的功能(((===============================================================
    if "查" in  event.message.text:
        msg.append(TextSendMessage(text = score_Search()))
    if "vc" in event.message.text or "VC" in event.message.text or "Vc" in event.message.text:
        msg.append(TextSendMessage(text = snowth("VC")))
    if "天堂門" in event.message.text:
        msg.append(TextSendMessage(text = snowth("天堂門")))
#群組會用到的功能(((=====================================================================
    if "運勢" in event.message.text:
        msg.append(TextSendMessage(text = fortunate()))
    if re.match(r'^[n][0-9]{1,6}$', event.message.text,re.IGNORECASE):
        msg.append(TextSendMessage(text = nhentai_Search(event.message.text)))
    if re.match(r'^[w][0-9]{1,5}$', event.message.text,re.IGNORECASE):
        msg.append(TextSendMessage(text = wancg_Search(event.message.text)))
        
    line_bot_api.reply_message(event.reply_token, messages=msg[:5])
    cursor.close()   #關閉游標
    database.close() #關閉DB


# 網頁端 #
# @app.route('/', methods=['GET'])
# def root(request: Request, response: Response):
#     response = templates.TemplateResponse('login.html',{'request':request})
#     response.delete_cookie("c_user")
#     return render_template('hello.html')
#     return response

# @app.get("/introduce", response_class=HTMLResponse) 
# async def introduce(request: Request, c_user: str = Cookie(None)):
#     if c_user:
#         return templates.TemplateResponse("introduce.html", {"request": request,"cookie" :c_user})
#     return RedirectResponse("/")
    
# @app.post("/insert_Complete", response_class=HTMLResponse) 
# async def insert(request: Request, Input:str=Form(None), Output:str=Form(None)):
#     web_insert_database(Input,Output)
#     return templates.TemplateResponse("insert_Complete.html", {"request": request})

# @app.get("/database", response_class=HTMLResponse) 
# async def database(request: Request, c_user: str = Cookie(None)):
#     show_data = show_database()
#     if c_user:
#         return templates.TemplateResponse("database.html", {"request": request, "data" : show_data  ,"cookie" :c_user})
#     return RedirectResponse("/")
# #註冊#
# @app.get("/register", response_class=HTMLResponse)
# async def register(request: Request):
#     return templates.TemplateResponse("register.html", {"request": request})
# #註冊狀態#
# @app.post("/register/judge")
# async def register_show(request: Request, account:str=Form(None), 
#                         password:str=Form(None), passwordCheck:str=Form(None),checkPwd:str=Form(None)):
#     reminderMessage = register_judge(account, password, passwordCheck, checkPwd)
#     return templates.TemplateResponse("register_Show.html", {"request": request, "reminderMessage": reminderMessage})
        
# #登入#
# @app.post('/home')
# async def get_user(request:Request, response: Response, account:str=Form(None), password:str=Form(None)):
#     reminderMessage = check_login(account,password)
#     if reminderMessage == "pass":
#         response = templates.TemplateResponse('home.html',{'request':request,'account':account})
#         response.set_cookie(key="c_user", value=account)
#         return response
#     else:
#         return templates.TemplateResponse('submit_Fail.html',{'request':request, 'reminderMessage':reminderMessage})
# @app.get('/home/change_password', response_class=HTMLResponse)
# async def change_password(request:Request, response: Response, c_user: str = Cookie(None)):
#     if c_user:
#         return templates.TemplateResponse("change_Password.html", {"request": request,"cookie" : c_user})
#     return RedirectResponse("/")

# @app.post('/home/change_password/judge', response_class=HTMLResponse)
# async def change_password(request:Request, c_user: str = Cookie(None),
#                         old_password:str=Form(None), new_password:str=Form(None), new_password_check:str=Form(None)):
#     if c_user:
#         state = change_password_database(c_user, old_password, new_password, new_password_check)
#         if state != None:
#             return templates.TemplateResponse('change_pwd_fail.html',{'request':request, 'state':state, "cookie" : c_user})
#         else:
#             return templates.TemplateResponse('change_pwd_success.html',{'request':request, "cookie" : c_user})

# @app.get("/items/{id}", response_class=HTMLResponse)
# async def read_item(request: Request, id: str):
#     return templates.TemplateResponse("item.html", {"request": request, "id": id})

if __name__ == '__main__':
   app.run()