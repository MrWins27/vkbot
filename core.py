from datetime import datetime

import vk_api
from config import acces_token
from vk_api.longpoll import VkLongPoll, VkEventType
from data_store import filter


class VkTools():
    offset = 0

    def __init__(self, acces_token):
        self.api = vk_api.VkApi(token=acces_token)

    def get_profile_info_request(self):
        longpoll = VkLongPoll(self.interface)
        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                command = event.text.lower()
        bdate = 1

    def get_profile_info(self, user_id):

        info, = self.api.method('users.get',
                                {'user_id': user_id,
                                 'fields': 'city,bdate,sex,relation,home_town'
                                 }
                                )
        user_info = {'name': info['first_name'] + ' ' + info['last_name'],
                     'id': info['id'],
                     'bdate': info['bdate'] if 'bdate' in info else None,
                     'home_town': info['home_town'] if 'home_town' in info else None,
                     'sex': info['sex'],
                     'city': info['city']['id'] if 'city' in info else None
                     }
        return user_info

    def search_users(self, params):

        sex = 1 if params['sex'] == 2 else 2
        city = params['city']
        curent_year = datetime.now().year
        user_year = int(params['bdate'].split('.')[2])
        age = curent_year - user_year
        age_from = age - 5
        age_to = age + 5
        offset = self.offset
        count = 10

        profile_id = params['id']
        viewed = filter(profile_id)

        users = self.api.method('users.search',
                                {'count': count,
                                 'offset': offset,
                                 'sex': sex,
                                 'age_from': age_from,
                                 'age_to': age_to,
                                 'city': city,
                                 'status': 6,
                                 'is_closed': False
                                 }
                                )

        try:
            users = users['items']
        except KeyError:
            return []

        res = []

        for user in users:
            if user['id'] not in viewed:
                if user['is_closed'] == False:
                    res.append({'id': user['id'],
                                'name': user['first_name'] + ' ' + user['last_name']
                                }
                               )
        self.offset += count
        return res

    def get_photos(self, user_id):
        photos = self.api.method('photos.get',
                                 {'user_id': user_id,
                                  'album_id': 'profile',
                                  'extended': 1,
                                  }
                                 )
        try:
            photos = photos['items']
        except KeyError:
            return []

        res = []

        for photo in photos:
            res.append({'owner_id': photo['owner_id'],
                        'id': photo['id'],
                        'likes': photo['likes']['count'],
                        'comments': photo['comments']['count'],
                        }
                       )

        res.sort(key=lambda x: x['likes'] + x['comments'], reverse=True)

        return res


if __name__ == '__main__':
    bot = VkTools(acces_token)