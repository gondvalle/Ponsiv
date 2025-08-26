# ponsiv/screens/detail.py
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout

from ..components.product_slide import ProductSlide
from ..store import store


class ProductDetailScreen(MDScreen):
    """Muestra un producto en grande con la misma UI del feed (ProductSlide)."""

    def show_product(self, product_id: str):
        self.clear_widgets()
        product = store.products.get(product_id)
        if not product:
            return
        root = MDBoxLayout(orientation="vertical")
        root.add_widget(ProductSlide(product, size_hint=(1, 1)))
        self.add_widget(root)
