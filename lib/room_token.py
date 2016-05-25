import logging
import rethinkdb as r
from datetime import datetime

logger = logging.getLogger('letSpotify.' + __name__)

DB_NO_ERR_MSG = ""
DB_DEFAULT_ERR_MSG = "Database Error"


class RoomToken:
    def __init__(self, db):
        self.db = db
        self.rk = r.table("room_tokens")

    def create_token(self, data):
        payload = {
            "rid": data['rid'],
            "timestamp": r.expr(datetime.now(r.make_timezone('+08:00')))
        }
        res = (yield self.rk.insert(payload).run(self.db))
        if res['inserted'] == 1:
            return res['generated_keys'][0], True, DB_NO_ERR_MSG
        else:
            return "", False, "Create Token Failed"

    def get_token(self, data):
        res = (yield self.rk.get(data['token']).run(self.db))
        if res:
            res.pop('timestamp')
            return res, True, DB_NO_ERR_MSG
        return {}, False, "No Token Found"

    def delete_token(self, data):
        res = (yield self.rk.get(data['token']).delete().run(self.db))
        logger.debug(res)
        if res['deleted']:
            return {}, True, DB_NO_ERR_MSG
        elif res['skipped']:
            return {}, False, "No Token Found"
        elif res['unchanged']:
            return {}, False, "Data not changed"
        else:
            return {}, False, "Unexpected error"
