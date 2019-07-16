#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# libs includes
import json
from urllib.parse   import quote
# project includes
from urlHandler     import urlOpener

class bot:
    def __init__(self, botID, allowed_updates=[], callback=None):
        self.botID  = botID
        self.baseURL = 'https://api.telegram.org/bot{}/'.format(botID)
        self.allowed_updates = allowed_updates
        self.callback = callback

    def setCallback(self, callback):
        if callable(callback):
            self.callback = callback

    def sendMessage(self, chatID, text, markdown=False, silent=False, callback=None):
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
        result = urlOpener.getUrlData(url, data=data.encode())

        for cb in (callback, self.callback):
            if cb is not None:
                if callable(cb):
                    cb({'uid':chatID, 'answer':result})
                break
        return result

    def getUpdate(self, offset='0', timeout='60', allowed_updates=[]):
        ''' Get updates with offset and timeout
        '''
        API    = 'getUpdates'
        url    = '{}{}?'.format(self.baseURL, API)
        params = 'offset={}&timeout={}'.format(offset, timeout)

        for allow_up in (allowed_updates, self.allowed_updates):
            if allow_up:
                params += '&allowed_updates={}'.format(json.dumps(allow_up))
                break

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
        ''' Send inline keyboard to user. *args* should be tuple of tuples:
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

    def sendStaticKeyboard(self, chatID, text, args, columns=1, oneTime=False):
        ''' Send static keyboard to user. *args* should be tuple of strings
        '''
        API    = 'sendMessage'
        url    = '{}{}?'.format(self.baseURL, API)
        params = '&chat_id={}'.format(chatID)

        keyboard = []
        row = []
        for a in args:
            row.append(a)
            if columns <= len(row):
                keyboard.append(row)
                row = []
        if 0 < len(row):
            keyboard.append(row)

        data = '{}&text={}&reply_markup={}'\
            .format(params, 
                quote(text), 
                json.dumps({'keyboard' : keyboard, "one_time_keyboard":oneTime}))
        return urlOpener.getUrlData(url, data=data.encode(), name='tg_answer')

    def deleteStaticKeyboard(self, chatID, text):
        ''' Delete static keyboard from user's interface
        '''
        API    = 'sendMessage'
        url    = '{}{}?'.format(self.baseURL, API)
        params = '&chat_id={}'.format(chatID)

        data = '{}&text={}&reply_markup={}'\
            .format(params, quote(text), json.dumps({"remove_keyboard":True}))
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