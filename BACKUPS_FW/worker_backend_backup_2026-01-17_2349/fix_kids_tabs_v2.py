#!/usr/bin/env python3
import re

with open('/Users/stanislav/Desktop/FAMILY_WALLET_MVP/frontend/kids.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Найти ключевые индексы
nav_start = None
script_start = None

for i, line in enumerate(lines):
    if '<div class="nav-tabs">' in line:
        nav_start = i
    if line.strip() == '<script>':
        script_start = i
        break

if not nav_start or not script_start:
    print('❌ Не найдены ключевые элементы')
    exit(1)

# Извлечь части файла
before_tabs = lines[:nav_start + 6]  # До конца навигации
scripts_part = lines[script_start:]  # Скрипты и дальше

# Найти все секции
content_str = ''.join(lines)

sections = {
    'dream': re.search(r'(<div class="section" id="dreamSection".*?</div>\n  </div>)', content_str, re.DOTALL),
    'balance': re.search(r'(<div class="section" id="balanceSection".*?</div>\n  </div>)', content_str, re.DOTALL),
    'myRewards': re.search(r'(<div class="section" id="myRewardsSection".*?</div>\n  </div>)', content_str, re.DOTALL),
    'tasks': re.search(r'(<div class="section" id="tasksSection".*?</div>\n  </div>)', content_str, re.DOTALL),
    'history': re.search(r'(<div class="section" id="historySection".*?</div>\n  </div>)', content_str, re.DOTALL),
    'shop': re.search(r'(<div class="section" id="shopSection".*?</div>\n  </div>)', content_str, re.DOTALL),
    'profile': re.search(r'(<div class="section">\s*<h2>👤 Мой профиль</h2>.*?</div>\n    </div>)', content_str, re.DOTALL)
}

# Проверить что все секции найдены
missing = [k for k, v in sections.items() if not v]
if missing:
    print(f'❌ Не найдены секции: {missing}')
    exit(1)

# Собрать новую структуру
new_content = before_tabs + [
    '\n',
    '  <!-- Вкладка: Кошелёк -->\n',
    '  <div id="tab-wallet" class="tab-content active">\n',
    '  ' + sections['dream'].group(1) + '\n\n',
    '  ' + sections['balance'].group(1) + '\n\n',
    '  ' + sections['myRewards'].group(1) + '\n\n',
    '  ' + sections['history'].group(1) + '\n',
    '  </div>\n\n',
    '  <!-- Вкладка: Миссии -->\n',
    '  <div id="tab-missions" class="tab-content">\n',
    '  ' + sections['tasks'].group(1) + '\n',
    '  </div>\n\n',
    '  <!-- Вкладка: Магазин -->\n',
    '  <div id="tab-shop" class="tab-content">\n',
    '  ' + sections['shop'].group(1) + '\n',
    '  </div>\n\n',
    '  <!-- Вкладка: Я (Профиль) -->\n',
    '  <div id="tab-profile" class="tab-content">\n',
    '    ' + sections['profile'].group(1) + '\n',
    '  </div>\n\n',
] + scripts_part

# Сохранить
with open('/Users/stanislav/Desktop/FAMILY_WALLET_MVP/frontend/kids.html', 'w', encoding='utf-8') as f:
    f.writelines(new_content)

print('✅ Структура вкладок исправлена!')
print('✅ Вкладка Кошелёк: Мечта + Баланс + Награды ожидают + История')
print('✅ Вкладка Миссии: Список миссий')
print('✅ Вкладка Магазин: Доступные награды')
print('✅ Вкладка Я: Профиль')
