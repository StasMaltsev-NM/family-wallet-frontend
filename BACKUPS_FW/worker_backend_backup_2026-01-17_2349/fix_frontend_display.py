file_path = 'index.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Добавляем очистку и принудительный рендер
old_logic = "document.getElementById('magic-preview-img').src = data.result_image;"
new_logic = """const imgEl = document.getElementById('magic-preview-img');
                imgEl.src = ''; // Очистка
                imgEl.src = data.result_image;
                imgEl.style.display = 'block';
                console.log('Картинка обновлена');"""

content = content.replace(old_logic, new_logic)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("FRONTEND_DISPLAY_FIX_OK")
