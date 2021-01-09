import json
import vk_api
import random
import requests

from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api import VkUpload

class Query(object):
    HostName = 'unknown'
    Version = 'unknown'
    Players = 'unknown'
    MaxPlayers = 'unknown'

    def __init__(self, host, port):
        response = requests.get(
            f'https://api.mcsrvstat.us/query/{host}:{port}', params={
            'Author': 'Haji'
            },
        )

        answer = response.json()
        self.HostName = answer['HostName']
        self.Version = answer['Version']
        self.Players = answer['Players']
        self.MaxPlayers = answer['MaxPlayers']


vk = vk_api.VkApi(token = '')
api = vk.get_api()
longpoll = VkLongPoll(vk)

print('Бот успешно запущен!')

def sendMessage(user_id, message):
    vk.method('messages.send', {'user_id': user_id, 'message': message, 'random_id': random.randint(100000000,900000000)})

while True:
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            if event.to_me:

                message = event.text;
                args = message.split();

                for check in event.text:
                    if args[0] == '/query' or args[0] == '/srv':
                        if(len(args) <= 2):
                            sendMessage(event.user_id, '# Используйте: /query <ip> <port>')
                            break

                        host = message.split()[1]
                        port = message.split()[2]

                        try:
                            query = Query(host, port)
                        except:
                            sendMessage(event.user_id, '# Сервер недоступен, либо вы ввели неверные данные!')
                            break

                        sendMessage(event.user_id,
                                    f'# Информация о сервере {host}:{port}' +
                                    f'\n' +
                                    f'\nНазвание: {query.HostName}' +
                                    f'\nВерсия: {query.Version}' +
                                    f'\nОнлайн: {query.Players}/{query.MaxPlayers}')
                        break
