import logging
import tornado
import json

from .base import BaseHandler
from .base import Service

logger = logging.getLogger('letSpotify.' + __name__)


class UserSubscribeHandler(BaseHandler):
    @tornado.gen.coroutine
    def get(self):
        user = self.get_user()
        para_q = [
            ('rid',),
        ]
        paras = self.get_parameters(para_q)
        paras['fid'] = int(user)
        subscribe, success, msg = yield from Service.rooms.subscribe(paras)
        if not success:
            self.api_response([], success, msg)
        self.api_response({"subscribe": subscribe, "rid": paras['rid']}, success, "")


class UserUnsubscribeHandler(BaseHandler):
    @tornado.gen.coroutine
    def get(self):
        user = self.get_user()
        para_q = [
            ('rid',),
        ]
        paras = self.get_parameters(para_q)
        paras['fid'] = int(user)
        yield from self.is_room_subscriber(paras['rid'])
        unsubscribe, success, msg = yield from Service.rooms.unsubscribe(paras)
        if not success:
            self.api_response([], success, msg)
        self.api_response({"unsubscribe": unsubscribe}, success, "")


class RoomSubscriberListHandler(BaseHandler):
    @tornado.gen.coroutine
    def get(self):
        para_q = [
            ('rid',),
        ]
        paras = self.get_parameters(para_q)
        room_subscriber, success, msg = yield from Service.rooms.get_room_subscriber_list(paras)
        if not success:
            self.api_response([], success, msg)
        self.api_response(room_subscriber, success, "")


class UserRoomListHandler(BaseHandler):
    @tornado.gen.coroutine
    def get(self):
        user = self.get_user()
        paras = {'fid': int(user)}
        user_subscribe, success_subscribe, msg_subscribe = yield from Service.rooms.get_user_subscribe_list(paras)
        user_master, success_master, msg_master = yield from Service.rooms.get_user_master_list(paras)
        if not (success_subscribe and success_master):
            self.api_response([], False, msg_subscribe + " " + msg_master)
        res = {
            "subscribe": user_subscribe,
            "master": user_master
        }
        self.api_response(res, True, "")
