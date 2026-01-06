file_path = 'index.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Этот блок содержит и HTML, и CSS, и JS. 
# Мы просто приклеим его перед </body>
magic_bundle = """
<div id="magicSection" style="margin: 30px 10px; padding: 20px; border: 3px solid #FFD700; background: #000; border-radius: 25px; color: white; font-family: sans-serif;">
    <h2 style="color: #FFD700; margin: 0;">🪄 МАГИЯ СТИЛЕЙ</h2>
    <p style="font-size: 10px; opacity: 0.5; margin-bottom: 20px;">ПРЕВРАТИ СЕБЯ В ГЕРОЯ</p>
    
    <input type="file" id="magic-input" accept="image/*" style="display: none" onchange="handleMagicUpload(event)">
    <div id="magic-upload-box" onclick="document.getElementById('magic-input').click()" style="border: 2px dashed gold; padding: 30px; text-align: center; border-radius: 15px; cursor: pointer;">
        <span style="font-size: 30px;">📸</span><br>ВЫБРАТЬ ФОТО
    </div>
    
    <img id="magic-preview-img" style="width: 100%; border-radius: 15px; display: none; margin-top: 20px; border: 2px solid gold;">
    
    <div id="style-selection" style="display: none; grid-template-columns: 1fr 1fr; gap: 10px; margin-top: 20px;">
        <button onclick="applyMagicStyle('roblox')" style="padding: 15px; background: #222; color: white; border-radius: 10px;">🤖 РОБЛОКС</button>
        <button onclick="applyMagicStyle('ghibli')" style="padding: 15px; background: #222; color: white; border-radius: 10px;">🌳 ГИБЛИ</button>
    </div>
    <div id="magic-loading" style="display: none; text-align: center; color: gold; padding: 20px;">🪄 КОЛДУЕМ...</div>
</div>

<script>
    let selectedImageBase64 = null;
    function handleMagicUpload(event) {
        const file = event.target.files[0];
        const reader = new FileReader();
        reader.onload = (e) => {
            selectedImageBase64 = e.target.result;
            document.getElementById('magic-preview-img').src = selectedImageBase64;
            document.getElementById('magic-preview-img').style.display = 'block';
            document.getElementById('magic-upload-box').style.display = 'none';
            document.getElementById('style-selection').style.display = 'grid';
        };
        reader.readAsDataURL(file);
    }
    async function applyMagicStyle(style) {
        document.getElementById('style-selection').style.display = 'none';
        document.getElementById('magic-loading').style.display = 'block';
        try {
            const res = await fetch('https://family-wallet-api.maltsevstas21.workers.dev/api/magic/transform', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json', 'X-Invite-Code': currentCode },
                body: JSON.stringify({ image: selectedImageBase64, style: style })
            });
            const data = await res.json();
            if (data.success) {
                document.getElementById('magic-preview-img').src = data.result_image;
                alert('ГОТОВО! ✨');
            }
        } catch (e) { alert('Ошибка ИИ'); }
        document.getElementById('magic-loading').style.display = 'none';
        document.getElementById('style-selection').style.display = 'grid';
    }
</script>
"""

content = content.replace('</body>', magic_bundle + '</body>')
with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("RESTORE_AND_MAGIC_OK")
