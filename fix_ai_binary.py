import re
file_path = 'backend/worker.js'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Исправляем блок конвертации бинарных данных в Base64
old_conversion = """        const aiResponse = await env.AI.run('@cf/bytedance/stable-diffusion-xl-lightning', { prompt });
        const binary = String.fromCharCode(...new Uint8Array(aiResponse));
        return json({ success: true, result_image: `data:image/png;base64,${btoa(binary)}` });"""

new_conversion = """        const aiResponse = await env.AI.run('@cf/bytedance/stable-diffusion-xl-lightning', { prompt });
        const base64Image = btoa(String.fromCharCode.apply(null, new Uint8Array(aiResponse)));
        return json({ 
          success: true, 
          result_image: `data:image/png;base64,${base64Image}` 
        });"""

content = content.replace(old_conversion, new_conversion)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("BACKEND_BINARY_FIX_OK")
