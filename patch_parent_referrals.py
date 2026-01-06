import os

file_path = 'frontend/parent.html'
backup_path = file_path + '.backup_referrals'
os.system(f'cp {file_path} {backup_path}')

with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 1. Добавляем стили для карточек (перед </style>)
css_patch = """
    .referrals-grid { display: grid; gap: 15px; margin-top: 20px; }
    .ref-card { background: #1c1f24; border-radius: 16px; padding: 20px; border: 1px solid rgba(255,255,255,0.05); }
    .ref-card.used { opacity: 0.5; border-color: #24a1de; }
    .ref-code { font-family: monospace; font-size: 22px; color: #24a1de; font-weight: 900; margin: 10px 0; }
    .copy-btn { background: #24a1de; color: white; border: none; padding: 10px 20px; border-radius: 10px; font-weight: bold; cursor: pointer; width: 100%; }
"""

# 2. Добавляем кнопку в навигацию
btn_patch = '      <button onclick="showTab(\'tab-referrals\')">Друзья</button>\n'

# 3. Добавляем контент вкладки
tab_patch = """
    <div id="tab-referrals" class="tab-content">
      <div class="header-section">
        <h1>👥 Пригласить друзей</h1>
        <p style="opacity: 0.6;">У вас есть 3 приглашения для других семей.</p>
      </div>
      <div id="referralsList" class="referrals-grid">
        <!-- Карточки загрузятся здесь -->
      </div>
    </div>
"""

# 4. Добавляем JS функции
js_patch = """
    async function loadReferrals() {
      const container = document.getElementById('referralsList');
      container.innerHTML = '<p>Загрузка кодов...</p>';
      try {
        const res = await fetch(`${API_URL}/api/referrals/my`, {
          headers: { 'X-Invite-Code': currentCode }
        });
        const data = await res.json();
        if (data.referrals) {
          container.innerHTML = data.referrals.map(ref => `
            <div class="ref-card ${ref.used_by_family_id ? 'used' : ''}">
              <div style="font-size: 11px; font-weight: bold; text-transform: uppercase; opacity: 0.5; margin-bottom: 5px;">
                ${ref.used_by_family_id ? '✅ Использован' : '🔓 Доступен'}
              </div>
              <div class="ref-code">${ref.invite_code}</div>
              ${ref.used_by_family_id ? '' : `<button class="copy-btn" onclick="copyText('${ref.invite_code}')">Копировать код</button>`}
            </div>
          `).join('');
        }
      } catch (e) { container.innerHTML = 'Ошибка загрузки кодов'; }
    }

    function copyText(text) {
      navigator.clipboard.writeText(text);
      alert('Код скопирован! Отправьте его друзьям.');
    }
"""

new_content = []
for line in lines:
    # Вставляем CSS
    if '</style>' in line:
        new_content.append(css_patch)
    
    new_content.append(line)
    
    # Вставляем кнопку
    if "showTab('tab-ai')" in line:
        new_content.append(btn_patch)
    
    # Вставляем вкладку
    if 'id="tab-ai"' in line:
        # Ищем конец дива tab-ai (упрощенно - перед следующим tab-content или script)
        new_content.append(tab_patch)

    # Обновляем логику showTab
    if "if (tabId === 'tab-missions')" in line:
        new_content.append("      if (tabId === 'tab-referrals') loadReferrals();\n")

    # Вставляем JS функции перед концом скрипта
    if 'async function loadPendingTasks()' in line:
        new_content.insert(-1, js_patch)

with open(file_path, 'w', encoding='utf-8') as f:
    f.writelines(new_content)

print("FRONTEND_PATCH_OK")
