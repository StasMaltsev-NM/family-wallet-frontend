import os

file_path = 'index.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Этот блок содержит СВОИ стили, СВОЙ HTML и СВОЙ JS. 
# Он полностью независим от остального кода страницы.
magic_bundle = """
<div id="magicSection" style="display:none; margin: 30px 10px; padding: 25px; border: 3px solid #FFD700; background: #000; border-radius: 30px; color: white; font-family: sans-serif;">
    <h2 style="color: #FFD700; margin: 0; font-size: 22px;">🪄 МАГИЯ СТИЛЕЙ</h2>
    <p style="font-size: 10px; opacity: 0.5; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 20px;">Преврати себя в героя игры</p>
    
    <input type="file" id="magic-input" accept="image/*" style="display: none" onchange="handleMagicUpload(event)">
    <div id="magic-upload-box" onclick="document.getElementById('magic-input').click()" style="border: 2px dashed rgba(255,215,0,0.4); padding: 40px; text-align: center; border-radius: 20px; cursor: pointer;">
        <span style="font-size: 40px;">📸</span><br><b style="font-size: 12px;">НАЖМИ ДЛЯ ЗАГРУЗКИ ФОТО</b>
    </div>
    
    <img id="magic-preview-img" style="width: 100%; border-radius: 20px; display: none; margin-top: 20px; border: 3px solid #FFD700;">
    
    <div id="style-selection" style="display: none; grid-template-columns: 1fr 1fr; gap: 12px; margin-top: 20px;">
        <button onclick="applyMagicStyle('roblox')" style="padding: 15px; background: #1c1f24; color: white; border-radius: 15px; border: 1px solid #333; font-weight: bold;">🤖 РОБЛОКС</button>
        <button onclick="applyMagicStyle('ghibli')" style="padding: 15px; background: #1c1f24; color: white; border-radius: 15px; border: 1px solid #333; font-weight: bold;">🌳 ГИБЛИ</button>
        <button onclick="applyMagicStyle('anime')" style="padding: 15px; background: #1c1f24; color: white; border-radius: 15px; border: 1px solid #333; font-weight: bold;">✨ АНИМЕ</button>
        <button onclick="applyMagicStyle('minecraft')" style="padding: 15px; background: #1c1f24; color: white; border-radius: 15px; border: 1px solid #333; font-weight: bold;">🧱 КРАФТ</button>
    </div>
    <div id="magic-loading" style="display: none; text-align: center; color: #FFD700; padding: 20px; font-weight: bold;">🪄 КОЛДУЕМ...</div>
</div>

<script>
    // Изолированная логика Магии
    let magicImageBase64 = null;

    function handleMagicUpload(event) {
        const file = event.target.files[0];
        const reader = new FileReader();
        reader.onload = (e) => {
            magicImageBase64 = e.target.result;
            const preview = document.getElementById('magic-preview-img');
            preview.src = magicImageBase64;
            preview.style.display = 'block';
            document.getElementById('magic-upload-box').style.display = 'none';
            document.getElementById('style-selection').style.display = 'grid';
        };
        reader.readAsDataURL(file);
    }

    async function applyMagicStyle(style) {
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
                document.getElementById('magic-preview-img').src = URL.createObjectURL(blob);
                alert('МАГИЯ ГОТОВА! ✨');
            }
        } catch (e) { alert('Ошибка ИИ'); }
        loading.style.display = 'none';
        selection.style.display = 'grid';
    }

    // Умный показ: ждем появления баланса и показываем магию
    const checkLogin = setInterval(() => {
        if (document.getElementById('balanceSection')?.style.display === 'block') {
            document.getElementById('magicSection').style.display = 'block';
            clearInterval(checkLogin);
        }
    }, 1000);
</script>
"""

# Просто приклеиваем в конец
content = content.replace('</body>', magic_bundle + '</body>')
with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("ISOLATED_PATCH_OK")
