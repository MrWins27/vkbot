import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id
from vk_api.keyboard import VkKeyboard, VkKeyboardColor

from config import comunity_token, acces_token
from core import VkTools
from data_store import adder




class BotInterface():

    keyboard = VkKeyboard(one_time=False)
    keyboard.add_button('Поиск', color=VkKeyboardColor.PRIMARY)

    def __init__(self, comunity_token, acces_token):
        self.interface = vk_api.VkApi(token=comunity_token)
        self.api = VkTools(acces_token)
        self.params = {}

    def message_send(self, user_id, message, attachment=None, ):
        self.interface.method('messages.send',
                              {'user_id': user_id,
                               'message': message,
                               'attachment': attachment,
                               'random_id': get_random_id(),
                               'keyboard': self.keyboard.get_keyboard()
                               }
                              )
    def event_handler(self):
        longpoll = VkLongPoll(self.interface)

        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                command = event.text.lower()

                if command == 'привет' or command == 'начать':
                    self.params = self.api.get_profile_info(event.user_id)
                    self.message_send(event.user_id, f'Приветствую тебя, {self.params["name"]}')
                    if self.params['city'] is None:
                        self.message_send(event.user_id, f'Введите город')
                        self.params['city'] = event.text.lower()
                elif command == 'поиск':
                    users = self.api.search_users(self.params)
                    if len(users) == 0:
                        users = self.api.search_users(self.params)
                        user = users.pop()
                    else:
                        user = users.pop()
                    attachment = ''
                    photos_user = self.api.get_photos(user['id'])
                    for num, photo in enumerate(photos_user):
                        attachment += f'photo{photo["owner_id"]}_{photo["id"]}'
                        if num == 2:
                            break
                    self.message_send(event.user_id,
                                      f'Встречайте {user["name"]} https://vk.com/id{user["id"]}',
                                      attachment=attachment
                                      )
                    """здесь логика для добавления в бд"""
                    profile_id = event.user_id
                    worksheet_id = user['id']
                    adder(profile_id, worksheet_id)
                elif command == 'пока':
                    self.message_send(event.user_id, 'До свидания!')
                else:
                    self.message_send(event.user_id, 'Команда не опознана')




if __name__ == '__main__':
    bot = BotInterface(comunity_token, acces_token)
    bot.event_handler()