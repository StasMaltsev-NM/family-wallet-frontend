import os

files = ['frontend/kids.html', 'kids.html']

magic_html = """
    <!-- Вкладка: Магия -->
    <div id="tab-magic" class="tab-content">
      <div class="section">
        <h1 class="text-2xl font-black mb-6">Магия стилей ✨</h1>
        <input type="file" id="magic-input" accept="image/*" style="display: none" onchange="handleMagicUpload(event)">
        <div id="magic-upload-box" style="border: 2px dashed #FFD700; border-radius: 24px; padding: 40px; text-align: center; cursor: pointer;" onclick="document.getElementById('magic-input').click()">
          <div class="text-4xl mb-2">📸</div>
          <p class="text-sm opacity-60">Нажми, чтобы загрузить фото</p>
        </div>
        <img id="magic-preview-img" style="width: 100%; border-radius: 24px; margin-bottom: 20px; display: none;">
        <div id="style-selection" style="display: none; margin-top: 20px;">
          <p class="text-xs font-bold uppercase opacity-50 mb-4">Выбери игровой мир:</p>
          <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px;">
            <button onclick="applyMagicStyle('roblox')" style="background: #1c1f24; padding: 20px; border-radius: 20px; border: 1px solid #333;">🤖 РОБЛОКС</button>
            <button onclick="applyMagicStyle('ghibli')" style="background: #1c1f24; padding: 20px; border-radius: 20px; border: 1px solid #333;">🌳 ГИБЛИ</button>
          </div>
        </div>
        <div id="magic-loading" style="display: none; text-align: center; color: #FFD700; font-weight: bold;">🪄 КОЛДУЕМ...</div>
      </div>
    </div>
"""

for f_path in files:
    if os.path.exists(f_path):
        with open(f_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if 'id="tab-magic"' not in content:
            # Вставляем перед последним закрывающим </div> (обычно это конец контейнера вкладок)
            content = content.replace('<nav', magic_html + '\n    <nav')
            with open(f_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"PATCHED: {f_path}")
        else:
            print(f"ALREADY_HAS_MAGIC: {f_path}")
