from kivymd.uix.screen import MDScreen
from kivymd.uix.label import MDLabel


class LooksScreen(MDScreen):
    def on_pre_enter(self, *args):
        if not self.children:
            self.add_widget(MDLabel(text="Looks", halign="center"))
