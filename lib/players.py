import logging

import rethinkdb as r

logger = logging.getLogger('letSpotify.' + __name__)

DBERROR_MSG = "database error"


class Players:
    def __init__(self, db):
        self.db = db
        self.us = r.table("players")

    def get_player(self, data):
        res = {}
        res['rid']
        res['uri']
        res['position']
        res['duration']
        res['time']
        res['playing']
