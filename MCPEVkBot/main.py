import json
import vk_api
import random
import requests

from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api import VkUpload

class Query(object):
    HostName = 'unknown'
    GameType = 'unknown'
    GameName = 'unknown'
    Version = 'unknown'
    Plugins = 'unknown'
    Players = 'unknown'
    MaxPlayers = 'unknown'
    Map = 'unknown'
    HostIp = 'unknown'
    HostPort = 'unknown'
    RawPlugins = 'unknown'
    Software = 'unknown'
    PlayerList = 'unknown'

    def __init__(self, host, port):
        try:
            response = requests.get(
                f'https://api.mcsrvstat.us/query/{host}:{port}', params={
                    'Author': 'Haji'
                },
            )

            answer = response.json()
            self.HostName = answer['HostName']
            self.GameType = answer['GameType']
            self.GameName = answer['GameName']
            self.Version = answer['Version']
            self.Plugins = answer['Plugins']
            self.Players = answer['Players']
            self.MaxPlayers = answer['MaxPlayers']
            self.Map = answer['Map']
            self.HostIp = answer['HostIp']
            self.HostPort = answer['HostPort']
            self.RawPlugins = answer['RawPlugins']
            self.Software = answer['Software']
            self.PlayerList = answer['PlayerList']
        except:
            return 'error'


vk = vk_api.VkApi(token = 'aa46d915d4906efb267f86b1a4a2f68f19a90af174e4eb41c168d2ed7145dc7b1b739aeb39eb0ab62be70')
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