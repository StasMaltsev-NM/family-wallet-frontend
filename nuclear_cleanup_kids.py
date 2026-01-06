import re

file_path = 'index.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Удаляем ВСЕ объявления переменной selectedImageBase64 (любые вариации)
content = re.sub(r'let\s+selectedImageBase64\s*=.*?;', '', content)

# 2. Вставляем её ОДИН раз сразу после первого тега <script>
content = content.replace('<script>', '<script>\n    let selectedImageBase64 = null;')

# 3. Убеждаемся, что функция applyMagicStyle использует правильный URL и логику
# Удаляем старые версии функции и вставляем чистую
new_js_func = """
    async function applyMagicStyle(style) {
      if (!selectedImageBase64) return alert('Сначала загрузи фото!');
      document.getElementById('style-selection').style.display = 'none';
      document.getElementById('magic-loading').style.display = 'block';
      try {
        const res = await fetch(`${API_URL}/api/magic/transform`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json', 'X-Invite-Code': currentCode },
          body: JSON.stringify({ image: selectedImageBase64, style: style })
        });
        const data = await res.json();
        if (data.success && data.result_image) {
          const img = document.getElementById('magic-preview-img');
          img.src = data.result_image;
          img.style.display = 'block';
          alert('МАГИЯ ГОТОВА! ✨');
        } else {
          alert('ИИ устал, попробуй позже');
        }
      } catch (e) { alert('Ошибка связи с магией'); }
      document.getElementById('magic-loading').style.display = 'none';
      document.getElementById('style-selection').style.display = 'block';
    }
"""
# Удаляем старую функцию (очень грубо, но надежно)
content = re.sub(r'async function applyMagicStyle.*?\}', '', content, flags=re.DOTALL)
content = content.replace('</script>', new_js_func + '\n</script>')

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("NUCLEAR_CLEANUP_OK")
