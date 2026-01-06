import re

file_path = 'backend/worker.js'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Обновляем SQL запрос, добавляя JOIN с таблицей families
old_sql = "SELECT * FROM referrals WHERE referrer_family_id = ?"
new_sql = "SELECT r.*, f.name as used_by_name FROM referrals r LEFT JOIN families f ON r.used_by_family_id = f.id WHERE r.referrer_family_id = ?"

content = content.replace(old_sql, new_sql)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("BACKEND_JOIN_PATCH_OK")
