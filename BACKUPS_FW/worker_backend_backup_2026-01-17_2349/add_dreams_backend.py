#!/usr/bin/env python3
import re

with open('worker.js', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Добавляем эндпоинт инициализации таблицы dreams
dreams_init = """
      // POST /api/dreams/init — создание таблицы dreams
      if (path === '/api/dreams/init' && request.method === 'POST') {
        try {
          await env.DB.prepare(`
            CREATE TABLE IF NOT EXISTS dreams (
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
            CREATE INDEX IF NOT EXISTS idx_dreams_child ON dreams(child_id, status)
          `).run();

          await env.DB.prepare(`
            CREATE INDEX IF NOT EXISTS idx_dreams_family ON dreams(family_id, status)
          `).run();

          return json({ message: 'Таблица dreams успешно создана' });
        } catch (err) {
          return error('Ошибка создания таблицы: ' + err.message, 'DB_ERROR', 500);
        }
      }

      // POST /api/dreams/create — создание мечты (ребёнок)
      if (path === '/api/dreams/create' && request.method === 'POST') {
        const inviteCode = request.headers.get('X-Invite-Code');
        
        if (!inviteCode) {
          return error('Отсутствует заголовок X-Invite-Code', 'NO_AUTH', 401);
        }

        const child = await env.DB.prepare(
          'SELECT id, family_id FROM children WHERE invite_code = ?'
        ).bind(inviteCode).first();

        if (!child) {
          return error('Недействительный код ребёнка', 'FORBIDDEN', 403);
        }

        const body = await request.json();
        const { title } = body;

        if (!title || title.trim().length === 0) {
          return error('Название мечты обязательно', 'INVALID_DATA', 400);
        }

        // Проверяем что нет активной мечты
        const existingDream = await env.DB.prepare(
          'SELECT id FROM dreams WHERE child_id = ? AND status IN ("pending", "active")'
        ).bind(child.id).first();

        if (existingDream) {
          return error('У ребёнка уже есть активная мечта', 'INVALID_DATA', 400);
        }

        const dreamId = 'dream_' + Date.now() + '_' + Math.random().toString(36).substring(2, 8);

        await env.DB.prepare(`
          INSERT INTO dreams (id, child_id, family_id, title, status, created_at)
          VALUES (?, ?, ?, ?, 'pending', datetime('now'))
        `).bind(dreamId, child.id, child.family_id, title.trim()).run();

        return json({ 
          message: 'Мечта создана',
          dream: { id: dreamId, title: title.trim(), status: 'pending' }
        });
      }

      // GET /api/dreams/my — получить мечту ребёнка
      if (path === '/api/dreams/my' && request.method === 'GET') {
        const inviteCode = request.headers.get('X-Invite-Code');
        
        if (!inviteCode) {
          return error('Отсутствует заголовок X-Invite-Code', 'NO_AUTH', 401);
        }

        const child = await env.DB.prepare(
          'SELECT id FROM children WHERE invite_code = ?'
        ).bind(inviteCode).first();

        if (!child) {
          return error('Недействительный код ребёнка', 'FORBIDDEN', 403);
        }

        const dream = await env.DB.prepare(`
          SELECT id, title, target_amount, current_amount, status, created_at, approved_at
          FROM dreams
          WHERE child_id = ? AND status IN ('pending', 'active')
          ORDER BY created_at DESC
          LIMIT 1
        `).bind(child.id).first();

        return json({ dream: dream || null });
      }

      // DELETE /api/dreams/delete — удаление мечты (ребёнок)
      if (path === '/api/dreams/delete' && request.method === 'DELETE') {
        const inviteCode = request.headers.get('X-Invite-Code');
        
        if (!inviteCode) {
          return error('Отсутствует заголовок X-Invite-Code', 'NO_AUTH', 401);
        }

        const child = await env.DB.prepare(
          'SELECT id FROM children WHERE invite_code = ?'
        ).bind(inviteCode).first();

        if (!child) {
          return error('Недействительный код ребёнка', 'FORBIDDEN', 403);
        }

        const body = await request.json();
        const { dream_id } = body;

        if (!dream_id) {
          return error('Не указан ID мечты', 'INVALID_DATA', 400);
        }

        // Проверяем принадлежность
        const dream = await env.DB.prepare(
          'SELECT id FROM dreams WHERE id = ? AND child_id = ?'
        ).bind(dream_id, child.id).first();

        if (!dream) {
          return error('Мечта не найдена', 'NOT_FOUND', 404);
        }

        await env.DB.prepare(
          'UPDATE dreams SET status = "cancelled" WHERE id = ?'
        ).bind(dream_id).run();

        return json({ message: 'Мечта удалена' });
      }

      // GET /api/dreams/pending — список pending мечт для родителя
      if (path === '/api/dreams/pending' && request.method === 'GET') {
        const inviteCode = request.headers.get('X-Invite-Code');
        
        if (!inviteCode) {
          return error('Отсутствует заголовок X-Invite-Code', 'NO_AUTH', 401);
        }

        const family = await env.DB.prepare(
          'SELECT id FROM families WHERE invite_code = ?'
        ).bind(inviteCode).first();

        if (!family) {
          return error('Недействительный код родителя', 'FORBIDDEN', 403);
        }

        const dreams = await env.DB.prepare(`
          SELECT 
            d.id,
            d.child_id,
            d.title,
            d.status,
            d.created_at,
            c.name as child_name
          FROM dreams d
          JOIN children c ON d.child_id = c.id
          WHERE d.family_id = ? AND d.status = 'pending'
          ORDER BY d.created_at DESC
        `).bind(family.id).all();

        return json({ dreams: dreams.results || [] });
      }

      // POST /api/dreams/set-goal — установка цели родителем
      if (path === '/api/dreams/set-goal' && request.method === 'POST') {
        const inviteCode = request.headers.get('X-Invite-Code');
        
        if (!inviteCode) {
          return error('Отсутствует заголовок X-Invite-Code', 'NO_AUTH', 401);
        }

        const family = await env.DB.prepare(
          'SELECT id FROM families WHERE invite_code = ?'
        ).bind(inviteCode).first();

        if (!family) {
          return error('Только родитель может устанавливать цель', 'FORBIDDEN', 403);
        }

        const body = await request.json();
        const { dream_id, target_amount } = body;

        if (!dream_id || !target_amount) {
          return error('Не указан ID мечты или сумма', 'INVALID_DATA', 400);
        }

        const amount = parseInt(target_amount);
        if (isNaN(amount) || amount < 1 || amount > 1000000) {
          return error('Сумма должна быть от 1 до 1000000', 'INVALID_DATA', 400);
        }

        // Проверяем принадлежность к семье
        const dream = await env.DB.prepare(
          'SELECT id, child_id FROM dreams WHERE id = ? AND family_id = ? AND status = "pending"'
        ).bind(dream_id, family.id).first();

        if (!dream) {
          return error('Мечта не найдена', 'NOT_FOUND', 404);
        }

        // Получаем текущий баланс ребёнка
        const child = await env.DB.prepare(
          'SELECT balance FROM children WHERE id = ?'
        ).bind(dream.child_id).first();

        await env.DB.prepare(`
          UPDATE dreams 
          SET target_amount = ?, current_amount = ?, status = 'active', approved_at = datetime('now')
          WHERE id = ?
        `).bind(amount, child.balance, dream_id).run();

        return json({ message: 'Цель установлена' });
      }

      // GET /api/dreams/active — список активных мечт для родителя
      if (path === '/api/dreams/active' && request.method === 'GET') {
        const inviteCode = request.headers.get('X-Invite-Code');
        
        if (!inviteCode) {
          return error('Отсутствует заголовок X-Invite-Code', 'NO_AUTH', 401);
        }

        const family = await env.DB.prepare(
          'SELECT id FROM families WHERE invite_code = ?'
        ).bind(inviteCode).first();

        if (!family) {
          return error('Недействительный код родителя', 'FORBIDDEN', 403);
        }

        const dreams = await env.DB.prepare(`
          SELECT 
            d.id,
            d.child_id,
            d.title,
            d.target_amount,
            d.current_amount,
            d.status,
            c.name as child_name
          FROM dreams d
          JOIN children c ON d.child_id = c.id
          WHERE d.family_id = ? AND d.status = 'active'
          ORDER BY d.created_at DESC
        `).bind(family.id).all();

        return json({ dreams: dreams.results || [] });
      }
"""

# Вставляем перед закрывающим 404
content = re.sub(
    r"(      // 404 — эндпоинт не найден|      return error\('Эндпоинт не найден', 'NOT_FOUND', 404\);)",
    dreams_init + "\n\n\\1",
    content,
    count=1
)

with open('worker.js', 'w', encoding='utf-8') as f:
    f.write(content)

print("OK")
