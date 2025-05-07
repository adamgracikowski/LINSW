import tornado.web
import tornado.escape

from routes import *
from config import *

class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_signed_cookie("user")

    def authenticate(self, username, password):
        return username == USERNAME and password == PASSWORD