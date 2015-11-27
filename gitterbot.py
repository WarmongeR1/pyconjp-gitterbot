# -*- coding: utf-8 -*-

import configparser
import json
import pprint

import requests


class Gitter:
    """
    Gitter API wrapper
    URL: https://developer.gitter.im/docs/welcome
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
        """
        """
        room_id_dict = {}
        for room in self.get_rooms():
            if room['githubType'] != 'ONETOONE':
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


def main(token):
    """
    main function

    :param str token: gitter access_token
    """
    gitter = Gitter(token)
    pprint.pprint(gitter.room_id_dict)
    # gitter.send_message('pythondigest/pythondigest', 'Тестовое сообщание с помощью API')


if __name__ == '__main__':
    # get access_token from config.ini
    config = configparser.ConfigParser()
    config.read('config.ini')
    token = config['DEFAULT']['access_token']

    main(token)
