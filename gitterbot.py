# -*- coding: utf-8 -*-

import configparser
import requests
import json

class Gitter:
    """Gitter API class
    """
    def __init__(self, token):
        """token: access_token
        """
        self.token = token
        self.room_id_dict = self.get_room_id_dict()

    def get_rooms(self):
        """get all room information
        """
        headers = {
            'Accept': 'application/json',
            'Authorization': 'Bearer {}'.format(self.token),
        }
        r = requests.get('https://api.gitter.im/v1/rooms', headers=headers)

        return r.json()

    def get_room_id_dict(self):
        """room情報を name: id の形式の辞書にする
        """
        room_id_dict = {}
        for room in self.get_rooms():
            room_id_dict[room['uri']] = room['id']

        return room_id_dict

    def send_message(self, room, text):
        """send message to room
        """
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': 'Bearer {}'.format(self.token),
        }
        room_id = self.room_id_dict.get(room)
        url = 'https://api.gitter.im/v1/rooms/{room_id}/chatMessages'.format(room_id=room_id)
        payload = {'text': text}
        r = requests.post(url, data=json.dumps(payload), headers=headers)

        return r

if __name__ == '__main__':
    # config.ini からパラメーターを取得
    config = configparser.ConfigParser()
    config.read('config.ini')
    token = config['DEFAULT']['access_token']

    gitter = Gitter(token)
    gitter.send_message('pyconjp/pyconjp2015-ja', 'testメッセージ2 http://pycon.jp/')
