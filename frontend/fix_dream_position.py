#!/usr/bin/env python3
import re

with open('kids.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Убираем dreamSection из текущей позиции
content = re.sub(
    r'\n  <div class="section" id="dreamSection"[^>]*>.*?</div>\n  </div>',
    '',
    content,
    flags=re.DOTALL
)

# Вставляем ПЕРЕД balanceSection
dream_html = """
  <div class="section" id="dreamSection" style="display:none;">
    <div id="dreamDashboard"></div>
  </div>

"""

content = re.sub(
    r'(  <div class="section" id="balanceSection")',
    dream_html + r'\1',
    content
)

with open('kids.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("OK")
