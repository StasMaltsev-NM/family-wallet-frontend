import os

file_path = 'frontend/parent.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Исправляем CSS: скрываем вкладки по умолчанию (чтобы ИИ не вылезал на логине)
css_fix = """
    .tab-content { display: none; }
    .tab-content.active { display: block; }
    .referrals-grid { display: grid; gap: 15px; margin-top: 20px; }
    .ref-card { background: #f9f9f9; border: 1px solid #ddd; border-radius: 12px; padding: 15px; }
    .ref-code { font-family: monospace; font-size: 20px; color: #24a1de; font-weight: bold; margin: 10px 0; }
    .copy-btn { background: #24a1de; color: white; border: none; padding: 8px 15px; border-radius: 8px; cursor: pointer; }
"""
content = content.replace('</style>', css_fix + '\n  </style>')

# 2. Добавляем кнопку в навигацию
content = content.replace(
    '<button onclick="showTab(\'tab-ai\')">ИИ</button>',
    '<button onclick="showTab(\'tab-ai\')">ИИ</button>\n      <button onclick="showTab(\'tab-referrals\')">Друзья</button>'
)

# 3. Добавляем контент вкладки (после блока ИИ)
# Ищем заголовок ИИ и вставляем после закрывающего div-а
referral_html = """
    <div id="tab-referrals" class="tab-content">
      <div class="section">
        <h2>👥 Пригласить друзей</h2>
        <p>У вас есть 3 приглашения для других семей.</p>
        <div id="referralsList" class="referrals-grid">
          <p>Загрузка кодов...</p>
        </div>
      </div>
    </div>"""
content = content.replace('<!-- Вкладка: ИИ -->', referral_html + '\n    <!-- Вкладка: ИИ -->')

# 4. Обновляем функцию showTab (добавляем вызов загрузки рефералов)
content = content.replace(
    "if (tabId === 'tab-missions') {",
    "if (tabId === 'tab-referrals') loadReferrals();\n      if (tabId === 'tab-missions') {"
)

# 5. Добавляем JS функции в самый конец скрипта
js_logic = """
    async function loadReferrals() {
      const container = document.getElementById('referralsList');
      try {
        const res = await fetch(`${API_URL}/api/referrals/my`, {
          headers: { 'X-Invite-Code': currentCode }
        });
        const data = await res.json();
        if (data.referrals) {
          container.innerHTML = data.referrals.map(ref => `
            <div class="ref-card">
              <div style="font-size: 11px; color: #888;">${ref.used_by_family_id ? '✅ ИСПОЛЬЗОВАН' : '🔓 ДОСТУПЕН'}</div>
              <div class="ref-code">${ref.invite_code}</div>
              ${ref.used_by_family_id ? '' : '<button class="copy-btn" onclick="copyText(\\''+ref.invite_code+'\\')">Копировать</button>'}
            </div>
          `).join('');
        }
      } catch (e) { container.innerHTML = 'Ошибка загрузки'; }
    }

    function copyText(text) {
      navigator.clipboard.writeText(text);
      alert('Код скопирован!');
    }
"""
content = content.replace('</script>', js_logic + '\n  </script>')

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("FINAL_PATCH_SUCCESS")
