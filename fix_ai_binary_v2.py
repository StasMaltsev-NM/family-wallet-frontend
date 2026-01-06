import os
file_path = 'backend/worker.js'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

import re
# Исправляем конвертацию бинарных данных
old = r"const binary = String\.fromCharCode\(\.\.\.new Uint8Array\(aiResponse\)\);\s*return json\(\{ success: true, result_image: `data:image/png;base64,\${btoa\(binary\)}` \}\);"
new = """const base64Image = btoa(String.fromCharCode.apply(null, new Uint8Array(aiResponse)));
        return json({ success: true, result_image: `data:image/png;base64,${base64Image}` });"""

content = re.sub(old, new, content)
with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("BACKEND_FIX_OK")
