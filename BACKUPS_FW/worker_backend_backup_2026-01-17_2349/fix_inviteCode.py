#!/usr/bin/env python3

# Читаем файл
with open('/Users/stanislav/Desktop/FAMILY_WALLET_MVP/backend/worker.js', 'r') as f:
    lines = f.readlines()

# Найти строку 1134 (if (path === '/api/referrals/my'))
# и добавить после неё извлечение inviteCode
for i, line in enumerate(lines):
    if i == 1134 and "path === '/api/referrals/my'" in line:
        # Вставить после строки 1134 новую строку с inviteCode
        lines.insert(i + 1, "        const inviteCode = request.headers.get('X-Invite-Code');\n")
        print(f'✅ Добавлена строка inviteCode после строки {i+1}')
        break
else:
    print('❌ Не найдена строка для вставки')
    exit(1)

# Сохранить
with open('/Users/stanislav/Desktop/FAMILY_WALLET_MVP/backend/worker.js', 'w') as f:
    f.writelines(lines)

print('✅ Файл обновлён!')
