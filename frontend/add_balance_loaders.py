#!/usr/bin/env python3
import re

file_path = 'kids.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Найти функцию showTab и добавить загрузку балансов
old_showTab = r'''    function showTab\(tabId\) \{
      document\.querySelectorAll\('\.tab-content'\)\.forEach\(tab => tab\.classList\.remove\('active'\)\);
      document\.querySelectorAll\('\.nav-tabs button'\)\.forEach\(btn => btn\.classList\.remove\('active'\)\);
      document\.getElementById\(tabId\)\.classList\.add\('active'\);
      event\.target\.classList\.add\('active'\);
      
      // Загрузить данные профиля при переходе на вкладку
      if \(tabId === 'tab-profile'\) loadProfile\(\);
    \}'''

new_showTab = '''    function showTab(tabId) {
      document.querySelectorAll('.tab-content').forEach(tab => tab.classList.remove('active'));
      document.querySelectorAll('.nav-tabs button').forEach(btn => btn.classList.remove('active'));
      document.getElementById(tabId).classList.add('active');
      event.target.classList.add('active');
      
      // Загрузить данные при переходе на вкладки
      if (tabId === 'tab-profile') loadProfile();
      if (tabId === 'tab-missions') loadMissionsBalance();
      if (tabId === 'tab-shop') loadShopBalance();
    }

    // Загрузка баланса для вкладки Миссии
    async function loadMissionsBalance() {
      try {
        const res = await fetch(`${API_URL}/api/auth/whoami`, {
          headers: { 'X-Invite-Code': currentCode }
        });
        const data = await res.json();
        document.getElementById('missionsBalance').textContent = `${data.balance || 0} ⭐`;
      } catch (e) {
        console.error('Ошибка загрузки баланса миссий:', e);
      }
    }

    // Загрузка баланса для вкладки Магазин
    async function loadShopBalance() {
      try {
        const res = await fetch(`${API_URL}/api/auth/whoami`, {
          headers: { 'X-Invite-Code': currentCode }
        });
        const data = await res.json();
        
        document.getElementById('shopBalance').textContent = `${data.balance || 0} ⭐`;
        document.getElementById('shopPending').textContent = `${data.pending_balance || 0} ⭐`;
      } catch (e) {
        console.error('Ошибка загрузки баланса магазина:', e);
      }
    }'''

content = re.sub(old_showTab, new_showTab, content)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print('✅ Логика загрузки балансов добавлена!')
print('📊 Теперь балансы обновляются при переходе на вкладки:')
print('   - Миссии: доступный баланс')
print('   - Магазин: доступный + на подтверждении')
