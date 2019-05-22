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

    def sendMessage(self, chatID, text, markdown=False, silent=False):
        ''' Send simple text message (with Markdown support)
        '''
        params = ''
        if markdown:
            params += '&parse_mode=Markdown'
        if silent:
            params += '&disable_notification=True'

        url = 'https://api.telegram.org/bot{b}/sendMessage?chat_id={c}{p}&text={t}'\
            .format(b=self.botID, c=chatID, p=params, t=quote(text))
        return urlOpener.getUrlData(url)

    def getUpdate(self, offset='0', timeout='60'):
        ''' Get updates with offset and timeout
        '''
        url = 'https://api.telegram.org/bot{b}/getUpdates?offset={o}&timeout={t}'\
            .format(b=self.botID, t=timeout, o=offset)
        if timeout == '0' or timeout == 0 or timeout is None:
            return urlOpener.getUrlData(url, name='tg_answer')
        else:
            return urlOpener.getUrlData(url, name='tg_answer', timeout=(int(timeout) * 2))

    def sendInKeyboard(self, chatID, text, args, addCancel=True):
        ''' Send keyboard to user. *args* should be tuple of tuples:
                        [0] : text
                        [1] : callback_data
        '''
        url = 'https://api.telegram.org/bot{b}/sendMessage?chat_id={c}&text={t}&reply_markup='\
            .format(b=self.botID, c=chatID, t=quote(text))
        mass = []
        for a in args:
            mass.append([{'text':a[0], 'callback_data':a[1]}])

        if addCancel:
            mass.append([{'text':'Отмена', 'callback_data':'%cancel%'}])

        d = {'inline_keyboard' : mass}
        url += json.dumps(d)
        return urlOpener.getUrlData(url, name='tg_answer')

    def deleteMessage(self, chatID, messageID):
        ''' Delete message
        '''
        url = 'https://api.telegram.org/bot{b}/deleteMessage?chat_id={c}&message_id={m}'\
            .format(b=self.botID, c=chatID, m=messageID)
        return urlOpener.getUrlData(url, name='tg_answer')


if __name__ == "__main__":
    pass