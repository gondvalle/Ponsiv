import { Hono } from "hono";
import { cors } from "hono/cors";
import { zValidator } from "@hono/zod-validator";
import {
  authMiddleware,
  exchangeCodeForSessionToken,
  getOAuthRedirectUrl,
  deleteSession,
  MOCHA_SESSION_TOKEN_COOKIE_NAME,
} from "@getmocha/users-service/backend";
import { getCookie, setCookie } from "hono/cookie";
import {
  CreateInteractionSchema,
  AddToWardrobeSchema,
  CreateOutfitSchema,
} from "@/shared/types";
import { z } from "zod";

const app = new Hono<{ Bindings: Env }>();

// Enable CORS
app.use("*", cors({
  origin: "*",
  allowMethods: ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
  allowHeaders: ["Content-Type", "Authorization"],
  credentials: true,
}));

// Authentication routes
app.get('/api/oauth/google/redirect_url', async (c) => {
  const redirectUrl = await getOAuthRedirectUrl('google', {
    apiUrl: c.env.MOCHA_USERS_SERVICE_API_URL,
    apiKey: c.env.MOCHA_USERS_SERVICE_API_KEY,
  });

  return c.json({ redirectUrl }, 200);
});

app.post("/api/sessions", zValidator("json", z.object({ code: z.string() })), async (c) => {
  const body = await c.req.json();

  if (!body.code) {
    return c.json({ error: "No authorization code provided" }, 400);
  }

  const sessionToken = await exchangeCodeForSessionToken(body.code, {
    apiUrl: c.env.MOCHA_USERS_SERVICE_API_URL,
    apiKey: c.env.MOCHA_USERS_SERVICE_API_KEY,
  });

  setCookie(c, MOCHA_SESSION_TOKEN_COOKIE_NAME, sessionToken, {
    httpOnly: true,
    path: "/",
    sameSite: "none",
    secure: true,
    maxAge: 60 * 24 * 60 * 60, // 60 days
  });

  return c.json({ success: true }, 200);
});

app.get("/api/users/me", authMiddleware, async (c) => {
  return c.json(c.get("user"));
});

app.get('/api/logout', async (c) => {
  const sessionToken = getCookie(c, MOCHA_SESSION_TOKEN_COOKIE_NAME);

  if (typeof sessionToken === 'string') {
    await deleteSession(sessionToken, {
      apiUrl: c.env.MOCHA_USERS_SERVICE_API_URL,
      apiKey: c.env.MOCHA_USERS_SERVICE_API_KEY,
    });
  }

  setCookie(c, MOCHA_SESSION_TOKEN_COOKIE_NAME, '', {
    httpOnly: true,
    path: '/',
    sameSite: 'none',
    secure: true,
    maxAge: 0,
  });

  return c.json({ success: true }, 200);
});

// Product feed routes
app.get('/api/feed', async (c) => {
  const page = parseInt(c.req.query('page') || '1');
  const limit = parseInt(c.req.query('limit') || '10');
  const offset = (page - 1) * limit;

  try {
    const { results } = await c.env.DB.prepare(`
      SELECT p.*, b.name as brand_name, b.logo_url as brand_logo_url,
             cat.name as category_name, cat.icon_name as category_icon_name
      FROM products p
      LEFT JOIN brands b ON p.brand_id = b.id
      LEFT JOIN categories cat ON p.category_id = cat.id
      WHERE p.is_active = 1 AND b.is_active = 1
      ORDER BY RANDOM()
      LIMIT ? OFFSET ?
    `).bind(limit + 1, offset).all();

    const hasMore = results.length > limit;
    const products = results.slice(0, limit).map(row => ({
      ...row,
      brand: row.brand_name ? {
        id: row.brand_id,
        name: row.brand_name,
        logo_url: row.brand_logo_url,
      } : undefined,
      category: row.category_name ? {
        id: row.category_id,
        name: row.category_name,
        icon_name: row.category_icon_name,
      } : undefined,
    }));

    return c.json({
      products,
      hasMore,
      nextPage: hasMore ? page + 1 : null,
    });
  } catch (error) {
    return c.json({ error: 'Failed to fetch feed' }, 500);
  }
});

