import logging
import rethinkdb as r
from handlers.base import Service

logger = logging.getLogger('letSpotify.' + __name__)

DB_NO_ERR_MSG = ""
DBERROR_MSG = "Database error"


class Rooms:
    def __init__(self, db):
        self.db = db
        self.rm = r.table("rooms")
        self.us = r.table("user_subscribes")

    def create_room(self, data):
        curs = yield (self.rm.filter({'uid': data['uid'], 'name': data['name']}).run(self.db))
        logger.info(data)
        if not (yield curs.fetch_next()):
            res = yield (self.rm.insert(data).run(self.db))
            if res['inserted'] == 1:
                return res['generated_keys'][0], True, DB_NO_ERR_MSG
            else:
                return "", False, "insert failed"
        else:
            return "", False, "User has already the room with same name"

    def delete_room(self, data):
        room = yield (self.rm.get(data['rid']).run(self.db))
        if room:
            res = yield (self.rm.get(data['rid']).delete().run(self.db))
            # Remove all the subscribes of this room
            yield (self.us.filter({'rid': data['rid']}).delete().run(self.db))
            if res['deleted']:
                return "", True, DB_NO_ERR_MSG
            else:
                return "", False, "Delete Failed"
        else:
            return "", False, "Room not found"

    def get_info(self, data):
        room = yield (self.rm.get(data['rid']).run(self.db))
        if room:
            return room, True, DB_NO_ERR_MSG
        else:
            return {}, False, "Room not found"

