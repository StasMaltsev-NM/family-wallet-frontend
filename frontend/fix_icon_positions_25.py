#!/usr/bin/env python3
import re

with open('kids.html', 'r') as f:
    content = f.read()

# Найти старый блок с иконками (space-around)
old_markers = '''            <div style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; display: flex; justify-content: space-around; align-items: center; pointer-events: none;">
              <span id="marker0" style="font-size: 16px; transition: opacity 0.3s;">❤️</span>
              <span id="marker25" style="font-size: 16px; opacity: 0.3; transition: opacity 0.3s;">🔷</span>
              <span id="marker50" style="font-size: 16px; opacity: 0.3; transition: opacity 0.3s;">🔺</span>
              <span id="marker75" style="font-size: 16px; opacity: 0.3; transition: opacity 0.3s;">⭐</span>
              <span id="marker100" style="font-size: 16px; opacity: 0.3; transition: opacity 0.3s;">🏆</span>
            </div>'''

# Новый блок с точным позиционированием: 0%, 25%, 50%, 75%, 100%
new_markers = '''            <div style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none;">
              <span id="marker0" style="position: absolute; left: 0%; top: 50%; transform: translate(0%, -50%); font-size: 16px; transition: opacity 0.3s;">❤️</span>
              <span id="marker25" style="position: absolute; left: 25%; top: 50%; transform: translate(-50%, -50%); font-size: 16px; opacity: 0.3; transition: opacity 0.3s;">🔷</span>
              <span id="marker50" style="position: absolute; left: 50%; top: 50%; transform: translate(-50%, -50%); font-size: 16px; opacity: 0.3; transition: opacity 0.3s;">🔺</span>
              <span id="marker75" style="position: absolute; left: 75%; top: 50%; transform: translate(-50%, -50%); font-size: 16px; opacity: 0.3; transition: opacity 0.3s;">⭐</span>
              <span id="marker100" style="position: absolute; left: 100%; top: 50%; transform: translate(-100%, -50%); font-size: 16px; opacity: 0.3; transition: opacity 0.3s;">🏆</span>
            </div>'''

content = content.replace(old_markers, new_markers)

with open('kids.html', 'w') as f:
    f.write(content)

print("✅ Позиции иконок исправлены!")
print("❤️ = 0% (0 миссий)")
print("🔷 = 25% (25 миссий)")
print("🔺 = 50% (50 миссий)")
print("⭐ = 75% (75 миссий)")
print("🏆 = 100% (100 миссий)")
