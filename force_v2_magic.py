import os

file_path = 'index.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Обновляем визуальный маркер на v2.0
content = content.replace('ВЕРСИЯ С МАГИЕЙ v1.0', 'ВЕРСИЯ С МАГИЕЙ v2.0 (БЛОК ВВЕРХУ)')

# 2. Удаляем старые вставки magicSection если они были внизу
import re
content = re.sub(r'<!-- СЕКЦИЯ МАГИИ -->.*?<!-- КОНЕЦ СЕКЦИИ -->', '', content, flags=re.DOTALL)

# 3. Готовим блок Магии для вставки ВВЕРХ
magic_top = """
  <!-- СЕКЦИЯ МАГИИ -->
  <div id="magicSection" style="margin: 20px; padding: 20px; background: #000; border: 3px solid gold; border-radius: 20px; color: white; position: relative; z-index: 9999;">
    <h2 style="color: gold;">🪄 МАГИЯ СТИЛЕЙ v2.0</h2>
    <input type="file" id="magic-input" accept="image/*" onchange="handleMagicUpload(event)" style="margin-bottom: 10px;">
    <div id="style-selection" style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
        <button onclick="applyMagicStyle('roblox')" style="padding: 10px;">🤖 РОБЛОКС</button>
        <button onclick="applyMagicStyle('ghibli')" style="padding: 10px;">🌳 ГИБЛИ</button>
    </div>
    <div id="magic-loading" style="display: none; color: gold;">🪄 КОЛДУЕМ...</div>
  </div>
  <!-- КОНЕЦ СЕКЦИИ -->
"""

# Вставляем сразу после открывающего body
content = content.replace('<body>', '<body>' + magic_top)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("FORCE_V2_PATCH_DONE")
