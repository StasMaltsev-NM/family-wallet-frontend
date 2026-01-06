#!/usr/bin/env python3

with open('parent.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Добавляем проверку перед обновлением pending мечт
old_code = """    async function loadPendingDreams() {
      try {
        const res = await fetch(`${API_URL}/api/dreams/pending`, {"""

new_code = """    async function loadPendingDreams() {
      // Не обновляем если пользователь печатает в поле цели
      const inputs = document.querySelectorAll('[id^="dreamGoal_"]');
      for (let input of inputs) {
        if (document.activeElement === input) {
          return;
        }
      }
      
      try {
        const res = await fetch(`${API_URL}/api/dreams/pending`, {"""

content = content.replace(old_code, new_code)

with open('parent.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("OK")
