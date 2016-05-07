#!/usr/bin/env python
import logging

import tornado.httpserver
import tornado.web
import tornado.gen
from tornado.options import options
from tornado.concurrent import Future, chain_future
from tornado.ioloop import IOLoop

import rethinkdb as r

from settings import settings
from urls import url_patterns

from handlers.base import Service
from lib.users import Users
from lib.facebook import FacebookAPI
from lib.rooms import Rooms
from lib.login_token import LoginToken
from lib.subscribes import Subscribes
from lib.ws_rooms import RoomClient

logger = logging.getLogger('letSpotify.' + __name__)


class LetSpotify(tornado.web.Application):
    def __init__(self, db):
        self.db = db
        logger.info(db)
        tornado.web.Application.__init__(self, url_patterns, **settings)
        logger.info("Server Start")


@tornado.gen.coroutine
def main():
    r.set_loop_type("tornado")
    db = yield r.connect(host='localhost', port=28015, db=settings['db_name'])

    Service.login_token = LoginToken(db)
    Service.users = Users(db)
    Service.rooms = Rooms(db)
    Service.subscribes = Subscribes(db)
    Service.ws_rooms = RoomClient(db)

    app = LetSpotify(db)
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)

if __name__ == "__main__":
    IOLoop.current().run_sync(main)
    IOLoop.current().start()


