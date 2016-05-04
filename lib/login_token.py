import logging

import psycopg2
import uuid
logger = logging.getLogger('letSpotify.' + __name__)


class LoginToken:
    def __init__(self, db):
        self.db = db

    def check_token(self, data):
        sql = "SELECT token, login, valid, fid, cookie FROM login_token WHERE token = %s;"
        result = yield self.db.execute(sql, (data['token'],))
        res = {}
        flag = False
        for i in result.fetchall():
            if i:
                res['token'] = i[0]
                res['login'] = i[1]
                res['valid'] = i[2]
                res['fid'] = i[3]
                res['cookie'] = i[4]
                flag = True
        if not flag:
            return {}, False, "token not exist"
        return res, True, ""

    def create_token(self):
        token = str(uuid.uuid4())
        sql = """
               INSERT INTO login_token (token, login, valid, fid)
               VALUES (%s, %s, %s, %s);
               """
        try:
            result = yield self.db.execute(sql, (token,
                                                 False,
                                                 False,
                                                 0,)
                                           )
            return token, True, ""
        except psycopg2.IntegrityError:
            return "", False, ""


    def update_token(self, data):
        sql = """UPDATE login_token SET (login, valid, fid, cookie) = (%s, %s, %s, %s) WHERE token = %s"""
        try:
            yield self.db.execute(sql, (data['login'],
                                        data['valid'],
                                        data['fid'],
                                        data['cookie'],
                                        data['token'],)
                                  )
        except:
            return False, False, ""
        return True, True, ""
