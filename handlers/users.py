import logging
import tornado
import json

from .base import BaseHandler
from .base import Service

logger = logging.getLogger('letSpotify.' + __name__)


class GetUserInfoHandler(BaseHandler):
    @tornado.gen.coroutine
    def get(self):
        user = self.get_user()
        paras = {'fid': user}
        user, success, msg = yield from Service.users.get_info(paras)
        if not success:
            self.api_response(user, success, msg)
        self.api_response(user, success, msg)
