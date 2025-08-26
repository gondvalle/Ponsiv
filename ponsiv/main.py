from kivy.core.window import Window
from kivy.metrics import dp
from kivy.uix.screenmanager import ScreenManager
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.button import MDIconButton
from kivymd.uix.card import MDCard
from kivymd.uix.fitimage import FitImage
from kivymd.uix.relativelayout import MDRelativeLayout

from .screens.feed import FeedScreen
from .screens.explore import ExploreScreen
from .screens.looks import LooksScreen
from .screens.cart import CartScreen
from .screens.profile import ProfileScreen
from .screens.login import LoginScreen
from .screens.detail import ProductDetailScreen
from .store import store

Window.size = (360, 640)


class BottomBar(MDCard):
    def __init__(self, on_select, **kwargs):
        super().__init__(
            size_hint_y=None,
            height=dp(54),
            radius=[0],
            elevation=0,
            md_bg_color=(1, 1, 1, 1),
            **kwargs
        )
        self.on_select = on_select

        row = MDBoxLayout(orientation="horizontal", padding=[dp(8), 0], spacing=dp(8))
        self.add_widget(row)

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

        self.highlight("feed")

    def select(self, name: str):
        self.on_select(name)
        self.highlight(name)

    def highlight(self, active: str):
        for name, btn in self.buttons.items():
            alpha = 1.0 if name == active else 0.55
            btn.text_color = (0, 0, 0, alpha)


class PonsivApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Light"

        root = MDBoxLayout(orientation="vertical")

        # ── Top bar + logo (guardamos referencia) ───────────────────────────────
        self.top_container = MDRelativeLayout(size_hint=(1, None), height=dp(56))

        top = MDTopAppBar(
            title="",
            md_bg_color=(1, 1, 1, 1),
            elevation=0,
            left_action_items=[],
            right_action_items=[
                ["heart-outline", lambda x: None],
                ["account-outline", lambda x: self.switch_screen("profile")],
            ],
            size_hint=(1, None),
            height=dp(56),
        )
        try:
            top.specific_text_color = (0, 0, 0, 1)
        except Exception:
            pass

        logo = FitImage(
            source="assets/logos/Ponsiv.png",
            size_hint=(None, None),
            height=dp(28),
            width=dp(100),
            pos_hint={"center_x": 0.2, "center_y": 0.5},
        )

        self.top_container.add_widget(top)
        self.top_container.add_widget(logo)
        root.add_widget(self.top_container)

        # ── Screens ─────────────────────────────────────────────────────────────
        self.sm = ScreenManager()
        self.sm.size_hint_y = 1
        self.sm.add_widget(FeedScreen(name="feed"))
        self.sm.add_widget(ExploreScreen(name="explore"))
        self.sm.add_widget(LooksScreen(name="looks"))
        self.sm.add_widget(CartScreen(name="cart"))
        self.sm.add_widget(ProfileScreen(name="profile"))
        self.sm.add_widget(LoginScreen(name="login"))
        self.sm.add_widget(ProductDetailScreen(name="detail"))
        root.add_widget(self.sm)

        # Pantalla inicial
        if store.current_user_id is None:
            self.sm.current = "login"
        else:
            self.sm.current = "feed"

        # ── Bottom nav (guardamos referencia) ───────────────────────────────────
        self.bottom_bar = BottomBar(on_select=self.switch_screen)
        root.add_widget(self.bottom_bar)

        # ── Ocultar/mostrar chrome según pantalla ───────────────────────────────
        self.sm.bind(current=lambda *_: self.update_chrome())
        self.update_chrome()

        return root

    def switch_screen(self, name: str) -> None:
        self.sm.current = name
        # update_chrome se dispara también por el bind, pero lo llamamos por si acaso
        self.update_chrome()

    def update_chrome(self):
        """Oculta top/bottom bar en login; las muestra en el resto."""
        on_login = (self.sm.current == "login")

        # Top bar
        self.top_container.disabled = on_login
        self.top_container.opacity = 0 if on_login else 1
        self.top_container.height = 0 if on_login else dp(56)

        # Bottom bar
        self.bottom_bar.disabled = on_login
        self.bottom_bar.opacity = 0 if on_login else 1
        self.bottom_bar.height = 0 if on_login else dp(54)


if __name__ == "__main__":
    PonsivApp().run()
