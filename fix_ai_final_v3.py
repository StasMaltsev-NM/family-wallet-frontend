import re
file_path = 'backend/worker.js'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Прописываем четкие промпты и надежную конвертацию
new_logic = """
      if (path === '/api/magic/transform' && request.method === 'POST') {
        const { style } = await request.json();
        
        const stylePrompts = {
          'roblox': 'roblox avatar style, blocky 3d character, high resolution, white background, masterpiece',
          'ghibli': 'studio ghibli style, hand-drawn anime, spirited away aesthetic, soft lighting, nature',
          'anime': 'modern high-quality anime style, sharp lines, cinematic lighting, masterpiece, vibrant',
          'minecraft': 'minecraft voxel style, 8-bit blocky character, cubic world aesthetic, high quality'
        };

        const prompt = stylePrompts[style] || stylePrompts['anime'];
        console.log('Generating style:', style, 'with prompt:', prompt);

        const aiResponse = await env.AI.run('@cf/bytedance/stable-diffusion-xl-lightning', { prompt });
        
        // Самый надежный метод конвертации бинарного ответа в Base64 для Cloudflare
        const base64Image = btoa(String.fromCharCode(...new Uint8Array(aiResponse)));
        
        return json({ 
          success: true, 
          result_image: `data:image/png;base64,${base64Image}`
        });
      }
"""

# Заменяем старый блок (ищем по ключевому слову transform)
pattern = r"if \(path === '/api/magic/transform'.*?return json\(\{ success: true, result_image:.*?\}\);\s*\}"
content = re.sub(pattern, new_logic, content, flags=re.DOTALL)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("BACKEND_PROMPTS_AND_IMAGE_FIX_OK")
