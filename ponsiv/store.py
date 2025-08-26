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
        """Load seed data from ``assets/seed`` relative to repository root."""
        seed_path = Path(__file__).resolve().parent.parent / "assets" / "seed"
        with open(seed_path / "products.json", "r", encoding="utf-8") as fh:
            for data in json.load(fh):
                product = Product(**data)
                self.products[product.id] = product
        with open(seed_path / "looks.json", "r", encoding="utf-8") as fh:
            for data in json.load(fh):
                author = LookAuthor(**data["author"])
                look = Look(id=data["id"], title=data["title"], author=author,
                            products=data["products"], cover_image=data["cover_image"])
                self.looks[look.id] = look
        with open(seed_path / "users.json", "r", encoding="utf-8") as fh:
            for data in json.load(fh):
                user = User(**data)
                self.users[user.id] = user
        with open(seed_path / "orders.json", "r", encoding="utf-8") as fh:
            for data in json.load(fh):
                order = Order(**data)
                self.orders.append(order)

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
