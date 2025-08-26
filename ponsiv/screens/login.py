from kivymd.uix.screen import MDScreen
from kivymd.uix.label import MDLabel


class LoginScreen(MDScreen):
    def on_pre_enter(self, *args):
        if not self.children:
            self.add_widget(MDLabel(text="Login", halign="center"))
