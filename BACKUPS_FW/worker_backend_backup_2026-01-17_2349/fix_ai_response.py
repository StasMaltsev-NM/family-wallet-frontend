#!/usr/bin/env python3
import re

file_path = 'worker.js'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Найти блок генерации AI
old_block = r'''        try \{
          // Генерация через Cloudflare AI
          const aiResult = await env\.AI\.run\(
            '@cf/stabilityai/stable-diffusion-xl-base-1\.0',
            \{
              prompt: prompt,
              num_steps: 20
            \}
          \);

          // Правильная конвертация в base64 для Workers
          const uint8Array = new Uint8Array\(aiResult\);
          let binaryString = '';
          const chunkSize = 8192;
          
          for \(let i = 0; i < uint8Array\.length; i \+= chunkSize\) \{
            const chunk = uint8Array\.subarray\(i, i \+ chunkSize\);
            binaryString \+= String\.fromCharCode\.apply\(null, chunk\);
          \}
          
          const base64Image = btoa\(binaryString\);

          return json\(\{
            success: true,
            image_url: `data:image/png;base64,\$\{base64Image\}`,
            world: world,
            child_name: child\.name
          \}\);

        \} catch \(aiError\) \{
          console\.error\('AI Generation Error:', aiError\);
          return error\('Ошибка генерации изображения', 'AI_ERROR', 500\);
        \}'''

new_block = '''        try {
          // Генерация через Cloudflare AI (правильный формат)
          const inputs = {
            prompt: prompt,
            num_steps: 20
          };

          const response = await env.AI.run(
            '@cf/stabilityai/stable-diffusion-xl-base-1.0',
            inputs
          );

          // Cloudflare AI возвращает Response с blob
          // Получаем ArrayBuffer напрямую
          const imageBlob = await response.arrayBuffer();
          
          // Конвертируем ArrayBuffer в base64
          const uint8Array = new Uint8Array(imageBlob);
          let binaryString = '';
          const chunkSize = 8192;
          
          for (let i = 0; i < uint8Array.length; i += chunkSize) {
            const chunk = uint8Array.subarray(i, Math.min(i + chunkSize, uint8Array.length));
            binaryString += String.fromCharCode.apply(null, Array.from(chunk));
          }
          
          const base64Image = btoa(binaryString);

          // Проверка, что base64 не пустой
          if (base64Image.length < 100) {
            throw new Error('Generated image is empty or corrupted');
          }

          return json({
            success: true,
            image_url: `data:image/png;base64,${base64Image}`,
            world: world,
            child_name: child.name
          });

        } catch (aiError) {
          console.error('AI Generation Error:', aiError);
          return error('Ошибка генерации изображения: ' + aiError.message, 'AI_ERROR', 500);
        }'''

content = re.sub(old_block, new_block, content, flags=re.MULTILINE | re.DOTALL)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print('✅ AI response обработка исправлена!')
print('🔧 Теперь изображения будут корректно конвертироваться')
