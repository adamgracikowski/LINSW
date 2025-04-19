import os
import tornado.web
import tornado.escape
from routes import Templates

USERNAME = "admin"
PASSWORD = "secret,123"

class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_signed_cookie("user")

    def authenticate(self, username, password):
        return username == USERNAME and password == PASSWORD

class ItemsModule(tornado.web.UIModule):
    def render(self, children):
        return self.render_string(Templates.items, children=children)