#!/usr/bin/env python3
import re

with open('kids.html', 'r') as f:
    content = f.read()

# Найти прогресс-бар и заменить его версией с делениями
old_progress = '''        <div style="margin: 20px 0; padding: 15px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 12px; color: white;">
          <h3 style="margin: 0 0 10px 0; font-size: 18px;">🏆 <span id="profileLevelName">Новичок</span> <span id="profileLevelIcon">❤️</span></h3>
          <div style="background: rgba(255,255,255,0.3); border-radius: 10px; height: 24px; overflow: hidden; margin-bottom: 8px;">
            <div id="profileProgressBar" style="background: white; height: 100%; width: 0%; transition: width 0.5s;"></div>
          </div>
          <p style="margin: 0; font-size: 14px; opacity: 0.9;">
            <span id="profileProgressText">0/25 миссий</span> • 
            <span id="profileProgressNext">До Опытного: 25 миссий</span>
          </p>
        </div>'''

new_progress = '''        <div style="margin: 20px 0; padding: 15px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 12px; color: white;">
          <h3 style="margin: 0 0 10px 0; font-size: 18px;">🏆 <span id="profileLevelName">Новичок</span> <span id="profileLevelIcon">❤️</span></h3>
          <div style="position: relative; background: rgba(255,255,255,0.3); border-radius: 10px; height: 24px; overflow: hidden; margin-bottom: 8px;">
            <div id="profileProgressBar" style="background: white; height: 100%; width: 0%; transition: width 0.5s;"></div>
            <div style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; display: flex; justify-content: space-around; align-items: center; pointer-events: none;">
              <span id="marker0" style="font-size: 16px; transition: opacity 0.3s;">❤️</span>
              <span id="marker25" style="font-size: 16px; opacity: 0.3; transition: opacity 0.3s;">🔷</span>
              <span id="marker50" style="font-size: 16px; opacity: 0.3; transition: opacity 0.3s;">🔺</span>
              <span id="marker75" style="font-size: 16px; opacity: 0.3; transition: opacity 0.3s;">⭐</span>
              <span id="marker100" style="font-size: 16px; opacity: 0.3; transition: opacity 0.3s;">🏆</span>
            </div>
          </div>
          <p style="margin: 0; font-size: 14px; opacity: 0.9;">
            <span id="profileProgressText">0/25 миссий</span> • 
            <span id="profileProgressNext">До Опытного: 25 миссий</span>
          </p>
        </div>'''

content = content.replace(old_progress, new_progress)

# Добавить JS для обновления прозрачности маркеров
js_marker = "document.getElementById('profileProgressNext').textContent = "
js_insert_before = '''
        // Обновить прозрачность маркеров уровней
        document.getElementById('marker0').style.opacity = missionsCount >= 0 ? '1' : '0.3';
        document.getElementById('marker25').style.opacity = missionsCount >= 25 ? '1' : '0.3';
        document.getElementById('marker50').style.opacity = missionsCount >= 50 ? '1' : '0.3';
        document.getElementById('marker75').style.opacity = missionsCount >= 75 ? '1' : '0.3';
        document.getElementById('marker100').style.opacity = missionsCount >= 100 ? '1' : '0.3';

        '''

# Найти позицию и вставить перед обновлением profileProgressNext
insert_pos = content.find(js_marker)
if insert_pos != -1:
    content = content[:insert_pos] + js_insert_before + content[insert_pos:]

with open('kids.html', 'w') as f:
    f.write(content)

print("✅ Деления уровней добавлены!")
