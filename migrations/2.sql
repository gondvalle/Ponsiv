
CREATE TABLE user_interactions (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id TEXT NOT NULL,
  product_id INTEGER NOT NULL,
  interaction_type TEXT NOT NULL, -- 'like', 'save', 'have', 'buy', 'view'
  interaction_data TEXT, -- JSON for additional data like view duration
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE user_wardrobes (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id TEXT NOT NULL,
  product_id INTEGER,
  custom_item_name TEXT,
  custom_item_image_url TEXT,
  custom_item_category TEXT,
  custom_item_color TEXT,
  custom_item_brand TEXT,
  tags TEXT, -- JSON array of tags
  is_custom BOOLEAN DEFAULT 0, -- true if user uploaded, false if from catalog
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE outfits (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id TEXT NOT NULL,
  name TEXT NOT NULL,
  description TEXT,
  image_url TEXT,
  is_public BOOLEAN DEFAULT 0,
  likes_count INTEGER DEFAULT 0,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
