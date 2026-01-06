import re
import os

file_path = 'index.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Удаляем все старые/сломанные попытки вставить Магию
content = re.sub(r'<!-- СЕКЦИЯ МАГИИ -->.*?<!-- КОНЕЦ СЕКЦИИ -->', '', content, flags=re.DOTALL)

# 2. Добавляем блок Магии в гарантированное место (перед </body>)
magic_html = """
  <!-- СЕКЦИЯ МАГИИ -->
  <div id="magicSection" class="section" style="display: none; border: 3px solid #FFD700; background: #000; border-radius: 30px; padding: 20px; color: white; margin-top: 30px;">
    <h2 style="color: #FFD700;">🪄 МАГИЯ СТИЛЕЙ</h2>
    <p style="font-size: 12px; opacity: 0.6;">ПРЕВРАТИ СЕБЯ В ГЕРОЯ ИГРЫ</p>
    <input type="file" id="magic-input" accept="image/*" style="display: none" onchange="handleMagicUpload(event)">
    <div id="magic-upload-box" onclick="document.getElementById('magic-input').click()" style="border: 2px dashed gold; padding: 40px; text-align: center; margin: 20px 0; border-radius: 20px; cursor: pointer;">
      <span style="font-size: 40px;">📸</span>
      <p>НАЖМИ ДЛЯ ЗАГРУЗКИ ФОТО</p>
    </div>
    <img id="magic-preview-img" style="width: 100%; border-radius: 20px; display: none; border: 2px solid gold; margin-bottom: 20px;">
    <div id="style-selection" style="display: none; grid-template-columns: 1fr 1fr; gap: 10px;">
        <button onclick="applyMagicStyle('roblox')" style="background: #222; color: white; border: 1px solid #444; padding: 15px; border-radius: 12px;">🤖 РОБЛОКС</button>
        <button onclick="applyMagicStyle('ghibli')" style="background: #222; color: white; border: 1px solid #444; padding: 15px; border-radius: 12px;">🌳 ГИБЛИ</button>
        <button onclick="applyMagicStyle('anime')" style="background: #222; color: white; border: 1px solid #444; padding: 15px; border-radius: 12px;">✨ АНИМЕ</button>
        <button onclick="applyMagicStyle('minecraft')" style="background: #222; color: white; border: 1px solid #444; padding: 15px; border-radius: 12px;">🧱 КРАФТ</button>
    </div>
    <div id="magic-loading" style="display: none; text-align: center; color: gold;">🪄 КОЛДУЕМ...</div>
  </div>
  <!-- КОНЕЦ СЕКЦИИ -->
"""
content = content.replace('</body>', magic_html + '</body>')

# 3. ЧИНИМ JS ОШИБКУ (делаем показ секций безопасным)
# Заменяем прямые вызовы .style.display на безопасную функцию
safe_show_js = """
    function safeShow(id) {
      const el = document.getElementById(id);
      if (el) el.style.display = 'block';
    }
"""
if 'function safeShow' not in content:
    content = content.replace('<script>', '<script>\n' + safe_show_js)

# Исправляем логику входа: заменяем проблемные строки на вызов safeShow
content = re.sub(r"document\.getElementById\('balanceSection'\)\.style\.display = 'block';", "safeShow('balanceSection');", content)
content = re.sub(r"document\.getElementById\('magicSection'\)\.style\.display = 'block';", "safeShow('magicSection');", content)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("SAFE_FIX_COMPLETED")
