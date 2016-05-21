import logging

import tornado

from .base import BaseHandler
from .base import Service

logger = logging.getLogger('letSpotify.' + __name__)


class RoomsCreateHandler(BaseHandler):
    @tornado.gen.coroutine
    def get(self):
        user = self.get_user()
        para_q = [
            ('name',)
        ]
        paras = self.get_parameters(para_q)
        paras['uid'] = user
        rid, success, msg = yield from Service.rooms.create_room(paras)
        self.api_response({"rid": rid}, success, msg)


class RoomsDeleteHandler(BaseHandler):
    @tornado.gen.coroutine
    def get(self):
        para_q = [
            ('rid',)
        ]
        paras = self.get_parameters(para_q)
        yield from self.is_room_master(paras)
        rid, success, msg = yield from Service.rooms.delete_room(paras)
        self.api_response({}, success, msg)


class RoomsGetHandler(BaseHandler):
    @tornado.gen.coroutine
    def get(self):
        para_q = [
            ('rid',)
        ]
        paras = self.get_parameters(para_q)
        room_info, success, msg = yield from Service.rooms.get_info(paras)
        self.api_response(room_info, success, "")


class RoomsNameUpdateHandler(BaseHandler):
    @tornado.gen.coroutine
    def get(self):
        para_q = [
            ('rid',),
            ('name',)
        ]
        paras = self.get_parameters(para_q)
        return