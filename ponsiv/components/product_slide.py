from kivy.graphics import Color, Ellipse, RoundedRectangle
from kivy.metrics import dp
from kivy.properties import ObjectProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivymd.uix.card import MDCard
from kivymd.uix.fitimage import FitImage
from kivymd.uix.button import MDIconButton
from kivymd.uix.label import MDLabel


class ProductSlide(FloatLayout):
    """Slide showing a single product with image and overlaid info."""

    product = ObjectProperty()

    def __init__(self, product, **kwargs):
        super().__init__(**kwargs)
        self.product = product

        self.img_card = MDCard(
            size_hint=(0.97, None),
            pos_hint={"center_x": 0.5, "y": 0.01},
            radius=[dp(20)],
            elevation=0,
        )
        if product.images:
            self.img_card.add_widget(FitImage(source=product.images[0]))
        self.add_widget(self.img_card)

        # ensure the image card adapts to the available space of the screen
        self.bind(size=self._update_layout)

        info_card = MDCard(
            size_hint=(0.9, None),
            height=dp(120),
            pos_hint={"center_x": 0.5, "y": 0.06},
            md_bg_color=(0, 0, 0, 0.6),
            radius=[dp(16)],
            elevation=0,
        )

        fl = FloatLayout(size_hint=(1, 1))

        if product.logo:
            with fl.canvas.before:
                Color(1, 1, 1, 1)
                Ellipse(
                    pos=(dp(27), info_card.height - dp(40) + dp(13)),
                    size=(dp(48), dp(48)),
                )
            fl.add_widget(
                Image(
                    source=product.logo,
                    size_hint=(None, None),
                    size=(dp(40), dp(40)),
                    pos=(dp(32), info_card.height - dp(40) + dp(17)),
                )
            )

        fl.add_widget(
            MDLabel(
                text=product.title,
                font_size="16sp",
                bold=True,
                theme_text_color="Custom",
                text_color=(1, 1, 1, 1),
                size_hint=(None, None),
                size=(dp(250), dp(20)),
                pos=(dp(80), info_card.height - dp(40) + dp(40)),
            )
        )

        fl.add_widget(
            MDLabel(
                text=product.brand,
                font_size="14sp",
                theme_text_color="Custom",
                text_color=(0.8, 0.8, 0.8, 1),
                size_hint=(None, None),
                size=(dp(100), dp(20)),
                pos=(dp(80), info_card.height - dp(40) + dp(20)),
            )
        )

        fl.add_widget(
            MDLabel(
                text=", ".join(product.sizes),
                font_size="12sp",
                theme_text_color="Custom",
                text_color=(0.8, 0.8, 0.8, 1),
                size_hint=(None, None),
                size=(dp(200), dp(18)),
                pos=(dp(230), info_card.height - dp(40) - dp(30)),
            )
        )

        fl.add_widget(
            MDLabel(
                text=f"{product.price:.2f} €",
                font_size="14sp",
                bold=True,
                theme_text_color="Custom",
                text_color=(1, 1, 1, 1),
                size_hint=(None, None),
                size=(dp(100), dp(20)),
                pos=(dp(29), info_card.height - dp(40) - dp(30)),
            )
        )

        info_card.add_widget(fl)
        self.add_widget(info_card)

        pw, ph = 0.18, 0.36
        px, py = 1 - pw - 0.07, 0.5 - ph / 2
        with self.canvas.before:
            Color(0, 0, 0, 0.4)
            self._rect = RoundedRectangle(radius=[dp(30)])

        # update rectangle and image sizes when layout changes
        self._pw, self._ph, self._px, self._py = pw, ph, px, py
        icons = ["heart-outline", "bookmark-outline", "share", "tshirt-crew"]
        for i, ic in enumerate(icons):
            btn = MDIconButton(
                icon=ic,
                icon_size="20sp",
                theme_text_color="Custom",
                text_color=(1, 1, 1, 1),
                size_hint=(None, None),
                size=("30sp", "30sp"),
                pos_hint={"x": px + (pw - 0.05) / 2, "y": py + ph - 0.15 - i * 0.06},
            )
            self.add_widget(btn)

    def _update_layout(self, *args):
        """Resize image card and overlay rectangle to fit current screen."""
        available_height = self.height - dp(15)
        self.img_card.height = available_height
        self._rect.pos = (self.width * self._px, self.height * self._py)
        self._rect.size = (self.width * self._pw, self.height * self._ph)
