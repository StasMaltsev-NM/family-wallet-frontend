import re
file_path = 'backend/worker.js'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Убеждаемся, что используется модель Lightning (она выдает результат за 2 секунды)
fast_ai_code = """
      if (path === '/api/magic/transform' && request.method === 'POST') {
        const { image, style } = await request.json();
        const stylePrompts = {
          'roblox': 'roblox 3d avatar style, blocky, high quality',
          'ghibli': 'studio ghibli hand-drawn style, anime nature',
          'anime': 'high quality anime style, sharp lines',
          'minecraft': 'minecraft voxel blocky style'
        };
        const prompt = stylePrompts[style] || stylePrompts['anime'];
        
        // Используем самую быструю модель
        const aiResponse = await env.AI.run('@cf/bytedance/stable-diffusion-xl-lightning', { prompt });
        const binary = String.fromCharCode(...new Uint8Array(aiResponse));
        return json({ success: true, result_image: `data:image/png;base64,${btoa(binary)}` });
      }
"""
# Вставляем в начало блока try
content = content.replace('try {', 'try {\n' + fast_ai_code)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("BACKEND_FAST_AI_OK")
