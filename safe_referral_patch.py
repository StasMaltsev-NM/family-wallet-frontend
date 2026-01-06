import os

file_path = 'frontend/parent.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Добавляем стили (в конец секции <style>)
css = """
    .referrals-grid { display: grid; gap: 15px; margin-top: 20px; }
    .ref-card { background: #1c1f24; border-radius: 16px; padding: 20px; border: 1px solid rgba(255,255,255,0.05); }
    .ref-code { font-family: monospace; font-size: 22px; color: #24a1de; font-weight: 900; margin: 10px 0; }
    .copy-btn { background: #24a1de; color: white; border: none; padding: 10px 20px; border-radius: 10px; font-weight: bold; cursor: pointer; width: 100%; }
"""
content = content.replace('</style>', css + '\n    </style>')

# 2. Добавляем кнопку в навигацию (после кнопки ИИ)
content = content.replace(
    '<button onclick="showTab(\'tab-ai\')">ИИ</button>',
    '<button onclick="showTab(\'tab-ai\')">ИИ</button>\n      <button onclick="showTab(\'tab-referrals\')">Друзья</button>'
)

# 3. Добавляем контент вкладки (ПЕРЕД началом скрипта)
tab_html = """
    <div id="tab-referrals" class="tab-content">
      <div class="header-section">
        <h1>👥 Пригласить друзей</h1>
        <p style="opacity: 0.6;">У вас есть 3 приглашения для других семей.</p>
      </div>
      <div id="referralsList" class="referrals-grid">
        <p>Загрузка кодов...</p>
      </div>
    </div>
"""
content = content.replace('<script>', tab_html + '\n  <script>')

# 4. Добавляем вызов загрузки в функцию showTab
# Ищем место после loadAllTasks();
content = content.replace(
    "loadAllTasks();",
    "loadAllTasks();\n      }\n      if (tabId === 'tab-referrals') {\n        loadReferrals();"
)

# 5. Добавляем саму функцию loadReferrals в конец скрипта (перед </body>)
js_funcs = """
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
              <div style="font-size: 11px; font-weight: bold; opacity: 0.5;">
                ${ref.used_by_family_id ? '✅ ИСПОЛЬЗОВАН' : '🔓 ДОСТУПЕН'}
              </div>
              <div class="ref-code">${ref.invite_code}</div>
              ${ref.used_by_family_id ? '' : `<button class="copy-btn" onclick="copyText('${ref.invite_code}')">Копировать</button>`}
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
content = content.replace('</body>', '<script>' + js_funcs + '</script>\n</body>')

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("SAFE_PATCH_COMPLETED")
