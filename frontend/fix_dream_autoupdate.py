#!/usr/bin/env python3

with open('kids.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Добавляем проверку перед обновлением
old_code = """    async function loadMyDream() {
      try {
        const res = await fetch(`${API_URL}/api/dreams/my`, {"""

new_code = """    async function loadMyDream() {
      // Не обновляем если пользователь печатает
      const input = document.getElementById('dreamTitleInput');
      if (input && document.activeElement === input) {
        return;
      }
      
      try {
        const res = await fetch(`${API_URL}/api/dreams/my`, {"""

content = content.replace(old_code, new_code)

with open('kids.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("OK")
