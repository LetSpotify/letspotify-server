import logging
import psycopg2

logger = logging.getLogger('letSpotify.' + __name__)

DBERROR_MSG = "database error"


class Users:
    def __init__(self, db):
        self.db = db

    def check_user_exists(self, data):
        sql = "SELECT count(*) FROM users WHERE fid = %s;"
        result = yield self.db.execute(sql, (data['fid'],))
        for i in result.fetchall():
            if i[0] == 1:
                return True
            else:
                return False

    def create_user(self, data):
        sql = """
               INSERT INTO users (name, access_token, locale, fid, session_expires)
               VALUES (%s, %s, %s, %s, %s);
               """
        try:
            yield self.db.execute(sql, (data['name'],
                                        data['access_token'],
                                        data['locale'],
                                        int(data['fid']),
                                        int(data['session_expires'])))
            return True, True, ""
        except Exception as e:
            return False, False, DBERROR_MSG + str(e)

    def get_info(self, data):
        sql = """
                SELECT name, locale, fid FROM users WHERE fid=%s;
        """
        try:
            result = yield self.db.execute(sql, (data['fid'],))
            res = {}
            for i in result:
                res['name'] = i[0]
                res['locale'] = i[1]
                res['fid'] = i[2]
            return res, True, ""
        except Exception as e:
            return {}, False, DBERROR_MSG
