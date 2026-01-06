#!/usr/bin/env python3

with open('worker.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Находим и исправляем SELECT в /api/rewards/purchases/family
old_select = """        const purchases = await env.DB.prepare(`
          SELECT 
            rp.id, 
            rp.reward_title, 
            rp.reward_icon, 
            rp.price, 
            rp.status,
            rp.purchased_at,
            c.name as child_name
          FROM reward_purchases rp
          JOIN children c ON rp.child_id = c.id
          WHERE rp.family_id = ? AND rp.status = 'pending'
          ORDER BY rp.purchased_at DESC
        `).bind(family.id).all();"""

new_select = """        const purchases = await env.DB.prepare(`
          SELECT 
            rp.id,
            rp.child_id,
            rp.reward_title, 
            rp.reward_icon, 
            rp.price, 
            rp.status,
            rp.purchased_at,
            c.name as child_name
          FROM reward_purchases rp
          JOIN children c ON rp.child_id = c.id
          WHERE rp.family_id = ? AND rp.status = 'pending'
          ORDER BY rp.purchased_at DESC
        `).bind(family.id).all();"""

content = content.replace(old_select, new_select)

with open('worker.js', 'w', encoding='utf-8') as f:
    f.write(content)

print("OK")
