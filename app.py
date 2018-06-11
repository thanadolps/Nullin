from flask import Flask, request
from typing import List
import json
import requests

# ตรง YOURSECRETKEY ต้องนำมาใส่เองครับจะกล่าวถึงในขั้นตอนต่อๆ ไป
global LINE_API_KEY

# True = release, False = debug
if False:
    LINE_API_KEY = 'Bearer e0yXiZe3IMlmFrOyj6WeULHPK0BwuVpaah2Yep+' \
                   'V00JhrU0Ub5HOh3eMt26lbEFjEv5dsqHzcYJ3oLhmNgmt0c' \
                   '30rD/aVFOLkVlFPbrdROB/7DfXbA40n8vlUYvwRvXNYH9dBGSPTBRi7OiQT3ZqDwdB04t89/1O/w1cDnyilFU='
else:
    LINE_API_KEY = 'Bearer NYaSpsiHBFxcAXuoKcq5188Si1ZveFJGjGYur7EKkOAXFOresHY1Qk6xHjJZFzWLCbRE40+3xpj1vrRALewASNv' \
                   'XWDsa+HvBzLvLqbV1YHsZrrm6Qqh1hkj12aJtcHTV7/umxC9H7OzBfDRDtPgQjgdB04t89/1O/w1cDnyilFU='


app = Flask(__name__)

#

bool_flag = {'debug': True}

#


def print_help(args, reply_stack):
    reply_stack.append('TODO: print help')


def toggle_debug(args, reply_stack):
    if bool_flag['debug']:
        reply_stack.append('ปิดโหมดบ่นมาก')
        bool_flag['debug'] = False
    else:
        reply_stack.append('เปิดโหมดบ่นมาก')
        bool_flag['debug'] = True


main_command_redirection = {'debug': toggle_debug, '': print_help}


def process_text(event, reply_stack):

    # strip whitespace and make it lowercase
    text: str = event['message']['text']
    text = text.strip().lower()

    args_and_prefix = text.split(' ')

    # check for prefix
    if args_and_prefix[0] in ["nlb", "nullib", "nulib"]:

        # check for empty command
        if len(args_and_prefix) <= 1:
            command = main_command_redirection.get('')
        else:
            command = main_command_redirection.get(args_and_prefix[1])

        command(args_and_prefix[1:], reply_stack)  # execute command


def execute_command(args, reply_stack):

    if not args:
        reply_stack.append("TODO: print help")
        return

#

@app.route('/')
def index():
    return 'This is chatbot server.'


@app.route('/bot', methods=['POST'])
def bot():

    # ข้อความที่ต้องการส่งกลับ
    replyStack : List[str] = list()
   
    # ข้อความที่ได้รับมา
    msg_in_json = request.get_json()
    msg_in_string = json.dumps(msg_in_json)

    # event ; json list
    for event in msg_in_json["events"]:

        # Token สำหรับตอบกลับ (จำเป็นต้องใช้ในการตอบกลับ)
        replyToken = event['replyToken']
        userID = event['source']['userId']
        msgType = event['message']['type']

        # ทดลอง Echo ข้อความกลับไปในรูปแบบที่ส่งไป-มา (แบบ json)
        if msgType == "text":
            process_text(event, replyStack)

        if bool_flag['debug']:
            replyStack.append(msg_in_string)

        reply(replyToken, replyStack[:5])
    
    return 'OK', 200


def reply(replyToken, textList):
    # Method สำหรับตอบกลับข้อความประเภท text กลับครับ เขียนแบบนี้เลยก็ได้ครับ
    LINE_API = 'https://api.line.me/v2/bot/message/reply'
    headers = {
        'Content-Type': 'application/json; charset=UTF-8',
        'Authorization': LINE_API_KEY
    }
    msgs = []
    for text in textList:
        msgs.append({
            "type":"text",
            "text": text
        })
    data = json.dumps({
        "replyToken": replyToken,
        "messages": msgs
    })
    requests.post(LINE_API, headers=headers, data=data)
    return


if __name__ == '__main__':
    app.run()
