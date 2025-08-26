from kivymd.uix.screen import MDScreen
from kivymd.uix.label import MDLabel
from ..store import store


class ProfileScreen(MDScreen):
    user_id = 1

    def on_pre_enter(self, *args):
        user = store.users.get(self.user_id)
        name = user.name if user else "Guest"
        self.clear_widgets()
        self.add_widget(MDLabel(text=f"Profile: {name}", halign="center"))
