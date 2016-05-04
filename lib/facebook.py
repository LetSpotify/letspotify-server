import tornado.ioloop
from tornado.httpclient import AsyncHTTPClient, HTTPRequest


def handle_request(response):
    if response.error:
        print("Error:", response.error)
    else:
        print('called')
        print(response.body)


class FacebookAPI:
    def __init__(self, db):
        self.db = db
        self.http_client = AsyncHTTPClient()
        self.user_id = 0
        self.access_token = ""

    def get_email(self):
        url = "http://kevchentw.nctu.me:12000/pages/"
        req = HTTPRequest(
            url=url,
            method='GET',
            validate_cert=False)
        self.http_client.fetch(req, handle_request)
        tornado.ioloop.IOLoop.instance().start()




