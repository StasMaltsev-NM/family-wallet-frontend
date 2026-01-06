#!/usr/bin/env python3
import re

with open('parent.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Исправляем loadChildPersonalData - добавляем обновление мечты
old_personal_data = """        // Загружаем награды ребёнка
        await loadChildPersonalRewards(childId);
        
        // Загружаем мечту ребёнка
        await loadChildPersonalDream(childId);"""

new_personal_data = """        // Загружаем награды ребёнка
        await loadChildPersonalRewards(childId);
        
        // Загружаем мечту ребёнка
        await loadChildPersonalDream(childId);
        
        // Обновляем pending мечты на главной
        await loadPendingDreams();"""

content = content.replace(old_personal_data, new_personal_data)

# 2. Добавляем вызов обновления мечты в интервал (только если на персональной странице)
old_interval = """      setInterval(() => {
        if (currentCode) {
          loadPendingTasks();
          loadHistory();
          loadChildren();
          loadPendingRewardPurchases();
        loadPendingDreams();
        }
      }, 5000);"""

new_interval = """      setInterval(() => {
        if (currentCode) {
          loadPendingTasks();
          loadHistory();
          loadChildren();
          loadPendingRewardPurchases();
          loadPendingDreams();
          
          // Если на персональной странице - обновляем мечту ребёнка
          if (selectedChildId) {
            loadChildPersonalDream(selectedChildId);
          }
        }
      }, 5000);"""

content = content.replace(old_interval, new_interval)

# 3. Полностью переписываем loadPendingDreams с правильной проверкой фокуса
old_load_pending = re.search(
    r'async function loadPendingDreams\(\) \{.*?^\s{4}\}',
    content,
    re.DOTALL | re.MULTILINE
)

if old_load_pending:
    new_load_pending = """async function loadPendingDreams() {
      // Проверяем все input'ы с именами dreamGoal_*
      const activeElement = document.activeElement;
      if (activeElement && activeElement.id && activeElement.id.startsWith('dreamGoal_')) {
        console.log('Пропускаем обновление - пользователь вводит сумму');
        return;
      }
      
      try {
        const res = await fetch(`${API_URL}/api/dreams/pending`, {
          headers: { 'X-Invite-Code': currentCode }
        });
        
        if (!res.ok) throw new Error('Ошибка загрузки мечт');
        
        const data = await res.json();
        const dashboard = document.getElementById('pendingDreamsDashboard');
        
        if (!data.dreams || data.dreams.length === 0) {
          dashboard.innerHTML = '';
          return;
        }
        
        const html = `
          <div style="margin: 20px 0;">
            <h3>💭 Мечты детей (ожидают подтверждения)</h3>
            ${data.dreams.map(d => `
              <div class="dream-pending-item">
                <strong>${d.child_name}</strong> создал(а) мечту:
                <div style="font-size: 18px; font-weight: bold; margin: 10px 0;">
                  🎯 "${d.title}"
                </div>
                <div class="dream-goal-form">
                  <label>Цель:</label>
                  <input type="number" id="dreamGoal_${d.id}" class="dream-goal-input" placeholder="Сумма" min="1" max="1000000">
                  <span>⭐</span>
                  <button class="dream-goal-button" onclick="setDreamGoal('${d.id}')">
                    ✅ Установить
                  </button>
                </div>
              </div>
            `).join('')}
          </div>
        `;
        
        dashboard.innerHTML = html;
        
      } catch (err) {
        console.error('Ошибка загрузки pending мечт:', err);
      }
    }"""
    
    content = content.replace(old_load_pending.group(0), new_load_pending)

with open('parent.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("OK")
