#!/usr/bin/env python3
import re

with open('kids.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Добавляем стили для дашборда мечты
styles = """
    .dream-dashboard { padding: 20px; margin: 20px 0; border: 2px solid #9C27B0; background: linear-gradient(135deg, #f3e5f5 0%, #e1bee7 100%); border-radius: 12px; position: relative; }
    .dream-input-form { display: flex; gap: 10px; align-items: center; }
    .dream-input { flex: 1; padding: 12px; border: 2px solid #9C27B0; border-radius: 8px; font-size: 16px; }
    .dream-button { background: #9C27B0; color: white; border: none; padding: 12px 24px; border-radius: 8px; cursor: pointer; font-size: 16px; font-weight: bold; }
    .dream-button:hover { background: #7B1FA2; }
    .dream-close { position: absolute; top: 10px; right: 10px; background: #f44336; color: white; border: none; width: 30px; height: 30px; border-radius: 50%; cursor: pointer; font-size: 18px; }
    .dream-progress-bar { width: 100%; height: 30px; background: #e0e0e0; border-radius: 15px; overflow: hidden; margin: 15px 0; }
    .dream-progress-fill { height: 100%; background: linear-gradient(90deg, #4CAF50 0%, #8BC34A 100%); transition: width 0.3s; }
    .dream-status { color: #9C27B0; font-weight: bold; margin-top: 10px; }
"""

content = re.sub(r'(\.confirm-button[^}]+\})', r'\1\n' + styles, content)

# 2. Добавляем HTML дашборд ПОСЛЕ секции баланса
dream_html = """
  <div class="section" id="dreamSection" style="display:none;">
    <div id="dreamDashboard"></div>
  </div>
"""

content = re.sub(
    r'(<div class="section" id="balanceSection"[^>]*>.*?</div>\s*</div>)',
    r'\1\n' + dream_html,
    content,
    flags=re.DOTALL
)

# 3. Добавляем JavaScript функции
js_functions = """
    // ============================
    // МЕЧТЫ РЕБЁНКА
    // ============================

    async function loadMyDream() {
      try {
        const res = await fetch(`${API_URL}/api/dreams/my`, {
          headers: { 'X-Invite-Code': currentCode }
        });
        
        if (!res.ok) throw new Error('Ошибка загрузки мечты');
        
        const data = await res.json();
        const dashboard = document.getElementById('dreamDashboard');
        
        if (!data.dream) {
          // Показываем форму создания мечты
          dashboard.innerHTML = `
            <div class="dream-dashboard">
              <h2>💭 Моя мечта</h2>
              <div class="dream-input-form">
                <input type="text" id="dreamTitleInput" class="dream-input" placeholder="О чём ты мечтаешь?" maxlength="100">
                <button class="dream-button" onclick="createDream()">+ Добавить</button>
              </div>
            </div>
          `;
          return;
        }
        
        const dream = data.dream;
        
        if (dream.status === 'pending') {
          // Ожидает подтверждения родителя
          dashboard.innerHTML = `
            <div class="dream-dashboard">
              <button class="dream-close" onclick="deleteDream('${dream.id}')">✕</button>
              <h2>🎯 ${dream.title}</h2>
              <div class="dream-status">⏳ Ожидает подтверждения родителя...</div>
            </div>
          `;
        } else if (dream.status === 'active') {
          // Показываем прогресс
          const progress = Math.min(100, Math.round((dream.current_amount / dream.target_amount) * 100));
          
          dashboard.innerHTML = `
            <div class="dream-dashboard">
              <button class="dream-close" onclick="deleteDream('${dream.id}')">✕</button>
              <h2>🎯 ${dream.title}</h2>
              <div class="dream-progress-bar">
                <div class="dream-progress-fill" style="width: ${progress}%"></div>
              </div>
              <div style="font-size: 18px; font-weight: bold; text-align: center;">
                ${dream.current_amount} / ${dream.target_amount} ⭐
              </div>
              <div style="text-align: center; color: #666; margin-top: 5px;">
                Прогресс: ${progress}%
              </div>
            </div>
          `;
        }
        
      } catch (err) {
        console.error('Ошибка загрузки мечты:', err);
      }
    }

    async function createDream() {
      const input = document.getElementById('dreamTitleInput');
      const title = input.value.trim();
      
      if (!title) {
        alert('Введи название мечты!');
        return;
      }
      
      try {
        const res = await fetch(`${API_URL}/api/dreams/create`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-Invite-Code': currentCode
          },
          body: JSON.stringify({ title })
        });
        
        if (!res.ok) {
          const err = await res.json();
          alert(`Ошибка: ${err.error || 'Не удалось создать мечту'}`);
          return;
        }
        
        const data = await res.json();
        alert(`✅ ${data.message}`);
        
        loadMyDream();
        
      } catch (err) {
        alert(`Ошибка: ${err.message}`);
      }
    }

    async function deleteDream(dreamId) {
      if (!confirm('Удалить мечту?')) return;
      
      try {
        const res = await fetch(`${API_URL}/api/dreams/delete`, {
          method: 'DELETE',
          headers: {
            'Content-Type': 'application/json',
            'X-Invite-Code': currentCode
          },
          body: JSON.stringify({ dream_id: dreamId })
        });
        
        if (!res.ok) {
          const err = await res.json();
          alert(`Ошибка: ${err.error}`);
          return;
        }
        
        const data = await res.json();
        alert(`✅ ${data.message}`);
        
        loadMyDream();
        
      } catch (err) {
        alert(`Ошибка: ${err.message}`);
      }
    }

"""

# Вставляем функции перед закрывающим </script>
content = re.sub(r'(  </script>)', js_functions + r'\n\1', content)

# 4. Добавляем отображение секции при логине
content = content.replace(
    "document.getElementById('historySection').style.display = 'block';",
    """document.getElementById('historySection').style.display = 'block';
        document.getElementById('dreamSection').style.display = 'block';"""
)

# 5. Добавляем вызов загрузки мечты при логине
content = content.replace(
    "loadShopRewards();",
    """loadShopRewards();
        loadMyDream();"""
)

with open('kids.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("OK")
