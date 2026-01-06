import re

file_path = 'index.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Проверяем, есть ли кнопка Магии в навигации
if 'tab-magic' not in content:
    # Ищем последнюю кнопку в навигации (обычно Профиль или Настройки)
    # Вставляем кнопку Магии перед закрывающим тегом </nav>
    magic_btn = '<button onclick="showTab(\'tab-magic\')" class="nav-btn">🪄<br><span>МАГИЯ</span></button>'
    content = content.replace('</nav>', magic_btn + '\n    </nav>')
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("NAV_BUTTON_ADDED")
else:
    print("NAV_BUTTON_ALREADY_EXISTS")
