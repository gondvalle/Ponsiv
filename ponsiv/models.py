from dataclasses import dataclass
from typing import List, Optional


@dataclass
class Product:
    id: str
    brand: str
    title: str
    price: float
    sizes: List[str]
    images: List[str]
    logo: Optional[str] = None
    category: Optional[str] = None


@dataclass
class LookAuthor:
    name: str
    avatar: str


@dataclass
class Look:
    id: str
    title: str
    author: LookAuthor
    products: List[str]
    cover_image: str


@dataclass
class User:
    """Basic user profile stored in the local SQLite database."""
    id: int
    email: str
    password_hash: str
    name: str
    handle: str
    avatar_path: Optional[str] = None
    age: Optional[int] = None
    city: Optional[str] = None
    sex: Optional[str] = None  # 'Mujer' | 'Hombre' | 'Otro'


@dataclass
class Order:
    id: str
    productId: str
    brand: str
    title: str
    size: str
    status: str
    date: str

