#!/usr/bin/env python3
import re

with open('worker.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Добавляем эндпоинт для миграции (DROP + CREATE)
migration = """
      // POST /api/dreams/migrate — миграция таблицы dreams (DROP + CREATE)
      if (path === '/api/dreams/migrate' && request.method === 'POST') {
        try {
          // Удаляем старую таблицу
          await env.DB.prepare('DROP TABLE IF EXISTS dreams').run();

          // Создаём заново
          await env.DB.prepare(`
            CREATE TABLE dreams (
              id TEXT PRIMARY KEY,
              child_id TEXT NOT NULL,
              family_id TEXT NOT NULL,
              title TEXT NOT NULL,
              target_amount INTEGER,
              current_amount INTEGER DEFAULT 0,
              status TEXT DEFAULT 'pending' CHECK (status IN ('pending', 'active', 'completed', 'cancelled')),
              created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
              approved_at TIMESTAMP
            )
          `).run();

          await env.DB.prepare(`
            CREATE INDEX idx_dreams_child ON dreams(child_id, status)
          `).run();

          await env.DB.prepare(`
            CREATE INDEX idx_dreams_family ON dreams(family_id, status)
          `).run();

          return json({ message: 'Таблица dreams пересоздана успешно' });
        } catch (err) {
          return error('Ошибка миграции: ' + err.message, 'DB_ERROR', 500);
        }
      }
"""

# Вставляем после /api/dreams/init
content = re.sub(
    r"(      // POST /api/dreams/create)",
    migration + "\n\n\\1",
    content
)

with open('worker.js', 'w', encoding='utf-8') as f:
    f.write(content)

print("OK")
