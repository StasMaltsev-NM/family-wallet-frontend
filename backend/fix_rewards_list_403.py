#!/usr/bin/env python3
import re

with open('worker.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Старый код (только родитель)
old_code = r"""      if \(path === '/api/rewards/list' && request\.method === 'GET'\) \{
        const inviteCode = request\.headers\.get\('X-Invite-Code'\);
        
        if \(!inviteCode\) \{
          return error\('Отсутствует заголовок X-Invite-Code', 'NO_AUTH', 401\);
        \}

        // Проверяем родителя
        const family = await env\.DB\.prepare\(
          'SELECT id FROM families WHERE invite_code = \?'
        \)\.bind\(inviteCode\)\.first\(\);

        if \(!family\) \{
          return error\('Недействительный код', 'FORBIDDEN', 403\);
        \}

        // Получаем список наград
        const rewards = await env\.DB\.prepare\(`
          SELECT id, family_id, title, description, price, icon, is_permanent, created_at, updated_at
          FROM rewards
          WHERE family_id = \? AND is_active = 1
          ORDER BY created_at DESC
        `\)\.bind\(family\.id\)\.all\(\);

        return json\(\{ rewards: rewards\.results \|\| \[\] \}\);
      \}"""

# Новый код (родитель ИЛИ ребёнок)
new_code = """      if (path === '/api/rewards/list' && request.method === 'GET') {
        const inviteCode = request.headers.get('X-Invite-Code');
        
        if (!inviteCode) {
          return error('Отсутствует заголовок X-Invite-Code', 'NO_AUTH', 401);
        }

        // Проверяем родителя
        let family = await env.DB.prepare(
          'SELECT id FROM families WHERE invite_code = ?'
        ).bind(inviteCode).first();

        // Если не родитель — проверяем ребёнка
        if (!family) {
          const child = await env.DB.prepare(
            'SELECT family_id FROM children WHERE invite_code = ?'
          ).bind(inviteCode).first();
          
          if (!child) {
            return error('Недействительный код', 'FORBIDDEN', 403);
          }
          
          // Используем family_id ребёнка
          family = { id: child.family_id };
        }

        // Получаем список наград
        const rewards = await env.DB.prepare(`
          SELECT id, family_id, title, description, price, icon, is_permanent, created_at, updated_at
          FROM rewards
          WHERE family_id = ? AND is_active = 1
          ORDER BY created_at DESC
        `).bind(family.id).all();

        return json({ rewards: rewards.results || [] });
      }"""

content = re.sub(old_code, new_code, content, flags=re.DOTALL)

with open('worker.js', 'w', encoding='utf-8') as f:
    f.write(content)

print("OK")
