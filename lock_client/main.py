
#from importlib.metadata import requires
#from unicodedata import name
from urllib import request, response
import requests
from kivymd.app import MDApp
from kivy.core.clipboard import Clipboard
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.screenmanager import Screen
import pyotp
import os
s = requests.Session()
host_url = "https://localhost:8000"
kv = """
<Password_screen>:
    MDTextField:
        id: password
        hint_text: 'password'
        helper_text_mode: "on_focus"
        pos_hint: {'center_x': 0.5, 'center_y': 0.4}
        size_hint_x: None
        width: 300
        required: True
        password: True
    MDTextField:
        id: username
        hint_text: 'username'
        helper_text_mode: "on_focus"
        pos_hint: {'center_x': 0.5, 'center_y': 0.5}
        size_hint_x: None
        width: 300
        icon_right: "account-search"
        required: True
    MDTextField:
        id: host_url
        hint_text: 'host_url(optional)'
        helper_text_mode: "on_focus"
        pos_hint: {'center_x': 0.5, 'center_y': 0.6}
        size_hint_x: None
        width: 300
        required: True
    MDRectangleFlatButton:
        text: 'Submit'
        pos_hint: {'center_x': 0.5, 'center_y': 0.3}
        on_press:
            root.auth()
    MDRectangleFlatButton:
        id:show_or_hide
        text: 'show password'
        pos_hint: {'center_x': 0.8, 'center_y': 0.4}
        on_press:
            root.show_or_hide()
    MDLabel:
        text: ''
        id: show
        pos_hint: {'center_x': 0.5, 'center_y': 0.2}
        halign: 'center'
<Totp_login>
    MDLabel:
        id:totp_hint
        text: ""
        pos_hint:{'center_x': 0.5, 'center_y': 0.2}
        halign:'center'
    MDTextField:
        id: totp_code
        hint_text: 'Enter 2-step verification code'
        helper_text_mode: "on_focus"
        pos_hint: {'center_x': 0.5, 'center_y': 0.5}
        size_hint_x: None
        width: 300
        required: True
    MDRectangleFlatButton:
        id: totp_submit
        text: 'Submit'
        pos_hint: {'center_x': 0.5, 'center_y': 0.4}
        on_press:
            root.auth()
<Dashboard>
    MDRectangleFlatButton:
        id:lock_control
        text: 'lock/unlock'
        pos_hint: {'center_x': 0.5, 'center_y': 0.2}
        on_press:
            root.lock_control()
    MDRectangleFlatButton:
        id:mfa_reset
        text: 'Reset MFA code'
        pos_hint: {'center_x': 0.5, 'center_y': 0.4}
        on_press:
            root.mfa_reset()
    MDRectangleFlatButton:
        id:password_reset
        text: 'Reset password'
        pos_hint: {'center_x': 0.5, 'center_y': 0.6}
        on_press:
            root.password_reset()
    MDRectangleFlatButton:
        id:logout
        text: 'Logout'
        pos_hint: {'center_x': 0.5, 'center_y': 0.8}
        on_press:
            root.logout()
<Dashboard_admin>
    MDRectangleFlatButton:
        id:newuser
        text: 'Add a new user'
        pos_hint: {'center_x': 0.5, 'center_y': 0.2}
        on_press:
            root.add_user()
    MDRectangleFlatButton:
        id:rm_user
        text: 'Remove a user'
        pos_hint: {'center_x': 0.5, 'center_y': 0.3}
        on_press:
            root.rm_user()
    MDRectangleFlatButton:
        id:user_mfa_reset
        text: 'Reset user MFA code'
        pos_hint: {'center_x': 0.5, 'center_y': 0.4}
        on_press:
            root.user_mfa_reset()
    MDRectangleFlatButton:
        id:lock_control
        text: 'lock/unlock'
        pos_hint: {'center_x': 0.5, 'center_y': 0.5}
        on_press:
            root.lock_control()
    MDRectangleFlatButton:
        id:mfa_reset
        text: 'Reset MFA code'
        pos_hint: {'center_x': 0.5, 'center_y': 0.6}
        on_press:
            root.mfa_reset()
    MDRectangleFlatButton:
        id:password_reset
        text: 'Reset password'
        pos_hint: {'center_x': 0.5, 'center_y': 0.7}
        on_press:
            root.password_reset()
    MDRectangleFlatButton:
        id:logout
        text: 'Logout'
        pos_hint: {'center_x': 0.5, 'center_y': 0.8}
        on_press:
            root.logout()
<Totp_register>
    MDLabel:
        id:hints
        text: "paste this 16-digit code in your authenticate app"
        pos_hint:{'center_x': 0.5, 'center_y': 0.7}
        halign:'center'
    MDLabel:
        id:totp_secret
        text: ""
        pos_hint:{'center_x': 0.5, 'center_y': 0.6}
        halign:'center'
    MDTextField:
        id: totp_code
        hint_text: 'Enter 2-step verification code'
        helper_text_mode: "on_focus"
        pos_hint: {'center_x': 0.5, 'center_y': 0.5}
        size_hint_x: None
        width: 300
        required: True
    MDLabel:
        id:totp_hint
        text: ""
        pos_hint:{'center_x': 0.5, 'center_y': 0.3}
        halign:'center'
    MDRectangleFlatButton:
        id: totp_submit
        text: 'Submit'
        pos_hint: {'center_x': 0.5, 'center_y': 0.4}
        on_press:
            root.auth()

<Password_reset>
    MDTextField:
        id: original_password
        hint_text: 'Enter original password'
        helper_text_mode: "on_focus"
        pos_hint: {'center_x': 0.5, 'center_y': 0.8}
        size_hint_x: None
        width: 300
        required: True
        password: True
    MDTextField:
        id: new_password
        hint_text: 'Enter new password'
        helper_text_mode: "on_focus"
        pos_hint: {'center_x': 0.5, 'center_y': 0.7}
        size_hint_x: None
        width: 300
        required: True
        password: True
    MDTextField:
        id: c_password
        hint_text: 'Enter new password again'
        helper_text_mode: "on_focus"
        pos_hint: {'center_x': 0.5, 'center_y': 0.6}
        size_hint_x: None
        width: 300
        required: True
        password: True
    MDRectangleFlatButton:
        id: reset
        text: 'Reset'
        pos_hint: {'center_x': 0.6, 'center_y': 0.5}
        on_press:
            root.reset()
    MDRectangleFlatButton:
        id: back
        text: 'Back'
        pos_hint: {'center_x': 0.4, 'center_y': 0.5}
        on_press:
            root.back()
    MDLabel:
        id: err_msg
        text: ''
        pos_hint: {'center_x': 0.5, 'center_y': 0.4}
        halign: 'center'

<Add_user>
    MDTextField:
        id: name
        hint_text: 'Enter username'
        helper_text_mode: "on_focus"
        pos_hint: {'center_x': 0.5, 'center_y': 0.8}
        size_hint_x: None
        width: 300
        required: True
    MDTextField:
        id: password
        hint_text: 'Enter password'
        helper_text_mode: "on_focus"
        pos_hint: {'center_x': 0.5, 'center_y': 0.7}
        size_hint_x: None
        width: 300
        required: True
        password: True
    MDTextField:
        id: password2
        hint_text: 'Enter password again'
        helper_text_mode: "on_focus"
        pos_hint: {'center_x': 0.5, 'center_y': 0.6}
        size_hint_x: None
        width: 300
        required: True
        password: True
    CheckBox:
        id: admin
        pos_hint: {'center_x': 0.4, 'center_y': 0.5}
        size_hint_x: .10
        size_hint_y: .10
    MDLabel:
        text: 'Set as admin'
        pos_hint: {'center_x': 0.6, 'center_y': 0.5}
        halign: 'center'
    MDRectangleFlatButton:
        id: add
        text: 'add'
        pos_hint: {'center_x': 0.6, 'center_y': 0.4}
        on_press:
            root.add()
    MDRectangleFlatButton:
        id: back
        text: 'Back'
        pos_hint: {'center_x': 0.4, 'center_y': 0.4}
        on_press:
            root.back()
    MDLabel:
        id: err_msg
        text: ''
        pos_hint: {'center_x': 0.5, 'center_y': 0.3}
        halign: 'center'
<Rm_user>
    MDTextField:
        id: password
        hint_text: 'Enter password'
        helper_text_mode: "on_focus"
        pos_hint: {'center_x': 0.5, 'center_y': 0.6}
        size_hint_x: None
        width: 300
        required: True
        password: True
    MDTextField:
        id: name
        hint_text: 'Enter user you want to remove'
        helper_text_mode: "on_focus"
        pos_hint: {'center_x': 0.5, 'center_y': 0.5}
        size_hint_x: None
        width: 300
        required: True
    MDRectangleFlatButton:
        id: remove
        text: 'Remove'
        pos_hint: {'center_x': 0.6, 'center_y': 0.4}
        on_press:
            root.remove()
    MDRectangleFlatButton:
        id: back
        text: 'Back'
        pos_hint: {'center_x': 0.4, 'center_y': 0.4}
        on_press:
            root.back()
<User_mfa_rst>
    MDTextField:
        id: password
        hint_text: 'Enter password'
        helper_text_mode: "on_focus"
        pos_hint: {'center_x': 0.5, 'center_y': 0.6}
        size_hint_x: None
        width: 300
        required: True
        password: True
    MDTextField:
        id: name
        hint_text: 'Enter user you want to reset'
        helper_text_mode: "on_focus"
        pos_hint: {'center_x': 0.5, 'center_y': 0.5}
        size_hint_x: None
        width: 300
        required: True
    MDRectangleFlatButton:
        id: reset
        text: 'Reset'
        pos_hint: {'center_x': 0.6, 'center_y': 0.4}
        on_press:
            root.reset()
    MDRectangleFlatButton:
        id: back
        text: 'Back'
        pos_hint: {'center_x': 0.4, 'center_y': 0.4}
        on_press:
            root.back()
"""


