import logging
import uuid

logger = logging.getLogger('letSpotify.' + __name__)

DBERROR_MSG = "database error"

class Rooms:
    def __init__(self, db):
        self.db = db

    def create(self, data):
        u = str(uuid.uuid4())
        sql = "INSERT INTO rooms (rid, alive, fid, name) VALUES (%s, TRUE, %s, %s);"
        try:
            yield self.db.execute(sql, (u, data['fid'], data['name']))
            return u, True, ""
        except:
            return "", False, DBERROR_MSG

    def close(self, data):
        sql = "UPDATE rooms SET (alive) = (FALSE) WHERE rid = %s;"
        try:
            yield self.db.execute(sql, (data['rid'],))
            return True, True, ""
        except:
            return False, False, DBERROR_MSG

    def delete(self, data):
        sql = """
            DELETE FROM rooms WHERE rid = %s;
            """
        try:
            yield self.db.execute(sql, (data['rid'],
                                        )
                                  )
            return True, True, ""
        except:
            return False, False, DBERROR_MSG

    def update_name(self, data):
        sql = "UPDATE rooms SET (name) = (%s) WHERE rid = %s;"
        try:
            yield self.db.execute(sql, (data['name'], data['rid'],))
            return True, True, ""
        except:
            return False, False, DBERROR_MSG

    def get_info(self, data):
        sql = "SELECT name, alive, fid FROM rooms WHERE rid = %s;"
        try:
            result = yield self.db.execute(sql, (data['rid'],))
            res = {}
            for i in result:
                res['name'] = i[0]
                res['alive'] = i[1]
                res['fid'] = i[2]
                if res:
                    return res, True, ""
                else:
                    return {}, False, "no room info"
        except:
            return "", False, DBERROR_MSG


    def check_exist(self, data):
        sql = "SELECT count(*) FROM rooms WHERE rid = %s;"
        try:
            result = yield self.db.execute(sql, (data['rid'],))
            for i in result:
                if i[0] == 0:
                    return False, True, "room not exist"
                else:
                    return True, True, ""
        except:
            return False, False, DBERROR_MSG

    def get_player(self, data):
        sql = "SELECT rid, uri, position, duration, time, playing FROM player WHERE rid = %s;"
        try:
            result = yield self.db.execute(sql, (data['rid'],))
            res = {}
            for i in result:
                res['rid'] = i[0]
                res['uri'] = i[1]
                res['position'] = int(i[2])
                res['duration'] = int(i[3])
                res['time'] = int(i[4])
                res['playing'] = i[5]
                res['error'] = ""
            if res:
                return res, True, ""
            else:
                return {}, False, "no player info"
        except:
            return {}, False, DBERROR_MSG

    def update_player(self, data):
        sql = """
              INSERT INTO player AS p (rid, uri, position, duration, time, playing)
              VALUES  (%s, %s, %s, %s, %s, %s)
              ON CONFLICT (rid)
              DO UPDATE SET (uri, position, duration, time, playing)
              = (%s, %s, %s, %s, %s)
              WHERE p.rid = %s;
              """
        try:
            yield self.db.execute(sql, (str(data['rid']),
                                        str(data['uri']),
                                        int(data['position']),
                                        int(data['duration']),
                                        int(data['time']),
                                        str(data['playing']),
                                        str(data['uri']),
                                        int(data['position']),
                                        int(data['duration']),
                                        int(data['time']),
                                        str(data['playing']),
                                        str(data['rid']),
                                        )
                                  )
            return True, True, ""
        except:
            return False, False, DBERROR_MSG

    def subscribe(self, data):
        sql = """
            INSERT INTO user_subscribe (fid, rid)
            VALUES  (%s, %s);
            """
        try:
            yield self.db.execute(sql, (data['fid'],
                                        data['rid'],
                                        )
                                  )
            return True, True, ""
        except:
            return False, False, DBERROR_MSG

    def unsubscribe(self, data):
        sql = """
            DELETE FROM user_subscribe WHERE fid = %s AND rid = %s;
            """
        try:
            yield self.db.execute(sql, (data['fid'],
                                        data['rid'],
                                        )
                                  )
            return True, True, ""
        except:
            return False, False, DBERROR_MSG

    def get_user_subscribe_list(self, data):
        sql = """
            SELECT u.rid, r.alive, r.public, r.fid, r.name, users.name FROM user_subscribe AS u, rooms AS r, users
            WHERE u.rid = r.rid AND u.fid = %s AND users.fid = r.fid
            """
        try:
            result = yield self.db.execute(sql, (data['fid'],))
            res = []
            for i in result:
                us = {}
                us['rid'] = i[0]
                us['alive'] = i[1]
                us['public'] = i[2]
                us['fid'] = i[3]
                us['name'] = i[4]
                us['master_name'] = i[5]
                res.append(us)
            return res, True, ""
        except:
            return [], False, DBERROR_MSG

    def get_user_master_list(self, data):
        sql = """
            SELECT r.rid, r.alive, r.public, r.fid, r.name, users.name FROM rooms AS r, users
            WHERE r.fid = %s AND r.fid = users.fid
            """
        try:
            result = yield self.db.execute(sql, (data['fid'],))
            res = []
            for i in result:
                us = {}
                us['rid'] = i[0]
                us['alive'] = i[1]
                us['public'] = i[2]
                us['fid'] = i[3]
                us['name'] = i[4]
                us['master_name'] = i[5]
                res.append(us)
            return res, True, ""
        except:
            return [], False, DBERROR_MSG

    def get_room_subscriber_list(self, data):
        sql = """
            SELECT r.fid FROM user_subscribe AS u, rooms AS r
            WHERE u.rid = r.rid AND u.rid = %s
            """
        try:
            result = yield self.db.execute(sql, (data['rid'],))
            res = []
            for i in result:
                us = {}
                us['fid'] = i[0]
                res.append(us)
            return res, True, ""
        except:
            return [], False, DBERROR_MSG

    def is_room_master(self, data):
        sql = """
            SELECT COUNT(*) FROM rooms
            WHERE rid = %s AND fid = %s;
            """
        try:
            result = yield self.db.execute(sql, (data['rid'], data['fid']))
        except:
            return
        for i in result:
            if i[0] == 0:
                return False
            else:
                return True

    def is_room_subscriber(self, data):
        sql = """
            SELECT COUNT(*) FROM user_subscribe
            WHERE rid = %s AND fid = %s;
            """
        try:
            result = yield self.db.execute(sql, (data['rid'], data['fid']))
        except:
            return
        for i in result:
            if i[0] == 0:
                return False
            else:
                return True
