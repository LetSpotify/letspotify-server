import logging

logger = logging.getLogger('letSpotify.' + __name__)


class RoomClient:
    def __init__(self, db):
        self.conns = {}
        self.db = db

    def check_room_exist(self, rid):
        if rid in self.conns:
            return True
        else:
            return False

    def new_room(self, rid):
        if self.check_room_exist(rid):
            return
        self.conns[rid] = set()

    def create_obj(self, uid, fid, name, conn):
        return uid, fid, name, conn

    def add_client(self, rid, obj):
        if self.check_room_exist(rid):
            logger.info(rid)
            self.conns[rid].add(obj)
        else:
            self.new_room(rid)
            self.add_client(rid, obj)

    def delete_client(self, rid, obj):
        if self.check_room_exist(rid):
            self.conns[rid].discard(obj)
            self.check_delete_room(rid)

    def get_clients(self, rid):
        if self.check_room_exist(rid):
            return self.conns[rid]

    def check_delete_room(self, rid):
        if self.check_room_exist(rid) and len(self.conns[rid]) == 0:
            del self.conns[rid]

    def get_conns(self):
        return self.conns