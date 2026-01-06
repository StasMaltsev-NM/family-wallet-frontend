import re
file_path = 'backend/worker.js'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Новая логика: безопасная сборка Base64
safe_ai_logic = """
      if (path === '/api/magic/transform' && request.method === 'POST') {
        const { image, style } = await request.json();
        const stylePrompts = {
          'roblox': 'roblox 3d avatar, blocky, high quality, vibrant colors',
          'ghibli': 'studio ghibli hand-drawn anime style, soft lighting',
          'anime': 'high quality anime style, sharp lines, masterpiece',
          'minecraft': 'minecraft voxel style, 8-bit blocky'
        };
        
        const base64Data = image.split(',')[1];
        const binaryString = atob(base64Data);
        const uint8Array = new Uint8Array(binaryString.length);
        for (let i = 0; i < binaryString.length; i++) uint8Array[i] = binaryString.charCodeAt(i);

        const aiResponse = await env.AI.run('@cf/bytedance/stable-diffusion-xl-lightning', {
          prompt: stylePrompts[style] || stylePrompts['anime'],
          image: [...uint8Array],
          strength: 0.6
        });

        // БЕЗОПАСНАЯ КОНВЕРТАЦИЯ (без ограничений по размеру)
        let binary = "";
        const bytes = new Uint8Array(aiResponse);
        for (let i = 0; i < bytes.byteLength; i++) {
          binary += String.fromCharCode(bytes[i]);
        }
        const base64Image = btoa(binary);

        return json({ 
          success: true, 
          result_image: `data:image/png;base64,${base64Image}` 
        });
      }
"""

# Заменяем старый блок transform
pattern = r"if \(path === '/api/magic/transform'.*?return new Response\(aiResponse.*?\);\s*\}"
content = re.sub(pattern, safe_ai_logic, content, flags=re.DOTALL)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("BACKEND_SAFE_BASE64_OK")
