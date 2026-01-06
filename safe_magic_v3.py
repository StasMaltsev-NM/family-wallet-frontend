file_path = 'index.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Добавляем логику в самый конец файла, ПЕРЕД </body>
# Это гарантирует, что мы не сломаем существующий JS
magic_logic = """
<script>
    // Магия стилей (изолированный блок)
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
      document.getElementById('style-selection').style.display = 'none';
      document.getElementById('magic-loading').style.display = 'block';
      try {
        const res = await fetch('https://family-wallet-api.maltsevstas21.workers.dev/api/magic/transform', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json', 'X-Invite-Code': currentCode },
          body: JSON.stringify({ image: selectedImageBase64, style: style })
        });
        const data = await res.json();
        if (data.success && data.result_image) {
          document.getElementById('magic-preview-img').src = data.result_image;
          alert('МАГИЯ ГОТОВА! ✨');
        } else {
          alert('ИИ сегодня отдыхает, попробуй позже');
        }
      } catch (e) { alert('Ошибка связи с ИИ'); }
      document.getElementById('magic-loading').style.display = 'none';
      document.getElementById('style-selection').style.display = 'grid';
    }
</script>
"""

if 'handleMagicUpload' not in content:
    content = content.replace('</body>', magic_logic + '\n</body>')
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("SAFE_MAGIC_V3_OK")
else:
    print("ALREADY_PATCHED")
