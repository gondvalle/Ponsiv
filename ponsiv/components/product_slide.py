from kivy.metrics import dp
from kivy.properties import ObjectProperty
from kivy.uix.floatlayout import FloatLayout
from kivymd.uix.card import MDCard
from kivymd.uix.fitimage import FitImage
from kivymd.uix.button import MDIconButton
from kivymd.uix.label import MDLabel
from ponsiv.components.image_icon import ImageToggleButton, icon_path

from ..store import store


def _round_image_chip(src_normal: str, src_selected: str | None = None,
                      pos_hint=None, selected=False, on_release=None) -> MDCard:
    """
    Crea el 'chip' blanco circular con tu imagen dentro.
    """
    wrap = MDCard(size_hint=(None, None), size=(dp(40), dp(40)),
                  radius=[dp(20)], elevation=0, md_bg_color=(1, 1, 1, 1),
                  pos_hint=pos_hint or {})
    btn = ImageToggleButton(
        normal_source=src_normal,
        selected_source=src_selected or src_normal,
        selected=selected,
        size_hint=(1, 1),
    )
    if on_release:
        btn.bind(on_release=on_release)
    wrap.add_widget(btn)
    wrap._img_btn = btn
    return wrap


class ProductSlide(FloatLayout):
    """
    Slide de producto a pantalla completa con:
      • Imagen full bleed
      • Tarjeta blanca flotante (abajo-izquierda) con título, marca y precio
      • Columna de iconos flotantes (derecha), círculos blancos
    """
    product = ObjectProperty()

    def __init__(self, product, **kwargs):
        super().__init__(**kwargs)
        self.product = product

        # ── Imagen a pantalla completa ────────────────────────────────────────────
        self.img_card = MDCard(
            size_hint=(1, 1),
            pos_hint={"x": 0, "y": 0},
            radius=[0],
            elevation=0,
        )
        if product.images:
            self.img_card.add_widget(
                FitImage(source=product.images[0], size_hint=(1, 1))
            )
        self.add_widget(self.img_card)

        # ── Tarjeta blanca de info como en el mock ───────────────────────────────
        info = MDCard(
            size_hint=(0.6, None),
            height=dp(86),
            pos_hint={"x": 0.05, "y": 0.06},
            md_bg_color=(1, 1, 1, 1),
            radius=[dp(16)],
            elevation=0,
        )

        # Contenido textual
        box = FloatLayout()
        # Título (1ª línea)
        box.add_widget(
            MDLabel(
                text=self.product.title,
                font_size="15sp",
                bold=True,
                theme_text_color="Custom",
                text_color=(0, 0, 0, 1),
                size_hint=(1, None),
                height=dp(24),
                pos_hint={"x": 0.05, "y": 0.55},
            )
        )
        # Marca (2ª línea)
        box.add_widget(
            MDLabel(
                text=self.product.brand,
                font_size="13sp",
                theme_text_color="Custom",
                text_color=(0, 0, 0, 0.7),
                size_hint=(1, None),
                height=dp(20),
                pos_hint={"x": 0.05, "y": 0.32},
            )
        )
        # Precio (3ª línea)
        box.add_widget(
            MDLabel(
                text=f"{self.product.price:.2f} €",
                font_size="13sp",
                bold=True,
                theme_text_color="Custom",
                text_color=(0, 0, 0, 1),
                size_hint=(1, None),
                height=dp(20),
                pos_hint={"x": 0.05, "y": 0.08},
            )
        )
        info.add_widget(box)
        self.add_widget(info)

        # ── Columna de iconos flotantes (derecha) estilo "chips" blancos ────────
        # Orden como en la imagen: corazón, paper-plane (share), comment, t-shirt
        base_y = 0.60
        step = 0.10

        heart_normal = icon_path("actions", "heart", "normal")
        heart_selected = icon_path("actions", "heart", "selected")
        if heart_normal:
            liked = store.current_user_id and store.is_product_liked(store.current_user_id, self.product.id)
            self.heart_chip = _round_image_chip(
                heart_normal, heart_selected,
                pos_hint={"center_x": 0.93, "center_y": base_y},
                selected=bool(liked),
                on_release=self.toggle_like,
            )
            self.add_widget(self.heart_chip)
        else:
            self.heart_btn = self._round_icon(
                "heart-outline", pos_hint={"center_x": 0.93, "center_y": base_y}
            )
            self.heart_btn.bind(on_release=self.toggle_like)
            if store.current_user_id and store.is_product_liked(store.current_user_id, self.product.id):
                self.heart_btn.icon = "heart"
            self.add_widget(self.heart_btn)

        pairs = [
            ("send", base_y - 1 * step),
            ("comment", base_y - 2 * step),
            ("tshirt", base_y - 3 * step),
        ]
        for name, cy in pairs:
            normal = icon_path("actions", name, "normal")
            if normal:
                chip = _round_image_chip(normal, pos_hint={"center_x": 0.93, "center_y": cy})
                self.add_widget(chip)
            else:
                fallback = {
                    "send": "send-outline",
                    "comment": "comment-outline",
                    "tshirt": "tshirt-crew",
                }[name]
                self.add_widget(
                    self._round_icon(
                        fallback, pos_hint={"center_x": 0.93, "center_y": cy}
                    )
                )

    def _round_icon(self, icon_name: str, pos_hint: dict) -> MDIconButton:
        """
        Botón circular blanco pequeño con icono gris oscuro, como en el mock.
        """
        btn = MDIconButton(
            icon=icon_name,
            theme_text_color="Custom",
            text_color=(0, 0, 0, 0.8),
            md_bg_color=(1, 1, 1, 1),
            icon_size="20sp",
            size_hint=(None, None),
            pos_hint=pos_hint,
        )
        # Forzamos el tamaño para que sea circular pequeño (≈40×40)
        btn.size = (dp(40), dp(40))
        btn.radius = [dp(20)]
        return btn

    def toggle_like(self, *_):
        if not store.current_user_id:
            return
        liked = store.toggle_like(store.current_user_id, self.product.id)
        if hasattr(self, "heart_chip"):
            self.heart_chip._img_btn.selected = liked
        if hasattr(self, "heart_btn"):
            self.heart_btn.icon = "heart" if liked else "heart-outline"
