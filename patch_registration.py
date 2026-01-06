import re

file_path = 'backend/worker.js'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

reg_logic = """
      // POST /api/families/register - Регистрация новой семьи по коду
      if (path === '/api/families/register' && request.method === 'POST') {
        const { name, currency_name, currency_symbol, referral_code } = await request.json();
        
        // 1. Проверяем код
        const ref = await env.DB.prepare('SELECT * FROM referrals WHERE invite_code = ? AND used_by_family_id IS NULL').bind(referral_code).first();
        if (!ref) return error('Код недействителен или уже использован', 'INVALID_REF', 400);

        // 2. Создаем новую семью
        const newFamilyId = 'fam_' + Date.now();
        const newInviteCode = Math.random().toString(36).substring(2, 8).toUpperCase();
        
        await env.DB.batch([
          env.DB.prepare('INSERT INTO families (id, name, currency_name, currency_symbol, invite_code) VALUES (?, ?, ?, ?, ?)').bind(newFamilyId, name, currency_name, currency_symbol, newInviteCode),
          env.DB.prepare('UPDATE referrals SET used_by_family_id = ?, used_at = CURRENT_TIMESTAMP WHERE invite_code = ?').bind(newFamilyId, referral_code)
        ]);

        return json({ message: 'Семья зарегистрирована!', invite_code: newInviteCode });
      }
"""

# Вставляем перед финальным 404
pattern = r"return error\(.*NOT_FOUND.*404\);"
content = re.sub(pattern, reg_logic + "\n      " + r"return error('Эндпоинт не найден', 'NOT_FOUND', 404);", content)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("REGISTRATION_PATCH_OK")
