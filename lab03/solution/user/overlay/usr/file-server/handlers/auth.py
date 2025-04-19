from routes import Routes, Templates
from .base import BaseHandler
import tornado.web
import tornado.escape

class LoginHandler(BaseHandler):
    def get(self):
        self.render(Templates.login)

    def post(self):
        username = self.get_argument("username")
        password = self.get_argument("password")

        if self.authenticate(username, password):
            self.set_signed_cookie("user", tornado.escape.json_encode(username))
            self.redirect(Routes.files)
        else:
            self.render(Templates.loginFailed)

class LogoutHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.clear_all_cookies()
        self.redirect(Routes.login)