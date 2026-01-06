#!/usr/bin/env python3
import re

file_path = 'kids.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Найти блок с логикой прогресса
old_logic = r'''        const currentLevel = levels\.find\(l => missionsCount >= l\.min && missionsCount <= l\.max\);
        const progress = currentLevel\.max === Infinity \? 100 : Math\.round\(\(\(missionsCount - currentLevel\.min\) / \(currentLevel\.max - currentLevel\.min \+ 1\)\) \* 100\);
        const remaining = currentLevel\.max === Infinity \? 0 : currentLevel\.max - missionsCount \+ 1;'''

new_logic = '''        const currentLevel = levels.find(l => missionsCount >= l.min && missionsCount <= l.max);
        
        // Прогресс ВНУТРИ текущего уровня
        const levelRange = currentLevel.max === Infinity ? 0 : (currentLevel.max - currentLevel.min + 1);
        const levelProgress = missionsCount - currentLevel.min;
        const progress = currentLevel.max === Infinity ? 100 : Math.round((levelProgress / levelRange) * 100);
        const remaining = currentLevel.max === Infinity ? 0 : (currentLevel.max - missionsCount + 1);'''

content = re.sub(old_logic, new_logic, content)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print('✅ Логика прогресс-бара исправлена!')
print('📊 Теперь шкала показывает прогресс ВНУТРИ текущего уровня:')
print('   Новичок (0-24): X/25 миссий до Опытного')
print('   Опытный (25-49): X/25 миссий до Мастера')
print('   Мастер (50-74): X/25 миссий до Эксперта')
print('   Эксперт (75-99): X/25 миссий до Легенды')
print('   Легенда (100+): Максимальный уровень!')
