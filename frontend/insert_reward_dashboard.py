#!/usr/bin/env python3

with open('parent.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 1. Найти и добавить HTML после pendingDashboard
new_lines = []
for i, line in enumerate(lines):
    new_lines.append(line)
    if '<div id="pendingDashboard"></div>' in line:
        # Добавляем новый div с тем же отступом
        indent = line[:len(line) - len(line.lstrip())]
        new_lines.append(f'{indent}<div id="rewardPurchasesDashboard"></div>\n')

lines = new_lines

# 2. Найти loadPendingTasks и добавить функцию ПЕРЕД ней
function_code = """    // Загрузка купленных наград детей
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
              <div style="padding: 15px; margin: 10px 0; border: 2px solid #FF9800; background: #fff8e1; border-radius: 8px;">
                <span style="font-size: 32px; margin-right: 10px;">${p.reward_icon}</span>
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

new_lines = []
for i, line in enumerate(lines):
    if 'async function loadPendingTasks()' in line:
        new_lines.append(function_code)
    new_lines.append(line)

lines = new_lines

# 3. Добавить вызов после loadPendingTasks();
new_lines = []
for i, line in enumerate(lines):
    new_lines.append(line)
    if 'loadPendingTasks();' in line and 'loadPendingRewardPurchases' not in line:
        indent = line[:len(line) - len(line.lstrip())]
        new_lines.append(f'{indent}loadPendingRewardPurchases();\n')

with open('parent.html', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print("OK")
