# -*- coding: utf-8 -*-
import requests
import re
import random
import time
import configparser
from bs4 import BeautifulSoup
from flask import Flask, request, abort
from imgurpython import ImgurClient
import tempfile, os
import sys 
reload(sys)
sys.setdefaultencoding('utf-8')

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

app = Flask(__name__)
config = configparser.ConfigParser()
config.read("config.ini")

line_bot_api = LineBotApi("Jnimxw7SFRpbMAYd+iFvMT9Nhj9CWSlrwPdJXQ4ow9UKUDmVPWnOZFe0EaV4RLTGrg80TtlhBq1xi/vXC3yhpZR3D/rRCdGA+zXLIjAhqrzvgVviQWH+jU85HLBzQILDp0t6O3PCd0x3xdYwaFw9bQdB04t89/1O/w1cDnyilFU=")
handler = WebhookHandler("7d382cd1f4beb217ee608513d76d6014")


@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'ok'


def pattern_mega(text):
    patterns = [
        'mega', 'mg', 'mu', 'ＭＥＧＡ', 'ＭＥ', 'ＭＵ',
        'ｍｅ', 'ｍｕ', 'ｍｅｇａ', 'GD', 'MG', 'google',
    ]
    for pattern in patterns:
        if re.search(pattern, text, re.IGNORECASE):
            return True


    
@handler.add(BeaconEvent)
def handle_beacon(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(
            text='【免費】試玩娃娃機 : https://www.facebook.com/c217UCL/?modal=media_composer&ref=page_homepage_panel'))

@handler.add(MessageEvent, message=(ImageMessage, TextMessage))
def handle_message(event):
        
    if event.message.text == "bang":
        content = "bang"
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content))
        return 0

    buttons_template = TemplateSendMessage(
        alt_text='目錄 template',
        template=ButtonsTemplate(
            title='選擇服務',
            text='請選擇',
            thumbnail_image_url='https://i.imgur.com/VRVap67.jpg',
            actions=[
                MessageTemplateAction(
                    label='開始',
                    text='開始'
                ),
                URITemplateAction(
                    label='FB 粉絲專業',
                    uri='https://www.facebook.com/c217UCL/?modal=media_composer&ref=page_homepage_panel'
                ),
                URITemplateAction(
                    label='高雄第一科技大學 資管系',
                    uri='http://www.mis.nkfust.edu.tw/newMis/home'
                )
            ]
        )
    )
    line_bot_api.reply_message(event.reply_token, buttons_template)


if __name__ == '__main__':
    app.run()
