import logging
import rethinkdb as r

logger = logging.getLogger('letSpotify.' + __name__)

DBERROR_MSG = "database error"
DB_NO_ERR_MSG = ""


class Users:
    def __init__(self, db):
        self.db = db
        self.ur = r.table("users")

    def create_user(self, data):
        curs = yield (self.ur.get_all(data['fid'], index='fid').run(self.db))
        if not (yield curs.fetch_next()):
            yield (self.ur.insert(data).run(self.db))
            return True, True, DB_NO_ERR_MSG
        else:
            return False, False, "User already created"

    def get_user(self, data):
        user = yield (self.ur.get(data['uid']).run(self.db))
        if user:
            user.pop('access_token')
            user.pop('session_expires')
            user['fid'] = int(user['fid'])
            return user, True, DB_NO_ERR_MSG
        return {}, False, "can't find user"

    def update_user(self, data):
        curs = yield (self.ur.get_all(data['fid'], index='fid').run(self.db))
        while (yield curs.fetch_next()):
            user = yield curs.next()
            res = yield self.ur.get(user['id']).update(data).run(self.db)
            if res['replaced']:
                return True, True, DB_NO_ERR_MSG
            else:
                return False, False, "can't update"
        return False, False, "can't find user"

    def get_user_id(self, data):
        curs = yield (self.ur.get_all(data['fid'], index='fid').run(self.db))
        while (yield curs.fetch_next()):
            user = yield curs.next()
            return user['id'], True, DB_NO_ERR_MSG
        return "", False, "can't find user"
