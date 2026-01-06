import re
file_path = 'index.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Полностью заменяем функцию applyMagicStyle на версию для работы с файлами (Blob)
new_function = """
    async function applyMagicStyle(style) {
      if (!selectedImageBase64) return alert('Загрузи фото!');
      document.getElementById('style-selection').style.display = 'none';
      document.getElementById('magic-loading').style.display = 'block';
      try {
        const res = await fetch('https://family-wallet-api.maltsevstas21.workers.dev/api/magic/transform', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json', 'X-Invite-Code': currentCode },
          body: JSON.stringify({ style: style })
        });
        
        if (res.ok) {
          const blob = await res.blob();
          const imageUrl = URL.createObjectURL(blob);
          const imgEl = document.getElementById('magic-preview-img');
          imgEl.src = imageUrl;
          imgEl.style.display = 'block';
          alert('МАГИЯ ГОТОВА! ✨');
        } else {
          alert('ИИ сегодня занят, попробуй позже');
        }
      } catch (e) { alert('Ошибка связи с магией'); }
      document.getElementById('magic-loading').style.display = 'none';
      document.getElementById('style-selection').style.display = 'grid';
    }
"""

# Удаляем старую функцию и вставляем новую перед </script>
content = re.sub(r'async function applyMagicStyle.*?\}', '', content, flags=re.DOTALL)
content = content.replace('</script>', new_function + '\n</script>')

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("FRONTEND_BLOB_SUCCESS")
