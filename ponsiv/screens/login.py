from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDFlatButton
from kivymd.uix.label import MDLabel

from ..store import store


class LoginScreen(MDScreen):
    """Screen that allows the user to login or create an account."""

    def on_pre_enter(self, *args):
        self.clear_widgets()
        layout = MDBoxLayout(orientation="vertical", padding=20, spacing=20)
        self.email_field = MDTextField(hint_text="Email")
        self.password_field = MDTextField(hint_text="Password", password=True)
        btn = MDFlatButton(text="Login / Signup", on_release=self.handle_auth)
        self.message = MDLabel(text="", halign="center")
        layout.add_widget(self.email_field)
        layout.add_widget(self.password_field)
        layout.add_widget(btn)
        layout.add_widget(self.message)
        self.add_widget(layout)

    def handle_auth(self, *_):
        email = self.email_field.text.strip()
        password = self.password_field.text
        if not email or not password:
            self.message.text = "Please enter email and password"
            return

        user_id = store.authenticate_user(email, password)
        if user_id is None:
            if store.get_user_by_email(email) is not None:
                self.message.text = "Incorrect password"
                return
            user_id = store.create_user(email, password)

        store.current_user_id = user_id
        self.manager.current = "feed"
