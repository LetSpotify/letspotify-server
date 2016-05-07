import logging
import tornado

from .base import BaseHandler
from .base import Service

logger = logging.getLogger('letSpotify.' + __name__)


class GetUserInfoHandler(BaseHandler):
    @tornado.gen.coroutine
    def get(self):
        user = self.get_user()
        paras = {'uid': user}
        user, success, msg = yield from Service.users.get_user(paras)
        self.api_response(user, success, msg)
