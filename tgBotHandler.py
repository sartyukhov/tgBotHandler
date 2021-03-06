import json
import requests

from urllib.parse import quote


class Bot:
    def __init__(self, botID, allowed_updates=[], callback=None):
        self.baseURL = f"https://api.telegram.org/bot{botID}/"
        self.allowed_updates = allowed_updates

    def sendMessage(self, chatID, text, markdown=False, silent=False,
                    callback=None):
        """
        Send simple text message (with Markdown support)
            chatID - telegram user id
            text - message
            markdown - text with markdown inserts
            silent - send with norification or not
            callback - function to call after all
        """

        url = f"{self.baseURL}sendMessage"

        params = {
            "chat_id": chatID,
            "parse_mode": markdown,
            "disable_notification": silent,
            "text": text
        }

        response = requests.get(url, params=params)
        return response

    def getUpdate(self, offset=0, timeout=60, allowed_updates=[]):
        """ Get updates with offset and timeout
        """
        url = f"{self.baseURL}getUpdates"

        params = {
            "offset": offset,
            "timeout": timeout
        }

        for allow_up in (allowed_updates, self.allowed_updates):
            if allow_up:
                params["&allowed_updates"] = json.dumps(allow_up)
                break

        response = requests.get(url, params=params)
        return response

    # def sendInKeyboard(self, chatID, text, args, columns=1, addCancel=True):
    #     """ Send inline keyboard to user. *args* should be tuple of tuples:
    #                     [0] : text
    #                     [1] : callback_data
    #     """
    #     API    = 'sendMessage'
    #     url    = '{}{}?'.format(self.baseURL, API)
    #     params = '&chat_id={}'.format(chatID)

    #     keyboard = []
    #     row = []
    #     for a in args:
    #         row.append({'text':a[0], 'callback_data':a[1]})
    #         if columns <= len(row):
    #             keyboard.append(row)
    #             row = []
    #     if 0 < len(row):
    #         keyboard.append(row)

    #     if addCancel:
    #         keyboard.append([{'text':'Отмена', 'callback_data':'@cancel@'}])

    #     data = '{}&text={}&reply_markup={}'\
    #         .format(params, quote(text), json.dumps({'inline_keyboard' : keyboard}))
    #     return urlOpener.getUrlData(url, data=data.encode(), name='tg_answer')

    # def sendStaticKeyboard(self, chatID, text, args, columns=1, oneTime=False):
    #     """ Send static keyboard to user. *args* should be tuple of strings
    #     """
    #     API    = 'sendMessage'
    #     url    = '{}{}?'.format(self.baseURL, API)
    #     params = '&chat_id={}'.format(chatID)

    #     keyboard = []
    #     row = []
    #     for a in args:
    #         row.append(a)
    #         if columns <= len(row):
    #             keyboard.append(row)
    #             row = []
    #     if 0 < len(row):
    #         keyboard.append(row)

    #     data = '{}&text={}&reply_markup={}'.format(
    #         params,
    #         quote(text),
    #         json.dumps({'keyboard': keyboard, "one_time_keyboard": oneTime})
    #     )
    #     return urlOpener.getUrlData(url, data=data.encode(), name='tg_answer')

    # def deleteStaticKeyboard(self, chatID, text):
    #     """ Delete static keyboard from user's interface
    #     """
    #     API = 'sendMessage'
    #     url = '{}{}?'.format(self.baseURL, API)
    #     params = '&chat_id={}'.format(chatID)

    #     data = '{}&text={}&reply_markup={}'\
    #         .format(params, quote(text), json.dumps({"remove_keyboard":True}))
    #     return urlOpener.getUrlData(url, data=data.encode(), name='tg_answer')

    # def deleteMessage(self, chatID, messageID):
    #     """ Delete message
    #     """
    #     API = 'deleteMessage'
    #     url = '{}{}?'.format(self.baseURL, API)
    #     params = '&chat_id={}&message_id={}'.format(chatID, messageID)
    #     return urlOpener.getUrlData(url, data=params.encode(), name='tg_answer')
