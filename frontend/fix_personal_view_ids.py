#!/usr/bin/env python3

with open('parent.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Исправляем ID в функции showChildPersonalView
content = content.replace(
    "document.getElementById('pendingTasksSection').style.display = 'none';",
    "document.getElementById('pendingTasks').parentElement.style.display = 'none';"
)

content = content.replace(
    "document.getElementById('historySection').style.display = 'none';",
    "document.getElementById('historyList').parentElement.style.display = 'none';"
)

# Исправляем в функции backToChildrenList
content = content.replace(
    "document.getElementById('pendingTasksSection').style.display = 'block';",
    "document.getElementById('pendingTasks').parentElement.style.display = 'block';"
)

content = content.replace(
    "document.getElementById('historySection').style.display = 'block';",
    "document.getElementById('historyList').parentElement.style.display = 'block';"
)

with open('parent.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("OK")
