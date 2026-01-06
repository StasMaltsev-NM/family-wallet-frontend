#!/usr/bin/env python3
import re

file_path = 'worker.js'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Найти блок обработки aiResult
old_block = r'''          const aiResult = await env\.AI\.run\(
            '@cf/stabilityai/stable-diffusion-xl-base-1\.0',
            inputs
          \);

          // DEBUG: Проверяем тип данных
          console\.log\('aiResult type:', typeof aiResult\);
          console\.log\('aiResult constructor:', aiResult\?\.constructor\?\.name\);
          console\.log\('aiResult keys:', Object\.keys\(aiResult \|\| \{\}\)\);
          
          // Cloudflare AI возвращает объект с полем image
          const imageBlob = aiResult\.image \|\| aiResult;
          
          // Конвертируем ArrayBuffer в base64'''

new_block = '''          const aiResult = await env.AI.run(
            '@cf/stabilityai/stable-diffusion-xl-base-1.0',
            inputs
          );

          // Cloudflare AI возвращает ReadableStream - нужно прочитать
          let imageBlob;
          
          if (aiResult instanceof ReadableStream) {
            // Читаем stream
            const reader = aiResult.getReader();
            const chunks = [];
            
            while (true) {
              const { done, value } = await reader.read();
              if (done) break;
              chunks.push(value);
            }
            
            // Объединяем все чанки в один ArrayBuffer
            const totalLength = chunks.reduce((acc, chunk) => acc + chunk.length, 0);
            imageBlob = new Uint8Array(totalLength);
            let offset = 0;
            for (const chunk of chunks) {
              imageBlob.set(chunk, offset);
              offset += chunk.length;
            }
          } else {
            // Fallback если вдруг вернулся ArrayBuffer напрямую
            imageBlob = new Uint8Array(aiResult);
          }
          
          // Конвертируем ArrayBuffer в base64'''

content = re.sub(old_block, new_block, content, flags=re.MULTILINE | re.DOTALL)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print('✅ Stream reading исправлен!')
print('🔧 Теперь корректно читаем ReadableStream от Cloudflare AI')
