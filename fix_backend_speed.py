import re
file_path = 'backend/worker.js'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Оптимизируем параметры ИИ для скорости и точности
old_ai = "strength: 0.6"
new_ai = "strength: 0.5, num_inference_steps: 4" # 4 шага - это мгновенно для Lightning модели

content = content.replace(old_ai, new_ai)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("BACKEND_SPEED_OPTIMIZED")
