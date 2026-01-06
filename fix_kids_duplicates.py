import re

file_path = 'index.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Удаляем все объявления этой переменной
content = content.replace('let selectedImageBase64 = null;', '')
# Добавляем её ОДИН раз в начало первого скрипта
content = content.replace('<script>', '<script>\n    let selectedImageBase64 = null;')

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("FRONTEND_CLEANUP_OK")
