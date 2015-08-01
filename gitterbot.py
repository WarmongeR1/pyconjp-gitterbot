# -*- coding: utf-8 -*-

import configparser
import json
import time

import requests
import feedparser

PYCONJP_BLOG_RSS = 'http://pyconjp.blogspot.com/feeds/posts/default?alt=rss'

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

def get_recent_entry(limit):
    """
    get recent entry from PyCon JP Blog(http://pyconjp.blogspot.jp/)
    limit: limit of receent entry(minutes)
    """
    d = feedparser.parse(PYCONJP_BLOG_RSS)
    entry = d.entries[0]

    published = time.mktime(d.entries[0].published_parsed)
    now = time.time()
    # alter 5 minutes
    if now - published > 60 * limit:
        entry = None
    return d.feed.title, entry

def main(token):
    gitter = Gitter(token)

    # send recent blog post(less than 5 minutes)
    title, entry = get_recent_entry(5)
    if entry:
        message = '[blog post] [{title}: {entry.title}]({entry.link})'.format(title=title, entry=entry)
    
        gitter.send_message('pyconjp/pyconjp2015-ja', message)
    
if __name__ == '__main__':
    # get access_token from config.ini
    config = configparser.ConfigParser()
    config.read('config.ini')
    token = config['DEFAULT']['access_token']

    main(token)
