#!/usr/bin/env python3

with open('parent.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Добавляем секцию ПОСЛЕ "Задачи на проверке" и ПЕРЕД "История"
reward_section = """
      <div class="section">
        <h2>🎁 Купленные награды детей</h2>
        <div id="rewardPurchasesDashboard"></div>
      </div>
"""

# Вставляем перед секцией "История"
content = content.replace(
    '''      <div class="section">
        <h2>История</h2>''',
    reward_section + '''      <div class="section">
        <h2>История</h2>'''
)

with open('parent.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("OK")
