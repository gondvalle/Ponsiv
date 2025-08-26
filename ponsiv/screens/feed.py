from kivy.uix.carousel import Carousel
from kivymd.uix.screen import MDScreen

from ..components.product_slide import ProductSlide
from ..store import store

class FeedScreen(MDScreen):
    """Screen displaying products in a vertical carousel."""

    def on_pre_enter(self, *args):
        if self.children:
            return
        carousel = Carousel(direction="bottom", loop=False, size_hint=(1, 1))
        for product in store.products.values():
            carousel.add_widget(ProductSlide(product, size_hint=(1, 1)))
        self.add_widget(carousel)
