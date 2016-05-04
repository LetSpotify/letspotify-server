import json
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
        paras['fid'] = user
        rid, success, msg = yield from Service.rooms.create(paras)
        self.api_response({"rid":rid}, success, msg)


class RoomsDeleteHandler(BaseHandler):
    @tornado.gen.coroutine
    def get(self):
        para_q = [
            ('rid',)
        ]
        paras = self.get_parameters(para_q)
        yield from self.is_room_master(paras['rid'])
        rid, success, msg = yield from Service.rooms.delete(paras)
        self.api_response({}, success, msg)


class RoomsNameUpdateHandler(BaseHandler):
    @tornado.gen.coroutine
    def get(self):
        para_q = [
            ('rid',),
            ('name',)
        ]
        paras = self.get_parameters(para_q)
        exist, success_exist, msg_exist = yield from Service.rooms.check_exist(paras)
        if not exist:
            self.api_response({}, False, msg_exist)
        yield from self.is_room_master(paras['rid'])
        updated, success, msg = yield from Service.rooms.update_name(paras)
        if not success:
            self.api_response({}, False, msg)
        self.api_response({"updated":updated}, success, msg)


class RoomsCheckHandler(BaseHandler):
    @tornado.gen.coroutine
    def get(self):
        para_q = [
            ('rid',)
        ]
        paras = self.get_parameters(para_q)
        exist, success_exist, msg_exist = yield from Service.rooms.check_exist(paras)
        if not exist:
            self.api_response({}, False, msg_exist)
        room_info, success_info, msg_info = yield from Service.rooms.get_info(paras)
        if not success_info:
            self.api_response({}, False, msg_info)
        res = {
            "alive": room_info['alive'],
            "name": room_info['name'],
            "rid": paras['rid'],
            "fid": room_info['fid']
        }
        self.api_response(res, True, "")


class RoomsPlayerSendHandler(BaseHandler):
    @tornado.gen.coroutine
    def get(self):
        para_q = [
            ('rid',),
            ('uri',),
            ('position',),
            ('duration',),
            ('time',),
            ('playing',)
        ]
        paras = self.get_parameters(para_q)
        exist, success_exist, msg_exist = yield from Service.rooms.check_exist(paras)
        if not exist:
            self.api_response({}, False, msg_exist+"not exist")
        yield from self.is_room_master(paras['rid'])
        print(paras)
        updated, success, msg = yield from Service.rooms.update_player(paras)
        if not success:
            self.api_response({}, success, msg+"success")
        self.api_response({"updated": updated}, success, "")



class RoomsPlayerGetHandler(BaseHandler):
    @tornado.gen.coroutine
    def get(self):
        para_q = [
            ('rid',),
        ]
        paras = self.get_parameters(para_q)
        exist, success_exist, msg_exist = yield from Service.rooms.check_exist(paras)
        if not exist:
            self.api_response({}, False, msg_exist)
        yield from self.is_room_master_or_subscriber(paras['rid'])
        player_info, success, msg = yield from Service.rooms.get_player(paras)
        if not success:
            self.api_response({}, success, msg)
        self.api_response(player_info, success, "")
