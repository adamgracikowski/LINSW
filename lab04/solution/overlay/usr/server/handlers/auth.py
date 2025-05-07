import tornado.web
import tornado.escape

from routes import *
from .base import BaseHandler

class LoginHandler(BaseHandler):
    def get(self):
        self.render(Templates.login)

    def post(self):
        username = self.get_argument("username")
        password = self.get_argument("password")

        if self.authenticate(username, password):
            self.set_signed_cookie("user", tornado.escape.json_encode(username))
            self.redirect(Routes.home)
        else:
            self.render(Templates.login_failed)

class LogoutHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.clear_all_cookies()
        self.redirect(Routes.login)