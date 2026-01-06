import os
file_path = 'index.html'
if not os.path.exists(file_path):
    print("ОШИБКА: Файл index.html не найден. Убедись, что ты в корне проекта!")
    exit()

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

magic_v7 = """
<div id="magicSection" style="display:none; margin: 30px 10px; padding: 25px; border: 3px solid #FFD700; background: #000; border-radius: 30px; color: white; font-family: sans-serif;">
    <h2 style="color: #FFD700; margin: 0;">🪄 МАГИЯ СТИЛЕЙ v7.0</h2>
    <p style="font-size: 10px; opacity: 0.5; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 20px;">ДЕТЕКТОР КОНТРАКТА ВКЛЮЧЕН</p>
    <input type="file" id="magic-input" accept="image/*" style="display: none" onchange="handleMagicUpload(event)">
    <div id="magic-upload-box" onclick="document.getElementById('magic-input').click()" style="border: 2px dashed rgba(255,215,0,0.4); padding: 40px; text-align: center; border-radius: 20px; cursor: pointer;">
        📸<br>ВЫБРАТЬ ФОТО
    </div>
    <img id="magic-preview-img" style="width: 100%; border-radius: 20px; display: none; margin-top: 20px; border: 3px solid #FFD700;">
    <div id="style-selection" style="display: none; grid-template-columns: 1fr 1fr; gap: 12px; margin-top: 20px;">
        <button onclick="applyMagicStyle('roblox')" style="padding: 15px; background: #1c1f24; color: white; border-radius: 12px; border: 1px solid #333;">🤖 РОБЛОКС</button>
        <button onclick="applyMagicStyle('ghibli')" style="padding: 15px; background: #1c1f24; color: white; border-radius: 12px; border: 1px solid #333;">🌳 ГИБЛИ</button>
        <button onclick="applyMagicStyle('anime')" style="padding: 15px; background: #1c1f24; color: white; border-radius: 12px; border: 1px solid #333;">✨ АНИМЕ</button>
        <button onclick="applyMagicStyle('minecraft')" style="padding: 15px; background: #1c1f24; color: white; border-radius: 12px; border: 1px solid #333;">🧱 КРАФТ</button>
    </div>
    <div id="magic-loading" style="display: none; text-align: center; color: #FFD700; padding: 20px;">🪄 КОЛДУЕМ...</div>
</div>
<script>
    let magicImageBase64 = null;
    function handleMagicUpload(event) {
        const file = event.target.files[0];
        const reader = new FileReader();
        reader.onload = (e) => {
            const img = new Image();
            img.onload = () => {
                const canvas = document.createElement('canvas');
                canvas.width = 512; canvas.height = 512;
                const ctx = canvas.getContext('2d');
                ctx.drawImage(img, 0, 0, 512, 512);
                magicImageBase64 = canvas.toDataURL('image/jpeg', 0.9);
                document.getElementById('magic-preview-img').src = magicImageBase64;
                document.getElementById('magic-preview-img').style.display = 'block';
                document.getElementById('magic-upload-box').style.display = 'none';
                document.getElementById('style-selection').style.display = 'grid';
            };
            img.src = e.target.result;
        };
        reader.readAsDataURL(file);
    }
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
            const ct = (res.headers.get('content-type') || '').toLowerCase();
            if (!res.ok || !ct.startsWith('image/')) {
                const txt = await res.text();
                console.error('MAGIC error:', txt);
                alert('Ошибка ИИ. Проверь консоль.');
                return;
            }
            const blob = await res.blob();
            document.getElementById('magic-preview-img').src = URL.createObjectURL(blob);
            alert('МАГИЯ ГОТОВА! ✨');
        } catch (e) { alert('Ошибка связи'); }
        loading.style.display = 'none';
        selection.style.display = 'grid';
    }
    const checkAuthMagic = setInterval(() => {
        if (document.getElementById('balanceSection')?.style.display === 'block') {
            document.getElementById('magicSection').style.display = 'block';
            clearInterval(checkAuthMagic);
        }
    }, 1000);
</script>
"""
if 'magicSection' not in content:
    content = content.replace('</body>', magic_v7 + '</body>')
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("PATCH_V7_SUCCESS")
else:
    print("ALREADY_PATCHED")
