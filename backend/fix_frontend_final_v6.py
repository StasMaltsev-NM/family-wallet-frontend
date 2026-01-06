import re
file_path = 'index.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Добавляем кнопку "Скачать" в HTML (скрытую по умолчанию)
download_btn = '<button id="magic-download-btn" onclick="downloadMagicImage()" style="display:none; width:100%; margin-top:10px; padding:15px; background:#FFD700; color:black; border-radius:12px; font-weight:bold; border:none;">📥 СКАЧАТЬ ФОТО</button>'
content = content.replace('<div id="magic-loading"', download_btn + '\n    <div id="magic-loading"')

# 2. Обновляем JS логику (прием JSON + функция скачивания)
new_js = """
    async function applyMagicStyle(style) {
      if (!magicImageBase64) return alert('Загрузи фото!');
      const loading = document.getElementById('magic-loading');
      const selection = document.getElementById('style-selection');
      selection.style.display = 'none';
      loading.style.display = 'block';
      try {
        const res = await fetch('https://family-wallet-api.maltsevstas21.workers.dev/api/magic/transform', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json', 'X-Invite-Code': currentCode },
          body: JSON.stringify({ image: magicImageBase64, style: style })
        });
        const data = await res.json();
        if (data.success && data.result_image) {
          const img = document.getElementById('magic-preview-img');
          img.src = data.result_image;
          document.getElementById('magic-download-btn').style.display = 'block';
          alert('МАГИЯ ГОТОВА! ✨');
        }
      } catch (e) { alert('Ошибка ИИ'); }
      loading.style.display = 'none';
      selection.style.display = 'grid';
    }

    function downloadMagicImage() {
      const link = document.createElement('a');
      link.href = document.getElementById('magic-preview-img').src;
      link.download = 'magic-avatar.png';
      link.click();
    }
"""
# Заменяем старую функцию на новую
content = re.sub(r'async function applyMagicStyle.*?\}', '', content, flags=re.DOTALL)
content = content.replace('</script>', new_js + '\n</script>')

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("FRONTEND_FINAL_V6_OK")
