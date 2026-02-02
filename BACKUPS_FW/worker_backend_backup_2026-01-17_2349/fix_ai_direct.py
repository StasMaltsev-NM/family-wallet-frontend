#!/usr/bin/env python3
import re

file_path = 'worker.js'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Найти блок с response.arrayBuffer()
old_block = r'''          const response = await env\.AI\.run\(
            '@cf/stabilityai/stable-diffusion-xl-base-1\.0',
            inputs
          \);

          // Cloudflare AI возвращает Response с blob
          // Получаем ArrayBuffer напрямую
          const imageBlob = await response\.arrayBuffer\(\);'''

new_block = '''          const aiResult = await env.AI.run(
            '@cf/stabilityai/stable-diffusion-xl-base-1.0',
            inputs
          );

          // Cloudflare AI возвращает данные напрямую (уже ArrayBuffer)
          const imageBlob = aiResult;'''

content = re.sub(old_block, new_block, content, flags=re.MULTILINE | re.DOTALL)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print('✅ AI response исправлен!')
print('🔧 Убрали лишний .arrayBuffer()')
