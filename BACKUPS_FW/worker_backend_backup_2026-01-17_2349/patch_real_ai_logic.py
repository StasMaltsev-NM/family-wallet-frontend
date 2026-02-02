import re

file_path = 'backend/worker.js'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Новая логика генерации через Cloudflare AI
real_ai_logic = """
      // POST /api/magic/transform - Реальная генерация изображения
      if (path === '/api/magic/transform' && request.method === 'POST') {
        const inviteCode = request.headers.get('X-Invite-Code');
        const { image, style } = await request.json();
        
        const stylePrompts = {
          'roblox': 'roblox character style, blocky 3d avatar, high resolution, vibrant colors',
          'ghibli': 'studio ghibli style, hand-drawn anime, spirited away aesthetic, soft lighting',
          'anime': 'modern high-quality anime style, sharp lines, cinematic lighting, masterpiece',
          'minecraft': 'minecraft voxel style, 8-bit blocky world, cubic aesthetic'
        };

        const prompt = stylePrompts[style] || stylePrompts['anime'];

        // Запуск генерации через Cloudflare AI
        // Мы используем текстовый промпт для создания нового образа
        const aiResponse = await env.AI.run('@cf/bytedance/stable-diffusion-xl-lightning', {
          prompt: prompt
        });

        // Конвертируем бинарный ответ в base64
        const binary = String.fromCharCode(...new Uint8Array(aiResponse));
        const base64Image = btoa(binary);
        const resultData = `data:image/png;base64,${base64Image}`;

        return json({ 
          success: true, 
          result_image: resultData,
          message: 'Магия завершена! ✨'
        });
      }
"""

# Заменяем старый эндпоинт на новый
pattern = r"// POST /api/magic/transform.*?return json\(\{.*?\}\);\s*\}"
content = re.sub(pattern, real_ai_logic, content, flags=re.DOTALL)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("REAL_AI_BACKEND_OK")
