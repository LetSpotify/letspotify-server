import logging
import json

import tornado
from tornado import auth
from tornado import web

from settings import settings

from .base import Service
from .base import BaseHandler

logger = logging.getLogger('letSpotify.' + __name__)


class FacebookGraphLoginHandler(BaseHandler,
                                tornado.auth.FacebookGraphMixin):
    @tornado.gen.coroutine
    def get(self):
        para_q = [
            ('token',),
        ]
        paras = self.get_parameters(para_q)
        if self.get_argument("code", False):
            user = yield self.get_authenticated_user(
                redirect_uri=settings['root_url'] + '/auth/facebook/login/?token=' + paras['token'],
                client_id=self.settings["facebook_api_key"],
                client_secret=self.settings["facebook_secret"],
                code=self.get_argument("code"))
            res = {}
            res['error'] = ""
            user_q = {}
            if user:
                token_q = {
                    "login": True,
                    "valid": True,
                    "token": paras['token'],
                    "fid": user['id'],
                    "cookie": False
                }
                token_status, success_token, msg_token = yield from Service.login_token.check_token(token_q)
                if not token_status['valid']:
                    yield from Service.login_token.update_token(token_q)
                    user_q['name'] = user['name']
                    user_q['access_token'] = user['access_token']
                    user_q['locale'] = user['locale']
                    user_q['fid'] = int(user['id'])
                    user_q['session_expires'] = int(user['session_expires'][0])
                    res['fid'] = user['id']
                    res['name'] = user['name']
                    res['new_user'], success, msg = yield from Service.users.create_user(data=user_q)
                    # self.set_secure_cookie("user", str(user_q['fid']))   
                    self.render("base.html", msg="login success")
                elif token_status['valid']:
                    self.render("base.html", msg="token already used")
                else:
                    print(token_status)  
                    self.render("base.html", msg="unexpected error")		              
            else:
                token_q = {
                    "login": False,
                    "valid": True,
                    "token": paras['token'],
                    "fid": 0,
                    "cookie": False,
                }
                yield from Service.login_token.update_token(token_q)
                res['error'] = "login failed"
            self.finish(json.dumps(res))
        else:
            yield self.authorize_redirect(
                redirect_uri=settings['root_url'] + '/auth/facebook/login/?token=' + paras['token'],
                client_id=self.settings["facebook_api_key"],
                extra_params={"scope": "public_profile,user_friends,email"},
            )


class FacebookGraphLogoutHandler(BaseHandler):
    @tornado.gen.coroutine
    def get(self):
        user = self.get_secure_cookie("user")
        self.clear_cookie("user")
        res = {}
        res['error'] = ""
        if not user:
            res['error'] = "no user login"
        self.finish(json.dumps(res))



class FacebookGraphStatusHandler(BaseHandler):
    @tornado.gen.coroutine
    def get(self):
        user = self.get_secure_cookie("user")
        res = {}
        res['error'] = ""
        if user:
            res['fid'] = int(user.decode())
            res['login'] = True
        else:
            res['login'] = False
            res['error'] = "no user login"
        self.finish(json.dumps(res))
