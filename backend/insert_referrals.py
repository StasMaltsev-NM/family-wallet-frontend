#!/usr/bin/env python3
import re

# Читаем файл
with open('/Users/stanislav/Desktop/FAMILY_WALLET_MVP/backend/worker.js', 'r') as f:
    content = f.read()

# Проверяем что эндпоинтов нет
if 'api/referrals/my' in content:
    print('❌ ОШИБКА: Эндпоинт api/referrals/my уже существует!')
    exit(1)

if 'api/families/register' in content:
    print('❌ ОШИБКА: Эндпоинт api/families/register уже существует!')
    exit(1)

# Код для вставки
referrals_code = """
      // GET /api/referrals/my - Получить/Генерировать 3 кода (для родителя)
      if (path === '/api/referrals/my' && request.method === 'GET') {
        const family = await env.DB.prepare('SELECT id FROM families WHERE invite_code = ?').bind(inviteCode).first();
        if (!family) return error('Forbidden', 'FORBIDDEN', 403);
        let refs = await env.DB.prepare('SELECT r.*, f.name as used_by_name FROM referrals r LEFT JOIN families f ON r.used_by_family_id = f.id WHERE r.referrer_family_id = ?').bind(family.id).all();
        if (refs.results.length === 0) {
          for (let i = 0; i < 3; i++) {
            const refCode = 'REF_' + Math.random().toString(36).substring(2, 8).toUpperCase();
            await env.DB.prepare('INSERT INTO referrals (id, referrer_family_id, invite_code) VALUES (?, ?, ?)').bind(`ref_${Date.now()}_${i}`, family.id, refCode).run();
          }
          refs = await env.DB.prepare('SELECT r.*, f.name as used_by_name FROM referrals r LEFT JOIN families f ON r.used_by_family_id = f.id WHERE r.referrer_family_id = ?').bind(family.id).all();
        }
        return new Response(JSON.stringify({ referrals: refs.results }), { headers: corsHeaders });
      }

      // POST /api/families/register - Регистрация новой семьи по коду
      if (path === '/api/families/register' && request.method === 'POST') {
        const { name, currency_name, currency_symbol, referral_code } = await request.json();
        const cleanCode = referral_code.trim().toUpperCase();
        const ref = await env.DB.prepare('SELECT * FROM referrals WHERE invite_code = ? AND used_by_family_id IS NULL').bind(cleanCode).first();
        if (!ref) return new Response(JSON.stringify({ error: 'Код недействителен', code: 'INVALID_REF' }), { status: 400, headers: corsHeaders });
        const newFamilyId = 'fam_' + Date.now();
        const newInviteCode = Math.random().toString(36).substring(2, 8).toUpperCase();
        await env.DB.batch([
          env.DB.prepare('INSERT INTO families (id, name, currency_name, currency_symbol, invite_code) VALUES (?, ?, ?, ?, ?)').bind(newFamilyId, name, currency_name, currency_symbol, newInviteCode),
          env.DB.prepare('UPDATE referrals SET used_by_family_id = ?, used_at = CURRENT_TIMESTAMP WHERE invite_code = ?').bind(newFamilyId, cleanCode)
        ]);
        return new Response(JSON.stringify({ message: 'Семья создана', invite_code: newInviteCode }), { headers: corsHeaders });
      }
"""

# Находим место вставки (перед "return error('Эндпоинт не найден'")
pattern = r"(\n\n      return error\('Эндпоинт не найден', 'NOT_FOUND', 404\);)"
if not re.search(pattern, content):
    print('❌ ОШИБКА: Не найдена строка для вставки!')
    exit(1)

# Вставляем код
new_content = re.sub(pattern, referrals_code + r'\1', content)

# Сохраняем
with open('/Users/stanislav/Desktop/FAMILY_WALLET_MVP/backend/worker.js', 'w') as f:
    f.write(new_content)

print('✅ Эндпоинты реферальной системы добавлены успешно!')
