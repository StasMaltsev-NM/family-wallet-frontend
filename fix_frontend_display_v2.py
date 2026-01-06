file_path = 'index.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Исправляем логику показа картинки
old = "document.getElementById('magic-preview-img').src = data.result_image;"
new = "const imgEl = document.getElementById('magic-preview-img'); imgEl.src = data.result_image; imgEl.style.display = 'block';"

if old in content:
    content = content.replace(old, new)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("FRONTEND_FIX_OK")
else:
    print("ALREADY_FIXED_OR_NOT_FOUND")
