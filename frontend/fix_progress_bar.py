#!/usr/bin/env python3
import re

with open('kids.html', 'r') as f:
    content = f.read()

# Удалить весь блок из catch (от "// Обновить прогресс-бар" до конца catch)
content = re.sub(
    r'(\} catch \(e\) \{\s+console\.error\(\'Ошибка загрузки профиля:\', e\);)\s+// Обновить прогресс-бар.*?(\s+\})',
    r'\1\2',
    content,
    flags=re.DOTALL
)

# Найти место для вставки (после profileRewardsCount, перед } catch)
insert_marker = "document.getElementById('profileRewardsCount').textContent = rewardsData.count || 0;"
insert_pos = content.find(insert_marker)

if insert_pos == -1:
    print("❌ Маркер не найден!")
    exit(1)

insert_pos = insert_pos + len(insert_marker)

# Код прогресс-бара
progress_code = """

        // Обновить прогресс-бар и уровень
        const missionsCount = (tasksData.tasks || []).filter(t => t.status === 'CONFIRMED').length;
        const levels = [
          { name: 'Новичок', icon: '❤️', min: 0, max: 24, next: 'Опытного' },
          { name: 'Опытный', icon: '🔷', min: 25, max: 49, next: 'Мастера' },
          { name: 'Мастер', icon: '🔺', min: 50, max: 74, next: 'Эксперта' },
          { name: 'Эксперт', icon: '⭐', min: 75, max: 99, next: 'Легенды' },
          { name: 'Легенда', icon: '🏆', min: 100, max: Infinity, next: null }
        ];

        const currentLevel = levels.find(l => missionsCount >= l.min && missionsCount <= l.max);
        const progress = currentLevel.max === Infinity 
          ? 100 
          : Math.round(((missionsCount - currentLevel.min) / (currentLevel.max - currentLevel.min + 1)) * 100);
        const remaining = currentLevel.max === Infinity ? 0 : currentLevel.max - missionsCount + 1;

        document.getElementById('profileLevelName').textContent = currentLevel.name;
        document.getElementById('profileLevelIcon').textContent = currentLevel.icon;
        document.getElementById('profileProgressBar').style.width = progress + '%';
        document.getElementById('profileProgressText').textContent = 
          currentLevel.max === Infinity 
            ? `${missionsCount} миссий (Максимум!)` 
            : `${missionsCount}/${currentLevel.max + 1} миссий`;
        document.getElementById('profileProgressNext').textContent = 
          currentLevel.next 
            ? `До ${currentLevel.next}: ${remaining} миссий` 
            : 'Максимальный уровень!';"""

# Вставка
content = content[:insert_pos] + progress_code + content[insert_pos:]

with open('kids.html', 'w') as f:
    f.write(content)

print("✅ Прогресс-бар исправлен!")
