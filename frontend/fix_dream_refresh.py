#!/usr/bin/env python3

with open('parent.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Добавляем обновление персональной страницы после установки цели
old_code = """        alert(`✅ ${data.message}`);
        
        loadPendingDreams();
        loadActiveDreams();"""

new_code = """        alert(`✅ ${data.message}`);
        
        loadPendingDreams();
        loadActiveDreams();
        
        // Если мы на персональной странице ребёнка - обновляем её
        if (selectedChildId) {
          loadChildPersonalDream(selectedChildId);
        }"""

content = content.replace(old_code, new_code)

with open('parent.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("OK")
