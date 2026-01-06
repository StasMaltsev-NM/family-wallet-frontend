import os

file_path = 'index.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Добавляем визуальный маркер для проверки деплоя
if 'DEBUG_MARKER' not in content:
    content = content.replace('<body>', '<body><div id="DEBUG_MARKER" style="background: red; color: white; text-align: center; font-size: 10px; z-index: 9999; position: fixed; top: 0; width: 100%;">ВЕРСИЯ С МАГИЕЙ v1.0</div>')

# 2. Добавляем кнопку в навигацию (ищем тег </nav> или последний nav-btn)
if 'tab-magic' not in content:
    magic_btn = '<button onclick="showTab(\'tab-magic\')" class="nav-btn">🪄<br><span>МАГИЯ</span></button>'
    if '</nav>' in content:
        content = content.replace('</nav>', magic_btn + '</nav>')
    else:
        # Если тега nav нет, ищем последний div с кнопками
        content = content.replace('</footer>', magic_btn + '</footer>')

# 3. Проверяем наличие самой вкладки
if 'id="tab-magic"' not in content:
    magic_tab = """
    <div id="tab-magic" class="tab-content" style="display:none; padding: 20px;">
        <h1 style="color: white;">Магия ✨</h1>
        <div style="border: 2px dashed gold; padding: 40px; text-align: center; border-radius: 20px;" onclick="alert('Загрузка скоро заработает!')">
            <span style="font-size: 40px;">📸</span><br>
            <p style="color: white;">Нажми для загрузки</p>
        </div>
    </div>
    """
    content = content.replace('</body>', magic_tab + '</body>')

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("MEGA_PATCH_DONE")
