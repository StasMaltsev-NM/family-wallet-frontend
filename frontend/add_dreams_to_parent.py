#!/usr/bin/env python3
import re

with open('parent.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Добавляем стили
styles = """
    .dream-pending-item { padding: 15px; margin: 10px 0; border: 2px solid #9C27B0; background: #f3e5f5; border-radius: 8px; }
    .dream-goal-form { display: flex; gap: 10px; margin-top: 10px; align-items: center; }
    .dream-goal-input { width: 150px; padding: 8px; border: 2px solid #9C27B0; border-radius: 5px; font-size: 16px; }
    .dream-goal-button { background: #9C27B0; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer; font-weight: bold; }
    .dream-active-item { padding: 15px; margin: 10px 0; border: 2px solid #4CAF50; background: #e8f5e9; border-radius: 8px; }
    .dream-progress-bar { width: 100%; height: 25px; background: #e0e0e0; border-radius: 12px; overflow: hidden; margin: 10px 0; }
    .dream-progress-fill { height: 100%; background: linear-gradient(90deg, #4CAF50 0%, #8BC34A 100%); transition: width 0.3s; }
"""

content = re.sub(r'(\.reward-purchase-icon[^}]+\})', r'\1\n' + styles, content)

# 2. Добавляем HTML для pending мечт (после rewardPurchasesDashboard)
pending_dreams_html = """
        <div id="pendingDreamsDashboard"></div>
"""

content = re.sub(
    r'(<div id="rewardPurchasesDashboard"></div>)',
    r'\1\n' + pending_dreams_html,
    content
)

# 3. Добавляем HTML для активных мечт (в начале персональной страницы ребёнка, перед миссиями)
active_dream_html = """        
        <div id="childPersonalDream"></div>
"""

content = re.sub(
    r'(<div class="section">\s*<h2>🎯 Миссии</h2>)',
    active_dream_html + '\n\n\\1',
    content
)

# 4. Добавляем JavaScript функции
js_functions = """
    // ============================
    // МЕЧТЫ ДЕТЕЙ (РОДИТЕЛЬ)
    // ============================

    async function loadPendingDreams() {
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
    }

    async function setDreamGoal(dreamId) {
      const input = document.getElementById(`dreamGoal_${dreamId}`);
      const amount = parseInt(input.value);
      
      if (!amount || amount < 1 || amount > 1000000) {
        alert('Введите сумму от 1 до 1000000');
        return;
      }
      
      try {
        const res = await fetch(`${API_URL}/api/dreams/set-goal`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-Invite-Code': currentCode
          },
          body: JSON.stringify({ dream_id: dreamId, target_amount: amount })
        });
        
        if (!res.ok) {
          const err = await res.json();
          alert(`Ошибка: ${err.error}`);
          return;
        }
        
        const data = await res.json();
        alert(`✅ ${data.message}`);
        
        loadPendingDreams();
        loadActiveDreams();
        
      } catch (err) {
        alert(`Ошибка: ${err.message}`);
      }
    }

    async function loadActiveDreams() {
      // Пока не используем на главной, только на персональной странице
      // Функция будет вызываться при открытии персональной страницы ребёнка
    }

    async function loadChildPersonalDream(childId) {
      try {
        const res = await fetch(`${API_URL}/api/dreams/active`, {
          headers: { 'X-Invite-Code': currentCode }
        });
        
        if (!res.ok) throw new Error('Ошибка загрузки мечт');
        
        const data = await res.json();
        const childDream = (data.dreams || []).find(d => d.child_id === childId);
        
        const container = document.getElementById('childPersonalDream');
        
        if (!childDream) {
          container.innerHTML = '';
          return;
        }
        
        const progress = Math.min(100, Math.round((childDream.current_amount / childDream.target_amount) * 100));
        
        container.innerHTML = `
          <div class="dream-active-item">
            <h3>🎯 Мечта: ${childDream.title}</h3>
            <div class="dream-progress-bar">
              <div class="dream-progress-fill" style="width: ${progress}%"></div>
            </div>
            <div style="text-align: center; font-size: 18px; font-weight: bold;">
              ${childDream.current_amount} / ${childDream.target_amount} ⭐
            </div>
            <div style="text-align: center; color: #666; margin-top: 5px;">
              Прогресс: ${progress}%
            </div>
          </div>
        `;
        
      } catch (err) {
        console.error('Ошибка загрузки мечты ребёнка:', err);
      }
    }

"""

# Вставляем функции перед loadPendingRewardPurchases
content = re.sub(
    r'(    // Загрузка купленных наград детей\n    async function loadPendingRewardPurchases)',
    js_functions + '\n\\1',
    content
)

# 5. Добавляем вызовы при загрузке главной
content = content.replace(
    "loadPendingRewardPurchases();",
    """loadPendingRewardPurchases();
        loadPendingDreams();""",
    1  # Только первое вхождение
)

# 6. Добавляем вызов в интервал обновления
content = re.sub(
    r'(setInterval\(\(\) => \{[^}]*loadPendingRewardPurchases\(\);)',
    r'\1\n        loadPendingDreams();',
    content
)

# 7. Добавляем загрузку мечты в loadChildPersonalData
content = re.sub(
    r'(await loadChildPersonalRewards\(childId\);)',
    r'\1\n        \n        // Загружаем мечту ребёнка\n        await loadChildPersonalDream(childId);',
    content
)

with open('parent.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("OK")
