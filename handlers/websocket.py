from tornado import websocket, web, ioloop
import json
import logging
from .base import Service
import tornado
logger = logging.getLogger('letSpotify.' + __name__)


class SocketHandler(websocket.WebSocketHandler):
    def check_origin(self, origin):
        return True

    @tornado.gen.coroutine
    def open(self):
        paras = {}
        paras['rid'] = self.get_argument("rid", "")
        paras['token'] = self.get_argument("token", "")
        data_token, success, msg = yield from Service.room_token.get_token(paras)
        if success and data_token['rid'] == paras['rid']:
            logger.debug("new client: rid = %s" % paras['rid'])
            Service.ws_rooms.add_client(paras['rid'], self)
            msg = {
                "type": "info",
                "data": {
                    'rid': paras['rid'],
                    'join': True,
                    'msg': ''
                }
            }
        else:
            msg = {
                "type": "info",
                "data": {
                    'rid': paras['rid'],
                    'join': False,
                    'msg': 'auth failed'
                }
            }
        self.write_message(json.dumps(msg))

    @tornado.gen.coroutine
    def on_message(self, message):
        pass

    @tornado.gen.coroutine
    def on_close(self):
        paras = {}
        paras['rid'] = self.get_argument("rid", "")
        paras['token'] = self.get_argument("token", "")
        data, success, msg = yield from Service.room_token.delete_token(paras)
        Service.ws_rooms.delete_client(paras['rid'], self)
