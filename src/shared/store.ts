import { create } from "zustand";
import { persist } from "zustand/middleware";
import type { Product, Look, User, Order } from "./types";
import { seedProducts, seedLooks, seedUsers, seedOrders } from "./data";

export interface CartItem {
  product: Product;
  quantity: number;
  size: string;
}

interface StoreState {
  products: Product[];
  looks: Look[];
  user: User;
  wishlist: string[];
  wardrobe: string[];
  cart: CartItem[];
  orders: Order[];
  toggleWishlist: (id: string) => void;
  toggleWardrobe: (id: string) => void;
  addToCart: (product: Product, size: string) => void;
  updateQuantity: (productId: string, size: string, qty: number) => void;
  removeFromCart: (productId: string, size: string) => void;
  cartTotal: () => number;
  createOrder: () => void;
}

export const useStore = create<StoreState>()(
  persist(
    (set, get) => ({
      products: seedProducts,
      looks: seedLooks,
      user: seedUsers[0],
      wishlist: [],
      wardrobe: [],
      cart: [],
      orders: seedOrders,
      toggleWishlist: (id) =>
        set((state) => ({
          wishlist: state.wishlist.includes(id)
            ? state.wishlist.filter((p) => p !== id)
            : [...state.wishlist, id],
        })),
      toggleWardrobe: (id) =>
        set((state) => ({
          wardrobe: state.wardrobe.includes(id)
            ? state.wardrobe.filter((p) => p !== id)
            : [...state.wardrobe, id],
        })),
      addToCart: (product, size) =>
        set((state) => {
          const existing = state.cart.find(
            (i) => i.product.id === product.id && i.size === size
          );
          if (existing) {
            return {
              cart: state.cart.map((i) =>
                i.product.id === product.id && i.size === size
                  ? { ...i, quantity: i.quantity + 1 }
                  : i
              ),
            };
          }
          return { cart: [...state.cart, { product, size, quantity: 1 }] };
        }),
      updateQuantity: (productId, size, qty) =>
        set((state) => ({
          cart: state.cart.map((i) =>
            i.product.id === productId && i.size === size
              ? { ...i, quantity: qty }
              : i
          ),
        })),
      removeFromCart: (productId, size) =>
        set((state) => ({
          cart: state.cart.filter(
            (i) => !(i.product.id === productId && i.size === size)
          ),
        })),
      cartTotal: () =>
        get().cart.reduce((sum, item) => sum + item.product.price * item.quantity, 0),
      createOrder: () =>
        set((state) => {
          const newOrders: Order[] = [
            ...state.orders,
            ...state.cart.map((item, idx) => ({
              id: `o${state.orders.length + idx + 1}`,
              productId: item.product.id,
              brand: item.product.brand,
              title: item.product.title,
              size: item.size,
              status: "Procesando",
              date: new Date().toISOString().split("T")[0],
            })),
          ];
          return { cart: [], orders: newOrders };
        }),
    }),
    { name: "ponsiv-store" }
  )
);