// User interaction routes
app.post('/api/interactions', authMiddleware, zValidator("json", CreateInteractionSchema), async (c) => {
  const user = c.get('user');
  const { product_id, interaction_type, interaction_data } = c.req.valid('json');

  try {
    await c.env.DB.prepare(`
      INSERT INTO user_interactions (user_id, product_id, interaction_type, interaction_data)
      VALUES (?, ?, ?, ?)
    `).bind(
      user!.id,
      product_id,
      interaction_type,
      interaction_data ? JSON.stringify(interaction_data) : null
    ).run();

    return c.json({ success: true });
  } catch (error) {
    return c.json({ error: 'Failed to record interaction' }, 500);
  }
});

// Wardrobe routes
app.get('/api/wardrobe', authMiddleware, async (c) => {
  const user = c.get('user');

  try {
    const { results } = await c.env.DB.prepare(`
      SELECT w.*, p.name as product_name, p.image_url as product_image_url,
             p.price as product_price, b.name as brand_name
      FROM user_wardrobes w
      LEFT JOIN products p ON w.product_id = p.id
      LEFT JOIN brands b ON p.brand_id = b.id
      WHERE w.user_id = ?
      ORDER BY w.created_at DESC
    `).bind(user!.id).all();

    const wardrobeItems = results.map(row => ({
      ...row,
      product: row.product_name ? {
        id: row.product_id,
        name: row.product_name,
        image_url: row.product_image_url,
        price: row.product_price,
        brand: { name: row.brand_name },
      } : undefined,
      tags: (() => {
        try {
          return row.tags && typeof row.tags === 'string' && row.tags.trim() !== '' ? JSON.parse(row.tags) : [];
        } catch {
          return [];
        }
      })(),
    }));

    return c.json(wardrobeItems);
  } catch (error) {
    return c.json({ error: 'Failed to fetch wardrobe' }, 500);
  }
});

app.post('/api/wardrobe', authMiddleware, zValidator("json", AddToWardrobeSchema), async (c) => {
  const user = c.get('user');
  const data = c.req.valid('json');

  try {
    await c.env.DB.prepare(`
      INSERT INTO user_wardrobes (
        user_id, product_id, custom_item_name, custom_item_image_url,
        custom_item_category, custom_item_color, custom_item_brand,
        tags, is_custom
      ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    `).bind(
      user!.id,
      data.product_id || null,
      data.custom_item_name || null,
      data.custom_item_image_url || null,
      data.custom_item_category || null,
      data.custom_item_color || null,
      data.custom_item_brand || null,
      data.tags ? JSON.stringify(data.tags) : null,
      data.product_id ? 0 : 1
    ).run();

    return c.json({ success: true });
  } catch (error) {
    return c.json({ error: 'Failed to add to wardrobe' }, 500);
  }
});

// Outfit routes
app.get('/api/outfits', async (c) => {
  const isPublic = c.req.query('public') === 'true';
  const user = c.get('user');

  try {
    let query = `
      SELECT o.*, COUNT(ol.id) as likes_count
      FROM outfits o
      LEFT JOIN outfit_likes ol ON o.id = ol.outfit_id
    `;
    
    const params: any[] = [];
    if (isPublic) {
      query += ' WHERE o.is_public = 1';
    } else if (user) {
      query += ' WHERE o.user_id = ?';
      params.push(user.id);
    } else {
      return c.json({ error: 'Authentication required' }, 401);
    }

    query += ' GROUP BY o.id ORDER BY o.created_at DESC';

    const { results } = params.length > 0 
      ? await c.env.DB.prepare(query).bind(params[0]).all()
      : await c.env.DB.prepare(query).all();
    
    // Always return an array, even if results is undefined or null
    return c.json(Array.isArray(results) ? results : []);
  } catch (error) {
    console.error('Database error in /api/outfits:', error);
    return c.json([]);
  }
});

app.post('/api/outfits', authMiddleware, zValidator("json", CreateOutfitSchema), async (c) => {
  const user = c.get('user');
  const { name, description, wardrobe_item_ids, is_public } = c.req.valid('json');

  try {
    const result = await c.env.DB.prepare(`
      INSERT INTO outfits (user_id, name, description, is_public)
      VALUES (?, ?, ?, ?)
    `).bind(
      user!.id,
      name,
      description || null,
      is_public || false
    ).run();

    const outfitId = result.meta.last_row_id;

    // Add outfit items
    for (const wardrobeItemId of wardrobe_item_ids) {
      await c.env.DB.prepare(`
        INSERT INTO outfit_items (outfit_id, wardrobe_item_id)
        VALUES (?, ?)
      `).bind(outfitId, wardrobeItemId).run();
    }

    return c.json({ success: true, outfit_id: outfitId });
  } catch (error) {
    return c.json({ error: 'Failed to create outfit' }, 500);
  }
});

export default app;