class Password_screen(Screen):
    
    def auth(self):
        global host_url
        if self.ids.host_url.text != "":
            host_url = self.ids.host_url.text
        if self.ids.password.text != '' and self.ids.username.text != "":
            r = s.post(host_url+"/users/login", data={
                "name": self.ids.username.text, "password": self.ids.password.text}, verify=False, allow_redirects=True)
            url = r.url
            if url == host_url+"/users/login":
                label = self.ids.show
                label.text = "wrong password or username"
            elif url == host_url+"/users/register_mfa":
                label = self.ids.show
                # label.text = "Login Sucess"
                # content = s.get(url, verify=False).content
                # print(content)
                self.manager.current = 'totp_register'
            else:
                label = self.ids.show
                label.text = "Login Sucess"
                r = s.get(url, verify=False)
                print(r.content)
                self.manager.current = 'totp_login'
        else:
            label = self.ids.show
            label.text = "Please fill in username and password"

    def show_or_hide(self):
        # print("show or hide func")

        if self.ids.show_or_hide.text == 'show password':
            print("*")
            self.ids.password.password = False
            self.ids.show_or_hide.text = 'hide password'
        elif self.ids.show_or_hide.text == 'hide password':
            print("--")
            self.ids.password.password = True
            self.ids.show_or_hide.text = 'show password'


