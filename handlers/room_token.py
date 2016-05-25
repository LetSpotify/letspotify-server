import logging
import tornado
from .base import Service
from .base import BaseHandler

logger = logging.getLogger('letSpotify.' + __name__)


class RoomTokenCreateHandler(BaseHandler):
    @tornado.gen.coroutine
    def get(self):
        para_q = [
            ('rid',),
        ]
        paras = self.get_parameters(para_q)
        yield from self.is_room_master_or_subscriber(paras)
        room, success, msg = yield from Service.rooms.get_info(paras)
        if room:
            token, success, msg = yield from Service.room_token.create_token(paras)
            data = {
                'token': token
            }
            return self.api_response({"token": token}, success, msg)
        else:
            return self.api_response({}, success, msg)
