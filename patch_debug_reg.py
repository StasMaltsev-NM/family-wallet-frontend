import re

file_path = 'backend/worker.js'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Добавляем эндпоинт диагностики
debug_logic = """
      // GET /api/debug/referrals - Посмотреть все коды в базе
      if (path === '/api/debug/referrals' && request.method === 'GET') {
        const { results } = await env.DB.prepare('SELECT * FROM referrals').all();
        return json({ results });
      }
"""

# 2. Делаем регистрацию более надежной (TRIM и UPPER)
old_reg = "const { name, currency_name, currency_symbol, referral_code } = await request.json();"
new_reg = """const { name, currency_name, currency_symbol, referral_code } = await request.json();
        const cleanCode = referral_code.trim().toUpperCase();"""

old_query = "WHERE invite_code = ? AND used_by_family_id IS NULL"
new_query = "WHERE UPPER(invite_code) = ? AND used_by_family_id IS NULL"

content = content.replace(debug_logic, "") # Удаляем если уже был
content = re.sub(r"(// POST /api/families/register)", debug_logic + "\n      \\1", content)
content = content.replace(old_reg, new_reg)
content = content.replace("bind(referral_code)", "bind(cleanCode)")
content = content.replace(old_query, new_query)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("DEBUG_PATCH_OK")
