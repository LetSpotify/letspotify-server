import logging
import json
import tornado
from tornado import auth
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
            try:
                user = yield self.get_authenticated_user(
                    redirect_uri=settings['root_url'] + '/auth/facebook/login/?token=' + paras['token'],
                    client_id=self.settings["facebook_api_key"],
                    client_secret=self.settings["facebook_secret"],
                    code=self.get_argument("code"))
            except Exception as e:
                logger.error(e)
                self.render("base.html", msg="Facebook auth error")
            user_q = {}
            if user:
                token_q = {
                    "token": paras['token'],
                }
                token_status, success_token, msg_token = yield from Service.login_token.get_token(token_q)
                if not token_status['valid']:
                    user_q['name'] = user['name']
                    user_q['access_token'] = user['access_token']
                    user_q['locale'] = user['locale']
                    user_q['fid'] = int(user['id'])
                    user_q['session_expires'] = int(user['session_expires'][0])
                    db_user, success, msg = yield from Service.users.get_user(user_q)
                    if success:
                        updated, success, msg = yield from Service.users.update_user(user_q)
                    else:
                        created, success, msg = yield from Service.users.create_user(user_q)
                    uid, success, msg = yield from Service.users.get_user_id(user_q)
                    token_q['valid'] = True
                    token_q['login'] = True
                    token_q['uid'] = uid
                    res, success, msg = yield from Service.login_token.update_token(token_q)
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
                    "cookie": False,
                }
                yield from Service.login_token.update_token(token_q)
                self.render("base.html", msg="Facebook auth error 2")
        else:
            yield self.authorize_redirect(
                redirect_uri=settings['root_url'] + '/auth/facebook/login/?token=' + paras['token'],
                client_id=self.settings["facebook_api_key"],
                extra_params={"scope": "public_profile,user_friends,email"},
            )
