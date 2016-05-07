import logging
import tornado

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
        paras['uid'] = user
        subscribe, success, msg = yield from Service.subscribes.create_subscribe(paras)
        self.api_response(subscribe, success, msg)


class UserUnsubscribeHandler(BaseHandler):
    @tornado.gen.coroutine
    def get(self):
        user = self.get_user()
        para_q = [
            ('rid',),
        ]
        paras = self.get_parameters(para_q)
        paras['uid'] = user
        yield from self.is_room_subscriber(paras['rid'])
        unsubscribe, success, msg = yield from Service.subscribes.delete_subscribe(paras)
        self.api_response(unsubscribe, success, msg)


class RoomSubscriberListHandler(BaseHandler):
    @tornado.gen.coroutine
    def get(self):
        para_q = [
            ('rid',),
        ]
        paras = self.get_parameters(para_q)
        room_subscriber, success, msg = yield from Service.subscribes.get_room_subscriber_list(paras)
        self.api_response(room_subscriber, success, "")


class UserRoomListHandler(BaseHandler):
    @tornado.gen.coroutine
    def get(self):
        user = self.get_user()
        paras = {'uid': user}
        user_subscribe, success_subscribe, msg_subscribe = yield from Service.subscribes.get_user_subscribe_list(paras)
        user_master, success_master, msg_master = yield from Service.subscribes.get_user_master_list(paras)
        if not (success_subscribe and success_master):
            self.api_response([], False, "")
        res = {
            "subscribe": user_subscribe,
            "master": user_master
        }
        self.api_response(res, True, "")
