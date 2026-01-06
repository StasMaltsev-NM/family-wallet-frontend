import re
file_path = 'backend/worker.js'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Исправляем /api/tasks/list (чтобы ребенок видел свои задачи)
old_tasks = r"const \{ results \} = await env\.DB\.prepare\('SELECT \* FROM tasks WHERE family_id = \(SELECT family_id FROM children WHERE invite_code = \?\)\s+OR family_id = \(SELECT id FROM families WHERE invite_code = \?\)'\)\.bind\(inviteCode, inviteCode\)\.all\(\);"
new_tasks = "const { results } = await env.DB.prepare('SELECT * FROM tasks WHERE family_id = (SELECT family_id FROM children WHERE invite_code = ?)').bind(inviteCode).all();"
content = re.sub(old_tasks, new_tasks, content)

# 2. Исправляем /api/auth/whoami (чтобы возвращались все поля ребенка)
old_whoami = "if (child) return json({ role: 'child', ...child });"
new_whoami = "if (child) return json({ role: 'child', name: child.name, balance: child.balance, pending_balance: child.pending_balance, family_id: child.family_id });"
content = content.replace(old_whoami, new_whoami)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("DATA_FLOW_FIXED")
