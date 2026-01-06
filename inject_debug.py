import re
file_path = 'index.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Добавляем логирование кода и проверку типа ответа
debug_js = """
    async function applyMagicStyle(style) {
      if (!magicImageBase64) return alert('Загрузи фото!');
      console.log('MAGIC: Запуск. Стиль:', style);
      console.log('MAGIC: currentCode =', typeof currentCode !== 'undefined' ? currentCode : 'UNDEFINED!');
      
      const loading = document.getElementById('magic-loading');
      const selection = document.getElementById('style-selection');
      selection.style.display = 'none';
      loading.style.display = 'block';

      try {
        const res = await fetch('https://family-wallet-api.maltsevstas21.workers.dev/api/magic/transform', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json', 'X-Invite-Code': typeof currentCode !== 'undefined' ? currentCode : '' },
          body: JSON.stringify({ image: magicImageBase64, style: style })
        });
        
        const ct = (res.headers.get('content-type') || '').toLowerCase();
        console.log('MAGIC: Status =', res.status, 'Content-Type =', ct);

        if (!res.ok) {
          const errTxt = await res.text();
          console.error('MAGIC: Ошибка сервера:', errTxt);
          alert('Ошибка ИИ: ' + res.status);
          return;
        }

        if (!ct.startsWith('image/')) {
          const txt = await res.text();
          console.warn('MAGIC: Получен текст вместо картинки:', txt);
          alert('Сервер вернул ошибку вместо фото. Проверь консоль (F12)');
          return;
        }

        const blob = await res.blob();
        console.log('MAGIC: Blob получен. Размер:', blob.size, 'тип:', blob.type);
        
        const url = URL.createObjectURL(blob);
        document.getElementById('magic-preview-img').src = url;
        document.getElementById('magic-download-btn').style.display = 'block';
        alert('МАГИЯ ГОТОВА! ✨');

      } catch (e) { 
        console.error('MAGIC: Критическая ошибка fetch:', e);
        alert('Ошибка связи с магией'); 
      } finally {
        loading.style.display = 'none';
        selection.style.display = 'grid';
      }
    }
"""

# Заменяем старую функцию v6.0 на отладочную
content = re.sub(r'async function applyMagicStyle.*?\}', debug_js, content, flags=re.DOTALL)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("DEBUG_INJECTED_OK")
