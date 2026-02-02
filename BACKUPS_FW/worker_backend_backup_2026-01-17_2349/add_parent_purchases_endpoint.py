#!/usr/bin/env python3
import re

with open('worker.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Новый эндпоинт для родителя (после GET /api/rewards/purchases)
new_endpoint = """
      // GET /api/rewards/purchases/family — список покупок всех детей семьи (для родителя)
      if (path === '/api/rewards/purchases/family' && request.method === 'GET') {
        const inviteCode = request.headers.get('X-Invite-Code');
        
        if (!inviteCode) {
          return error('Отсутствует заголовок X-Invite-Code', 'NO_AUTH', 401);
        }

        // Проверяем родителя
        const family = await env.DB.prepare(
          'SELECT id FROM families WHERE invite_code = ?'
        ).bind(inviteCode).first();

        if (!family) {
          return error('Только родитель может видеть все покупки', 'FORBIDDEN', 403);
        }

        // Получаем покупки со статусом pending для всей семьи
        const purchases = await env.DB.prepare(`
          SELECT 
            rp.id, 
            rp.reward_title, 
            rp.reward_icon, 
            rp.price, 
            rp.status,
            rp.purchased_at,
            c.name as child_name
          FROM reward_purchases rp
          JOIN children c ON rp.child_id = c.id
          WHERE rp.family_id = ? AND rp.status = 'pending'
          ORDER BY rp.purchased_at DESC
        `).bind(family.id).all();

        return json({ purchases: purchases.results || [] });
      }
"""

# Вставляем после GET /api/rewards/purchases
content = re.sub(
    r"(      // POST /api/rewards/confirm-received)",
    new_endpoint + r"\n\1",
    content
)

with open('worker.js', 'w', encoding='utf-8') as f:
    f.write(content)

print("OK")
