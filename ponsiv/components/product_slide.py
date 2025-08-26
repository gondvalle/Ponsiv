from kivy.properties import ObjectProperty
from kivymd.uix.card import MDCard
from kivymd.uix.image import FitImage
from kivymd.uix.label import MDLabel


class ProductSlide(MDCard):
    """Simple card displaying a product image and name."""

    product = ObjectProperty()

    def __init__(self, product, **kwargs):
        super().__init__(**kwargs)
        self.product = product
        self.orientation = "vertical"
        self.radius = [12]
        self.elevation = 2
        self.padding = 4

        if product.images:
            self.add_widget(FitImage(source=product.images[0]))
        self.add_widget(
            MDLabel(text=f"{product.title} - ${product.price:.2f}", halign="center")
        )
