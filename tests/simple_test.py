import requests as r
import json
import webbrowser
from time import time


BASE_URL = "http://140.113.89.94:8888"
TOKEN_CREATE = "/auth/token/create/"
TOKEN_GET = "/auth/token/get/"
TOKEN_COOKIE = "/auth/token/cookie/"
FACEBOOK_LOGIN = "/auth/facebook/login/"
ROOMS_GET = "/rooms/get/"
ROOMS_CREATE = "/rooms/create/"
ROOMS_DELETE = "/rooms/delete/"
PLAYER_UPDATE = "/rooms/player/update/"
ROOMS_SUBSCRIBE = "/rooms/subscribe/"
ROOMS_UNSUBSCRIBE = "/rooms/unsubscribe/"
ROOMS_SUBSCRIBER = "/rooms/subscriber/"
ROOMS_CHAT = "/rooms/chat/"
USER_GET = "/user/get/"
USER_ROOMS_GET = "/user/rooms/get/"


class SimpleTest:
    def __init__(self):
        self.cookies = None
        self.token = None
        self.room = {}

    def test_token_create(self):
        res = r.get(BASE_URL+TOKEN_CREATE)
        j = json.loads(res.text)
        assert j['success']
        assert j['data']['token'] != ''
        self.token = j['data']['token']

    def test_token_get(self):
        if self.token:
            data = {'token': self.token}
        else:
            self.test_token_create()
            data = {'token': self.token}
        res = r.get(BASE_URL+TOKEN_GET, data=data)
        j = json.loads(res.text)
        assert j['success']

    def test_token_cookie(self):
        if self.token:
            data = {'token': self.token}
        else:
            self.test_token_create()
            data = {'token': self.token}
        res = r.get(BASE_URL+TOKEN_COOKIE, data=data)
        self.cookies = res.cookies
        j = json.loads(res.text)
        assert self.cookies
        assert j['success']

    def test_facebook_login(self):
        if self.token:
            data = {'token': self.token}
        else:
            self.test_token_create()
            data = {'token': self.token}
        res = r.get(BASE_URL + FACEBOOK_LOGIN, data=data)
        webbrowser.open(res.url, new=2)
        input("Press Enter After Login Success")
        res = r.get(BASE_URL + TOKEN_GET, data=data)
        j = json.loads(res.text)
        assert j['success']
        assert j['data']['login'] == True

    def test_rooms_create(self):
        data = {'name': 'test_' + str(time())}
        res = r.get(BASE_URL + ROOMS_CREATE, cookies=self.cookies, data=data)
        j = json.loads(res.text)
        assert j['success']
        assert j['data']['rid']
        self.room['id'] = j['data']['rid']
        self.room['name'] = data['name']

    def test_rooms_get(self):
        data = {'rid': self.room['id']}
        res = r.get(BASE_URL + ROOMS_GET, cookies=self.cookies, data=data)
        j = json.loads(res.text)
        assert j['success']
        assert j['data']['id'] == self.room['id']
        assert j['data']['name'] == self.room['name']

    def test_rooms_delete(self):
        data = {'rid': self.room['id']}
        res = r.get(BASE_URL + ROOMS_DELETE, cookies=self.cookies, data=data)
        j = json.loads(res.text)
        assert j['success']

    def test_player_update(self):
        data = {
            'rid': self.room['id'],
            'uri': 'spotify:track:5VPdnalo32c10YxIOzFWl8',
            'playing': True,
            'time': 1462368085,
            'duration': 262,
            'position': 1
        }
        res = r.get(BASE_URL + PLAYER_UPDATE, cookies=self.cookies, data=data)
        j = json.loads(res.text)
        assert j['success']

    def test_rooms_subscribe(self):
        data = {'rid': self.room['id']}
        res = r.get(BASE_URL + ROOMS_SUBSCRIBE, cookies=self.cookies, data=data)
        # j = json.loads(res.text)
        # assert j['success']

    def test_rooms_unsubscribe(self):
        data = {'rid': self.room['id']}
        res = r.get(BASE_URL + ROOMS_UNSUBSCRIBE, cookies=self.cookies, data=data)
        # j = json.loads(res.text)
        # assert j['success']

    def test_rooms_subscriber(self):
        data = {'rid': self.room['id']}
        res = r.get(BASE_URL + ROOMS_SUBSCRIBER, cookies=self.cookies, data=data)
        j = json.loads(res.text)
        assert j['success']

    def test_rooms_chat(self):
        data = {'rid': self.room['id'], 'msg': 'test'}
        res = r.get(BASE_URL + ROOMS_CHAT, cookies=self.cookies, data=data)
        j = json.loads(res.text)
        assert j['success']

    def test_user_get(self):
        res = r.get(BASE_URL + USER_GET, cookies=self.cookies)
        j = json.loads(res.text)
        assert j['success']

    def test_user_rooms_get(self):
        res = r.get(BASE_URL + USER_ROOMS_GET, cookies=self.cookies)
        j = json.loads(res.text)
        assert j['success']


test = SimpleTest()
test.test_token_create()
test.test_token_get()
test.test_facebook_login()
test.test_token_cookie()
test.test_rooms_create()
test.test_rooms_get()
test.test_player_update()
test.test_rooms_subscribe()
test.test_rooms_subscriber()
test.test_rooms_chat()
test.test_user_get()
test.test_user_rooms_get()
test.test_rooms_unsubscribe()
test.test_rooms_delete()
