from handlers.facebook_login import FacebookGraphLoginHandler
from handlers.rooms import RoomsCreateHandler
from handlers.rooms import RoomsDeleteHandler
from handlers.rooms import RoomsGetHandler
from handlers.players import RoomsPlayerSendHandler
from handlers.rooms import RoomsNameUpdateHandler
from handlers.login_token import TokenCreateHandler
from handlers.login_token import TokenGetHandler
from handlers.login_token import TokenGetCookieHandler
from handlers.subscribes import UserRoomListHandler
from handlers.subscribes import UserSubscribeHandler
from handlers.subscribes import UserUnsubscribeHandler
from handlers.subscribes import RoomSubscriberListHandler
from handlers.users import GetUserInfoHandler
from handlers.websocket import SocketHandler
from handlers.chats import ChatHandler

url_patterns = [
    (r"/auth/facebook/login/?", FacebookGraphLoginHandler),
    (r"/auth/token/create/?", TokenCreateHandler),
    (r"/auth/token/get/?", TokenGetHandler),
    (r"/auth/token/cookie/?", TokenGetCookieHandler),
    (r"/rooms/get/?", RoomsGetHandler),
    (r"/rooms/create/?", RoomsCreateHandler),
    (r"/rooms/delete/?", RoomsDeleteHandler),
    # (r"/rooms/update/name/?", RoomsNameUpdateHandler),
    # (r"/rooms/player/get/?", RoomsPlayerGetHandler),
    (r"/rooms/player/update/?", RoomsPlayerSendHandler),
    (r"/rooms/subscribe/?", UserSubscribeHandler),
    (r"/rooms/unsubscribe/?", UserUnsubscribeHandler),
    (r"/rooms/subscriber/?", RoomSubscriberListHandler),
    (r"/rooms/chat/?", ChatHandler),
    (r"/user/get/?", GetUserInfoHandler),
    (r"/user/rooms/get/?", UserRoomListHandler),
    (r'/ws/?', SocketHandler),
]
