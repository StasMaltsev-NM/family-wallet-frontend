import re
import os

# Проверяем путь (корень или папка backend)
file_path = 'backend/worker.js' if os.path.exists('backend/worker.js') else 'worker.js'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

new_logic = """
      // === REFERRAL SYSTEM ===
      // POST /api/referrals/init - Создание таблицы
      if (path === '/api/referrals/init' && request.method === 'POST') {
        await env.DB.prepare(`
          CREATE TABLE IF NOT EXISTS referrals (
            id TEXT PRIMARY KEY,
            referrer_family_id TEXT NOT NULL,
            invite_code TEXT NOT NULL UNIQUE,
            used_by_family_id TEXT,
            used_at TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
          )
        `).run();
        return json({ message: 'Таблица рефералов инициализирована' });
      }

      // GET /api/referrals/my - Получить мои 3 кода
      if (path === '/api/referrals/my' && request.method === 'GET') {
        const inviteCode = request.headers.get('X-Invite-Code');
        const family = await env.DB.prepare('SELECT id FROM families WHERE invite_code = ?').bind(inviteCode).first();
        if (!family) return error('Доступ только для родителей', 'FORBIDDEN', 403);

        let refs = await env.DB.prepare('SELECT * FROM referrals WHERE referrer_family_id = ?').bind(family.id).all();
        
        if (refs.results.length === 0) {
          for (let i = 0; i < 3; i++) {
            const refCode = 'REF_' + Math.random().toString(36).substring(2, 8).toUpperCase();
            const refId = 'ref_' + Date.now() + '_' + i;
            await env.DB.prepare('INSERT INTO referrals (id, referrer_family_id, invite_code) VALUES (?, ?, ?)')
              .bind(refId, family.id, refCode).run();
          }
          refs = await env.DB.prepare('SELECT * FROM referrals WHERE referrer_family_id = ?').bind(family.id).all();
        }
        return json({ referrals: refs.results });
      }
"""

pattern = r"return error\(.*NOT_FOUND.*404\);"
if re.search(pattern, content):
    content = re.sub(pattern, new_logic + "\n      " + r"return error('Эндпоинт не найден', 'NOT_FOUND', 404);", content)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("PATCH_V3_OK")
else:
    print("PATTERN_NOT_FOUND")
