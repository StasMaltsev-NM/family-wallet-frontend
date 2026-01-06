import re
file_path = 'worker.js'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

ai_logic = """
      // === MAGIC TRANSFORM (BINARY) ===
      if (path === '/api/magic/transform' && request.method === 'POST') {
        try {
          const { image, style } = await request.json();
          const stylePrompts = {
            'roblox': 'roblox 3d avatar style, blocky, high quality',
            'ghibli': 'studio ghibli style, anime, soft colors',
            'anime': 'high quality anime style, sharp lines',
            'minecraft': 'minecraft voxel blocky style'
          };
          const base64Data = image.split(',')[1];
          const binaryString = atob(base64Data);
          const uint8Array = new Uint8Array(binaryString.length);
          for (let i = 0; i < binaryString.length; i++) uint8Array[i] = binaryString.charCodeAt(i);

          const aiResponse = await env.AI.run('@cf/bytedance/stable-diffusion-xl-lightning', {
            prompt: stylePrompts[style] || 'anime style',
            image: [...uint8Array],
            strength: 0.6
          });

          return new Response(aiResponse, { headers: { 'Content-Type': 'image/png', 'Access-Control-Allow-Origin': '*' } });
        } catch (e) { return new Response(e.message, { status: 500 }); }
      }
"""

# Вставляем перед финальным 404
pattern = r"return error\('Эндпоинт не найден', 'NOT_FOUND', 404\);"
content = content.replace(pattern, ai_logic + "\n      " + pattern)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("PATCH_SUCCESS")
