import logging
import json
import uuid

import tornado
from tornado import auth
from tornado import web

from settings import settings

from .base import Service
from .base import BaseHandler

logger = logging.getLogger('letSpotify.' + __name__)


class TokenCreateHandler(BaseHandler):
    @tornado.gen.coroutine
    def get(self):
        token, success, msg = yield from Service.login_token.create_token()
        self.api_response({"token":token}, success, msg)


class TokenCheckHandler(BaseHandler):
    @tornado.gen.coroutine
    def get(self):
        para_q = [
            ('token',),
        ]
        paras = self.get_parameters(para_q)
        token_data, success, msg = yield from Service.login_token.check_token(paras)
        self.api_response(token_data, success, msg)


class TokenGetCookieHandler(BaseHandler):
    @tornado.gen.coroutine
    def get(self):
        para_q = [
            ('token',),
        ]
        paras = self.get_parameters(para_q)
        token_data, success, msg = yield from Service.login_token.check_token(paras)
        if not success:
            self.api_response({}, success, msg)
        else:
            if token_data['login'] and not token_data['cookie']:
                self.set_secure_cookie("user", str(token_data['fid']))
                token_data['cookie'] = True
                updated, success, msg = yield from Service.login_token.update_token(token_data)
                self.api_response({"updated": updated}, success, msg)
            elif not token_data['login']:
                self.api_response({}, False, "token is not login yet")
            elif token_data['cookie']:
                self.api_response({}, False, "cookie sent before")
            else:
                loggin.error("Token Get Cookie Unexpected Error")
                logging.error(token_data)
                self.api_response({}, False, "unexpected error")
