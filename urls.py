from handlers.facebook_login import FacebookGraphLoginHandler
from handlers.facebook_login import FacebookGraphStatusHandler
from handlers.rooms import RoomsCreateHandler
from handlers.rooms import RoomsDeleteHandler
from handlers.rooms import RoomsCheckHandler
from handlers.rooms import RoomsPlayerSendHandler
from handlers.rooms import RoomsPlayerGetHandler
from handlers.rooms import RoomsNameUpdateHandler
from handlers.login_token import TokenCreateHandler
from handlers.login_token import TokenCheckHandler
from handlers.login_token import TokenGetCookieHandler
from handlers.subscribes import UserRoomListHandler
from handlers.subscribes import UserSubscribeHandler
from handlers.subscribes import UserUnsubscribeHandler
from handlers.subscribes import RoomSubscriberListHandler
from handlers.users import GetUserInfoHandler

url_patterns = [
    (r"/auth/facebook/login/?", FacebookGraphLoginHandler),
    (r"/auth/facebook/status/?", FacebookGraphStatusHandler),
    (r"/auth/token/create/?", TokenCreateHandler),
    (r"/auth/token/get/?", TokenCheckHandler),
    (r"/auth/token/cookie/?", TokenGetCookieHandler),
    (r"/rooms/get/?", RoomsCheckHandler),
    (r"/rooms/create/?", RoomsCreateHandler),
    (r"/rooms/delete/?", RoomsDeleteHandler),
    (r"/rooms/update/name/?", RoomsNameUpdateHandler),
    (r"/rooms/player/get/?", RoomsPlayerGetHandler),
    (r"/rooms/player/update/?", RoomsPlayerSendHandler),
    (r"/rooms/subscribe/?", UserSubscribeHandler),
    (r"/rooms/unsubscribe/?", UserUnsubscribeHandler),
    (r"/rooms/subscriber/?", RoomSubscriberListHandler),
    (r"/user/get/?", GetUserInfoHandler),
    (r"/user/rooms/get/?", UserRoomListHandler),
]
