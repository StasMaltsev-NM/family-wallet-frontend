import re
file_path = 'backend/worker.js'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Новая логика: правильная модель img2img + отдача картинки напрямую
img2img_logic = """
      if (path === '/api/magic/transform' && request.method === 'POST') {
        const { image, style } = await request.json();
        const stylePrompts = {
          'roblox': 'roblox 3d character, blocky, toy, white background',
          'ghibli': 'studio ghibli style, anime, hand-drawn, lush colors',
          'anime': 'high quality anime style, sharp lines, masterpiece',
          'minecraft': 'minecraft voxel style, 8-bit, blocky'
        };
        
        const base64Data = image.split(',')[1];
        const binaryString = atob(base64Data);
        const uint8Array = new Uint8Array(binaryString.length);
        for (let i = 0; i < binaryString.length; i++) uint8Array[i] = binaryString.charCodeAt(i);

        // ИСПОЛЬЗУЕМ МОДЕЛЬ IMG2IMG
        const aiResponse = await env.AI.run('@cf/runwayml/stable-diffusion-v1-5-img2img', {
          prompt: stylePrompts[style] || stylePrompts['anime'],
          image: [...uint8Array],
          strength: 0.7, // Насколько сильно менять (0.7 - заметно)
          num_inference_steps: 20
        });

        return new Response(aiResponse, {
          headers: { 
            'Content-Type': 'image/png',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': '*'
          }
        });
      }
"""

# Заменяем весь блок transform (очень широким захватом)
content = re.sub(r'if \(path === \'/api/magic/transform\'.*?\}\s*\}\s*\}\s*catch', img2img_logic + '\n      } catch', content, flags=re.DOTALL)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("BACKEND_IMG2IMG_OK")
