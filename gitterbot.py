# -*- coding: utf-8 -*-

import configparser
import json

import requests
import feedparser

# RSS URL of PyCon JP Blog
PYCONJP_BLOG_RSS = 'http://pyconjp.blogspot.com/feeds/posts/default?alt=rss'

# file name for URLs of published blog entries
PUBLISHED_URL_FILE = 'published_url.txt'

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

def get_recent_entry(url_list):
    """
    get recent entry from PyCon JP Blog(http://pyconjp.blogspot.jp/)

    :param int limit: limit of receent entry(minutes)
    """
    target_entry = None
    d = feedparser.parse(PYCONJP_BLOG_RSS)
    for entry in d.entries[::-1]:
        if entry.link not in url_list:
            target_entry = entry

    return d.feed.title, target_entry

def get_published_url_list():
    """
    get published entries URL list from file
    
    :rtype: list
    :return: url_list
    """

    url_list = []

    try:
        with open(PUBLISHED_URL_FILE) as f:
            url_list = [x.rstrip() for x in f.readlines()]
    except IOError:
        pass
    
    return url_list
    
def add_published_url_list(url):
    """
    add URL to published entries URL list

    :param str url: URL of blog entry
    :rtype: list
    :return: url_list
    """

    with open(PUBLISHED_URL_FILE, 'a') as f:
        f.write(url + '\n')
    
def main(token):
    """
    main function

    :param str token: gitter access_token
    """

    url_list = get_published_url_list()

    gitter = Gitter(token)

    # send recent blog post
    title, entry = get_recent_entry(url_list)
    if entry:
        message = '[blog post] [{title}: {entry.title}]({entry.link})'.format(title=title, entry=entry)
    
        gitter.send_message('pyconjp/pyconjp2015-ja', message)
        add_published_url_list(entry.link)
    
if __name__ == '__main__':
    # get access_token from config.ini
    config = configparser.ConfigParser()
    config.read('config.ini')
    token = config['DEFAULT']['access_token']

    main(token)
