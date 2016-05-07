import logging
import rethinkdb as r

logger = logging.getLogger('letSpotify.' + __name__)

DBERROR_MSG = "database error"


class Subscribes:
    def __init__(self, db):
        self.db = db
        self.us = r.table("user_subscribes")
        self.rm = r.table("rooms")

    def create_subscribe(self, data):
        room = yield (self.rm.get(data['rid']).run(self.db))
        if room:
            if room['uid'] == data['uid']:
                return False, False, "Can't subscribe own room"
        else:
            return False, False, "No room for this room id"
        curs = yield (self.us.filter({'uid': data['uid'], 'rid': data['rid']}).run(self.db))
        if not (yield curs.fetch_next()):
            res = yield (self.us.insert(data).run(self.db))
            if res['inserted']:
                return True, True, ""
            else:
                return False, False, "Subscribe failed"
        else:
            return False, False, "Already Subscribe"

    def delete_subscribe(self, data):
        curs = yield (self.us.filter({'uid': data['uid'], 'rid': data['rid']}).run(self.db))
        if (yield curs.fetch_next()):
            subscribe = yield curs.next()
            res = yield self.us.get(subscribe['id']).delete().run(self.db)
            if res['deleted']:
                return True, True, ""
            else:
                return False, False, "Delete failed"
        else:
            return False, False, "No subscribe found"

    def get_user_subscribe_list(self, data):
        curs = yield (self.us.get_all(data['uid'], index='uid')
                      .eq_join("uid", r.table("users")).zip()
                      .eq_join("rid", r.table("rooms"))
                      .run(self.db))
        subscribe_list = []
        while (yield curs.fetch_next()):
            cur = yield curs.next()
            logger.info(cur)
            subscribe = {}
            subscribe['room_name'] = cur['right']['name']
            subscribe['user_name'] = cur['left']['name']
            subscribe['rid'] = cur['left']['rid']
            subscribe['user_fid'] = int(cur['left']['fid'])
            subscribe_list.append(subscribe)
        return subscribe_list, True, ""

    def get_user_master_list(self, data):
        curs = yield (self.rm.get_all(data['uid'], index='uid').eq_join("uid", r.table("users")).run(self.db))
        master_list = []
        while (yield curs.fetch_next()):
            cur = yield curs.next()
            master = {}
            master['room_name'] = cur['left']['name']
            master['rid'] = cur['left']['id']
            master['user_name'] = cur['right']['name']
            master['user_fid'] = int(cur['right']['fid'])
            master_list.append(master)
        return master_list, True, ""

    def get_room_subscriber_list(self, data):
        curs = yield (self.us.get_all(data['rid'], index='rid').eq_join("uid", r.table("users")).run(self.db))
        subscriber_list = []
        while (yield curs.fetch_next()):
            cur = yield curs.next()
            subscriber = {}
            subscriber['name'] = cur['right']['name']
            subscriber['fid'] = int(cur['right']['fid'])
            subscriber_list.append(subscriber)
        return subscriber_list, True, ""

    def is_room_master(self, data):
        curs = yield (self.rm.get_all([data['rid'], data['uid']], index='id_uid').run(self.db))
        while (yield curs.fetch_next()):
            cur = yield curs.next()
            return True, True, ""
        return False, True, ""

    def is_room_subscriber(self, data):
        curs = yield (self.us.get_all([data['rid'], data['uid']], index='rid_uid').run(self.db))
        while (yield curs.fetch_next()):
            cur = yield curs.next()
            return True, True, ""
        return False, True, ""
