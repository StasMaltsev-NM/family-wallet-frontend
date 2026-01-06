import re
file_path = 'index.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Обновляем функцию handleMagicUpload: добавляем ресайзер
new_upload_logic = """
    function handleMagicUpload(event) {
        const file = event.target.files[0];
        const reader = new FileReader();
        reader.onload = (e) => {
            const img = new Image();
            img.onload = () => {
                // Создаем холст 512x512
                const canvas = document.createElement('canvas');
                canvas.width = 512;
                canvas.height = 512;
                const ctx = canvas.getContext('2d');
                // Рисуем фото, вписывая его в квадрат
                ctx.drawImage(img, 0, 0, 512, 512);
                magicImageBase64 = canvas.toDataURL('image/jpeg', 0.8);
                
                const preview = document.getElementById('magic-preview-img');
                preview.src = magicImageBase64;
                preview.style.display = 'block';
                preview.style.height = 'auto';
                document.getElementById('magic-upload-box').style.display = 'none';
                document.getElementById('style-selection').style.display = 'grid';
            };
            img.src = e.target.result;
        };
        reader.readAsDataURL(file);
    }
"""

content = re.sub(r'function handleMagicUpload.*?\}', new_upload_logic, content, flags=re.DOTALL)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("FRONTEND_RESIZER_ADDED")
