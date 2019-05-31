#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# libs includes
import json
from urllib.parse   import quote
# project includes
from urlHandler     import urlOpener

class bot:
    def __init__(self, botID):
        self.botID  = botID
        self.baseURL = 'https://api.telegram.org/bot{}/'.format(botID)

    def sendMessage(self, chatID, text, markdown=False, silent=False):
        ''' Send simple text message (with Markdown support)
        '''
        API    = 'sendMessage'
        url    = '{}{}?'.format(self.baseURL, API)
        params = '&chat_id={}'.format(chatID)

        if markdown:
            params += '&parse_mode=Markdown'
        if silent:
            params += '&disable_notification=True'

        data = '{}&text={}'.format(params, quote(text))
        return urlOpener.getUrlData(url, data=data.encode())

    def getUpdate(self, offset='0', timeout='60'):
        ''' Get updates with offset and timeout
        '''
        API    = 'getUpdates'
        url    = '{}{}?'.format(self.baseURL, API)
        params = 'offset={}&timeout={}'.format(offset, timeout)

        if timeout == '0' or timeout == 0 or timeout is None:
            return urlOpener.getUrlData(url,\
                data=params.encode(),\
                name='tg_answer')
        else:
            return urlOpener.getUrlData(url,\
                data=params.encode(),\
                name='tg_answer',\
                timeout=(int(timeout) * 2))

    def sendInKeyboard(self, chatID, text, args, columns=1, addCancel=True):
        ''' Send keyboard to user. *args* should be tuple of tuples:
                        [0] : text
                        [1] : callback_data
        '''
        API    = 'sendMessage'
        url    = '{}{}?'.format(self.baseURL, API)
        params = '&chat_id={}'.format(chatID)

        keyboard = []
        row = []
        for a in args:
            row.append({'text':a[0], 'callback_data':a[1]})
            if columns <= len(row):
                keyboard.append(row)
                row = []
        if 0 < len(row):
            keyboard.append(row)

        if addCancel:
            keyboard.append([{'text':'Отмена', 'callback_data':'@cancel@'}])

        data = '{}&text={}&reply_markup={}'\
            .format(params, quote(text), json.dumps({'inline_keyboard' : keyboard}))
        return urlOpener.getUrlData(url, data=data.encode(), name='tg_answer')

    def deleteMessage(self, chatID, messageID):
        ''' Delete message
        '''
        API    = 'deleteMessage'
        url    = '{}{}?'.format(self.baseURL, API)
        params = '&chat_id={}&message_id={}'.format(chatID, messageID)
        return urlOpener.getUrlData(url, data=params.encode(), name='tg_answer')

if __name__ == "__main__":
    pass