#!/usr/bin/env python3

with open('/Users/stanislav/Desktop/FAMILY_WALLET_MVP/frontend/kids.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Секция авторизации
auth_section = """  
  <div class="section">
    <h2>Авторизация</h2>
    <input type="text" id="inviteCode" placeholder="Введите код ребёнка (KID_STAS)" value="KID_STAS">
    <button onclick="login()">Войти</button>
    <div id="authStatus"></div>
  </div>

"""

# Вставить перед навигацией
content = content.replace('  <div class="nav-tabs">', auth_section + '  <div class="nav-tabs">')

# Сохранить
with open('/Users/stanislav/Desktop/FAMILY_WALLET_MVP/frontend/kids.html', 'w', encoding='utf-8') as f:
    f.write(content)

print('✅ Секция авторизации добавлена!')
