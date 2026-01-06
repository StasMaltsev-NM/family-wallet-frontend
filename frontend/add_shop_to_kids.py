#!/usr/bin/env python3
import re

with open('kids.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Добавляем стили для магазина
styles_to_add = """
    .reward-item { padding: 15px; margin: 10px 0; border: 2px solid #4CAF50; background: #f0fff0; border-radius: 8px; }
    .reward-icon { font-size: 48px; display: inline-block; margin-right: 15px; }
    .reward-info { display: inline-block; vertical-align: top; }
    .reward-price { font-size: 20px; font-weight: bold; color: #FF9800; margin: 10px 0; }
    .buy-button { background: #4CAF50; color: white; border: none; padding: 12px 24px; border-radius: 5px; font-size: 16px; cursor: pointer; }
    .buy-button:disabled { background: #ccc; cursor: not-allowed; }
    .my-reward-item { padding: 15px; margin: 10px 0; border: 2px solid #FF9800; background: #fff8e1; border-radius: 8px; }
    .confirm-button { background: #4CAF50; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer; }
"""

content = content.replace('  </style>', styles_to_add + '  </style>')

# 2. Добавляем секцию "Мои награды" после balanceSection
my_rewards_section = """
  <div class="section" id="myRewardsSection" style="display:none;">
    <h2>🎁 Мои награды</h2>
    <div id="myRewardsList"></div>
  </div>
"""

content = re.sub(
    r'(<div class="section" id="balanceSection"[^>]*>.*?</div>\s*</div>)',
    r'\1\n' + my_rewards_section,
    content,
    flags=re.DOTALL
)

# 3. Добавляем секцию "Магазин" после historySection
shop_section = """
  <div class="section" id="shopSection" style="display:none;">
    <h2>🛒 Магазин наград</h2>
    <div id="shopRewardsList"></div>
  </div>
"""

content = re.sub(
    r'(<div class="section" id="historySection"[^>]*>.*?</div>\s*</div>)',
    r'\1\n' + shop_section,
    content,
    flags=re.DOTALL
)

with open('kids.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("OK")
