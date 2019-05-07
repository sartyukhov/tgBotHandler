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

    def sendMessage(self, chatID, text):
        '''
        @ description | Send simple text message (with Markdown support)
        '''
        url = 'https://api.telegram.org/bot{b}/sendMessage?chat_id={c}&text={t}&parse_mode=Markdown'\
            .format(b=self.botID, c=chatID, t=quote(text))
        return urlOpener.getUrlData(url)

    def getUpdate(self, offset='0', timeout='60'):
        '''
        @ description | Get updates with offset and timeout
        '''
        url = 'https://api.telegram.org/bot{b}/getUpdates?offset={o}&timeout={t}'\
            .format(b=self.botID, t=timeout, o=offset)
        return urlOpener.getUrlData(url, name='tg_answer')

    def sendInKeyboard(self, chatID, text, args):
        '''
        @ description | Send keyboard to user. *args* should be tuple of tuples:
                        [0] : text
                        [1] : callback_data
        '''
        url = 'https://api.telegram.org/bot{b}/sendMessage?chat_id={c}&text={t}&reply_markup='\
            .format(b=self.botID, c=chatID, t=quote(text))
        mass = []
        for a in args:
            mass.append([{'text':a[0], 'callback_data':a[1]}])

        d = {'inline_keyboard' : mass}
        url += json.dumps(d)
        return urlOpener.getUrlData(url, name='tg_answer')

if __name__ == "__main__":
    pass