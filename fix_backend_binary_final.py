import re
file_path = 'backend/worker.js'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Новая логика: возвращаем Response с картинкой напрямую
binary_logic = """
      if (path === '/api/magic/transform' && request.method === 'POST') {
        const { style } = await request.json();
        const stylePrompts = {
          'roblox': 'roblox 3d avatar style, blocky, high quality, white background',
          'ghibli': 'studio ghibli hand-drawn style, anime nature, soft colors',
          'anime': 'high quality anime style, sharp lines, vibrant',
          'minecraft': 'minecraft voxel blocky style, 8-bit'
        };
        const prompt = stylePrompts[style] || stylePrompts['anime'];
        
        const aiResponse = await env.AI.run('@cf/bytedance/stable-diffusion-xl-lightning', { prompt });
        
        return new Response(aiResponse, {
          headers: { 
            'Content-Type': 'image/png',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type, X-Invite-Code'
          }
        });
      }
"""

# Заменяем старый блок transform
pattern = r"if \(path === '/api/magic/transform'.*?return json\(\{ success: true, result_image:.*?\}\);\s*\}"
content = re.sub(pattern, binary_logic, content, flags=re.DOTALL)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("BACKEND_BINARY_SUCCESS")