class Totp_login(Screen):
    def on_enter(self, *args):
        try:
            f=open(".secret")
            print(f.read())
            self.ids.totp_code.text = pyotp.TOTP(f.read()).now()
        except:
            self.ids.totp_hint.text = "local 2FA secret not found \n check your authenticator"
    def auth(self):
        global host_url
        if self.ids.totp_code.text != '':
            # requests.get(host_url+"/users/login_mfa",verify=False, allow_redirects=True)
            r = s.post(host_url+"/users/login_mfa",
                       data={"code": self.ids.totp_code.text}, verify=False, allow_redirects=True)
            url = r.url
            print(url)
            if url == host_url+"/users/login_mfa":
                self.ids.totp_hint.text = "Wrong verification code"
                print(open(".secret").read())
                self.ids.totp_code.text = pyotp.TOTP(open(".secret").read()).now()
                self.manager.current = "totp_login"
            elif url == host_url+"/dashboard":
                self.ids.totp_hint.text = "correct verification code"
                content = s.get(url).content.decode()
                if content.find('Add new user') == -1:
                    print('not admin')
                    print(content)
                    self.manager.current = 'dashboard'
                else:
                    print(content.find('Add new user'))
                    print(content)
                    self.manager.current = "dashboard_admin"

        else:
            self.ids.totp_hint.text = "Please fill in 2-step verification code"


