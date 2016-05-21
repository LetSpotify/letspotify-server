import logging
import json
import tornado

from .base import BaseHandler
from .base import Service

logger = logging.getLogger('letSpotify.' + __name__)


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
        yield from self.is_room_master(paras)
        room, success, msg = yield from Service.rooms.get_info(paras)
        if room:
            clients = Service.ws_rooms.get_clients(paras['rid'])
            paras.pop('rid')
            if clients:
                for client in clients:
                    msg = {
                        "type": "player",
                        "msg": paras
                    }
                    client.write_message(json.dumps(msg))
                    return self.api_response({}, True, "")
            else:
                return self.api_response({}, True, "No people in this room")
