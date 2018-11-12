
# -*- coding: utf-8 -*-

from flask import Flask, request, jsonify
import telebot
import requests
import config
import time
from config import URL
import json
from utils import logger as my_lg
from utils import get_file_contetn, send_message, get_feature_names, get_logs

app = Flask(__name__)

app.debug = False


bot = telebot.TeleBot(config.token) #only to set up a webhook


HOST = config.HOST
WEBHOOK_PORT = config.WEBHOOK_PORT
WEBHOOK_LISTEN = config.WEBHOOK_LISTEN
WEBHOOK_SSL_CERT = config.WEBHOOK_SSL_CERT
WEBHOOK_URL_BASE =  config.WEBHOOK_URL_BASE
WEBHOOK_URL_PATH = config.WEBHOOK_URL_PATH



@app.route("/set_webhook")
def set_webhook():
    bot.remove_webhook()
    s=bot.set_webhook(url=WEBHOOK_URL_BASE+WEBHOOK_URL_PATH,
                certificate=open(WEBHOOK_SSL_CERT, 'rb'))
    my_lg(content_type='setting up webhook', chat_id=None, logger_content=s)
    if s:
        return str(s), 200
    return "Webhook was not set properly, use https://{}/check_webhook to check the status".format(HOST)



@app.route("/check_webhook",  methods=['GET', 'POST'])
def check_webhook():
    url = URL + 'getWebhookinfo'
    r = requests.get(url)
    my_lg(content_type='checking_webhook', chat_id=None, logger_content=r.text)
    if r:
        return str(r.text)
    else:
        return "something went wrong"


@app.route(WEBHOOK_URL_PATH,  methods=['POST'])
def webhook():
    if request.method == 'POST':
        r=request.get_json()
        if r:
            if 'document' in r['message']:
                file_id=r['message']['document']['file_id']
                chat_id=r['message']['chat']['id']

                check, get_file_message = get_file_contetn(file_id)
                if check==True:
                    message, file_path=get_feature_names(file_id)
                    send_message(chat_id, text=message)
                    if len(file_path) > 0:
                        my_lg(content_type='sending_a_file', chat_id=chat_id, logger_content='file path > 0  {}'.format(file_path))
                        doc = open(file_path, 'rb')
                        my_lg(content_type='sending_a_file', chat_id=chat_id, logger_content='file opned')
                        bot.send_document(chat_id, doc)
                        my_lg(content_type='sending_a_file', chat_id=None, logger_content='file sent')
                    my_lg(content_type='sending_a_file', chat_id=None, logger_content=message)
                else:
                    send_message(chat_id, text=get_file_message)
                    my_lg(content_type='getting_a_file', chat_id=None, logger_content=get_file_message)

            elif r['message']['text']=='logs' or r['message']['text']=='Logs':
                message=get_logs()
                chat_id=r['message']['chat']['id']
                send_message(chat_id, text=message)

            elif r['message']['text']=='info' or r['message']['text']=='Info' :
                message=get_logs()
                chat_id=r['message']['chat']['id']
                send_message(chat_id, text=config.info)

            else:
                my_lg(content_type='messages_incoming', chat_id=None, logger_content=r)
                chat_id=r['message']['chat']['id']
                message=r['message']['text']
                send_message(chat_id, text='"{}" is not a valid command, type "info" to get more information'.format(message))

        return jsonify(r), 200
    else:
        my_lg(content_type='telegram response', chat_id=None, logger_content=None)
        return 'ok',200


@app.route('/')
def index():
    return '<h1>Hello</h1>'


if __name__ == "__main__":
    app.run(host='0.0.0.0')
