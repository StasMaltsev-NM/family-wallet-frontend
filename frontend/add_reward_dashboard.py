#!/usr/bin/env python3
import re

with open('parent.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Добавляем стили для дашборда наград
styles = """
    .reward-purchase-item { padding: 15px; margin: 10px 0; border: 2px solid #FF9800; background: #fff8e1; border-radius: 8px; }
    .reward-purchase-icon { font-size: 32px; display: inline-block; margin-right: 10px; }
"""

content = re.sub(r'(\.pending-dashboard[^}]+\})', r'\1\n' + styles, content)

# 2. Добавляем секцию на главной (после pendingDashboard)
dashboard_html = """
        <div id="rewardPurchasesDashboard"></div>
"""

content = re.sub(
    r'(<div id="pendingDashboard"></div>)',
    r'\1\n' + dashboard_html,
    content
)

# 3. Добавляем функцию загрузки
function_code = """
    // Загрузка купленных наград детей
    async function loadPendingRewardPurchases() {
      try {
        const res = await fetch(`${API_URL}/api/rewards/purchases/family`, {
          headers: { 'X-Invite-Code': currentCode }
        });
        
        if (!res.ok) throw new Error('Ошибка загрузки покупок');
        
        const data = await res.json();
        const dashboard = document.getElementById('rewardPurchasesDashboard');
        
        if (!data.purchases || data.purchases.length === 0) {
          dashboard.innerHTML = '';
          return;
        }
        
        const html = `
          <div style="margin: 20px 0;">
            <h3>🎁 Купленные награды детей</h3>
            ${data.purchases.map(p => `
              <div class="reward-purchase-item">
                <span class="reward-purchase-icon">${p.reward_icon}</span>
                <strong>${p.child_name}</strong> купил(а):
                <strong>${p.reward_title}</strong> за <strong>${p.price} ⭐</strong>
                <div style="color: #666; font-size: 14px; margin-top: 5px;">
                  ${new Date(p.purchased_at).toLocaleString('ru-RU')}
                </div>
                <div style="color: #FF9800; font-weight: bold; margin-top: 5px;">
                  ⏳ Ожидает выдачи
                </div>
              </div>
            `).join('')}
          </div>
        `;
        
        dashboard.innerHTML = html;
        
      } catch (err) {
        console.error('Ошибка загрузки покупок:', err);
      }
    }
"""

# Вставляем перед loadPendingTasks
content = re.sub(
    r'(    async function loadPendingTasks\(\))',
    function_code + '\n\1',
    content
)

# 4. Добавляем вызов при загрузке
content = re.sub(
    r'(loadPendingTasks\(\);)',
    r'\1\n        loadPendingRewardPurchases();',
    content
)

# 5. Добавляем в интервал обновления
content = re.sub(
    r'(setInterval\(\(\) => \{[^}]+loadPendingTasks\(\);)',
    r'\1\n        loadPendingRewardPurchases();',
    content
)

with open('parent.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("OK")
