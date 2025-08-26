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
    id: str
    name: str
    handle: str
    avatar: str
    following: int
    followers: int
    outfitsCount: int
    wardrobe: List[str]
    likes: List[str]
    orders: List[str]


@dataclass
class Order:
    id: str
    productId: str
    brand: str
    title: str
    size: str
    status: str
    date: str
