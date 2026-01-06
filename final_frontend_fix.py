file_path = 'index.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Делаем обращение к стилям безопасным
content = content.replace("document.getElementById('magicSection').style.display", "if(document.getElementById('magicSection')) document.getElementById('magicSection').style.display")
content = content.replace("document.getElementById('balanceSection').style.display", "if(document.getElementById('balanceSection')) document.getElementById('balanceSection').style.display")

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("FRONTEND_SAFE_OK")
