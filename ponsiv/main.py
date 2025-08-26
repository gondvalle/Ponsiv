from kivy.core.window import Window
from kivy.metrics import dp
from kivy.uix.screenmanager import ScreenManager
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.button import MDIconButton
from kivymd.uix.card import MDCard

from .screens.feed import FeedScreen
from .screens.explore import ExploreScreen
from .screens.looks import LooksScreen
from .screens.cart import CartScreen
from .screens.profile import ProfileScreen
from .screens.login import LoginScreen

Window.size = (360, 640)


class BottomBar(MDCard):
    """
    Bottom nav de sólo iconos, fondo blanco y sin etiquetas (estilo del mock).
    Controla un ScreenManager externo.
    """
    def __init__(self, on_select, **kwargs):
        super().__init__(
            size_hint_y=None,
            height=dp(64),
            radius=[0],
            elevation=0,
            md_bg_color=(1, 1, 1, 1),
            **kwargs
        )
        self.on_select = on_select

        row = MDBoxLayout(orientation="horizontal", padding=[dp(8), 0], spacing=dp(8))
        self.add_widget(row)

        # Orden aproximado como en la captura (home, search/explore, t-shirt, cart, profile)
        items = [
            ("feed",    "home"),
            ("explore", "magnify"),
            ("looks",   "tshirt-crew"),
            ("cart",    "shopping-outline"),
            ("profile", "account-outline"),
        ]

        self.buttons = {}
        for name, icon in items:
            btn = MDIconButton(
                icon=icon,
                theme_text_color="Custom",
                text_color=(0, 0, 0, 0.55),
                icon_size="24sp",
                on_release=lambda *_ , n=name: self.select(n),
            )
            row.add_widget(btn)
            self.buttons[name] = btn

        self.highlight("feed")  # por defecto

    def select(self, name: str):
        self.on_select(name)
        self.highlight(name)

    def highlight(self, active: str):
        for name, btn in self.buttons.items():
            alpha = 1.0 if name == active else 0.55
            btn.text_color = (0, 0, 0, alpha)


class PonsivApp(MDApp):
    def build(self):
        # Tema oscuro general, pero cabecera transparente y bottom blanca
        self.theme_cls.theme_style = "Light"

        root = MDBoxLayout(orientation="vertical")

        # ── TOP BAR estilo mock: transparente, título "PONSIV" y dos iconos a la derecha ──
        top = MDTopAppBar(
            title="PONSIV",
            md_bg_color=(1, 1, 1, 1),
            elevation=0,
            right_action_items=[
                ["heart-outline", lambda x: None],
                ["account-outline", lambda x: self.switch_screen("profile")],
            ],
        )
        # Aseguramos texto/íconos en blanco para que se lean sobre la foto
        try:
            top.specific_text_color = (0, 0, 0, 1)
        except Exception:
            pass
        root.add_widget(top)

        # ── Contenido principal ──
        self.sm = ScreenManager()
        self.sm.size_hint_y = 1
        self.sm.add_widget(FeedScreen(name="feed"))
        self.sm.add_widget(ExploreScreen(name="explore"))
        self.sm.add_widget(LooksScreen(name="looks"))
        self.sm.add_widget(CartScreen(name="cart"))
        self.sm.add_widget(ProfileScreen(name="profile"))
        self.sm.add_widget(LoginScreen(name="login"))
        root.add_widget(self.sm)

        # ── Bottom nav de iconos ──
        bottom = BottomBar(on_select=self.switch_screen)
        root.add_widget(bottom)

        return root

    def switch_screen(self, name: str) -> None:
        self.sm.current = name


if __name__ == "__main__":
    PonsivApp().run()
