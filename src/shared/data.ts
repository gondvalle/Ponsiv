import products from "../../assets/seed/products.json";
import looks from "../../assets/seed/looks.json";
import users from "../../assets/seed/users.json";
import orders from "../../assets/seed/orders.json";
import type { Product, Look, User, Order } from "./types";

export const seedProducts = products as Product[];
export const seedLooks = looks as Look[];
export const seedUsers = users as User[];
export const seedOrders = orders as Order[];
