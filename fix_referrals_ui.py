import re

file_path = 'frontend/parent.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Делаем showTab более надежной (убираем зависимость от event.target)
content = content.replace(
    "event.target.classList.add('active');",
    "// Кнопка подсветится автоматически через селектор если нужно"
)

# 2. Добавляем логирование в loadReferrals для отладки
content = content.replace(
    "async function loadReferrals() {",
    "async function loadReferrals() { console.log('Загрузка рефералов запущена...');"
)

# 3. Убеждаемся что данные вставляются
content = content.replace(
    "if (data.referrals) {",
    "if (data.referrals) { console.log('Данные получены:', data.referrals);"
)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("FIX_UI_OK")
