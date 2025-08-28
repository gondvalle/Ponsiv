import random

from kivy.uix.carousel import Carousel
from kivymd.uix.screen import MDScreen
from ..components.product_slide import ProductSlide
from ..store import store


class FeedScreen(MDScreen):
    """
    Feed con scroll infinito:
      - Cada 'vuelta' es una permutación aleatoria de todos los productos.
      - Poda de memoria: mantenemos como mucho `max_chunks` vueltas en el carrusel.
    """
    def on_pre_enter(self, *args):
        if hasattr(self, "_initialized") and self._initialized:
            return

        self.carousel = Carousel(direction="bottom", loop=False, size_hint=(1, 1))
        self.add_widget(self.carousel)

        # --- Parámetros de ventana/memoria ---
        self.chunk_size = max(1, len(store.products))  # nº de slides por vuelta
        self.max_chunks = 3                            # mantén 3 vueltas en memoria (ajústalo)
        self._chunks_loaded = 0

        # Semilla inicial: dos vueltas para suavidad
        self._append_random_chunk()
        self._append_random_chunk()

        # Extiende cuando te acerques al final
        self.carousel.bind(index=self._maybe_extend)

        self._initialized = True

    # ---------- lógica de "vuelta" aleatoria ----------
    def _append_random_chunk(self):
        """Añade una vuelta (todos los productos barajados) al final."""
        items = list(store.products.values())
        if not items:
            return
        random.shuffle(items)
        for product in items:
            self.carousel.add_widget(ProductSlide(product, size_hint=(1, 1)))

        self._chunks_loaded += 1
        self._prune_if_needed()

    def _maybe_extend(self, *_):
        """Cuando queden 2 slides para el final, añade otra vuelta."""
        total = len(self.carousel.slides)
        idx = self.carousel.index
        if total - idx <= 2:
            self._append_random_chunk()

    # ---------- poda de memoria ----------
    def _prune_if_needed(self):
        """
        Si hay más de `max_chunks` vueltas cargadas, elimina la más antigua (primer bloque).
        Evita podar si el usuario aún está dentro de ese primer bloque.
        """
        # Mientras nos pasemos de la ventana permitida…
        while self._chunks_loaded > self.max_chunks:
            # Si el usuario está aún en el primer bloque, no podar (evita tirones).
            if self.carousel.index < self.chunk_size:
                # Salimos y ya se podará en el siguiente avance
                return

            # Elimina el bloque más antiguo (primeros `chunk_size` slides)
            old_index = self.carousel.index
            for _ in range(min(self.chunk_size, len(self.carousel.slides))):
                # defensivo: puede haber menos slides en estados intermedios
                if not self.carousel.slides:
                    break
                self.carousel.remove_widget(self.carousel.slides[0])

            # Recoloca el índice para seguir mostrando el mismo contenido lógico
            # (se ha corrido hacia atrás exactamente chunk_size posiciones).
            self.carousel.index = max(0, old_index - self.chunk_size)
            self._chunks_loaded -= 1

