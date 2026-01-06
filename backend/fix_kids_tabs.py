#!/usr/bin/env python3
import re

with open('/Users/stanislav/Desktop/FAMILY_WALLET_MVP/frontend/kids.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Удалить все обёртки вкладок (кроме профиля)
# Найти начало вкладок и конец профиля
start_marker = '  <!-- Вкладка: Кошелёк -->'
profile_start = '  <!-- Вкладка: Я (Профиль) -->'

# Извлечь часть до вкладок
before_tabs = content.split(start_marker)[0]

# Извлечь профиль
profile_match = re.search(r'(  <!-- Вкладка: Я \(Профиль\) -->.*?</div>\n  </div>)', content, re.DOTALL)
profile_section = profile_match.group(1) if profile_match else ''

# Найти все секции (без комментариев обёрток)
dream_section = re.search(r'(  <div class="section" id="dreamSection".*?</div>\n  </div>)', content, re.DOTALL).group(1)
balance_section = re.search(r'(  <div class="section" id="balanceSection".*?</div>\n  </div>)', content, re.DOTALL).group(1)
my_rewards_section = re.search(r'(  <div class="section" id="myRewardsSection".*?</div>\n  </div>)', content, re.DOTALL).group(1)
tasks_section = re.search(r'(  <div class="section" id="tasksSection".*?</div>\n  </div>)', content, re.DOTALL).group(1)
history_section = re.search(r'(  <div class="section" id="historySection".*?</div>\n  </div>)', content, re.DOTALL).group(1)
shop_section = re.search(r'(  <div class="section" id="shopSection".*?</div>\n  </div>)', content, re.DOTALL).group(1)

# Собрать правильную структуру
new_structure = before_tabs + """
  <!-- Вкладка: Кошелёк -->
  <div id="tab-wallet" class="tab-content active">
""" + dream_section + """

""" + balance_section + """

""" + my_rewards_section + """

""" + history_section + """
  </div>

  <!-- Вкладка: Миссии -->
  <div id="tab-missions" class="tab-content">
""" + tasks_section + """
  </div>

  <!-- Вкладка: Магазин -->
  <div id="tab-shop" class="tab-content">
""" + shop_section + """
  </div>

""" + profile_section

# Найти часть после профиля (скрипты)
after_profile = content.split('</div>\n  </div>\n\n  <script>')[1]
new_structure += '\n\n  <script>' + after_profile

# Сохранить
with open('/Users/stanislav/Desktop/FAMILY_WALLET_MVP/frontend/kids.html', 'w', encoding='utf-8') as f:
    f.write(new_structure)

print('✅ Структура вкладок исправлена!')
print('✅ Вкладка Кошелёк: Мечта + Баланс + Награды ожидают + История')
print('✅ Вкладка Миссии: Список миссий')
print('✅ Вкладка Магазин: Доступные награды')
print('✅ Вкладка Я: Профиль')
