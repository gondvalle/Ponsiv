from kivy.core.window import Window
from kivy.metrics import dp
from kivy.uix.screenmanager import ScreenManager
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.button import MDIconButton
from kivymd.uix.label import MDLabel
from kivymd.uix.card import MDCard

from .screens.feed import FeedScreen
from .screens.explore import ExploreScreen
from .screens.looks import LooksScreen
from .screens.cart import CartScreen
from .screens.profile import ProfileScreen
from .screens.login import LoginScreen

Window.size = (360, 640)

class BottomBar(MDCard):
    """Barra inferior personalizada (icono + texto) que controla un ScreenManager externo."""
    def __init__(self, on_select, **kwargs):
        super().__init__(
            size_hint_y=None,
            height=dp(64),
            radius=[0],
            elevation=0,
            md_bg_color=(0, 0, 0, 1),
            **kwargs
        )
        self.on_select = on_select

        row = MDBoxLayout(orientation="horizontal", padding=[dp(8), 0], spacing=dp(8))
        self.add_widget(row)

        items = [
            ("feed",    "home",            "Feed"),
            ("explore", "compass",         "Explore"),
            ("looks",   "image-multiple",  "Looks"),
            ("cart",    "cart",            "Cart"),
            ("profile", "account",         "Profile"),
        ]

        # construimos cada item (icono arriba, texto abajo)
        self.buttons = {}
        for name, icon, text in items:
            col = MDBoxLayout(orientation="vertical", padding=[0, dp(6), 0, dp(6)])
            btn = MDIconButton(
                icon=icon,
                theme_text_color="Custom",
                text_color=(1, 1, 1, 1),
                icon_size="24sp",
                on_release=lambda *_ , n=name: self.select(n),
            )
            lbl = MDLabel(
                text=text,
                halign="center",
                font_size="11sp",
                theme_text_color="Custom",
                text_color=(1, 1, 1, 0.7),
                size_hint_y=None,
                height=dp(16),
            )
            col.add_widget(btn)
            col.add_widget(lbl)
            row.add_widget(col)
            self.buttons[name] = (btn, lbl)

        self.highlight("feed")  # por defecto

    def select(self, name: str):
        self.on_select(name)
        self.highlight(name)

    def highlight(self, active: str):
        # resalta el seleccionado
        for name, (btn, lbl) in self.buttons.items():
            alpha = 1.0 if name == active else 0.6
            btn.text_color = (1, 1, 1, alpha)
            lbl.text_color = (1, 1, 1, alpha)

class PonsivApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"

        root = MDBoxLayout(orientation="vertical")

        # Top bar fija
        top = MDTopAppBar(title="Ponsiv")
        top.size_hint_y = None
        root.add_widget(top)

        # ScreenManager ocupa TODO el espacio disponible
        self.sm = ScreenManager()
        self.sm.size_hint_y = 1
        self.sm.add_widget(FeedScreen(name="feed"))
        self.sm.add_widget(ExploreScreen(name="explore"))
        self.sm.add_widget(LooksScreen(name="looks"))
        self.sm.add_widget(CartScreen(name="cart"))
        self.sm.add_widget(ProfileScreen(name="profile"))
        self.sm.add_widget(LoginScreen(name="login"))
        root.add_widget(self.sm)

        # Bottom bar personalizada (sin ScreenManager interno)
        bottom = BottomBar(on_select=self.switch_screen)
        root.add_widget(bottom)

        return root

    def switch_screen(self, name: str) -> None:
        self.sm.current = name

if __name__ == "__main__":
    PonsivApp().run()
