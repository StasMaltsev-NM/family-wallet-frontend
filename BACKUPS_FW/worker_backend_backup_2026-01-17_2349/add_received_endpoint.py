#!/usr/bin/env python3
import re

with open('worker.js', 'r') as f:
    content = f.read()

# Найти место после эндпоинта /api/rewards/purchases
marker = "return json({ purchases: purchases.results || [] });\n      }"
insert_pos = content.find(marker)

if insert_pos == -1:
    print("❌ Не найден маркер для вставки!")
    exit(1)

# Позиция после маркера
insert_pos = insert_pos + len(marker)

# Новый эндпоинт
new_endpoint = """

      // GET /api/rewards/received — count received rewards for profile
      if (path === '/api/rewards/received' && request.method === 'GET') {
        const inviteCode = request.headers.get('X-Invite-Code');
        
        if (!inviteCode) {
          return error('Отсутствует заголовок X-Invite-Code', 'NO_AUTH', 401);
        }

        const child = await env.DB.prepare(
          'SELECT id FROM children WHERE invite_code = ?'
        ).bind(inviteCode).first();

        if (!child) {
          return error('Недействительный код', 'FORBIDDEN', 403);
        }

        const received = await env.DB.prepare(`
          SELECT COUNT(*) as count
          FROM reward_purchases
          WHERE child_id = ? AND status = 'received'
        `).bind(child.id).first();

        return json({ count: received.count || 0 });
      }"""

# Вставка
new_content = content[:insert_pos] + new_endpoint + content[insert_pos:]

with open('worker.js', 'w') as f:
    f.write(new_content)

print("✅ Эндпоинт /api/rewards/received добавлен!")
