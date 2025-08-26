import json
from pathlib import Path
from typing import Dict, List
from datetime import date

from .models import Product, Look, LookAuthor, User, Order


class PonsivStore:
    """In memory store for Ponsiv data and user cart/orders."""

    def __init__(self) -> None:
        self.products: Dict[str, Product] = {}
        self.looks: Dict[str, Look] = {}
        self.users: Dict[str, User] = {}
        self.orders: List[Order] = []
        self.cart: List[str] = []

    def load_seed(self) -> None:
        """Load product data from the ``assets`` directory.

        Each product has a JSON description in ``assets/informacion`` and an
        image with the same file name in ``assets/prendas``. Brand logos are
        located in ``assets/logos``. New products can be added simply by
        placing the corresponding JSON and image files in these folders.
        """
        base_path = Path(__file__).resolve().parent.parent / "assets"
        info_path = base_path / "informacion"
        image_path = base_path / "prendas"
        logo_path = base_path / "logos"

        for info_file in sorted(info_path.glob("*.json")):
            with open(info_file, "r", encoding="utf-8") as fh:
                data = json.load(fh)

            pid = info_file.stem
            brand = data.get("marca", "")
            title = data.get("nombre", pid)
            price = data.get("precio", 0.0)
            sizes = data.get("tallas", [])

            image_file = None
            for ext in (".jpg", ".png"):
                candidate = image_path / f"{pid}{ext}"
                if candidate.exists():
                    image_file = candidate
                    break
            images = [str(image_file)] if image_file else []

            logo_file = None
            for ext in (".png", ".jpg", ".jpeg"):
                candidate = logo_path / f"{brand}{ext}"
                if candidate.exists():
                    logo_file = candidate
                    break

            product = Product(
                id=pid,
                brand=brand,
                title=title,
                price=price,
                sizes=sizes,
                images=images,
                logo=str(logo_file) if logo_file else None,
            )
            self.products[product.id] = product

    # Cart management -----------------------------------------------------
    def add_to_cart(self, product_id: str) -> None:
        if product_id in self.products:
            self.cart.append(product_id)

    def remove_from_cart(self, product_id: str) -> None:
        if product_id in self.cart:
            self.cart.remove(product_id)

    def place_order(self, product_id: str, size: str) -> Order:
        product = self.products[product_id]
        order = Order(
            id=f"o{len(self.orders) + 1}",
            productId=product.id,
            brand=product.brand,
            title=product.title,
            size=size,
            status="Pending",
            date=date.today().isoformat(),
        )
        self.orders.append(order)
        return order


store = PonsivStore()
store.load_seed()
