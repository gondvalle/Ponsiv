import { z } from "zod";

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

export const CreateInteractionSchema = z.object({
  product_id: z.string(),
  interaction_type: z.string(),
  interaction_data: z.record(z.any()).optional(),
});

export const AddToWardrobeSchema = z.object({
  product_id: z.string().optional(),
  custom_item_name: z.string().optional(),
  custom_item_image_url: z.string().optional(),
  custom_item_category: z.string().optional(),
  custom_item_color: z.string().optional(),
  custom_item_brand: z.string().optional(),
  tags: z.array(z.string()).optional(),
});

export const CreateOutfitSchema = z.object({
  name: z.string(),
  description: z.string().optional(),
  wardrobe_item_ids: z.array(z.number()),
  is_public: z.boolean().optional(),
});
