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
        rid = self.get_argument("rid", "")
        logger.info("new client: rid = %s" % rid)
        Service.ws_rooms.add_client(rid, self)

    @tornado.gen.coroutine
    def on_message(self, message):
        pass

    @tornado.gen.coroutine
    def on_close(self):
        rid = self.get_argument("rid", "")
        logger.info("remove client: rid = %s" % rid)
        Service.ws_rooms.delete_client(rid, self)
