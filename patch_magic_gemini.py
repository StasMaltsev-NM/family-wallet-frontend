import re
import os

file_path = 'backend/worker.js'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

magic_logic = """
      // POST /api/magic/transform - Стилизация фото через Gemini
      if (path === '/api/magic/transform' && request.method === 'POST') {
        const inviteCode = request.headers.get('X-Invite-Code');
        const { image, style } = await request.json(); // image: base64
        
        const stylePrompts = {
          'roblox': 'Transform this image into a 3D Roblox world style. Characters should look like blocky avatars.',
          'ghibli': 'Transform this image into Studio Ghibli anime style. Soft colors, hand-drawn aesthetic.',
          'anime': 'Transform this image into high-quality modern anime style.',
          'minecraft': 'Transform this image into Minecraft voxel style. Everything made of blocks.'
        };

        const prompt = stylePrompts[style] || stylePrompts['anime'];

        // Запрос к Google Gemini API
        const response = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=${env.GEMINI_API_KEY}`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            contents: [{
              parts: [
                { text: prompt },
                { inline_data: { mime_type: "image/jpeg", data: image.split(',')[1] } }
              ]
            }]
          })
        });

        const data = await response.json();
        // Примечание: Gemini API возвращает текст описания или байты изображения в зависимости от модели.
        // Для MVP мы получаем подтверждение обработки.
        return json({ 
          success: true, 
          message: "Магия в процессе! ✨",
          data: data 
        });
      }
"""

# Вставка перед финальным 404
pattern = r"return error\(.*NOT_FOUND.*404\);"
content = re.sub(pattern, magic_logic + "\n      " + r"return error('Эндпоинт не найден', 'NOT_FOUND', 404);", content)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("GEMINI_BACKEND_PATCH_OK")
