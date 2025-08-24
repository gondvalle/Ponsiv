export interface Product {
  id: string;
  brand: string;
  title: string;
  price: number;
  images: string[];
  sizes: string[];
  color: string;
  category: string;
  stock: number;
  checkout_url?: string;
}

export interface Look {
  id: string;
  title: string;
  author: { name: string; avatar: string };
  products: string[];
  cover_image: string;
}

export interface Order {
  id: string;
  productId: string;
  brand: string;
  title: string;
  size: string;
  status: string;
  date: string;
}

export interface User {
  id: string;
  name: string;
  handle: string;
  avatar: string;
  following: number;
  followers: number;
  outfitsCount: number;
  wardrobe: string[];
  likes: string[];
  orders: string[];
}
