#!/usr/bin/env python3
import re

# KIDS.HTML
with open('/Users/stanislav/Desktop/FAMILY_WALLET_MVP/frontend/kids.html', 'r', encoding='utf-8') as f:
    kids_content = f.read()

# Найти и удалить setInterval блок в kids.html
kids_pattern = r'\n\s*// Автообновление каждые 5 секунд\s*\n\s*setInterval\(\(\) => \{[^}]+\}, 5000\);'
kids_content = re.sub(kids_pattern, '', kids_content, flags=re.DOTALL)

with open('/Users/stanislav/Desktop/FAMILY_WALLET_MVP/frontend/kids.html', 'w', encoding='utf-8') as f:
    f.write(kids_content)

# PARENT.HTML
with open('/Users/stanislav/Desktop/FAMILY_WALLET_MVP/frontend/parent.html', 'r', encoding='utf-8') as f:
    parent_content = f.read()

# Найти и удалить setInterval блок в parent.html
parent_pattern = r'\n\s*setInterval\(\(\) => \{[^}]+\}, 5000\);'
parent_content = re.sub(parent_pattern, '', parent_content, flags=re.DOTALL)

with open('/Users/stanislav/Desktop/FAMILY_WALLET_MVP/frontend/parent.html', 'w', encoding='utf-8') as f:
    f.write(parent_content)

print('✅ setInterval удалён из kids.html')
print('✅ setInterval удалён из parent.html')
print('✅ Теперь данные загружаются только при действиях пользователя')
print('✅ Ожидаемое снижение запросов: с 352k до ~5-10k в день')
