import re
import os

file_path = 'backend/worker.js'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

real_ai_logic = """
      // POST /api/magic/transform - Реальная генерация изображения
      if (path === '/api/magic/transform' && request.method === 'POST') {
        const { image, style } = await request.json();
        
        const stylePrompts = {
          'roblox': 'roblox character style, blocky 3d avatar, high resolution, white background',
          'ghibli': 'studio ghibli style, hand-drawn anime, soft lighting, nature',
          'anime': 'modern high-quality anime style, sharp lines, cinematic',
          'minecraft': 'minecraft voxel style, 8-bit blocky world'
        };

        const prompt = stylePrompts[style] || stylePrompts['anime'];

        // Запуск Cloudflare AI
        const aiResponse = await env.AI.run('@cf/bytedance/stable-diffusion-xl-lightning', {
          prompt: prompt
        });

        const binary = String.fromCharCode(...new Uint8Array(aiResponse));
        const base64Image = btoa(binary);
        
        return json({ 
          success: true, 
          result_image: `data:image/png;base64,${base64Image}`,
          message: 'Магия завершена! ✨'
        });
      }
"""

# Заменяем старую заглушку (даже если она сломана)
pattern = r"// POST /api/magic/transform.*?return json\(\{.*?\}\);\s*\}"
content = re.sub(pattern, real_ai_logic, content, flags=re.DOTALL)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("BACKEND_AI_FIX_OK")
