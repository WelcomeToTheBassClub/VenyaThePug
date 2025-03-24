import json

from kivy.app import App
from kivy.network.urlrequest import UrlRequest
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.slider import Slider

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.slider import Slider
from kivy.event import EventDispatcher
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle, Color, Line
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
from random import random
from kivy.properties import ListProperty, NumericProperty, DictProperty, ObjectProperty, StringProperty
import urllib.parse
from kivy.uix.floatlayout import FloatLayout


class User(EventDispatcher):
    token = DictProperty()

    def __init__(self, **kwargs):
        self.register_event_type("on_login")
        self.register_event_type("on_login_error")
        super(User, self).__init__(**kwargs)

    def success_callback(self, req, result):
        self.token = result
        self.dispatch('on_login', result)

    def failure_callback(self, req, result):
        error_msg = "Ошибка авторизации"

        if req.error:
            detail_msg = str(req.error)
        elif req.resp_status and req.resp_status == 401:
            detail_msg = "Неверный логин или пароль"

        self.dispatch('on_login_error', f"{error_msg}: {detail_msg}")

    def on_login(self, *args):
        pass

    def on_login_error(self, *args):
        pass

    def login(self, username, password):
        params = urllib.parse.urlencode({
            'grant_type': 'password',
            'username': username,
            'password': password
        })
        headers = {
            'Content-type': 'application/x-www-form-urlencoded',
            'Accept': 'text/plain'
        }
        UrlRequest(
            'http://pug-venya.ddns.net/token',
            on_success=self.success_callback,
            on_failure=self.failure_callback,
            on_error=self.failure_callback,
            req_body=params,
            req_headers=headers,
            timeout=3
        )

        return None

    def about_me(self):
        if not self.token:
            return None

        authorization = " ".join([
            self.token.get('token_type'),
            self.token.get('access_token')
        ])

        headers = {
            'Accept': 'application/json',
            'Authorization': authorization
        }
        UrlRequest(
            'http://pug-venya.ddns.net/users/me/',
            on_success=print,
            req_headers=headers
        )


class PopupWindow(Widget):
    def btn(self):
        popFun()


class P(FloatLayout):
    pass


def popFun():
    print('popFun')
    show = P()
    window = Popup(title="popup", content=show,
                   size_hint=(None, None), size=(300, 300))
    window.open()


class LoginWindow(Screen):
    username = StringProperty()
    password = StringProperty()
    fail_login_msg = StringProperty()

    def disable(self, *args):
        self.fail_login_msg = ""
        self.disabled = True

    def enable(self, *args):
        if len(args) > 1:
            self.fail_login_msg = args[1]

        self.disabled = False

    def login(self):
        if not (self.username and self.password):
            return None

        current_app = App.get_running_app()
        current_app.user.login(self.username, self.password)
        self.disable()


# class to display validation result
class Interface(Screen):
    pass


# class for managing screens
class WindowManager(ScreenManager):
    def switch_to_main(self, *args):
        self.current = 'main'


class VenyaPugApp(App):
    user = ObjectProperty(User())

    def build(self):
        screen_manager = WindowManager()
        login_screen = LoginWindow(name='login')
        main_screen = Interface(name='main')
        screen_manager.add_widget(login_screen)
        screen_manager.add_widget(main_screen)

        self.user.bind(on_login=screen_manager.switch_to_main)
        self.user.bind(on_login_error=login_screen.enable)

        return screen_manager


VenyaPugApp().run()
