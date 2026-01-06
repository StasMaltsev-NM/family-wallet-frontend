#!/usr/bin/env python3
import re

with open('parent.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Добавляем HTML для персональной страницы ПОСЛЕ списка детей
personal_view_html = """
      <!-- Персональная страница ребёнка -->
      <div id="childPersonalView" style="display:none;">
        <button onclick="backToChildrenList()" style="margin-bottom: 20px;">
          ← Назад к списку детей
        </button>
        
        <div id="childPersonalHeader"></div>
        
        <div class="section">
          <h2>🎯 Миссии</h2>
          <div id="childPersonalTasks"></div>
        </div>
        
        <div class="section">
          <h2>🎁 Купленные награды</h2>
          <div id="childPersonalRewards"></div>
        </div>
      </div>
"""

# Вставляем после childrenList
content = re.sub(
    r'(<div id="childrenList"></div>)',
    r'\1\n' + personal_view_html,
    content
)

# 2. Добавляем CSS для кликабельных карточек
css_addition = """
    .child-card { cursor: pointer; transition: transform 0.2s, box-shadow 0.2s; }
    .child-card:hover { transform: translateY(-2px); box-shadow: 0 4px 8px rgba(0,0,0,0.2); }
"""

content = re.sub(
    r'(\.history-item[^}]+\})',
    r'\1\n' + css_addition,
    content
)

# 3. Добавляем JavaScript функции
js_functions = """
    // ============================
    // ПЕРСОНАЛЬНАЯ СТРАНИЦА РЕБЁНКА
    // ============================
    
    let selectedChildId = null;

    function showChildPersonalView(childId) {
      selectedChildId = childId;
      
      // Скрываем общий view
      document.getElementById('childrenList').style.display = 'none';
      document.getElementById('pendingTasksSection').style.display = 'none';
      document.getElementById('rewardPurchasesDashboard').style.display = 'none';
      document.getElementById('historySection').style.display = 'none';
      
      // Показываем персональный view
      document.getElementById('childPersonalView').style.display = 'block';
      
      loadChildPersonalData(childId);
    }

    function backToChildrenList() {
      selectedChildId = null;
      
      // Показываем общий view
      document.getElementById('childrenList').style.display = 'block';
      document.getElementById('pendingTasksSection').style.display = 'block';
      document.getElementById('rewardPurchasesDashboard').style.display = 'block';
      document.getElementById('historySection').style.display = 'block';
      
      // Скрываем персональный view
      document.getElementById('childPersonalView').style.display = 'none';
    }

    async function loadChildPersonalData(childId) {
      try {
        // Загружаем данные ребёнка
        const childRes = await fetch(`${API_URL}/api/children/${childId}`, {
          headers: { 'X-Invite-Code': currentCode }
        });
        
        if (!childRes.ok) throw new Error('Ошибка загрузки данных ребёнка');
        
        const childData = await childRes.json();
        const child = childData.child;
        
        // Отображаем заголовок
        document.getElementById('childPersonalHeader').innerHTML = `
          <div style="padding: 20px; background: #f0f0f0; border-radius: 8px; margin-bottom: 20px;">
            <h2>${child.name} (${child.role}, ${child.age} лет)</h2>
            <div style="font-size: 24px; font-weight: bold; margin-top: 10px;">
              Баланс: ${child.balance} ⭐ | На проверке: ${child.pending_balance} ⭐
            </div>
            <div style="color: #666; margin-top: 5px;">
              Код ребёнка: ${child.invite_code}
            </div>
          </div>
        `;
        
        // Загружаем миссии ребёнка
        await loadChildPersonalTasks(childId);
        
        // Загружаем награды ребёнка
        await loadChildPersonalRewards(childId);
        
      } catch (err) {
        alert(`Ошибка: ${err.message}`);
        backToChildrenList();
      }
    }

    async function loadChildPersonalTasks(childId) {
      try {
        const res = await fetch(`${API_URL}/api/tasks/list`, {
          headers: { 'X-Invite-Code': currentCode }
        });
        
        if (!res.ok) throw new Error('Ошибка загрузки миссий');
        
        const data = await res.json();
        const childTasks = (data.tasks || []).filter(t => t.child_id === childId && t.status !== 'ARCHIVED');
        
        const list = document.getElementById('childPersonalTasks');
        
        if (childTasks.length === 0) {
          list.innerHTML = '<div class="empty-state">Нет миссий</div>';
          return;
        }
        
        const idleTasks = childTasks.filter(t => t.status === 'IDLE');
        const waitingTasks = childTasks.filter(t => t.status === 'WAITING');
        
        let html = '';
        
        if (idleTasks.length > 0) {
          html += '<h3>📋 Назначенные миссии</h3>';
          html += idleTasks.map(t => `
            <div class="task-item status-${t.status}">
              <span style="font-size: 24px; margin-right: 10px;">${t.icon}</span>
              <strong>${t.title}</strong><br>
              ${t.description || ''}<br>
              Награда: <strong>${t.reward_amount} ⭐</strong>
            </div>
          `).join('');
        }
        
        if (waitingTasks.length > 0) {
          html += '<h3 style="margin-top: 20px;">⏳ На проверке</h3>';
          html += waitingTasks.map(t => `
            <div class="task-item status-${t.status}">
              <span style="font-size: 24px; margin-right: 10px;">${t.icon}</span>
              <strong>${t.title}</strong><br>
              ${t.description || ''}<br>
              Награда: <strong>${t.reward_amount} ⭐</strong><br>
              <button onclick="handleTaskAction('${t.id}', 'confirm')" style="background: #4CAF50; color: white; margin-top: 10px;">
                ✅ Подтвердить
              </button>
              <button onclick="handleTaskAction('${t.id}', 'reject')" style="background: #f44336; color: white; margin-top: 10px;">
                ❌ Отклонить
              </button>
            </div>
          `).join('');
        }
        
        list.innerHTML = html;
        
      } catch (err) {
        document.getElementById('childPersonalTasks').innerHTML = 
          `<p class="error">Ошибка: ${err.message}</p>`;
      }
    }

    async function loadChildPersonalRewards(childId) {
      try {
        const res = await fetch(`${API_URL}/api/rewards/purchases`, {
          headers: { 'X-Invite-Code': currentCode }
        });
        
        if (!res.ok) throw new Error('Ошибка загрузки наград');
        
        const data = await res.json();
        const childRewards = (data.purchases || []).filter(p => p.child_id === childId && p.status === 'pending');
        
        const list = document.getElementById('childPersonalRewards');
        
        if (childRewards.length === 0) {
          list.innerHTML = '<div class="empty-state">Нет купленных наград</div>';
          return;
        }
        
        list.innerHTML = childRewards.map(p => `
          <div style="padding: 15px; margin: 10px 0; border: 2px solid #FF9800; background: #fff8e1; border-radius: 8px;">
            <span style="font-size: 32px; margin-right: 10px;">${p.reward_icon}</span>
            <strong>${p.reward_title}</strong> за <strong>${p.price} ⭐</strong>
            <div style="color: #666; font-size: 14px; margin-top: 5px;">
              ${new Date(p.purchased_at).toLocaleString('ru-RU')}
            </div>
            <div style="color: #FF9800; font-weight: bold; margin-top: 5px;">
              ⏳ Ожидает выдачи
            </div>
          </div>
        `).join('');
        
      } catch (err) {
        document.getElementById('childPersonalRewards').innerHTML = 
          `<p class="error">Ошибка: ${err.message}</p>`;
      }
    }

"""

# Вставляем функции перед loadPendingRewardPurchases
content = re.sub(
    r'(    // Загрузка купленных наград детей\n    async function loadPendingRewardPurchases)',
    js_functions + r'\n\1',
    content
)

# 4. Модифицируем loadChildren чтобы карточки были кликабельными
content = re.sub(
    r'(<div class="child-item">)',
    r'<div class="child-item child-card" onclick="showChildPersonalView(\'' + r"${child.id}'" + r')">',
    content
)

with open('parent.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("OK")