class Totp_register(Screen):
    def on_enter(self, *args):
        global host_url
        r = s.get(host_url+"/users/register_mfa")
        print(r.content.decode())
        offset = r.content.decode().find(': ')
        secret = r.content.decode()[offset+2:offset+18]
        print(secret)
        Clipboard.copy(secret)
        self.ids.totp_secret.text = secret
        self.ids.totp_code.text = pyotp.TOTP(secret).now()

    def auth(self):
        global host_url
        if self.ids.totp_code.text != '':
            # requests.get(host_url+"/users/login_mfa",verify=False, allow_redirects=True)
            # print(s.)
            r = s.post(host_url+"/users/register_mfa",
                       data={"code": self.ids.totp_code.text}, verify=False, allow_redirects=True)
            url = r.url
            print(url)
            if url == host_url+"/users/register_mfa":
                self.ids.totp_hint.text = "Wrong verification code"
                try:
                    print(open(".secret").read())
                    self.ids.totp_code.text = pyotp.TOTP(open(".secret").read()).now()
                except:
                    print(self.ids.totp_secret.text)
                    self.ids.totp_code.text = pyotp.TOTP(self.ids.totp_secret.text).now()
                self.manager.current = "totp_register"
            else:
                self.ids.totp_hint.text = "correct verification code"
                print(s.get(url).content)
                try:
                    f = open(".secret","w")
                except:
                    os.remove(".secret")
                    f = open(".secret","w")
                f.write(self.ids.totp_secret.text)
                f.close()
                self.manager.current = "password_screen"
        else:
            self.ids.totp_hint.text = "Please fill in 2-step verification code"


class Dashboard_admin(Screen):
    def on_enter(self, *args):
        global host_url
        print(s.get(host_url+"/dashboard").content.decode())
        if s.get(host_url+"/dashboard").content.decode().find("unlock") == -1:
            self.ids.lock_control.text = "lock"
        else:
            self.ids.lock_control.text = "unlock"

    def add_user(self):
        global host_url
        r = s.get(host_url+"/userop/newuser",
                  allow_redirects=True)
        if r.url == host_url+"/users/login":
            self.manager.current = "password_screen"
        elif r.url == host_url+"/userop/newuser":
            self.manager.current = "add_user"

    def rm_user(self):
        global host_url
        r = s.get(host_url+"/userop/rm_user",
                  allow_redirects=True)
        if r.url == host_url+"/users/login":
            self.manager.current = "password_screen"
        elif r.url == host_url+"/userop/rm_user":
            self.manager.current = "rm_user"

    def user_mfa_reset(self):
        global host_url
        r = s.get(host_url+"/userop/rst_user_secret",
                  allow_redirects=True)
        if r.url == host_url+"/users/login":
            self.manager.current = "password_screen"
        elif r.url == host_url+"/userop/rst_user_secret":
            self.manager.current = "user_mfa_rst"

    def lock_control(self):
        global host_url
        if self.ids.lock_control.text == "lock":
            r = s.post(host_url+"/userop/lock",
                       allow_redirects=True)
            if r.url == host_url+"/users/login":
                self.manager.current = "password_screen"
            elif r.url == host_url+"/dashboard":
                self.ids.lock_control.text = "unlock"
                self.manager.current = "dashboard_admin"
        elif self.ids.lock_control.text == "unlock":
            r = s.post(host_url+"/userop/unlock",
                       allow_redirects=True)
            if r.url == host_url+"/users/login":
                self.manager.current = "password_screen"
            elif r.url == host_url+"/dashboard":
                self.ids.lock_control.text = "lock"
                self.manager.current = "dashboard_admin"

    def mfa_reset(self):
        global host_url
        r = s.post(host_url+"/userop/rst_secret",
                   allow_redirects=True)
        if r.url == host_url+"/users/login":
            self.manager.current = "password_screen"
        elif r.url == host_url+"/dashboard":
            self.manager.current = "dashboard_admin"

    def password_reset(self):
        global host_url
        r = s.get(host_url+"/userop/rst_password",
                  allow_redirects=True)
        if r.url == host_url+"/users/login":
            self.manager.current = "password_screen"
        elif r.url == host_url+"/userop/rst_password":
            self.manager.current = "password_reset"

    def logout(self):
        global host_url
        r = s.get(host_url+"/users/logout",
                  allow_redirects=True)
        if r.url == host_url+"/users/login":
            self.manager.current = "password_screen"


