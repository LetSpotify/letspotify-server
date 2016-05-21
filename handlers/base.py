import json
import logging
import rethinkdb as r

import tornado.web


logger = logging.getLogger('letSpotify.' + __name__)


class BaseHandler(tornado.web.RequestHandler):
    def initialize(self):
        self.db = self.application.db

    def load_json(self):
        """Load JSON from the request body and store them in
        self.request.arguments, like Tornado does by default for POSTed form
        parameters.

        If JSON cannot be decoded, raises an HTTPError with status 400.
        """
        try:
            self.request.arguments = json.loads(self.request.body)
        except ValueError:
            msg = "Could not decode JSON: %s" % self.request.body
            logger.debug(msg)
            raise tornado.web.HTTPError(400, msg)

    def get_json_argument(self, name, default=None):
        """Find and return the argument with key 'name' from JSON request data.
        Similar to Tornado's get_argument() method.
        """
        if default is None:
            default = self._ARG_DEFAULT
        if not self.request.arguments:
            self.load_json()
        if name not in self.request.arguments:
            if default is self._ARG_DEFAULT:
                msg = "Missing argument '%s'" % name
                logger.debug(msg)
                raise tornado.web.HTTPError(400, msg)
            logger.debug("Returning default argument %s, as we couldn't find "
                         "'%s' in %s" % (default, name, self.request.arguments))
            return default
        arg = self.request.arguments[name]
        logger.debug("Found '%s': %s in JSON arguments" % (name, arg))
        return arg

    def get_parameters(self, paras):
        missing = []
        res = {}
        for para in paras:
            if len(para) == 1:
                try:
                    res[para[0]] = self.get_argument(para[0])
                except:
                   missing.append(para[0])
            else:
                res[para[0]] = self.get_argument(para[0], para[1])
        if len(missing) > 0:
            self.set_status(400)
            err = "missing parameters: "
            for m in missing:
                err += m + ', '
            res = {
                "data": {},
                "success": False,
                "msg": err
            }
            self.finish(json.dumps(res))
            return res
        else:
            return res

    def api_response(self, data, success, msg):
        res = {
            "data": data,
            "success": success,
            "msg": msg
        }
        self.set_status(200)
        self.finish(json.dumps(res))

    def get_user(self):
        try:
            return self.get_secure_cookie("user").decode()
        except:
            self.set_status(401)
            res = {
                "msg": "Unauthorized",
                "success": False
            }
            self.finish(json.dumps(res))
            raise tornado.web.Finish()

    def is_room_master(self, data):
        uid = self.get_user()
        data['uid'] = uid
        master = yield from Service.subscribes.is_room_master(data)
        if master:
            return True
        else:
            self.set_status(403)
            res = {
                "msg": "You are not the master of this room",
                "success": False
            }
            self.finish(json.dumps(res))
            raise tornado.web.Finish()

    def is_room_subscriber(self, data):
        uid = self.get_user()
        data['uid'] = uid
        subscriber, success, msg = yield from Service.subscribes.is_room_subscriber(data)
        if subscriber:
            return True
        else:
            self.set_status(403)
            res = {
                "msg": "You are not the subscriber of this room",
                "success": False
            }
            self.finish(json.dumps(res))
            raise tornado.web.Finish()

    def is_room_master_or_subscriber(self, data):
        uid = self.get_user()
        data['uid'] = uid
        master, success, msg = yield from Service.subscribes.is_room_master(data)
        subscriber, success, msg = yield from Service.subscribes.is_room_subscriber(data)
        if master or subscriber:
            return True
        else:
            self.set_status(403)
            res = {
                "msg": "You are not the master or subscriber of this room",
                "success": False
            }
            self.finish(json.dumps(res))
            raise tornado.web.Finish()

    def fid_to_uid(self, data):
        user_id, success, msg = yield from Service.users.get_user_id(data)
        if success:
            data.pop('fid')
            data['uid'] = user_id
            return data
        else:
            return {}

class Service:
    pass
