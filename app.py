#!/usr/bin/env python
import logging

import tornado.httpserver
import tornado.ioloop
import tornado.web
from tornado.options import options

import psycopg2
import momoko


from settings import settings
from urls import url_patterns

from handlers.base import Service
from lib.users import Users
from lib.facebook import FacebookAPI
from lib.rooms import Rooms
from lib.login_token import LoginToken

logger = logging.getLogger('letSpotify.' + __name__)


class LetSpotify(tornado.web.Application):
    def __init__(self):
        tornado.web.Application.__init__(self, url_patterns, **settings)
        logger.info("Server Start")


def main():
    app = LetSpotify()
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    ioloop = tornado.ioloop.IOLoop.instance()

    app.db = momoko.Pool(
        dsn=settings['dsn'],
        size=5,
        raise_connect_errors=False,
        reconnect_interval=50,
        ioloop=ioloop,
    )

    future = app.db.connect()
    ioloop.add_future(future, lambda f: ioloop.stop())
    ioloop.start()
    future.result()  # raises exception on connection error

    Service.users = Users(app.db)
    Service.facebook = FacebookAPI(app.db)
    Service.rooms = Rooms(app.db)
    Service.login_token = LoginToken(app.db)

    ioloop.start()

if __name__ == "__main__":
    main()

