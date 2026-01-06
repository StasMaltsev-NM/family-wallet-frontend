import re

file_path = 'index.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Удаляем все старые куски Магии, чтобы не было дублей
content = re.sub(r'<div id="tab-magic".*?</div>\s*</div>', '', content, flags=re.DOTALL)
content = re.sub(r'<div id="magicSection".*?</div>\s*</div>', '', content, flags=re.DOTALL)

# 2. Готовим чистый HTML блок в стиле твоего скриншота (Yellow Glow + Dark Cards)
magic_html = """
  <!-- СЕКЦИЯ МАГИИ -->
  <div id="magicSection" style="margin: 40px 0; padding: 25px; background: #0a0a0a; border: 2px solid #FFD700; border-radius: 35px; box-shadow: 0 0 20px rgba(255, 215, 0, 0.1); color: white;">
    <h2 style="color: #FFD700; font-size: 24px; font-weight: 900; margin-bottom: 10px;">🪄 МАГИЯ СТИЛЕЙ</h2>
    <p style="opacity: 0.6; font-size: 12px; margin-bottom: 20px;">ПРЕВРАТИ СЕБЯ В ГЕРОЯ ИГРЫ</p>

    <input type="file" id="magic-input" accept="image/*" style="display: none" onchange="handleMagicUpload(event)">
    
    <!-- Рамка загрузки -->
    <div id="magic-upload-box" onclick="document.getElementById('magic-input').click()" style="border: 2px dashed rgba(255,215,0,0.4); border-radius: 25px; padding: 50px; text-align: center; cursor: pointer; margin-bottom: 20px;">
      <span style="font-size: 50px;">📸</span>
      <p style="margin-top: 10px; font-weight: bold; opacity: 0.8;">НАЖМИ, ЧТОБЫ ВЫБРАТЬ ФОТО</p>
    </div>

    <!-- Превью -->
    <img id="magic-preview-img" style="width: 100%; border-radius: 25px; display: none; border: 4px solid #FFD700; margin-bottom: 20px;">

    <!-- Кнопки стилей -->
    <div id="style-selection" style="display: none">
      <p style="font-size: 10px; font-weight: 900; color: #FFD700; letter-spacing: 2px; margin-bottom: 15px;">⚡️ ВЫБЕРИ ИГРОВОЙ МИР:</p>
      <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px;">
        <div onclick="applyMagicStyle('roblox')" style="background: #1c1f24; padding: 20px; border-radius: 20px; text-align: center; border: 1px solid #333;">
          <span style="font-size: 30px;">🤖</span><br><b style="font-size: 12px;">РОБЛОКС</b>
        </div>
        <div onclick="applyMagicStyle('ghibli')" style="background: #1c1f24; padding: 20px; border-radius: 20px; text-align: center; border: 1px solid #333;">
          <span style="font-size: 30px;">🌳</span><br><b style="font-size: 12px;">ГИБЛИ</b>
        </div>
        <div onclick="applyMagicStyle('anime')" style="background: #1c1f24; padding: 20px; border-radius: 20px; text-align: center; border: 1px solid #333;">
          <span style="font-size: 30px;">✨</span><br><b style="font-size: 12px;">АНИМЕ</b>
        </div>
        <div onclick="applyMagicStyle('minecraft')" style="background: #1c1f24; padding: 20px; border-radius: 20px; text-align: center; border: 1px solid #333;">
          <span style="font-size: 30px;">🧱</span><br><b style="font-size: 12px;">КРАФТ</b>
        </div>
      </div>
    </div>

    <div id="magic-loading" style="display: none; text-align: center; padding: 30px; font-weight: 900; color: #FFD700; letter-spacing: 3px;">🪄 КОЛДУЕМ...</div>
  </div>
"""

# 3. Добавляем JS логику
magic_js = """
  <script>
    let selectedImageBase64 = null;
    function handleMagicUpload(event) {
      const file = event.target.files[0];
      if (!file) return;
      const reader = new FileReader();
      reader.onload = function(e) {
        selectedImageBase64 = e.target.result;
        document.getElementById('magic-preview-img').src = selectedImageBase64;
        document.getElementById('magic-preview-img').style.display = 'block';
        document.getElementById('magic-upload-box').style.display = 'none';
        document.getElementById('style-selection').style.display = 'block';
      };
      reader.readAsDataURL(file);
    }

    async function applyMagicStyle(style) {
      document.getElementById('style-selection').style.display = 'none';
      document.getElementById('magic-loading').style.display = 'block';
      try {
        const res = await fetch(`${API_URL}/api/magic/transform`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json', 'X-Invite-Code': currentCode },
          body: JSON.stringify({ image: selectedImageBase64, style: style })
        });
        const data = await res.json();
        alert('Магия в процессе! Скоро здесь появится результат. ✨');
      } catch (e) { alert('Ошибка магии'); }
      document.getElementById('magic-loading').style.display = 'none';
      document.getElementById('style-selection').style.display = 'block';
    }
  </script>
"""

# Вставляем всё перед закрывающим тегом body
content = content.replace('</body>', magic_html + magic_js + '</body>')

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("MAGIC_FIX_COMPLETED")
