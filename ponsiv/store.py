import json
import sqlite3
import hashlib
from pathlib import Path
from typing import Dict, List, Optional
from datetime import date

from .models import Product, Look, LookAuthor, User, Order


class PonsivStore:
    """Store backed by SQLite for user accounts and likes."""

    def __init__(self) -> None:
        # In-memory collections for products and orders
        self.products: Dict[str, Product] = {}
        self.looks: Dict[str, Look] = {}
        self.orders: List[Order] = []
        self.cart: List[str] = []

        # Database setup
        self.db_path = Path(__file__).resolve().parent / "users.db"
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        self._create_tables()

        # Logged in user id (None means not authenticated)
        self.current_user_id: Optional[int] = None

    # ------------------------------------------------------------------ DB --
    def _create_tables(self) -> None:
        with self.conn:
            self.conn.execute(
                """
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    email TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    name TEXT,
                    handle TEXT,
                    avatar_path TEXT
                )
                """
            )
            self.conn.execute(
                """
                CREATE TABLE IF NOT EXISTS likes (
                    user_id INTEGER NOT NULL,
                    product_id TEXT NOT NULL,
                    UNIQUE(user_id, product_id)
                )
                """
            )
        # Migración suave: añadir columnas si faltan
        self._ensure_user_column("age", "INTEGER")
        self._ensure_user_column("city", "TEXT")
        self._ensure_user_column("sex", "TEXT")

    def _ensure_user_column(self, col: str, sql_type: str) -> None:
        cur = self.conn.execute("PRAGMA table_info(users)")
        existing = {row["name"] for row in cur.fetchall()}
        if col not in existing:
            with self.conn:
                self.conn.execute(f"ALTER TABLE users ADD COLUMN {col} {sql_type}")

    # User management -------------------------------------------------------
    def create_user(
        self,
        email: str,
        password: str,
        *,
        name: Optional[str] = None,
        handle: Optional[str] = None,
        age: Optional[int] = None,
        city: Optional[str] = None,
        sex: Optional[str] = None,
    ) -> int:
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        # valores por defecto si no vienen
        if not name:
            name = email.split("@")[0]
        if not handle:
            handle = name

        with self.conn:
            cur = self.conn.execute(
                """
                INSERT INTO users (email, password_hash, name, handle, age, city, sex)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (email, password_hash, name, handle, age, city, sex),
            )
        return cur.lastrowid

    def authenticate_user(self, email: str, password: str) -> Optional[int]:
        cur = self.conn.execute("SELECT id, password_hash FROM users WHERE email=?", (email,))
        row = cur.fetchone()
        if not row:
            return None
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        if row["password_hash"] == password_hash:
            return row["id"]
        return None

    def get_user_by_email(self, email: str) -> Optional[int]:
        cur = self.conn.execute("SELECT id FROM users WHERE email=?", (email,))
        row = cur.fetchone()
        return row["id"] if row else None

    def get_user_by_handle(self, handle: str) -> Optional[int]:
        cur = self.conn.execute("SELECT id FROM users WHERE handle=?", (handle,))
        row = cur.fetchone()
        return row["id"] if row else None

    def get_user(self, user_id: int) -> Optional[User]:
        cur = self.conn.execute(
            """
            SELECT id, email, password_hash, name, handle, avatar_path,
                   age, city, sex
            FROM users WHERE id=?
            """,
            (user_id,),
        )
        row = cur.fetchone()
        if row:
            return User(**row)
        return None

    def update_user_avatar(self, user_id: int, avatar_path: str) -> None:
        with self.conn:
            self.conn.execute(
                "UPDATE users SET avatar_path=? WHERE id=?", (avatar_path, user_id)
            )

    # Likes management ------------------------------------------------------
    def is_product_liked(self, user_id: int, product_id: str) -> bool:
        cur = self.conn.execute(
            "SELECT 1 FROM likes WHERE user_id=? AND product_id=?",
            (user_id, product_id),
        )
        return cur.fetchone() is not None

    def toggle_like(self, user_id: int, product_id: str) -> bool:
        if self.is_product_liked(user_id, product_id):
            with self.conn:
                self.conn.execute(
                    "DELETE FROM likes WHERE user_id=? AND product_id=?",
                    (user_id, product_id),
                )
            return False
        else:
            with self.conn:
                self.conn.execute(
                    "INSERT OR IGNORE INTO likes (user_id, product_id) VALUES (?, ?)",
                    (user_id, product_id),
                )
            return True

    def get_liked_product_ids(self, user_id: int) -> List[str]:
        cur = self.conn.execute(
            "SELECT product_id FROM likes WHERE user_id=?",
            (user_id,),
        )
        return [row["product_id"] for row in cur.fetchall()]

    # Trending / Like counts ---------------------------------------------------
    def get_like_count(self, product_id: str) -> int:
        cur = self.conn.execute(
            "SELECT COUNT(*) AS c FROM likes WHERE product_id=?", (product_id,)
        )
        row = cur.fetchone()
        return int(row["c"] if row and row["c"] is not None else 0)

    def get_all_like_counts(self) -> dict[str, int]:
        cur = self.conn.execute(
            "SELECT product_id, COUNT(*) AS c FROM likes GROUP BY product_id"
        )
        return {row["product_id"]: int(row["c"]) for row in cur.fetchall()}

    def sort_products_by_likes(self, products):
        counts = self.get_all_like_counts()
        # 1º likes desc, 2º título para desempatar
        return sorted(
            products,
            key=lambda p: (counts.get(p.id, 0), (p.title or "")),
            reverse=True,
        )

    # ----------------------------------------------------------------- Seed --
    def load_seed(self) -> None:
        """Load product data from the ``assets`` directory."""
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
            category = data.get("categoria") or None

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
                category=category,
            )
            self.products[product.id] = product

    def get_categories(self) -> list[str]:
        return sorted({p.category for p in self.products.values() if p.category})

    def get_products_by_category(self, category: str) -> list[Product]:
        c = (category or "").lower()
        return [p for p in self.products.values() if (p.category or "").lower() == c]

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

