#!/usr/bin/env python3

with open('/Users/stanislav/Desktop/FAMILY_WALLET_MVP/backend/worker.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Проверить что эндпоинта ещё нет
if 'api/shop/mark-received' in content:
    print('⚠️ Эндпоинт /api/shop/mark-received уже существует!')
    exit(0)

# Код нового эндпоинта
new_endpoint = """
      // POST /api/shop/mark-received - Ребёнок подтверждает получение награды
      if (path === '/api/shop/mark-received' && request.method === 'POST') {
        const { reward_id } = await request.json();
        const inviteCode = request.headers.get('X-Invite-Code');
        
        if (!reward_id) {
          return error('reward_id обязателен', 'MISSING_FIELD', 400);
        }

        // Получить ребёнка
        const child = await env.DB.prepare('SELECT id, family_id, name FROM children WHERE invite_code = ?').bind(inviteCode).first();
        if (!child) {
          return error('Недействительный код ребёнка', 'FORBIDDEN', 403);
        }

        // Проверить что награда принадлежит этому ребёнку и ещё не получена
        const purchase = await env.DB.prepare(
          'SELECT id, status FROM reward_purchases WHERE id = ? AND child_id = ? AND status = ?'
        ).bind(reward_id, child.id, 'pending').first();

        if (!purchase) {
          return error('Награда не найдена или уже получена', 'NOT_FOUND', 404);
        }

        // Обновить статус на received
        await env.DB.prepare(
          'UPDATE reward_purchases SET status = ?, received_at = CURRENT_TIMESTAMP WHERE id = ?'
        ).bind('received', reward_id).run();

        // Записать событие в event log
        const eventId = 'evt_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
        await env.DB.prepare(
          'INSERT INTO events (id, family_id, child_id, event_type, payload) VALUES (?, ?, ?, ?, ?)'
        ).bind(
          eventId,
          child.family_id,
          child.id,
          'reward_received',
          JSON.stringify({ reward_id, child_name: child.name })
        ).run();

        return json({ success: true, message: 'Награда помечена как полученная' });
      }
"""

# Найти место вставки (перед return error('Эндпоинт не найден'))
insert_marker = "      return error('Эндпоинт не найден', 'NOT_FOUND', 404);"
if insert_marker not in content:
    print('❌ Не найдена строка для вставки эндпоинта!')
    exit(1)

# Вставить эндпоинт
content = content.replace(insert_marker, new_endpoint + '\n' + insert_marker)

# Сохранить
with open('/Users/stanislav/Desktop/FAMILY_WALLET_MVP/backend/worker.js', 'w', encoding='utf-8') as f:
    f.write(content)

print('✅ Эндпоинт /api/shop/mark-received добавлен!')
print('✅ Записывает событие в таблицу events')
print('✅ Обновляет статус награды на received')
