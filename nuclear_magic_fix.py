import re

file_path = 'index.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Удаляем ВСЕ старые версии функций магии (очень широкая очистка)
content = re.sub(r'async function applyMagicStyle.*?\}', '', content, flags=re.DOTALL)
content = re.sub(r'function handleMagicUpload.*?\}', '', content, flags=re.DOTALL)
content = re.sub(r'let selectedImageBase64 = null;', '', content)

# 2. Чистим возможные "зависшие" запятые и мусор в JS
content = content.replace(', ,', ',').replace(';,', ';')

# 3. Вставляем ЧИСТУЮ логику в самый конец файла перед </body>
clean_logic = """
<script>
    // === ЧИСТАЯ МАГИЯ v3.0 ===
    let selectedImageBase64 = null;

    function handleMagicUpload(event) {
      const file = event.target.files[0];
      if (!file) return;
      const reader = new FileReader();
      reader.onload = (e) => {
        selectedImageBase64 = e.target.result;
        const preview = document.getElementById('magic-preview-img');
        if (preview) {
          preview.src = selectedImageBase64;
          preview.style.display = 'block';
          document.getElementById('magic-upload-box').style.display = 'none';
          document.getElementById('style-selection').style.display = 'grid';
        }
      };
      reader.readAsDataURL(file);
    }

    async function applyMagicStyle(style) {
      if (!selectedImageBase64) return alert('Загрузи фото!');
      const loading = document.getElementById('magic-loading');
      const selection = document.getElementById('style-selection');
      
      selection.style.display = 'none';
      loading.style.display = 'block';

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
          alert('МАГИЯ ГОТОВА! ✨');
        } else {
          alert('ИИ сегодня отдыхает, попробуй позже');
        }
      } catch (e) { 
        console.error(e);
        alert('Ошибка связи с магией'); 
      } finally {
        loading.style.display = 'none';
        selection.style.display = 'grid';
      }
    }
</script>
"""

content = content.replace('</body>', clean_logic + '\n</body>')

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("NUCLEAR_FIX_COMPLETED")
