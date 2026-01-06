file_path = 'index.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Обновляем функцию applyMagicStyle, чтобы она показывала результат
old_js = "alert('Магия в процессе! Скоро здесь появится результат. ✨');"
new_js = """
        if (data.success && data.result_image) {
          const img = document.getElementById('magic-preview-img');
          img.src = data.result_image;
          img.style.border = '5px solid #FFD700';
          img.style.boxShadow = '0 0 30px rgba(255, 215, 0, 0.5)';
          alert('ГОТОВО! Посмотри, какой классный образ получился! 😍');
        }
"""
content = content.replace(old_js, new_js)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("FRONTEND_RESULT_UI_OK")
