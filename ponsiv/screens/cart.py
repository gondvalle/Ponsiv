from kivymd.uix.screen import MDScreen
from kivymd.uix.label import MDLabel
from ..store import store


class CartScreen(MDScreen):
    def on_pre_enter(self, *args):
        self.clear_widgets()
        if store.cart:
            items = "\n".join(str(pid) for pid in store.cart)
            text = f"Cart:\n{items}"
        else:
            text = "Cart is empty"
        self.add_widget(MDLabel(text=text, halign="center"))
