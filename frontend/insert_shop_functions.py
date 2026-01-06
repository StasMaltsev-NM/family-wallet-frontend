import sys

# Читаем файл
with open('parent.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Читаем функции магазина
with open('shop_functions.txt', 'r', encoding='utf-8') as f:
    shop_code = f.read()

# Находим строку с </script> и вставляем перед ней
new_lines = []
for line in lines:
    if line.strip() == '</script>':
        new_lines.append(shop_code + '\n')
    new_lines.append(line)

# Сохраняем
with open('parent.html', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print("✅ Функции магазина добавлены!")
