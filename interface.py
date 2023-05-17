import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id

from config import comunity_token, acces_token
from core import VkTools
from data_store import Viewed




class BotInterface():

    def __init__(self, comunity_token, acces_token):
        self.interface = vk_api.VkApi(token=comunity_token)
        self.api = VkTools(acces_token)
        self.params = {}

    def message_send(self, user_id, message, attachment=None):
        self.interface.method('messages.send',
                              {'user_id': user_id,
                               'message': message,
                               'attachment': attachment,
                               'random_id': get_random_id()
                               }
                              )
    def event_handler(self):
        longpoll = VkLongPoll(self.interface)

        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                command = event.text.lower()

                if command == 'привет':
                    self.params = self.api.get_profile_info(event.user_id)
                    self.message_send(event.user_id, f'Приветствую тебя, {self.params["name"]}')
                elif command == 'поиск':
                    users = self.api.search_users(self.params)
                    user = users.pop()
                    # здесь логика дял проверки бд
                    from_bd = Viewed.extract_from_db(self)
                    for p, w in from_bd:
                       if p != event.user_id and w != user['id']:
                           photos_user = self.api.get_photos(user['id'])
                           attachment = ''
                           for num, photo in enumerate(photos_user):
                               attachment += f'photo{photo["owner_id"]}_{photo["id"]}'
                               if num == 3:
                                   break
                           self.message_send(event.user_id,
                                             f'Встречайте {user["name"]} https://vk.com/id{user["id"]}',
                                             attachment=attachment
                                             )
                           # здесь логика для добавленяи в бд
                           to_bd = Viewed(profile_id=event.user_id, worksheet_id=user["id"])
                           to_bd.add_in_db(event.user_id, user["id"])
                elif command == 'пока':
                    self.message_send(event.user_id, 'До свидания!')
                else:
                    self.message_send(event.user_id, 'Команда не опознана')


if __name__ == '__main__':
    bot = BotInterface(comunity_token, acces_token)
    bot.event_handler()


