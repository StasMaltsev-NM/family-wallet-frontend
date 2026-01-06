import re

file_path = 'index.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Полная очистка от старых маркеров и блоков
content = content.replace('<div id="DEBUG_MARKER" style="background: red; color: white; text-align: center; font-size: 10px; z-index: 9999; position: fixed; top: 0; width: 100%;">ВЕРСИЯ С МАГИЕЙ v2.0 (БЛОК ВВЕРХУ)</div>', '')
content = re.sub(r'<!-- СЕКЦИЯ МАГИИ -->.*?<!-- КОНЕЦ СЕКЦИИ -->', '', content, flags=re.DOTALL)
content = re.sub(r'<div id="magicSection".*?</div>\s*</div>', '', content, flags=re.DOTALL)

# 2. Добавляем стили для сетки 2х2
style_css = """
    .magic-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-top: 20px; }
    .magic-btn { background: #1c1f24; border: 1px solid #333; border-radius: 20px; padding: 15px; text-align: center; cursor: pointer; transition: all 0.2s; }
    .magic-btn:active { transform: scale(0.95); background: #2c3138; }
"""
if '.magic-grid' not in content:
    content = content.replace('</style>', style_css + '</style>')

# 3. Готовим блок Магии (скрыт по умолчанию)
magic_html = """
  <!-- СЕКЦИЯ МАГИИ -->
  <div id="magicSection" class="section" style="display: none; border: 2px solid #FFD700; background: #000; border-radius: 30px; padding: 20px; color: white;">
    <h2 style="color: #FFD700; margin-bottom: 5px;">🪄 МАГИЯ СТИЛЕЙ</h2>
    <p style="font-size: 10px; opacity: 0.5; text-transform: uppercase; letter-spacing: 1px;">Преврати себя в героя игры</p>
    
    <input type="file" id="magic-input" accept="image/*" style="display: none" onchange="handleMagicUpload(event)">
    
    <div id="magic-upload-box" onclick="document.getElementById('magic-input').click()" style="border: 2px dashed rgba(255,215,0,0.3); border-radius: 20px; padding: 40px; text-align: center; margin: 20px 0;">
      <span style="font-size: 40px;">📸</span>
      <p style="font-size: 12px; font-weight: bold; margin-top: 10px;">НАЖМИ, ЧТОБЫ ВЫБРАТЬ ФОТО</p>
    </div>

    <img id="magic-preview-img" style="width: 100%; border-radius: 20px; display: none; border: 3px solid #FFD700; margin-bottom: 20px;">

    <div id="style-selection" style="display: none">
      <div class="magic-grid">
        <div class="magic-btn" onclick="applyMagicStyle('roblox')">🤖<br><small>РОБЛОКС</small></div>
        <div class="magic-btn" onclick="applyMagicStyle('ghibli')">🌳<br><small>ГИБЛИ</small></div>
        <div class="magic-btn" onclick="applyMagicStyle('anime')">✨<br><small>АНИМЕ</small></div>
        <div class="magic-btn" onclick="applyMagicStyle('minecraft')">🧱<br><small>КРАФТ</small></div>
      </div>
    </div>
    <div id="magic-loading" style="display: none; text-align: center; padding: 20px; color: #FFD700; font-weight: bold;">🪄 КОЛДУЕМ...</div>
  </div>
  <!-- КОНЕЦ СЕКЦИИ -->
"""

# Вставляем перед историей (historySection)
content = content.replace('<div id="historySection"', magic_html + '\n    <div id="historySection"')

# 4. Логика появления после входа
# Ищем функцию, которая показывает баланс после входа
content = content.replace(
    "document.getElementById('balanceSection').style.display = 'block';",
    "document.getElementById('balanceSection').style.display = 'block';\n      document.getElementById('magicSection').style.display = 'block';"
)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("CLEANUP_AND_FINAL_MAGIC_OK")
