#!/usr/bin/env python3
import re

with open('kids.html', 'r') as f:
    content = f.read()

# 1. Вставить HTML прогресс-бара (после "Баланс", перед "Выполнено миссий")
html_marker = '<p><strong>Баланс:</strong> <span id="profileBalance">0</span> ₽</p>'
html_insert = '''

        <div style="margin: 20px 0; padding: 15px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 12px; color: white;">
          <h3 style="margin: 0 0 10px 0; font-size: 18px;">🏆 <span id="profileLevelName">Новичок</span> <span id="profileLevelIcon">❤️</span></h3>
          <div style="background: rgba(255,255,255,0.3); border-radius: 10px; height: 24px; overflow: hidden; margin-bottom: 8px;">
            <div id="profileProgressBar" style="background: white; height: 100%; width: 0%; transition: width 0.5s;"></div>
          </div>
          <p style="margin: 0; font-size: 14px; opacity: 0.9;">
            <span id="profileProgressText">0/25 миссий</span> • 
            <span id="profileProgressNext">До Опытного: 25 миссий</span>
          </p>
        </div>'''

content = content.replace(html_marker, html_marker + html_insert)

# 2. Вставить JavaScript логику (после profileRewardsCount, перед } catch)
js_marker = "document.getElementById('profileRewardsCount').textContent = rewardsData.count || 0;"
js_insert = '''

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
            : 'Максимальный уровень!';'''

content = content.replace(js_marker, js_marker + js_insert)

with open('kids.html', 'w') as f:
    f.write(content)

print("✅ Прогресс-бар добавлен!")
