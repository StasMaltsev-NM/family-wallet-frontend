file_path = 'index.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Этот блок полностью автономен. Он сам себя стилизует и запускает.
magic_v6 = """
<div id="magicSection" style="display:none; margin: 30px 10px; padding: 25px; border: 3px solid #FFD700; background: #000; border-radius: 30px; color: white; font-family: sans-serif; box-shadow: 0 0 20px rgba(255,215,0,0.2);">
    <h2 style="color: #FFD700; margin: 0; font-size: 22px;">🪄 МАГИЯ СТИЛЕЙ v6.0</h2>
    <p style="font-size: 10px; opacity: 0.5; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 20px;">ПРЕВРАТИ СЕБЯ В ГЕРОЯ ИГРЫ</p>
    
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
    
    <button id="magic-download-btn" onclick="downloadMagicImage()" style="display:none; width:100%; margin-top:20px; padding:18px; background:#FFD700; color:black; border-radius:15px; font-weight:900; border:none; text-transform:uppercase;">📥 СОХРАНИТЬ ФОТО</button>
    
    <div id="magic-loading" style="display: none; text-align: center; color: #FFD700; padding: 20px; font-weight: bold;">🪄 КОЛДУЕМ (20 сек)...</div>
</div>

<script>
    let magicImageBase64 = null;

    function handleMagicUpload(event) {
        const file = event.target.files[0];
        if (!file) return;
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
        const downloadBtn = document.getElementById('magic-download-btn');
        
        selection.style.display = 'none';
        loading.style.display = 'block';
        downloadBtn.style.display = 'none';

        try {
            const res = await fetch('https://family-wallet-api.maltsevstas21.workers.dev/api/magic/transform', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json', 'X-Invite-Code': currentCode },
                body: JSON.stringify({ image: magicImageBase64, style: style })
            });
            
            if (res.ok) {
                const blob = await res.blob();
                const url = URL.createObjectURL(blob);
                document.getElementById('magic-preview-img').src = url;
                downloadBtn.style.display = 'block';
                alert('МАГИЯ ГОТОВА! ✨');
            } else { alert('ИИ перегружен, попробуй еще раз'); }
        } catch (e) { alert('Ошибка связи с ИИ'); }
        loading.style.display = 'none';
        selection.style.display = 'grid';
    }

    function downloadMagicImage() {
        const link = document.createElement('a');
        link.href = document.getElementById('magic-preview-img').src;
        link.download = 'magic-hero.png';
        link.click();
    }

    // Показываем магию только после входа
    const checkAuth = setInterval(() => {
        if (document.getElementById('balanceSection')?.style.display === 'block') {
            document.getElementById('magicSection').style.display = 'block';
            clearInterval(checkAuth);
        }
    }, 1000);
</script>
"""

content = content.replace('</body>', magic_v6 + '</body>')
with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("MAGIC_V6_DEPLOYED")