class Dashboard(Screen):
    def on_enter(self, *args):
        global host_url
        print(s.get(host_url+"/dashboard").content.decode())
        if s.get(host_url+"/dashboard").content.decode().find("unlock") == -1:
            self.ids.lock_control.text = "lock"
        else:
            self.ids.lock_control.text = "unlock"

    def lock_control(self):
        global host_url
        if self.ids.lock_control.text == "lock":
            r = s.post(host_url+"/userop/lock",
                       allow_redirects=True)
            if r.url == host_url+"/users/login":
                self.manager.current = "password_screen"
            elif r.url == host_url+"/dashboard":
                self.ids.lock_control.text = "unlock"
                self.manager.current = "dashboard"
        elif self.ids.lock_control.text == "unlock":
            r = s.post(host_url+"/userop/unlock",
                       allow_redirects=True)
            if r.url == host_url+"/users/login":
                self.manager.current = "password_screen"
            elif r.url == host_url+"/dashboard":
                self.ids.lock_control.text = "lock"
                self.manager.current = "dashboard"

    def mfa_reset(self):
        global host_url
        r = s.post(host_url+"/userop/rst_secret",
                   allow_redirects=True)
        if r.url == host_url+"/users/login":
            self.manager.current = "password_screen"
        elif r.url == host_url+"/dashboard":
            self.manager.current = "dashboard"

    def password_reset(self):
        global host_url
        r = s.get(host_url+"/userop/rst_password",
                  allow_redirects=True)
        if r.url == host_url+"/users/login":
            self.manager.current = "password_screen"
        elif r.url == host_url+"/userop/rst_password":
            self.manager.current = "password_reset"

    def logout(self):
        global host_url
        r = s.get(host_url+"/users/logout",
                  allow_redirects=True)
        if r.url == host_url+"/users/login":
            self.manager.current = "password_screen"


class Password_reset(Screen):
    def back(self):
        global host_url
        r = s.get(host_url+"/dashboard")
        if r.url == host_url+"/users/login":
            self.manager.current = "password_screen"
        content = r.content.decode()
        if content.find('Add new user') == -1:
            print('not admin')
            print(content)
            self.manager.current = 'dashboard'
        else:
            print(content.find('Add new user'))
            print(content)
            self.manager.current = "dashboard_admin"

    def reset(self):
        global host_url
        if self.ids.original_password.text == self.ids.new_password.text:
            self.ids.err_msg.text = 'new password can not be original password'
        elif self.ids.c_password.text != self.ids.new_password.text:
            self.ids.err_msg.text = 'Confirm password does not match'
        elif len(self.ids.new_password.text) < 6:
            self.ids.err_msg.text = 'New password is too short'
        else:
            r = s.post(host_url+"/userop/rst_password", data={"original_password": self.ids.original_password.text,
                       "new_password": self.ids.new_password.text, "c_password": self.ids.c_password.text}, allow_redirects=True, verify=False)
            print(r.url)
            print(r.content.decode())
            print(r.url)
            if r.url == host_url+"/users/login":
                print("***")
                self.manager.current = "password_screen"
            elif r.url == host_url+"/userop/rst_password":
                self.manager.current = "password_reset"

            print("no jump")


