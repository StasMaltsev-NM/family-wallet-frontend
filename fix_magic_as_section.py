import re

file_path = 'index.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Удаляем старую попытку вставить вкладку (если она есть)
content = re.sub(r'<div id="tab-magic".*?</div>\s*</div>', '', content, flags=re.DOTALL)

# 2. Создаем код Магии как полноценной СЕКЦИИ (как Миссии или Магазин)
magic_section = """
  <div id="magicSection" class="section" style="border: 2px solid #FFD700; background: #000; color: white;">
    <h2 style="color: #FFD700;">✨ МАГИЯ СТИЛЕЙ</h2>
    <p class="text-sm opacity-60">Преврати своё фото в игровой мир!</p>
    
    <input type="file" id="magic-input" accept="image/*" style="display: none" onchange="handleMagicUpload(event)">
    
    <div id="magic-upload-box" class="magic-upload-area" onclick="document.getElementById('magic-input').click()" style="border: 2px dashed #FFD700; padding: 30px; text-align: center; margin: 20px 0; border-radius: 15px;">
      <span style="font-size: 40px;">📸</span>
      <p>Нажми, чтобы выбрать фото</p>
    </div>

    <img id="magic-preview-img" style="width: 100%; border-radius: 15px; display: none; margin-bottom: 20px;">
    
    <div id="style-selection" style="display: none">
      <p style="font-size: 12px; font-weight: bold; margin-bottom: 10px;">ВЫБЕРИ СТИЛЬ:</p>
      <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
        <button onclick="applyMagicStyle('roblox')" style="background: #333; color: white; border: 1px solid #555; padding: 15px; border-radius: 10px;">🤖 РОБЛОКС</button>
        <button onclick="applyMagicStyle('ghibli')" style="background: #333; color: white; border: 1px solid #555; padding: 15px; border-radius: 10px;">🌳 ГИБЛИ</button>
        <button onclick="applyMagicStyle('anime')" style="background: #333; color: white; border: 1px solid #555; padding: 15px; border-radius: 10px;">✨ АНИМЕ</button>
        <button onclick="applyMagicStyle('minecraft')" style="background: #333; color: white; border: 1px solid #555; padding: 15px; border-radius: 10px;">🧱 КРАФТ</button>
      </div>
    </div>

    <div id="magic-loading" style="display: none; text-align: center; padding: 20px; color: #FFD700;">🪄 КОЛДУЕМ...</div>
  </div>
"""

# 3. Вставляем Магию ПОСЛЕ секции Магазина (shopSection)
if 'id="shopSection"' in content:
    content = content.replace('id="shopSection"', 'id="shopSection"') # оставляем как есть
    # Вставляем после закрывающего тега секции магазина
    parts = content.split('<div id="shopSection"')
    if len(parts) > 1:
        # Ищем конец дива магазина
        content = content.replace('<!-- Конец магазина -->', '<!-- Конец магазина -->\n' + magic_section)
        # Если комментария нет, просто вставим перед </body>
        if magic_section not in content:
            content = content.replace('</body>', magic_section + '\n</body>')

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("SECTION_PATCH_DONE")
