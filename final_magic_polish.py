import re

file_path = 'index.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Скрываем блок магии по умолчанию
content = content.replace('id="magicSection" style="', 'id="magicSection" style="display: none; ')

# 2. Добавляем все 4 стиля в сетку
new_grid = """
    <div id="style-selection" style="display: none; grid-template-columns: 1fr 1fr; gap: 10px; margin-top: 20px;">
        <button onclick="applyMagicStyle('roblox')" style="padding: 15px; background: #222; color: white; border-radius: 12px; border: 1px solid #444;">🤖 РОБЛОКС</button>
        <button onclick="applyMagicStyle('ghibli')" style="padding: 15px; background: #222; color: white; border-radius: 12px; border: 1px solid #444;">🌳 ГИБЛИ</button>
        <button onclick="applyMagicStyle('anime')" style="padding: 15px; background: #222; color: white; border-radius: 12px; border: 1px solid #444;">✨ АНИМЕ</button>
        <button onclick="applyMagicStyle('minecraft')" style="padding: 15px; background: #222; color: white; border-radius: 12px; border: 1px solid #444;">🧱 КРАФТ</button>
    </div>
"""
content = re.sub(r'<div id="style-selection".*?</div>', new_grid, content, flags=re.DOTALL)

# 3. Привязываем появление магии к успешному входу
# Ищем строку, где показывается баланс, и добавляем показ магии
content = content.replace(
    "document.getElementById('balanceSection').style.display = 'block';",
    "document.getElementById('balanceSection').style.display = 'block'; document.getElementById('magicSection').style.display = 'block';"
)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("FRONTEND_POLISH_OK")
