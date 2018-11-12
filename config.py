# -*- coding: utf-8 -*-

#some parametrs may be changed depending on your settings

# Changable settings 

token='709805067:AAHfT29gaqOhf3RB5Dl3aKUaGHx8xp5UfBo' # your telegram bot token
dir_path='/home/donkey/flask_bot/' #path to flask project 
json_file_path=dir_path+'file.json' #name of the file, should not be changed unless it interfers with other file names
WEBHOOK_SSL_CERT = '/etc/ssl/server.crt' # path to ssl sertificate
HOST = '104.248.35.29' # your ip address

# Permanent settings settings 

URL='https://api.telegram.org/bot{}/'.format(token)
WEBHOOK_PORT = 443
WEBHOOK_LISTEN = '0.0.0.0'  
WEBHOOK_URL_BASE = "https://{}:{}".format(HOST, WEBHOOK_PORT)
WEBHOOK_URL_PATH = "/{}".format('web_hook')

info='-> to get your json file descirption drag and drop files here or upload \n-> to see last logs type "logs" \n-> to see webhook status follow "https://{}/check_webhook" \n-> to reset the webhook follow "https://{}/set_webhook" \n-> github: https://github.com/diff7/flask_telegram_bot_geojson'.format(HOST, HOST)