import re
import os

file_path = 'backend/worker.js'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

ai_code = """
      if (path === '/api/magic/transform' && request.method === 'POST') {
        const { image, style } = await request.json();
        const stylePrompts = {
          'roblox': 'roblox 3d avatar style, blocky, high quality',
          'ghibli': 'studio ghibli hand-drawn style, anime nature',
          'anime': 'high quality anime style, sharp lines',
          'minecraft': 'minecraft voxel blocky style'
        };
        const prompt = stylePrompts[style] || stylePrompts['anime'];
        
        const aiResponse = await env.AI.run('@cf/bytedance/stable-diffusion-xl-lightning', { prompt });
        const binary = String.fromCharCode(...new Uint8Array(aiResponse));
        return json({ success: true, result_image: `data:image/png;base64,${btoa(binary)}` });
      }
"""

# Вставляем в начало блока обработки путей (после try {)
content = content.replace('try {', 'try {\n' + ai_code)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("WORKER_AI_FIXED")
