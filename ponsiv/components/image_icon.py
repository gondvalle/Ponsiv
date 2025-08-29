from pathlib import Path
from kivy.properties import StringProperty, BooleanProperty
from kivy.uix.behaviors import ButtonBehavior
from kivymd.uix.fitimage import FitImage


class ImageToggleButton(ButtonBehavior, FitImage):
    """
    Botón basado en imagen con dos estados: normal / selected.
    - normal_source: ruta PNG para estado normal
    - selected_source: ruta PNG para estado seleccionado (opcional; si no, usa normal)
    - selected: bool que cambia la imagen mostrada
    """
    normal_source = StringProperty("")
    selected_source = StringProperty("")
    selected = BooleanProperty(False)

    def __init__(self, normal_source: str, selected_source: str | None = None,
                 selected: bool = False, **kwargs):
        super().__init__(**kwargs)
        self.normal_source = normal_source
        self.selected_source = selected_source or normal_source
        self.selected = selected
        self._refresh()

    def on_selected(self, *_):
        self._refresh()

    def _refresh(self):
        self.source = self.selected_source if self.selected else self.normal_source


def icon_path(group: str, name: str, state: str = "normal") -> str | None:
    """
    Devuelve 'assets/icons/<group>/<name>/<state>.png' si existe; si no, None.
    group: 'nav' | 'actions' | 'topbar'
    state: 'normal' | 'selected'
    """
    p = Path(__file__).resolve().parents[2] / "assets" / "icons" / group / name / f"{state}.png"
    return str(p) if p.exists() else None


def single_icon_path(group: str, name: str) -> str | None:
    """
    Para iconos de un solo estado, p.ej. search/magnify.png
    """
    p = Path(__file__).resolve().parents[2] / "assets" / "icons" / group / f"{name}.png"
    return str(p) if p.exists() else None
