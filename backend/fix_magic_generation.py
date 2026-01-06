#!/usr/bin/env python3
import re

file_path = 'worker.js'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Найти старый блок конвертации
old_conversion = r'''          // Конвертируем в base64
          const base64Image = btoa\(
            String\.fromCharCode\(\.\.\.new Uint8Array\(aiResult\)\)
          \);

          return json\(\{
            success: true,
            image_url: `data:image/png;base64,\$\{base64Image\}`,
            world: world,
            child_name: child\.name
          \}\);'''

# Новый правильный блок
new_conversion = '''          // Правильная конвертация в base64 для Workers
          const uint8Array = new Uint8Array(aiResult);
          let binaryString = '';
          const chunkSize = 8192;
          
          for (let i = 0; i < uint8Array.length; i += chunkSize) {
            const chunk = uint8Array.subarray(i, i + chunkSize);
            binaryString += String.fromCharCode.apply(null, chunk);
          }
          
          const base64Image = btoa(binaryString);

          return json({
            success: true,
            image_url: `data:image/png;base64,${base64Image}`,
            world: world,
            child_name: child.name
          });'''

content = re.sub(old_conversion, new_conversion, content, flags=re.MULTILINE)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print('✅ Конвертация base64 исправлена!')
print('🔧 Теперь изображения будут корректно отображаться')
