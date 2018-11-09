
import datetime
import config
from config import URL
import requests
import json
import collections

def logger(content_type, chat_id=None, logger_content=None):
    with open('{}logs.log'.format(config.dir_path), 'a') as f:
            f.write("{}, CONTENT_TYPE: {}, chat_id: {}, INFO: {}\n".format(datetime.datetime.now(), content_type, chat_id, logger_content ))


def get_file_contetn(file_id):
    url='https://api.telegram.org/bot{}/getFile?file_id={}'.format(config.token, file_id)
    r=requests.post(url)
    print('ok')
    if r:
        result=r.json()['result']
        if 'file_path' in result:
            file_path = result['file_path']

            file_url='https://api.telegram.org/file/bot{}/{}'.format(config.token, file_path)
            
            try:
                data=requests.get(file_url).json()
                logger('getting json out of the file', chat_id=None,logger_content='converted to json succesfully')
                with open(config.json_file_path, 'w') as outfile:
                    json.dump(data, outfile)
                return True, 'File saved and ready to be processed'

            except:
                return False, 'Not a json file or wrong format'
           

    else: 
        logger('get_file_content', chat_id=None,logger_content='could not get the file from telegram')
        return False, "Error, probably wrong file ID recieved or your file is too big, try to upload your file again. Note, files should be less than 20 mb"


def send_message(chat_id, text='hello'):
    url = URL + 'sendMessage'
    answer = {'chat_id':chat_id, 'text':text}
    logger(content_type='messages_outcoming', chat_id=None, logger_content=answer)
    r = requests.post(url, json=answer)



def get_feature_names(json_file_path=config.json_file_path):
    with open(json_file_path) as json_data:
        try:
            json_file = json.load(json_data)
        except: 
            return 'Could not read json file'
    c = collections.Counter()
    if 'features' in json_file:
        for item in json_file['features']:
            c[item['geometry']['type']]+=1
            result = '\n '.join([item+' : '+str(c[item]) for item in list(c)])
        if len(result) > 0:
            return result
        else: return 'File does not contain features'
    else: 
        return 'File does not contain field "features"'


#not the best way, need to change it later
def get_logs(log_file_path='{}logs.log'.format(config.dir_path), n=5):
    with open(log_file_path) as f:
        data = f.readlines()
    lastline = data[-1]
    tail = data[-n:]
    return ''.join(['->> '+x for x in tail])