class Add_user(Screen):

    def back(self):
        global host_url
        r = s.get(host_url+"/dashboard")
        if r.url == host_url+"/users/login":
            self.manager.current = "password_screen"
        content = r.content.decode()
        if content.find('Add new user') == -1:
            print('not admin')
            print(content)
            self.manager.current = 'dashboard'
        else:
            print(content.find('Add new user'))
            print(content)
            self.manager.current = "dashboard_admin"

    def add(self):
        global host_url
        if len(self.ids.password.text) < 6:
            self.ids.err_msg.text = "password must be 6 characters or more"
        elif self.ids.password.text != self.ids.password2.text:
            self.ids.err_msg.text = "Confirm password does not match"
        else:
            print(self.ids.admin.active)
            r = s.post(host_url+"/userop/newuser", data={
                       "name": self.ids.name.text, "password": self.ids.password.text, "password2": self.ids.password2.text, "admin": "admin" if self.ids.admin.active else ""})
            if r.url == host_url+"/users/login":
                self.manager.current = "password_screen"
            elif r.url == host_url+"/userop/newuser":
                self.manager.current = 'add_user'
            elif r.url == host_url+"/dashboard":
                r = s.get(host_url+"/dashboard")
                if r.url == host_url+"/users/login":
                    self.manager.current = "password_screen"
                else:
                    content = r.content.decode()
                    if content.find('Add new user') == -1:
                        print('not admin')
                        print(content)
                        self.manager.current = 'dashboard'
                    else:
                        print(content.find('Add new user'))
                        print(content)
                        self.manager.current = "dashboard_admin"


class Rm_user(Screen):
    def back(self):
        global host_url
        r = s.get(host_url+"/dashboard")
        
        if r.url == host_url+"/users/login":
            self.manager.current = "password_screen"
        content = r.content.decode()
        if content.find('Add new user') == -1:
            print('not admin')
            print(content)
            self.manager.current = 'dashboard'
        else:
            print(content.find('Add new user'))
            print(content)
            self.manager.current = "dashboard_admin"

    def remove(self):
        global host_url
        r = s.post(host_url+"/userop/rm_user",
                   data={"password": self.ids.password.text, "name": self.ids.name.text})
        if r.url == host_url+"/users/login":
            self.manager.current = "password_screen"
        elif r.url == host_url+"/userop/rm_user":
            self.manager.current = 'rm_user'
        elif r.url == host_url+"/dashboard":
            r = s.get(host_url+"/dashboard")
            if r.url == host_url+"/users/login":
                self.manager.current = "password_screen"
            else:
                content = r.content.decode()
                if content.find('Add new user') == -1:
                    print('not admin')
                    print(content)
                    self.manager.current = 'dashboard'
                else:
                    print(content.find('Add new user'))
                    print(content)
                    self.manager.current = "dashboard_admin"


class User_mfa_rst(Screen):
    def back(self):
        global host_url
        r = s.get(host_url+"/dashboard")
        if r.url == host_url+"/users/login":
            self.manager.current = "password_screen"
        content = r.content.decode()
        if content.find('Add new user') == -1:
            print('not admin')
            print(content)
            self.manager.current = 'dashboard'
        else:
            print(content.find('Add new user'))
            print(content)
            self.manager.current = "dashboard_admin"

    def reset(self):
        global host_url
        r = s.post(host_url+"/userop/rst_user_secret",
                   data={"password": self.ids.password.text, "name": self.ids.name.text})

        if r.url == host_url+"/users/login":
            self.manager.current = "password_screen"
        elif r.url == host_url+"/userop/rst_user_secret":
            self.manager.current = 'rst_user_secret'
        elif r.url == host_url+"/dashboard":
            r = s.get(host_url+"/dashboard")
            if r.url == host_url+"/users/login":
                self.manager.current = "password_screen"
            else:
                content = r.content.decode()
                if content.find('Add new user') == -1:
                    print('not admin')
                    print(content)
                    self.manager.current = 'dashboard'
                else:
                    print(content.find('Add new user'))
                    print(content)
                    self.manager.current = "dashboard_admin"


class app(MDApp):
    in_class = ObjectProperty(None)

    def build(self):
        self.root = Builder.load_string(kv)
        screen_manager = ScreenManager()
        screen_manager.add_widget(Password_screen(name="password_screen"))
        screen_manager.add_widget(Totp_login(name='totp_login'))
        screen_manager.add_widget(Totp_register(name='totp_register'))
        screen_manager.add_widget(Dashboard(name="dashboard"))
        screen_manager.add_widget(Dashboard_admin(name="dashboard_admin"))
        screen_manager.add_widget(Password_reset(name="password_reset"))
        screen_manager.add_widget(Add_user(name='add_user'))
        screen_manager.add_widget(Rm_user(name='rm_user'))
        screen_manager.add_widget(User_mfa_rst(name='user_mfa_rst'))
        return screen_manager


if __name__ == '__main__':
    app().run()
    