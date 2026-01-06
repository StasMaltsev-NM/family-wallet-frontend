#!/usr/bin/env python3
import re

with open('/Users/stanislav/Desktop/FAMILY_WALLET_MVP/frontend/kids.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Добавить CSS для навигации (после существующих стилей, перед </style>)
nav_css = """
    /* Навигация */
    .nav-tabs { display: flex; background: #333; margin: 0; padding: 0; }
    .nav-tabs button { flex: 1; padding: 15px; background: #333; color: white; border: none; cursor: pointer; font-size: 16px; }
    .nav-tabs button.active { background: #4CAF50; }
    .tab-content { display: none; }
    .tab-content.active { display: block; }
"""

content = content.replace('  </style>', nav_css + '\n  </style>')

# 2. Добавить навигационные кнопки после заголовка <h1>
nav_buttons = """
  
  <div class="nav-tabs">
    <button class="active" onclick="showTab('tab-wallet')">💰 Кошелёк</button>
    <button onclick="showTab('tab-missions')">🎯 Миссии</button>
    <button onclick="showTab('tab-shop')">🎁 Магазин</button>
    <button onclick="showTab('tab-profile')">👤 Я</button>
  </div>
"""

content = content.replace('  <h1>👶 Family Wallet — Ребёнок</h1>', 
                         '  <h1>👶 Family Wallet — Ребёнок</h1>' + nav_buttons)

# 3. Обернуть секции в вкладки
# Вкладка "Кошелёк" (баланс + мечты + история)
content = content.replace(
    '  <div class="section" id="dreamSection"',
    '  <!-- Вкладка: Кошелёк -->\n  <div id="tab-wallet" class="tab-content active">\n  <div class="section" id="dreamSection"'
)

# Закрыть вкладку "Кошелёк" перед tasksSection
content = re.sub(
    r'(  <div class="section" id="tasksSection")',
    r'  </div>\n  <!-- Конец вкладки: Кошелёк -->\n\n  <!-- Вкладка: Миссии -->\n  <div id="tab-missions" class="tab-content">\n\1',
    content
)

# Закрыть вкладку "Миссии" и открыть "Магазин" перед myRewardsSection
content = re.sub(
    r'(  <div class="section" id="myRewardsSection")',
    r'  </div>\n  <!-- Конец вкладки: Миссии -->\n\n  <!-- Вкладка: Магазин -->\n  <div id="tab-shop" class="tab-content">\n\1',
    content
)

# 4. Добавить вкладку "Я" (профиль) перед закрывающим <script>
profile_tab = """
  </div>
  <!-- Конец вкладки: Магазин -->

  <!-- Вкладка: Я (Профиль) -->
  <div id="tab-profile" class="tab-content">
    <div class="section">
      <h2>👤 Мой профиль</h2>
      <div id="profileInfo">
        <p><strong>Имя:</strong> <span id="profileName">-</span></p>
        <p><strong>Баланс:</strong> <span id="profileBalance">0</span> ₽</p>
        <p><strong>Выполнено миссий:</strong> <span id="profileMissionsCount">0</span></p>
        <p><strong>Получено наград:</strong> <span id="profileRewardsCount">0</span></p>
      </div>
    </div>
  </div>
"""

# Найти место перед <script> и вставить профиль
content = re.sub(r'(\s*<script>)', profile_tab + r'\n\1', content)

# 5. Добавить функцию showTab в JavaScript (перед закрывающим </script>)
show_tab_js = """
    // Функция переключения вкладок
    function showTab(tabId) {
      document.querySelectorAll('.tab-content').forEach(tab => tab.classList.remove('active'));
      document.querySelectorAll('.nav-tabs button').forEach(btn => btn.classList.remove('active'));
      document.getElementById(tabId).classList.add('active');
      event.target.classList.add('active');
      
      // Загрузить данные профиля при переходе на вкладку
      if (tabId === 'tab-profile') loadProfile();
    }

    // Загрузка данных профиля
    async function loadProfile() {
      const inviteCode = localStorage.getItem('childCode');
      if (!inviteCode) return;
      
      try {
        // Получить баланс
        const balanceRes = await fetch(`${API_URL}/api/wallet/balance`, {
          headers: { 'X-Invite-Code': inviteCode }
        });
        const balanceData = await balanceRes.json();
        
        // Получить миссии
        const tasksRes = await fetch(`${API_URL}/api/tasks/list`, {
          headers: { 'X-Invite-Code': inviteCode }
        });
        const tasksData = await tasksRes.json();
        
        // Получить награды
        const rewardsRes = await fetch(`${API_URL}/api/shop/my-rewards`, {
          headers: { 'X-Invite-Code': inviteCode }
        });
        const rewardsData = await rewardsRes.json();
        
        // Обновить UI
        document.getElementById('profileName').textContent = inviteCode.replace('KID_', '');
        document.getElementById('profileBalance').textContent = balanceData.balance || 0;
        document.getElementById('profileMissionsCount').textContent = tasksData.tasks?.filter(t => t.status === 'CONFIRMED').length || 0;
        document.getElementById('profileRewardsCount').textContent = rewardsData.my_rewards?.length || 0;
        
      } catch (e) {
        console.error('Ошибка загрузки профиля:', e);
      }
    }
"""

content = content.replace('  </script>', show_tab_js + '\n  </script>')

# Сохранить
with open('/Users/stanislav/Desktop/FAMILY_WALLET_MVP/frontend/kids.html', 'w', encoding='utf-8') as f:
    f.write(content)

print('✅ Навигация по вкладкам добавлена в kids.html!')
print('✅ Добавлена вкладка "Я" (профиль)')
