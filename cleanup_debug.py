import re

file_path = 'backend/worker.js'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Удаляем блок диагностики
pattern = r"// GET /api/debug/referrals.*?\n\s*\}\n"
content = re.sub(pattern, "", content, flags=re.DOTALL)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("CLEANUP_OK")
