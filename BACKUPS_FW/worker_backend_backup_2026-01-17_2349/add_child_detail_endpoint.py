#!/usr/bin/env python3
import re

with open('worker.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Новый эндпоинт GET /api/children/:child_id
new_endpoint = """
      // GET /api/children/:child_id — детальная информация о ребёнке
      const childDetailMatch = path.match(/^\/api\/children\/([^\/]+)$/);
      if (childDetailMatch && request.method === 'GET') {
        const childId = childDetailMatch[1];
        const inviteCode = request.headers.get('X-Invite-Code');
        
        if (!inviteCode) {
          return error('Отсутствует заголовок X-Invite-Code', 'NO_AUTH', 401);
        }

        // Проверяем родителя
        const family = await env.DB.prepare(
          'SELECT id FROM families WHERE invite_code = ?'
        ).bind(inviteCode).first();

        if (!family) {
          return error('Только родитель может видеть детали', 'FORBIDDEN', 403);
        }

        // Получаем ребёнка с проверкой принадлежности к семье
        const child = await env.DB.prepare(`
          SELECT id, name, role, age, balance, pending_balance, invite_code, child_number
          FROM children
          WHERE id = ? AND family_id = ?
        `).bind(childId, family.id).first();

        if (!child) {
          return error('Ребёнок не найден', 'NOT_FOUND', 404);
        }

        return json({ child });
      }
"""

# Вставляем после GET /api/children/list
content = re.sub(
    r"(      // POST /api/children/add)",
    new_endpoint + r"\n\1",
    content
)

with open('worker.js', 'w', encoding='utf-8') as f:
    f.write(content)

print("OK")
