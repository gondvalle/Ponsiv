from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel, MDIcon
from kivymd.uix.button import MDFlatButton
from kivymd.uix.fitimage import FitImage
from kivymd.uix.dialog import MDDialog
from kivy.uix.filechooser import FileChooserIconView
import os

from ..store import store


class ProfileScreen(MDScreen):
    dialog = None

    def on_pre_enter(self, *args):
        self.clear_widgets()
        layout = MDBoxLayout(orientation="vertical", padding=20, spacing=20)
        user = store.get_user(store.current_user_id) if store.current_user_id else None

        if user and user.avatar_path:
            self.avatar_widget = FitImage(source=user.avatar_path, size_hint=(None, None), size=(150, 150))
        else:
            self.avatar_widget = MDIcon(icon="account-circle", halign="center", font_size="64sp")
        layout.add_widget(self.avatar_widget)
        layout.add_widget(MDFlatButton(text="Change Photo", on_release=self.open_file_chooser))

        name = user.name if user else "Guest"
        layout.add_widget(MDLabel(text=f"{name}", halign="center"))

        liked_ids = store.get_liked_product_ids(store.current_user_id) if store.current_user_id else []
        for pid in liked_ids:
            product = store.products.get(pid)
            if product:
                layout.add_widget(MDLabel(text=product.title, halign="center"))

        self.add_widget(layout)

    def open_file_chooser(self, *_):
        chooser = FileChooserIconView(
            path=os.path.expanduser("~"),
            filters=["*.png", "*.jpg", "*.jpeg"],
            show_hidden=False,
        )
        self.dialog = MDDialog(
            title="Select Avatar",
            type="custom",
            content_cls=chooser,
            buttons=[MDFlatButton(text="Close", on_release=lambda *x: self.dialog.dismiss())],
        )
        chooser.bind(on_selection=self._file_selected)
        self.dialog.open()

    def _file_selected(self, chooser, selection):
        if selection:
            path = selection[0]
            store.update_user_avatar(store.current_user_id, path)
            self.dialog.dismiss()
            self.on_pre_enter()
