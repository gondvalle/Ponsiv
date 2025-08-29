# ponsiv/screens/profile.py
from kivy.metrics import dp
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout

from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.fitimage import FitImage
from kivymd.uix.button import MDIconButton
from ponsiv.components.image_icon import ImageToggleButton, icon_path

from ..store import store


class ProfileScreen(MDScreen):
    """Perfil estilo iOS con grid de 'likes' y detalle on tap."""

    def on_pre_enter(self, *args):
        self.clear_widgets()

        user = store.get_user(store.current_user_id) if store.current_user_id else None
        likes = store.get_liked_product_ids(store.current_user_id) if store.current_user_id else []
        outfits_count = len(likes)

        root = MDBoxLayout(orientation="vertical", padding=(dp(16), dp(8)), spacing=dp(8))

        # ── Encabezado:  Foto, nombre, handle (en ese orden), todo centrado ──
        header = MDBoxLayout(orientation="vertical", spacing=dp(18), size_hint=(1, None))
        header.height = dp(160)

        # Foto (avatar) debajo
        avatar_wrap = MDCard(size_hint=(None, None), size=(dp(70), dp(70)),
                             radius=[dp(45)], elevation=0, md_bg_color=(1, 1, 1, 1))
        if user and user.avatar_path:
            avatar_wrap.add_widget(FitImage(source=user.avatar_path))
        else:
            avatar_wrap.add_widget(FitImage(source="assets/logos/Ponsiv.png"))
        avatar_row = MDBoxLayout(orientation="horizontal", size_hint=(1, None), height=dp(100))
        avatar_row.add_widget(MDBoxLayout(size_hint_x=1))
        avatar_row.add_widget(avatar_wrap)
        avatar_row.add_widget(MDBoxLayout(size_hint_x=1))
        header.add_widget(avatar_row)

        name = (user.name if (user and user.name) else "Usuario")
        handle = f"@{(user.handle if user and user.handle else 'ponsiver')}"

        header.add_widget(MDLabel(
            text=name, halign="center", font_size="20sp", bold=True,
            theme_text_color="Custom", text_color=(0, 0, 0, 1)
        ))
        header.add_widget(MDLabel(
            text=handle, halign="center", font_size="13sp",
            theme_text_color="Custom", text_color=(0, 0, 0, 0.65)
        ))


        # Métricas
        metrics = MDBoxLayout(orientation="horizontal", size_hint=(1, None), height=dp(40),
                              spacing=dp(16), padding=(dp(16), 0))
        metrics.add_widget(self._metric_column(outfits_count if outfits_count else 0, "Outfits"))
        metrics.add_widget(self._metric_column(0, "Siguiendo"))
        metrics.add_widget(self._metric_column(0, "Seguidores"))
        header.add_widget(metrics)

        root.add_widget(header)

        # Tabs (igual que antes)
        tabs = MDBoxLayout(orientation="horizontal", size_hint=(1, None), height=dp(40),
                           padding=(dp(8), 0), spacing=dp(16))

        _tab_names = [("tshirt", False), ("heart", True), ("file", False), ("shopping", False)]
        self._tab_btns = []
        for name, active in _tab_names:
            group = "actions"
            normal = icon_path(group, name if name != "file" else "file", "normal")
            selected = icon_path(group, name if name != "file" else "file", "selected")
            if normal:
                btn = ImageToggleButton(normal_source=normal, selected_source=selected or normal,
                                        selected=active, size_hint=(None, None), size=(dp(22), dp(22)))
            else:
                fallback = {
                    "tshirt": "tshirt-crew",
                    "heart": "heart",
                    "file": "file-document-outline",
                    "shopping": "shopping-outline",
                }[name]
                btn = MDIconButton(icon=fallback, theme_text_color="Custom",
                                   text_color=(0, 0, 0, 1 if active else 0.45), icon_size="22sp")
            tabs.add_widget(btn)
            self._tab_btns.append(btn)
        root.add_widget(tabs)

        # ── Grid de likes: 1 columna y tarjetas altas para ocupar más pantalla ──
        scroll = ScrollView(size_hint=(1, 1))
        grid = GridLayout(cols=2, padding=[dp(8), dp(8)], spacing=dp(10), size_hint_y=None)
        grid.bind(minimum_height=grid.setter("height"))

        for pid in likes:
            product = store.products.get(pid)
            if not product:
                continue
            grid.add_widget(self._product_card_big2col(product))

        if not likes:
            grid.add_widget(MDLabel(text="Aún no has dado like a ninguna prenda.",
                                    size_hint_y=None, height=dp(40),
                                    theme_text_color="Custom", text_color=(0, 0, 0, 0.6)))

        scroll.add_widget(grid)
        root.add_widget(scroll)

        self.add_widget(root)

    def _product_card_big2col(self, product) -> MDCard:
        """
        Tarjeta grande para grid de 2 columnas: imagen alta + franja inferior.
        Más grande que la versión anterior (height ~ 280 dp).
        """
        card = MDCard(size_hint=(1, None), height=dp(280), radius=[dp(16)],
                    elevation=0, md_bg_color=(1, 1, 1, 1))
        box = MDBoxLayout(orientation="vertical")

        # Imagen (ocupa la mayor parte)
        if product.images:
            box.add_widget(FitImage(source=product.images[0], size_hint=(1, 1)))
        else:
            box.add_widget(MDLabel(text="Sin imagen", halign="center"))

        # Franja inferior (marca y precio)
        info = MDBoxLayout(orientation="vertical", size_hint=(1, None), height=dp(56),
                        padding=(dp(10), dp(6)))
        info.add_widget(MDLabel(text=product.brand or "", font_size="12sp",
                                theme_text_color="Custom", text_color=(0, 0, 0, 0.8)))
        info.add_widget(MDLabel(text=f"{product.price:.2f} €", font_size="13sp", bold=True,
                                theme_text_color="Custom", text_color=(0, 0, 0, 1)))
        box.add_widget(info)

        card.add_widget(box)

        # Tap → detalle
        card.bind(on_touch_up=lambda inst, touch, pid=product.id:
                self._open_detail_if_hit(inst, touch, pid))
        return card



    # ───────────────────────── Helpers UI ───────────────────────────────────────
    def _metric_column(self, number: int, label: str) -> MDBoxLayout:
        col = MDBoxLayout(orientation="vertical")
        col.add_widget(MDLabel(text=str(number), halign="center", font_size="15sp",
                               bold=True, theme_text_color="Custom", text_color=(0, 0, 0, 1)))
        col.add_widget(MDLabel(text=label, halign="center", font_size="12sp",
                               theme_text_color="Custom", text_color=(0, 0, 0, 0.6)))
        return col

    def _product_card(self, product) -> MDCard:
        """
        Tarjeta clickable: imagen arriba + franja inferior con marca y precio.
        Al tocar, abre detalle a pantalla completa con ProductSlide.
        """
        card = MDCard(size_hint=(1, None), height=dp(220), radius=[dp(14)], elevation=0, md_bg_color=(1, 1, 1, 1))

        box = MDBoxLayout(orientation="vertical")
        # Imagen
        if product.images:
            box.add_widget(FitImage(source=product.images[0], size_hint=(1, 1)))
        else:
            box.add_widget(MDLabel(text="Sin imagen", halign="center"))

        # Franja inferior
        info = MDBoxLayout(orientation="vertical", size_hint=(1, None), height=dp(52), padding=(dp(10), dp(6)))
        info.add_widget(MDLabel(text=product.brand or "", font_size="12sp",
                                theme_text_color="Custom", text_color=(0, 0, 0, 0.8)))
        info.add_widget(MDLabel(text=f"{product.price:.2f} €", font_size="13sp", bold=True,
                                theme_text_color="Custom", text_color=(0, 0, 0, 1)))
        box.add_widget(info)

        card.add_widget(box)

        # Captura del toque
        card.bind(on_touch_up=lambda inst, touch, pid=product.id:
                  self._open_detail_if_hit(inst, touch, pid))
        return card

    def _open_detail_if_hit(self, widget, touch, product_id: str):
        if widget.collide_point(*touch.pos):
            detail = self.manager.get_screen("detail")
            detail.show_product(product_id)
            self.manager.current = "detail"
            return True
        return False
