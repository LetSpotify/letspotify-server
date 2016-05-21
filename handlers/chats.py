import logging
import json
import tornado

from .base import BaseHandler
from .base import Service

logger = logging.getLogger('letSpotify.' + __name__)


class ChatHandler(BaseHandler):
    @tornado.gen.coroutine
    def get(self):
        para_q = [
            ('rid',),
            ('msg',),
        ]
        paras = self.get_parameters(para_q)
        yield from self.is_room_master_or_subscriber(paras)
        room, success, msg = yield from Service.rooms.get_info(paras)
        if room:
            clients = Service.ws_rooms.get_clients(paras['rid'])
            if clients:
                for client in clients:
                    msg = {
                        "type": "chat",
                        "msg": paras['msg']
                    }
                    client.write_message(json.dumps(msg))
                    return self.api_response({}, True, "")
            else:
                return self.api_response({}, True, "No people in this room")
        else:
            return self.api_response({}, False, "Room Not Found")
