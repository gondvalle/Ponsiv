import z from "zod";

// Brand types
export const BrandSchema = z.object({
  id: z.number(),
  name: z.string(),
  logo_url: z.string().nullable(),
  website_url: z.string().nullable(),
  is_active: z.boolean(),
  created_at: z.string(),
  updated_at: z.string(),
});

export type Brand = z.infer<typeof BrandSchema>;

// Category types
export const CategorySchema = z.object({
  id: z.number(),
  name: z.string(),
  parent_id: z.number().nullable(),
  icon_name: z.string().nullable(),
  created_at: z.string(),
  updated_at: z.string(),
});

export type Category = z.infer<typeof CategorySchema>;

// Product types
export const ProductSchema = z.object({
  id: z.number(),
  brand_id: z.number(),
  category_id: z.number(),
  name: z.string(),
  description: z.string().nullable(),
  price: z.number(),
  currency: z.string(),
  image_url: z.string().nullable(),
  video_url: z.string().nullable(),
  sizes_available: z.string().nullable(), // JSON array
  colors_available: z.string().nullable(), // JSON array
  stock_quantity: z.number(),
  is_active: z.boolean(),
  external_product_id: z.string().nullable(),
  purchase_url: z.string().nullable(),
  created_at: z.string(),
  updated_at: z.string(),
  brand: BrandSchema.optional(),
  category: CategorySchema.optional(),
});

export type Product = z.infer<typeof ProductSchema>;

// User interaction types
export const UserInteractionSchema = z.object({
  id: z.number(),
  user_id: z.string(),
  product_id: z.number(),
  interaction_type: z.enum(['like', 'save', 'have', 'buy', 'view']),
  interaction_data: z.string().nullable(), // JSON
  created_at: z.string(),
  updated_at: z.string(),
});

export type UserInteraction = z.infer<typeof UserInteractionSchema>;

// Wardrobe types
export const WardrobeItemSchema = z.object({
  id: z.number(),
  user_id: z.string(),
  product_id: z.number().nullable(),
  custom_item_name: z.string().nullable(),
  custom_item_image_url: z.string().nullable(),
  custom_item_category: z.string().nullable(),
  custom_item_color: z.string().nullable(),
  custom_item_brand: z.string().nullable(),
  tags: z.string().nullable(), // JSON array
  is_custom: z.boolean(),
  created_at: z.string(),
  updated_at: z.string(),
  product: ProductSchema.optional(),
});

export type WardrobeItem = z.infer<typeof WardrobeItemSchema>;

// Outfit types
export const OutfitSchema = z.object({
  id: z.number(),
  user_id: z.string(),
  name: z.string(),
  description: z.string().nullable(),
  image_url: z.string().nullable(),
  is_public: z.boolean(),
  likes_count: z.number(),
  created_at: z.string(),
  updated_at: z.string(),
});

export type Outfit = z.infer<typeof OutfitSchema>;

// Feed response types
export const FeedResponseSchema = z.object({
  products: z.array(ProductSchema),
  hasMore: z.boolean(),
  nextPage: z.number().nullable(),
});

export type FeedResponse = z.infer<typeof FeedResponseSchema>;

// API Request schemas
export const CreateInteractionSchema = z.object({
  product_id: z.number(),
  interaction_type: z.enum(['like', 'save', 'have', 'buy', 'view']),
  interaction_data: z.object({}).passthrough().optional(),
});

export const AddToWardrobeSchema = z.object({
  product_id: z.number().optional(),
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
