from kivy.metrics import dp
from kivy.uix.gridlayout import GridLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.graphics import Color, Rectangle

from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.fitimage import FitImage
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.label import MDLabel
from kivymd.uix.chip import MDChip

from ..store import store

IOS_BG = (0.96, 0.97, 0.98, 1)
IOS_TEXT = (0, 0, 0, 1)
IOS_SUBTEXT = (0, 0, 0, 0.55)
IOS_CARD = (1, 1, 1, 1)


class LoginScreen(MDScreen):
    """
    Autenticación estilo iOS compacto:
      - Toggle Iniciar / Crear (sin solapes)
      - Login minimal
      - Registro con Edad / Ciudad / Sexo
    """
    mode = "login"  # 'login' | 'signup'

    def on_pre_enter(self, *args):
        self.clear_widgets()

        root = MDBoxLayout(orientation="vertical", padding=(dp(16), dp(8)), spacing=dp(8))
        root.md_bg_color = IOS_BG

        # Logo compacto
        logo_bar = AnchorLayout(size_hint=(1, None), height=dp(56), anchor_x="center", anchor_y="center")
        logo = FitImage(source="assets/logos/Ponsiv.png", size_hint=(None, None), size=(dp(128), dp(38)))
        logo_bar.add_widget(logo)
        root.add_widget(logo_bar)

        # Título + subtítulo
        titles = MDBoxLayout(orientation="vertical", spacing=dp(2), size_hint=(1, None), height=dp(60))
        titles.add_widget(MDLabel(text="Bienvenido a Ponsiv", font_size="20sp", bold=True,
                                  theme_text_color="Custom", text_color=IOS_TEXT))
        self.subtitle = MDLabel(text="Inicia sesión para continuar", font_size="13sp",
                                theme_text_color="Custom", text_color=IOS_SUBTEXT)
        titles.add_widget(self.subtitle)
        root.add_widget(titles)

        # Toggle: Iniciar / Crear  (sin props conflictivas)
        toggle = MDBoxLayout(orientation="horizontal", spacing=dp(6), size_hint=(1, None), height=dp(40))
        self.btn_tab_login = MDRaisedButton(text="Iniciar", on_release=lambda *_: self._switch("login"), height=dp(40))
        self.btn_tab_signup = MDFlatButton(text="Crear", on_release=lambda *_: self._switch("signup"), height=dp(40))
        toggle.add_widget(self.btn_tab_login)
        toggle.add_widget(self.btn_tab_signup)
        root.add_widget(toggle)

        # Contenedor del formulario (solo 1 a la vez)
        self.form_host = MDBoxLayout(orientation="vertical", size_hint=(1, 1))
        root.add_widget(self.form_host)

        # Mensaje de estado
        self.message = MDLabel(text="", halign="center",
                               theme_text_color="Custom", text_color=(0.8, 0.1, 0.1, 1),
                               size_hint=(1, None), height=dp(20))
        root.add_widget(self.message)

        # Primera render
        self.add_widget(root)
        self._render()

    # ───────────── helpers UI ─────────────
    def _filled_field(self, hint: str, password: bool = False) -> MDCard:
        card = MDCard(md_bg_color=IOS_CARD, radius=[dp(12)], size_hint=(1, None),
                      height=dp(48), elevation=0, padding=(dp(10), 0))
        tf = MDTextField(hint_text=hint, password=password)
        card.add_widget(tf)
        return card

    def _hairline(self) -> MDBoxLayout:
        # Línea fina opcional por si quieres separadores
        box = MDBoxLayout(size_hint=(1, None), height=dp(1))
        with box.canvas:
            Color(0, 0, 0, 0.10)
            rect = Rectangle(pos=box.pos, size=box.size)
        def _upd(*_):
            rect.pos = box.pos
            rect.size = box.size
        box.bind(pos=_upd, size=_upd)
        return box

    # ───────────── construir formularios ─────────────
    def _build_login_form(self):
        wrap = MDBoxLayout(orientation="vertical", spacing=dp(8), size_hint=(1, None))
        # Campos
        email_card = self._filled_field("Email")
        pass_card = self._filled_field("Contraseña", password=True)
        self.login_email = email_card.children[0]
        self.login_password = pass_card.children[0]

        # Botón
        btn = MDRaisedButton(text="Iniciar sesión", size_hint=(1, None), height=dp(44),
                             on_release=self.handle_login)

        # Montaje
        wrap.add_widget(email_card)
        wrap.add_widget(pass_card)
        wrap.add_widget(btn)

        # Ajuste de altura total (48*2 + 44 + 8*2 = 156)
        wrap.size_hint_y = None
        wrap.height = dp(156)
        return wrap

    def _build_signup_form(self):
        wrap = MDBoxLayout(orientation="vertical", spacing=dp(8), size_hint=(1, None))

        email_card = self._filled_field("Email")
        pass_card = self._filled_field("Contraseña (mín. 6)", password=True)
        self.signup_email = email_card.children[0]
        self.signup_password = pass_card.children[0]

        # Grid Edad / Ciudad
        grid = GridLayout(cols=2, spacing=dp(8), size_hint=(1, None), height=dp(48))
        age_card = self._filled_field("Edad")
        city_card = self._filled_field("Ciudad")
        self.signup_age = age_card.children[0]
        self.signup_age.input_filter = "int"
        self.signup_city = city_card.children[0]
        grid.add_widget(age_card)
        grid.add_widget(city_card)

        # Sexo chips (compatibles 1.1.1)
        sex_box = MDBoxLayout(orientation="horizontal", spacing=dp(6), size_hint=(1, None), height=dp(34))
        sex_label = MDLabel(text="Sexo:", size_hint=(None, 1), width=dp(50),
                            theme_text_color="Custom", text_color=IOS_SUBTEXT)
        sex_box.add_widget(sex_label)
        self.sex_value = None
        self.sex_chips = []
        for label in ("Mujer", "Hombre", "Otro"):
            chip = MDChip(text=label)  # sin 'check' en 1.1.1
            chip.bind(on_release=lambda inst, l=label: self._select_sex(inst, l))
            self.sex_chips.append(chip)
            sex_box.add_widget(chip)

        btn = MDRaisedButton(text="Crear cuenta", size_hint=(1, None), height=dp(44),
                             on_release=self.handle_signup)

        wrap.add_widget(email_card)
        wrap.add_widget(pass_card)
        wrap.add_widget(grid)
        wrap.add_widget(sex_box)
        wrap.add_widget(btn)

        # Altura aprox: 48*4 + 44 + 8*4 = 252
        wrap.size_hint_y = None
        wrap.height = dp(252)
        return wrap

    # ───────────── render / toggle ─────────────
    def _switch(self, mode: str):
        if mode == self.mode:
            return
        self.mode = mode
        self._render()

    def _render(self):
        # 1) estilo del toggle
        if self.mode == "login":
            self.btn_tab_login.disabled = True
            self.btn_tab_login.elevation = 0
            self.btn_tab_signup.disabled = False
            self.subtitle.text = "Inicia sesión para continuar"
        else:
            self.btn_tab_login.disabled = False
            self.btn_tab_signup.disabled = True
            self.btn_tab_signup.elevation = 0
            self.subtitle.text = "Crea una cuenta para una experiencia personalizada"

        # 2) quitar formulario previo y poner el actual (sin overlays)
        self.form_host.clear_widgets()
        if self.mode == "login":
            self.form_host.add_widget(self._build_login_form())
        else:
            self.form_host.add_widget(self._build_signup_form())

        # 3) limpiar mensajes
        self.message.text = ""

    # ───────────── acciones ─────────────
    def _select_sex(self, chip: MDChip, value: str):
        for c in self.sex_chips:
            c.active = (c is chip)
        self.sex_value = value

    def handle_login(self, *_):
        email = (self.login_email.text or "").strip()
        password = self.login_password.text or ""
        if not email or not password:
            self.message.text = "Introduce email y contraseña."
            return

        user_id = store.authenticate_user(email, password)
        if user_id is None:
            if store.get_user_by_email(email) is not None:
                self.message.text = "Contraseña incorrecta."
                return
            self.message.text = "No existe esa cuenta. Pulsa 'Crear'."
            return

        store.current_user_id = user_id
        self.manager.current = "feed"

    def handle_signup(self, *_):
        email = (self.signup_email.text or "").strip()
        password = self.signup_password.text or ""
        age_txt = (self.signup_age.text or "").strip()
        city = (self.signup_city.text or "").strip()
        sex = self.sex_value

        if not email or not password:
            self.message.text = "Email y contraseña son obligatorios."
            return
        if len(password) < 6:
            self.message.text = "La contraseña debe tener 6+ caracteres."
            return

        age = int(age_txt) if age_txt.isdigit() else None

        if store.get_user_by_email(email) is not None:
            self.message.text = "Ese email ya está registrado. Inicia sesión."
            self._switch("login")
            return

        user_id = store.create_user(email, password, age=age, city=city or None, sex=sex or None)
        store.current_user_id = user_id
        self.manager.current = "feed"
