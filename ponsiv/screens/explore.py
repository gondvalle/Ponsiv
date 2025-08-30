from pathlib import Path
import random
from kivy.metrics import dp
from kivy.uix.scrollview import ScrollView
from kivy.uix.floatlayout import FloatLayout

from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.fitimage import FitImage
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDIconButton
from kivymd.uix.chip import MDChip
from kivymd.uix.textfield import MDTextField

from ..store import store
from ponsiv.components.image_icon import single_icon_path

IOS_BG = (0.965, 0.973, 0.985, 1)
IOS_TEXT = (0, 0, 0, 1)
IOS_SUB = (0, 0, 0, 0.6)
CHIP_BG = (0.93, 0.94, 0.96, 1)
CHIP_BG_ACTIVE = (0.85, 0.88, 0.92, 1)

# Qué consideramos "verano"
SUMMER_CATS = ("Vestidos", "Camisetas", "Tops", "Bermudas")


class ExploreScreen(MDScreen):
    def on_pre_enter(self, *args):
        if getattr(self, "_initialized", False):
            self._apply_active_filters()
            return

        self._selected_category = None  # categoría elegida en tarjetas o banner

        # Scroll raíz
        root_scroll = ScrollView(size_hint=(1, 1))
        root = MDBoxLayout(
            orientation="vertical",
            padding=(dp(12), dp(10)),
            spacing=dp(12),
            size_hint_y=None,
        )
        root.bind(minimum_height=root.setter("height"))
        root_scroll.add_widget(root)
        self.add_widget(root_scroll)

        # ---------- HERO BANNER (ARRIBA, CLICKABLE "VERANO") ----------
        banner_card = MDCard(
            size_hint=(1, None),
            height=dp(140),
            radius=[dp(16)],
            elevation=0,
            md_bg_color=(1, 1, 1, 1),
        )
        fl = FloatLayout()
        img_src = self._get_banner_image()
        if img_src:
            fl.add_widget(FitImage(source=img_src, size_hint=(1, 1)))
        fl.add_widget(MDLabel(
            text="VERANO",
            bold=True,
            font_size="28sp",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
            pos_hint={"x": 0.05, "center_y": 0.5},
        ))
        banner_card.add_widget(fl)
        # Tap → filtro verano
        def _banner_tap(inst, touch):
            if inst.collide_point(*touch.pos):
                self._selected_category = "__summer__"
                self._active_chip = "Todos"
                self._apply_active_filters()
                return True
            return False
        banner_card.bind(on_touch_up=_banner_tap)
        root.add_widget(banner_card)

        # ---------- CONTENIDO con FONDO BLANCO opaco (no se ve el banner detrás) ----------
        content_wrap = MDBoxLayout(orientation="vertical", spacing=dp(12), size_hint_y=None)
        content_wrap.bind(minimum_height=content_wrap.setter("height"))
        from kivy.graphics import Color, Rectangle
        with content_wrap.canvas.before:
            Color(1, 1, 1, 1)
            _bg = Rectangle(pos=content_wrap.pos, size=content_wrap.size)
        def _sync_bg(*_):
            _bg.pos = content_wrap.pos
            _bg.size = content_wrap.size
        content_wrap.bind(pos=_sync_bg, size=_sync_bg)
        root.add_widget(content_wrap)

        # ---------- BUSCADOR ----------
        search_card = MDCard(
            size_hint=(1, None),
            height=dp(44),
            radius=[dp(22)],
            elevation=0,
            md_bg_color=IOS_BG,
            padding=(dp(10), 0),
        )
        row = MDBoxLayout(orientation="horizontal", spacing=dp(6))
        lupa_src = single_icon_path("search", "magnify")
        if lupa_src:
            row.add_widget(FitImage(source=lupa_src, size_hint=(None, None), size=(dp(22), dp(22))))
        else:
            row.add_widget(MDIconButton(icon="magnify", theme_text_color="Custom", text_color=IOS_SUB, icon_size="22sp"))
        self.search_tf = MDTextField(hint_text="Buscar marcas, estilos o prendas...", size_hint_x=1)
        # ocultar subrayado
        for prop in ("line_color_normal", "line_color_focus", "line_color_disabled",
                     "error_color", "hint_text_color_normal", "hint_text_color_focus"):
            try:
                setattr(self.search_tf, prop, (0, 0, 0, 0))
            except Exception:
                pass
        try:
            self.search_tf.mode = "fill"
            self.search_tf.fill_color_normal = IOS_BG
            self.search_tf.fill_color_focus = IOS_BG
        except Exception:
            pass
        self.search_tf.bind(text=lambda *_: self._apply_active_filters())
        row.add_widget(self.search_tf)
        search_card.add_widget(row)
        content_wrap.add_widget(search_card)

        # ---------- CHIPS (puedes dejarlos, pero “Verano” ya lo hace el banner) ----------
        chips_scroll = ScrollView(size_hint=(1, None), height=dp(40), do_scroll_y=False)
        self.chips_row = MDBoxLayout(orientation="horizontal", spacing=dp(8), padding=(dp(2), 0), size_hint_x=None)
        self.chips_row.bind(minimum_width=self.chips_row.setter("width"))
        chips_scroll.add_widget(self.chips_row)
        content_wrap.add_widget(chips_scroll)

        self._chip_filters = {
            "Todos": [],
            "Camisas": ["CAMISA"],
            "Zapatillas": ["ZAPATILLA", "SNEAKER", "NIKE", "ADIDAS"],
            "Pantalones": ["PANTALON", "PANTALÓN"],
            "Chaquetas": ["CHAQUETA", "SOBRECAMISA"],
            "Vestidos": ["VESTIDO"],
            "Tops": ["TOP"],
            "Camisetas": ["CAMISETA"],
        }
        self._chips, self._active_chip = [], "Todos"
        for label in self._chip_filters.keys():
            chip = MDChip(text=label)
            try:
                chip.md_bg_color = CHIP_BG
                chip.text_color = IOS_TEXT
                chip.radius = [dp(16)]
            except Exception:
                pass
            chip.bind(on_release=lambda inst, l=label: self._select_chip(inst, l))
            self.chips_row.add_widget(chip)
            self._chips.append(chip)

        # ---------- TENDENCIAS ----------
        content_wrap.add_widget(self._section_title("Tendencias del momento"))
        self.trend_scroll = ScrollView(size_hint=(1, None), height=dp(200), do_scroll_y=False)
        self.trend_row = MDBoxLayout(orientation="horizontal", spacing=dp(10), padding=(dp(2), 0), size_hint_x=None)
        self.trend_row.bind(minimum_width=self.trend_row.setter("width"))
        self.trend_scroll.add_widget(self.trend_row)
        content_wrap.add_widget(self.trend_scroll)

        # separador fino
        content_wrap.add_widget(self._hairline())

        # ---------- CATEGORÍAS (por JSON) ----------
        content_wrap.add_widget(self._section_title("Categorías"))
        cat_scroll = ScrollView(size_hint=(1, None), height=dp(120), do_scroll_y=False)
        self.cat_row = MDBoxLayout(orientation="horizontal", spacing=dp(10), padding=(dp(2), 0), size_hint_x=None)
        self.cat_row.bind(minimum_width=self.cat_row.setter("width"))
        cat_scroll.add_widget(self.cat_row)
        content_wrap.add_widget(cat_scroll)

        self._render_categories_dynamic()

        # primera carga
        self._apply_active_filters()
        self._initialized = True

    # --------------------------- helpers UI ---------------------------
    def _section_title(self, txt: str) -> MDLabel:
        return MDLabel(text=txt, bold=True, font_size="16sp",
                       theme_text_color="Custom", text_color=IOS_TEXT,
                       size_hint=(1, None), height=dp(24))

    def _hairline(self):
        box = MDBoxLayout(size_hint=(1, None), height=dp(1), opacity=0.9)
        from kivy.graphics import Color, Rectangle
        with box.canvas:
            Color(0, 0, 0, 0.08)
            rect = Rectangle(pos=box.pos, size=box.size)
        def _upd(*_):
            rect.pos = box.pos
            rect.size = box.size
        box.bind(pos=_upd, size=_upd)
        return box

    def _get_banner_image(self) -> str | None:
        base = Path(__file__).resolve().parents[2] / "assets" / "banners"
        for name in ("verano.png", "verano.jpg", "verano.jpeg"):
            p = base / name
            if p.exists():
                return str(p)
        # fallback
        for p in store.products.values():
            if p.images:
                return p.images[0]
        return None

    def _render_trending(self, products):
        from kivymd.uix.card import MDCard
        self.trend_row.clear_widgets()
        for p in products:
            card = MDCard(size_hint=(None, None), size=(dp(120), dp(180)),
                          radius=[dp(12)], elevation=0, md_bg_color=(1, 1, 1, 1))
            v = MDBoxLayout(orientation="vertical")
            if p.images:
                v.add_widget(FitImage(source=p.images[0], size_hint=(1, 1)))
            else:
                v.add_widget(MDLabel(text="Sin imagen", halign="center"))
            info = MDBoxLayout(orientation="vertical", size_hint=(1, None), height=dp(54), padding=(dp(8), dp(6)))
            info.add_widget(MDLabel(text=p.brand or "", font_size="12sp",
                                    theme_text_color="Custom", text_color=(0, 0, 0, 0.9)))
            info.add_widget(MDLabel(text=f"{p.price:.2f} €", font_size="13sp", bold=True,
                                    theme_text_color="Custom", text_color=(0, 0, 0, 1)))
            v.add_widget(info)
            card.add_widget(v)
            card.bind(on_touch_up=lambda inst, touch, pid=p.id: self._open_detail_if_hit(inst, touch, pid))
            self.trend_row.add_widget(card)

    def _render_categories_dynamic(self):
        """Dibuja categorías a partir del campo 'categoria' de los JSON y
        usa una IMAGEN ALEATORIA de un producto de esa categoría."""
        from kivymd.uix.card import MDCard
        self.cat_row.clear_widgets()
        cats = store.get_categories()
        if not cats:
            return
        for cat in cats:
            prods = [p for p in store.get_products_by_category(cat) if p.images]
            thumb = random.choice(prods).images[0] if prods else None

            wrap = MDBoxLayout(orientation="vertical", size_hint=(None, None), size=(dp(82), dp(110)))
            box = MDCard(size_hint=(1, None), height=dp(78), radius=[dp(14)], elevation=0, md_bg_color=(1, 1, 1, 1))
            if thumb:
                box.add_widget(FitImage(source=thumb, size_hint=(1, 1)))
            wrap.add_widget(box)
            wrap.add_widget(MDLabel(text=cat, halign="center", font_size="12sp",
                                    theme_text_color="Custom", text_color=(0, 0, 0, 0.9),
                                    size_hint=(1, None), height=dp(26)))
            # Tap → filtra por categoría
            def _tap(inst, touch, c=cat):
                if inst.collide_point(*touch.pos):
                    self._selected_category = c
                    self._active_chip = "Todos"
                    self._apply_active_filters()
                    return True
                return False
            wrap.bind(on_touch_up=_tap)
            self.cat_row.add_widget(wrap)

    # --------------------------- interacción & filtros ---------------------------
    def _select_chip(self, chip: MDChip, label: str):
        for c in self._chips:
            try:
                c.icon = ""
                c.md_bg_color = CHIP_BG
                c.text_color = IOS_TEXT
            except Exception:
                pass
        try:
            chip.icon = "check"
            chip.md_bg_color = CHIP_BG_ACTIVE
            chip.text_color = IOS_TEXT
        except Exception:
            pass
        self._active_chip = label
        self._selected_category = None  # si tocas chip, sales de un filtro de categoría
        self._apply_active_filters()

    def _apply_active_filters(self):
        items = list(store.products.values())

        # 1) Filtro por categoría elegida (banner o tarjeta)
        if self._selected_category:
            if self._selected_category == "__summer__":
                items = [p for p in items if (p.category in SUMMER_CATS)]
            else:
                items = [p for p in items if (p.category == self._selected_category)]
        else:
            # 2) Chips (si no hay categoría activa)
            kws = self._chip_filters.get(self._active_chip or "Todos", [])
            if kws:
                up = lambda s: (s or "").upper()
                items = [p for p in items if any(k in up(p.title) for k in kws)]

        # 3) Texto búsqueda
        q = (self.search_tf.text or "").strip().lower()
        if q:
            items = [p for p in items if q in (p.title or "").lower() or q in (p.brand or "").lower()]

        # 4) Ordenar por likes
        items = store.sort_products_by_likes(items)
        self._render_trending(items)

    def _open_detail_if_hit(self, widget, touch, product_id: str):
        if widget.collide_point(*touch.pos):
            detail = self.manager.get_screen("detail")
            detail.show_product(product_id)
            self.manager.current = "detail"
            return True
        return False

