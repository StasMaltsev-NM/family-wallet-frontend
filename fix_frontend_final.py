import re
file_path = 'index.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Обновляем функцию applyMagicStyle для работы с Blob (файлом)
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
        
        if (res.ok) {
          const blob = await res.blob();
          const url = URL.createObjectURL(blob);
          const img = document.getElementById('magic-preview-img');
          img.src = url;
          img.style.display = 'block';
          if (document.getElementById('magic-download-btn')) {
            document.getElementById('magic-download-btn').style.display = 'block';
          }
          alert('МАГИЯ ГОТОВА! ✨');
        } else { alert('ИИ сегодня устал...'); }
      } catch (e) { alert('Ошибка связи'); }
      loading.style.display = 'none';
      selection.style.display = 'grid';
    }
"""
content = re.sub(r'async function applyMagicStyle.*?\}', '', content, flags=re.DOTALL)
content = content.replace('</script>', new_js + '\n</script>')

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("FRONTEND_BLOB_OK")
