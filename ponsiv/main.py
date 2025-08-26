from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.bottomnavigation import MDBottomNavigation, MDBottomNavigationItem

from .screens.feed import FeedScreen
from .screens.explore import ExploreScreen
from .screens.looks import LooksScreen
from .screens.cart import CartScreen
from .screens.profile import ProfileScreen
from .screens.login import LoginScreen

Window.size = (360, 640)


class PonsivApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"

        root = MDBoxLayout(orientation="vertical")
        root.add_widget(MDTopAppBar(title="Ponsiv"))

        self.sm = ScreenManager()
        self.sm.add_widget(FeedScreen(name="feed"))
        self.sm.add_widget(ExploreScreen(name="explore"))
        self.sm.add_widget(LooksScreen(name="looks"))
        self.sm.add_widget(CartScreen(name="cart"))
        self.sm.add_widget(ProfileScreen(name="profile"))
        self.sm.add_widget(LoginScreen(name="login"))
        root.add_widget(self.sm)

        nav = MDBottomNavigation()
        for name, text, icon in [
            ("feed", "Feed", "home"),
            ("explore", "Explore", "compass"),
            ("looks", "Looks", "image-multiple"),
            ("cart", "Cart", "cart"),
            ("profile", "Profile", "account"),
        ]:
            item = MDBottomNavigationItem(name=name, text=text, icon=icon)
            item.bind(on_tab_press=lambda instance, n=name: self.switch_screen(n))
            nav.add_widget(item)
        root.add_widget(nav)
        return root

    def switch_screen(self, name: str) -> None:
        self.sm.current = name


if __name__ == "__main__":
    PonsivApp().run()
