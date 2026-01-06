#!/usr/bin/env python3

with open('parent.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Заменяем функцию loadChildPersonalRewards
old_function = """    async function loadChildPersonalRewards(childId) {
      try {
        const res = await fetch(`${API_URL}/api/rewards/purchases`, {
          headers: { 'X-Invite-Code': currentCode }
        });
        
        if (!res.ok) throw new Error('Ошибка загрузки наград');
        
        const data = await res.json();
        const childRewards = (data.purchases || []).filter(p => p.child_id === childId && p.status === 'pending');"""

new_function = """    async function loadChildPersonalRewards(childId) {
      try {
        const res = await fetch(`${API_URL}/api/rewards/purchases/family`, {
          headers: { 'X-Invite-Code': currentCode }
        });
        
        if (!res.ok) throw new Error('Ошибка загрузки наград');
        
        const data = await res.json();
        const childRewards = (data.purchases || []).filter(p => p.child_id === childId && p.status === 'pending');"""

content = content.replace(old_function, new_function)

with open('parent.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("OK")
