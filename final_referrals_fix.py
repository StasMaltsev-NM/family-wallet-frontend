import re

file_path = 'frontend/parent.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Гарантируем, что класс .active делает вкладку видимой
if '.tab-content.active { display: block;' not in content:
    content = content.replace(
        '</style>',
        '.tab-content.active { display: block !important; }\n    .tab-content { display: none; }\n    </style>'
    )

# 2. Переписываем функцию showTab на максимально простую и надежную
new_show_tab = """
    function showTab(tabId) {
      console.log('Переключение на:', tabId);
      // Скрываем все вкладки
      document.querySelectorAll('.tab-content').forEach(tab => {
        tab.classList.remove('active');
        tab.style.display = 'none';
      });
      
      // Показываем нужную
      const activeTab = document.getElementById(tabId);
      if (activeTab) {
        activeTab.classList.add('active');
        activeTab.style.display = 'block';
      }

      // Подсвечиваем кнопку в меню
      document.querySelectorAll('.nav-tabs button').forEach(btn => btn.classList.remove('active'));
      
      // Загружаем данные если нужно
      if (tabId === 'tab-missions') loadAllTasks();
      if (tabId === 'tab-referrals') loadReferrals();
    }
"""

# Ищем старую функцию и заменяем её (от function showTab до следующей функции)
content = re.sub(r'function showTab\(tabId\)\s*\{.*?\}', new_show_tab, content, flags=re.DOTALL)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("FINAL_UI_FIX_OK")
