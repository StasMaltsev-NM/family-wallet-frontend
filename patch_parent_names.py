import re

file_path = 'frontend/parent.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Обновляем шаблон карточки в функции loadReferrals
old_template = "${ref.used_by_family_id ? '✅ ИСПОЛЬЗОВАН' : '🔓 ДОСТУПЕН'}"
new_template = "${ref.used_by_family_id ? '✅ Использован: ' + (ref.used_by_name || 'Другая семья') : '🔓 Доступен'}"

content = content.replace(old_template, new_template)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("FRONTEND_NAME_PATCH_OK")
