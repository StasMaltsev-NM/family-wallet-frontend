#!/usr/bin/env python3
import re

file_path = 'worker.js'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Найти блок после env.AI.run
old_block = r'''          const aiResult = await env\.AI\.run\(
            '@cf/stabilityai/stable-diffusion-xl-base-1\.0',
            inputs
          \);

          // Cloudflare AI возвращает данные напрямую \(уже ArrayBuffer\)
          const imageBlob = aiResult;'''

new_block = '''          const aiResult = await env.AI.run(
            '@cf/stabilityai/stable-diffusion-xl-base-1.0',
            inputs
          );

          // DEBUG: Проверяем тип данных
          console.log('aiResult type:', typeof aiResult);
          console.log('aiResult constructor:', aiResult?.constructor?.name);
          console.log('aiResult keys:', Object.keys(aiResult || {}));
          
          // Cloudflare AI возвращает объект с полем image
          const imageBlob = aiResult.image || aiResult;'''

content = re.sub(old_block, new_block, content, flags=re.MULTILINE | re.DOTALL)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print('✅ Debug логирование добавлено!')
