file_path = 'backend/worker.js'
with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_worker_code = []
skip = False

# Новая бинарная логика
binary_logic = """
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

          return new Response(aiResponse, {
            headers: { 'Content-Type': 'image/png', 'Access-Control-Allow-Origin': '*' }
          });
        } catch (e) {
          return new Response(e.message, { status: 500, headers: { 'Access-Control-Allow-Origin': '*' } });
        }
      }
"""

for line in lines:
    # Если находим начало старого блока магии - начинаем пропуск
    if "path === '/api/magic/transform'" in line:
        skip = True
        new_worker_code.append(binary_logic)
        continue
    
    # Если мы в режиме пропуска, ищем закрывающую скобку блока
    if skip:
        if "}" in line and "      if" not in line: # Конец блока if
            skip = False
        continue
    
    new_worker_code.append(line)

with open(file_path, 'w', encoding='utf-8') as f:
    f.writelines(new_worker_code)
print("WORKER_V8_FORCE_REPLACED")
