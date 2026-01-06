import re

file_path = 'frontend/kids.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Добавляем стили для магии (перед </style>)
magic_css = """
    .magic-upload-area { border: 2px dashed #FFD700; border-radius: 24px; padding: 40px; text-align: center; margin-bottom: 20px; cursor: pointer; }
    .style-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 15px; }
    .style-btn { background: #1c1f24; border: 1px solid rgba(255,255,255,0.1); border-radius: 20px; padding: 20px; text-align: center; }
    .style-btn.active { border-color: #FFD700; box-shadow: 0 0 15px rgba(255, 215, 0, 0.3); }
    .magic-preview { width: 100%; border-radius: 24px; margin-bottom: 20px; display: none; }
    #magic-loading { display: none; text-align: center; padding: 20px; font-weight: bold; color: #FFD700; }
"""
content = content.replace('</style>', magic_css + '\n    </style>')

# 2. Обновляем содержимое вкладки Магия
# Ищем блок с id="tab-magic" и заменяем его содержимое
new_tab_content = """
    <div id="tab-magic" class="tab-content">
      <div class="section">
        <h1 class="text-2xl font-black mb-6">Магия стилей ✨</h1>
        
        <input type="file" id="magic-input" accept="image/*" style="display: none" onchange="handleMagicUpload(event)">
        
        <div id="magic-upload-box" class="magic-upload-area" onclick="document.getElementById('magic-input').click()">
          <div class="text-4xl mb-2">📸</div>
          <p class="text-sm opacity-60">Нажми, чтобы загрузить фото</p>
        </div>

        <img id="magic-preview-img" class="magic-preview">
        
        <div id="style-selection" style="display: none">
          <p class="text-xs font-bold uppercase opacity-50 mb-4">Выбери игровой мир:</p>
          <div class="style-grid">
            <div class="style-btn" onclick="applyMagicStyle('roblox')">🤖<br><b>РОБЛОКС</b></div>
            <div class="style-btn" onclick="applyMagicStyle('ghibli')">🌳<br><b>ГИБЛИ</b></div>
            <div class="style-btn" onclick="applyMagicStyle('anime')">✨<br><b>АНИМЕ</b></div>
            <div class="style-btn" onclick="applyMagicStyle('minecraft')">🧱<br><b>КРАФТ</b></div>
          </div>
        </div>

        <div id="magic-loading">🪄 КОЛДУЕМ...</div>
      </div>
    </div>
"""
content = re.sub(r'<div id="tab-magic".*?</div>\s*</div>', new_tab_content, content, flags=re.DOTALL)

# 3. Добавляем JS функции (перед </script>)
magic_js = """
    let selectedImageBase64 = null;

    function handleMagicUpload(event) {
      const file = event.target.files[0];
      if (!file) return;
      const reader = new FileReader();
      reader.onload = function(e) {
        selectedImageBase64 = e.target.result;
        const img = document.getElementById('magic-preview-img');
        img.src = selectedImageBase64;
        img.style.display = 'block';
        document.getElementById('magic-upload-box').style.display = 'none';
        document.getElementById('style-selection').style.display = 'block';
      };
      reader.readAsDataURL(file);
    }

    async function applyMagicStyle(style) {
      document.getElementById('style-selection').style.display = 'none';
      document.getElementById('magic-loading').style.display = 'block';
      
      try {
        const res = await fetch(`${API_BASE}/api/magic/transform`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json', 'X-Invite-Code': currentCode },
          body: JSON.stringify({ image: selectedImageBase64, style: style })
        });
        const data = await res.json();
        if (data.success) {
          alert('Магия сработала! (В MVP Gemini описывает изменения, в финале — заменит фото)');
          // Здесь будет логика замены превью на результат
        }
      } catch (e) { alert('Магия временно недоступна'); }
      
      document.getElementById('magic-loading').style.display = 'none';
      document.getElementById('style-selection').style.display = 'block';
    }
"""
content = content.replace('</script>', magic_js + '\n  </script>')

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("KIDS_MAGIC_UI_PATCH_OK")
