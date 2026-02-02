-- Удаляем старую таблицу
DROP TABLE IF EXISTS rewards;

-- Создаём новую с child_id
CREATE TABLE rewards (
  id TEXT PRIMARY KEY,
  family_id TEXT NOT NULL,
  child_id TEXT,
  title TEXT NOT NULL,
  description TEXT,
  price INTEGER NOT NULL CHECK (price >= 1 AND price <= 10000),
  icon TEXT DEFAULT '🎁',
  is_permanent INTEGER DEFAULT 0 CHECK (is_permanent IN (0, 1)),
  is_active INTEGER DEFAULT 1 CHECK (is_active IN (0, 1)),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
