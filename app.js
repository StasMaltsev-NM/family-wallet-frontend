    const API_URL = 'https://family-wallet-api.maltsevstas21.workers.dev';
    let currentCode = '';
    let familyId = '';
    let childrenData = [];

    // ========================================
    // ГЛОБАЛЬНЫЙ КОНТЕКСТ РЕБЁНКА
    // ========================================
    let selectedChildId = null;

    // Восстановить selectedChildId при загрузке
    function restoreSelectedChild() {
      selectedChildId = localStorage.getItem("selectedChildId");
      console.log("Восстановлен selectedChildId:", selectedChildId);
    }

    // Переключение ребёнка
function switchChild(childId) {
  console.log('Переключение на ребёнка:', childId);
  selectedChildId = childId;
  localStorage.setItem('selectedChildId', childId);

  renderTopBar();

  const activeTab = document.querySelector('.tab-content.active');
  if (activeTab && activeTab.id === 'tab-missions') {
    loadFilteredTasks(childId);
  }

  // Показать кнопку Профиль и загрузить данные
  const profileBtn = document.getElementById('profileTabButton');
  if (profileBtn) profileBtn.style.display = 'block';
  const child = childrenData.find(c => c.id === childId);
  if (child && profileBtn) profileBtn.textContent = child.name;

  // Если открыта вкладка Профиль — обновить данные
  if (activeTab && activeTab.id === 'tab-profile') {
    loadChildProfile(childId);
  }
  
  // Показать профиль выбранного ребёнка
  showChildPersonalView(childId);
  
  // Показываем Child Bottom Navigation
  const childNav = document.getElementById('childBottomNavigation');
  if (childNav) childNav.style.display = 'flex';
  
  // Скрываем Parent Navigation
  const parentNav = document.querySelector('.nav-tabs');
  if (parentNav) parentNav.style.display = 'none';
  
} // ← ВОТ ТУТ закрывается функция!
      
    // ========================================
    // ОТРИСОВКА ВЕРХНЕЙ ШАПКИ (список детей)
    // ========================================
    function renderTopBar() {
      const container = document.getElementById('childrenTabs');
      if (!container) return;

      if (!childrenData || childrenData.length === 0) {
        container.innerHTML = '<p style="color: white; font-size: 14px;">Нет детей</p>';
        return;
      }

      container.innerHTML = childrenData.map(child => {
        const isActive = selectedChildId === child.id;
  // Проверяем, есть ли уведомления (задачи WAITING)
  const hasNotifications = child.pending_balance > 0; // Если есть баланс на проверке
        return `
          <div onclick="switchChild('${child.id}')" 
               style="cursor: pointer; text-align: center; position: relative;">
            <!-- Двойное кольцо -->
<div style="width: 70px; height: 70px; border-radius: 50%;
            background: ${isActive ? 'linear-gradient(135deg, #A78BFA 0%, #818CF8 100%)' : 'transparent'};
            padding: 3px; display: flex; align-items: center; justify-content: center;
            box-shadow: ${isActive ? '0 0 15px rgba(167, 139, 250, 0.7)' : 'none'};
            transition: all 0.3s; position: relative;">
  ${hasNotifications ? '<div class="avatar-notification-ring"></div>' : ''}
              <!-- Внутренний круг (аватар) -->
              <div style="width: 100%; height: 100%; border-radius: 50%; 
                          background: #1a1a1a; border: 2px solid #2D2B3F;
                          display: flex; align-items: center; justify-content: center; 
                          font-size: 28px; filter: ${isActive ? 'none' : 'grayscale(1) opacity(0.5)'};
                          transition: all 0.3s;">
                👶
              </div>
            </div>
            <!-- Имя ребёнка -->
            <div style="font-size: 11px; margin-top: 6px; color: ${isActive ? '#A78BFA' : '#666'}; 
                        font-weight: ${isActive ? '800' : '400'}; text-transform: uppercase; 
                        letter-spacing: 0.05em; font-family: 'Plus Jakarta Sans', Arial, sans-serif;">
              ${child.name}
            </div>
          </div>
        `;
      }).join('');
    }
    function showTab(tabId) {
      document.querySelectorAll('.tab-content').forEach(tab => tab.classList.remove('active'));
      document.querySelectorAll('.nav-tabs button').forEach(btn => btn.classList.remove('active'));
      
      document.getElementById(tabId).classList.add('active');
      event.target.classList.add('active');
      
      if (tabId === 'tab-missions') {
        if (selectedChildId) {
          loadFilteredTasks(selectedChildId);
        } else {
          loadAllTasks();
        }
      }
      
      // Загружаем награды при открытии Магазина
      if (tabId === 'tab-shop') {
        if (selectedChildId) {
          loadFilteredRewards(selectedChildId);
        } else {
          loadRewards();
        }
      }
      
      // Загружаем профиль при открытии вкладки Профиль
      if (tabId === 'tab-profile') {
        if (selectedChildId) {
          loadChildProfile(selectedChildId);

        }
      }
    }

    function toggleRecurringOptions() {
      const isChecked = document.getElementById('taskRecurring').checked;
      document.getElementById('recurringOptions').style.display = isChecked ? 'block' : 'none';
    }

    function toggleDaysSelection() {
      const type = document.getElementById('recurringType').value;
      document.getElementById('daysSelection').style.display = type === 'custom' ? 'block' : 'none';
    }

    function toggleAddChildForm() {
      const modal = document.getElementById('addChildModal');
      const isOpening = !modal.classList.contains('active');
      
      if (isOpening) {
        // Открытие модалки - очистка полей
        document.getElementById('childName').value = '';
        document.getElementById('childRole').value = '';
        document.getElementById('childAge').value = '';
        document.getElementById('childAiDescription').value = '';
        document.getElementById('addChildStatus').innerHTML = '';
        
        // Сброс режима редактирования
        editingChildId = null;
        document.querySelector('#addChildForm h3').textContent = 'Добавить ребёнка';
        const submitBtn = document.querySelector('#addChildForm button[onclick*="Child"]');
        if (submitBtn) {
          submitBtn.textContent = 'Создать';
          submitBtn.setAttribute('onclick', 'addChild()');
        }
        
        modal.classList.add('active');
      } else {
        // Закрытие модалки
        modal.classList.remove('active');
        editingChildId = null;
      }
    }


    // Закрытие модалки по клику на backdrop
    document.addEventListener('DOMContentLoaded', function() {
      const modal = document.getElementById('addChildModal');
      if (modal) {
        modal.addEventListener('click', function(e) {
          if (e.target === modal) {
            toggleAddChildForm();
          }
        });
      }
    });

    function toggleAddTaskForm() {
      const form = document.getElementById('addTaskForm');
      form.style.display = form.style.display === 'none' ? 'block' : 'none';
      if (form.style.display === 'block') {
        document.getElementById('taskTitle').value = '';
        document.getElementById('taskDescription').value = '';
        document.getElementById('taskReward').value = '';
        document.getElementById('taskRecurring').checked = false;
        document.getElementById('addTaskStatus').innerHTML = '';
        toggleRecurringOptions();
        updateChildrenSelection();
      }
    }

    function updateChildrenSelection() {
      const container = document.getElementById('taskChildrenSelection');
      if (childrenData.length === 0) {
        container.innerHTML = '<p class="error">Сначала добавьте детей</p>';
        return;
      }
      
      container.innerHTML = childrenData.map(child => `
        <label>
          <input type="checkbox" class="child-checkbox" value="${child.id}">
          ${child.name} (${child.role}, ${child.age} лет)
        </label>
      `).join('');
    }

    async function createTask() {
      const title = document.getElementById('taskTitle').value.trim();
      const description = document.getElementById('taskDescription').value.trim();
      const reward = document.getElementById('taskReward').value.trim();
      const isRecurring = document.getElementById('taskRecurring').checked;
      
      if (!title || !reward) {
        document.getElementById('addTaskStatus').innerHTML = '<p class="error">Заполните обязательные поля (название и сумма)</p>';
        return;
      }

      const selectedChildren = Array.from(document.querySelectorAll('.child-checkbox:checked')).map(cb => cb.value);
      
      if (selectedChildren.length === 0) {
        document.getElementById('addTaskStatus').innerHTML = '<p class="error">Выберите хотя бы одного ребёнка</p>';
        return;
      }

      let recurring = null;
      let recurringDays = null;

      if (isRecurring) {
        const recurringType = document.getElementById('recurringType').value;
        if (!recurringType) {
          document.getElementById('addTaskStatus').innerHTML = '<p class="error">Выберите тип повторения</p>';
          return;
        }

        if (recurringType === 'daily') {
          recurring = 'daily';
        } else if (recurringType === 'weekends') {
          recurring = 'weekends';
        } else if (recurringType === 'custom') {
          const selectedDays = Array.from(document.querySelectorAll('#daysSelection input:checked')).map(cb => cb.value);
          if (selectedDays.length === 0) {
            document.getElementById('addTaskStatus').innerHTML = '<p class="error">Выберите дни недели</p>';
            return;
          }
          recurring = 'custom';
          recurringDays = JSON.stringify(selectedDays);
        }
      }

      try {
        // Создаём задачу для каждого выбранного ребёнка
        for (const childId of selectedChildren) {
          const res = await fetch(`${API_URL}/api/tasks/create`, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              'X-Invite-Code': currentCode
            },
            body: JSON.stringify({
              child_id: childId,
              title,
              description,
              reward_amount: parseInt(reward),
              recurring,
              recurring_days: recurringDays
            })
          });

          const data = await res.json();
          if (!res.ok) {
            document.getElementById('addTaskStatus').innerHTML = `<p class="error">Ошибка: ${data.error}</p>`;
            return;
          }
        }

        document.getElementById('addTaskStatus').innerHTML = '<p class="success">✅ Миссия создана!</p>';
        setTimeout(() => {
          toggleAddTaskForm();
          loadAllTasks();
        }, 1500);

      } catch (err) {
        document.getElementById('addTaskStatus').innerHTML = `<p class="error">Ошибка: ${err.message}</p>`;
      }
    }

    async function loadAllTasks() {
      try {
        const res = await fetch(`${API_URL}/api/tasks/list`, {
          headers: { 'X-Invite-Code': currentCode }
        });

        const data = await res.json();
        
        if (!Array.isArray(data.tasks)) {
          document.getElementById('tasksList').innerHTML = '<p class="error">Ошибка загрузки задач</p>';
          return;
        }

        if (data.tasks.length === 0) {
          document.getElementById('tasksList').innerHTML = '<p>Миссий пока нет. Нажмите "+" чтобы создать.</p>';
          return;
        }

        document.getElementById('tasksList').innerHTML = data.tasks.map(task => `
          <div class="task-item">
            <button class="delete-button" onclick="deleteTask('${task.id}')">✕</button>
            <strong>${task.title}</strong> — ${task.reward_amount} ⭐<br>
            ${task.description || ''}<br>
            <small>Статус: ${task.status} ${task.recurring ? '(повторяющаяся: ' + task.recurring + ')' : ''}</small>
            ${task.status === 'WAITING' ? '<br><button onclick="confirmTask(\''+task.id+'\', \'confirm\')">✅ Подтвердить</button> <button onclick="confirmTask(\''+task.id+'\', \'reject\')">❌ Отклонить</button>' : ''}
          </div>
        `).join('');

      } catch (err) {
        document.getElementById('tasksList').innerHTML = `<p class="error">Ошибка: ${err.message}</p>`;
      }
    }


    async function loadFilteredTasks(childId) {
      try {
        const res = await fetch(`${API_URL}/api/tasks/list`, {
          headers: { 'X-Invite-Code': currentCode }
        });
        const data = await res.json();
        if (!Array.isArray(data.tasks)) {
          document.getElementById('tasksList').innerHTML = '<p class="error">Ошибка загрузки задач</p>';
          return;
        }
        const childTasks = data.tasks.filter(t => t.child_id === childId);
        if (childTasks.length === 0) {
          document.getElementById('tasksList').innerHTML = '<p>У этого ребёнка пока нет миссий.</p>';
          return;
        }
        document.getElementById('tasksList').innerHTML = childTasks.map(task => `
          <div class="task-item">
            <button class="delete-button" onclick="deleteTask('${task.id}')">✕</button>
            <strong>${task.title}</strong> — ${task.reward_amount} ⭐<br>
            ${task.description || ''}<br>
            <small>Статус: ${task.status}</small>
            ${task.status === 'WAITING' ? '<br><button onclick="confirmTask(\''+task.id+'\', \'confirm\')">✅ Подтвердить</button>' : ''}
          </div>
        `).join('');
      } catch (err) {
        document.getElementById('tasksList').innerHTML = `<p class="error">Ошибка: ${err.message}</p>`;
      }
    }

    async function deleteTask(taskId) {
      

      try {
        const res = await fetch(`${API_URL}/api/tasks/delete`, {
          method: 'DELETE',
          headers: {
            'Content-Type': 'application/json',
            'X-Invite-Code': currentCode
          },
          body: JSON.stringify({ task_id: taskId })
        });

        const data = await res.json();
        
        if (!res.ok) {
          alert('Ошибка: ' + data.error);
          return;
        }

        loadAllTasks();

      } catch (err) {
        alert('Ошибка: ' + err.message);
      }
    }

    async function addChild() {
      const name = document.getElementById('childName').value.trim();
      const role = document.getElementById('childRole').value.trim();
      const age = document.getElementById('childAge').value.trim();
      const ai_description = document.getElementById('childAiDescription').value.trim();

      if (!name || !role || !age) {
        document.getElementById('addChildStatus').innerHTML = '<p class="error">Заполните все поля</p>';
        return;
      }

      try {
        const res = await fetch(`${API_URL}/api/children/add`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-Invite-Code': currentCode
          },
          body: JSON.stringify({ name, role, age: parseInt(age), ai_description: ai_description || null })
        });

        const data = await res.json();

        if (!res.ok) {
          document.getElementById('addChildStatus').innerHTML = `<p class="error">Ошибка: ${data.error}</p>`;
          return;
        }

        document.getElementById('addChildStatus').innerHTML = `
          <p class="success">✅ ${data.message}</p>
          <div class="invite-code-display">
            КОД РЕБЁНКА: ${data.child.invite_code}
            <br><button onclick="copyToClipboard('${data.child.invite_code}')">📋 Скопировать</button>
          </div>
          <p><strong>Отправьте этот код ребёнку для входа в детское приложение</strong></p>
        `;

        loadChildren();
        renderTopBar();

        document.getElementById('childName').value = '';
        document.getElementById('childRole').value = '';
        document.getElementById('childAge').value = '';
        document.getElementById('childAiDescription').value = '';

      } catch (err) {
        document.getElementById('addChildStatus').innerHTML = `<p class="error">Ошибка: ${err.message}</p>`;
      }
    }

    // Редактирование ребёнка
    let editingChildId = null;

    function editChild(childId) {
      editingChildId = childId;
      
      // Найти ребёнка в данных
      const child = childrenData.find(c => c.id === childId);
      if (!child) return;

      // Заполнить форму существующими данными
      document.getElementById('childName').value = child.name;
      document.getElementById('childRole').value = child.role;
      document.getElementById('childAge').value = child.age;
      document.getElementById('childAiDescription').value = child.ai_description || '';

      // Показать форму
      document.getElementById('addChildForm').style.display = 'flex';

      // Изменить текст кнопки
      const submitBtn = document.querySelector('#addChildForm button[onclick="addChild()"]');
      submitBtn.textContent = '💾 Сохранить изменения';
      submitBtn.setAttribute('onclick', 'saveChildEdit()');

      // Изменить заголовок
      document.querySelector('#addChildForm h3').textContent = '✏️ Редактировать ребёнка';
    }

    async function saveChildEdit() {
      const name = document.getElementById('childName').value.trim();
      const role = document.getElementById('childRole').value.trim();
      const age = document.getElementById('childAge').value.trim();
      const ai_description = document.getElementById('childAiDescription').value.trim();

      if (!name || !role || !age) {
        document.getElementById('addChildStatus').innerHTML = '<p class="error">Заполните все обязательные поля</p>';
        return;
      }

      try {
        const res = await fetch(`${API_URL}/api/children/edit/${editingChildId}`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
            'X-Invite-Code': currentCode
          },
          body: JSON.stringify({ name, role, age: parseInt(age), ai_description: ai_description || null })
        });

        const data = await res.json();

        if (!res.ok) {
          document.getElementById('addChildStatus').innerHTML = `<p class="error">Ошибка: ${data.error}</p>`;
          return;
        }

        document.getElementById('addChildStatus').innerHTML = '<p class="success">✅ Изменения сохранены!</p>';

        // Перезагрузить список детей
        await loadChildren();
        renderTopBar();

        // Закрыть форму через 1 секунду
        setTimeout(() => {
          toggleAddChildForm();
        }, 1000);

      } catch (err) {
        document.getElementById('addChildStatus').innerHTML = `<p class="error">Ошибка: ${err.message}</p>`;
      }
    }

    function copyToClipboard(text) {
      navigator.clipboard.writeText(text).then(() => {
        alert('Код скопирован в буфер обмена!');
      }).catch(() => {
        alert('Не удалось скопировать. Перепишите код вручную.');
      });
    }
    async function loadHistory() {
      try {
        const res = await fetch(`${API_URL}/api/tasks/list`, {
          headers: { 'X-Invite-Code': currentCode }
        });
        const data = await res.json();
        if (!Array.isArray(data.tasks)) return;
        const completed = data.tasks.filter(t => t.status === 'CONFIRMED').slice(0, 10);
        if (completed.length === 0) {
          document.getElementById('historyList').innerHTML = '<div class="empty-state">История пуста</div>';
          return;
        }
        document.getElementById('historyList').innerHTML = completed.map(task => `
          <div class="history-item">✅ ${task.title} — +${task.reward_amount} ⭐</div>
        `).join('');
      } catch (err) {
        document.getElementById('historyList').innerHTML = `<p class="error">Ошибка загрузки истории</p>`;
      }
    }



    async function login() {
      const code = document.getElementById('inviteCode').value.trim();
      if (!code) {
        document.getElementById('authStatus').innerHTML = '<p class="error">Введите код приглашения</p>';
        return;
      }

      try {
        const res = await fetch(`${API_URL}/api/auth/whoami`, {
          headers: { 'X-Invite-Code': code }
        });

        if (!res.ok) {
          const err = await res.json();
          document.getElementById('authStatus').innerHTML = `<p class="error">Ошибка: ${err.error}</p>`;
          return;
        }

        const data = await res.json();
        
        if (data.role !== 'parent') {
          document.getElementById('authStatus').innerHTML = '<p class="error">Этот код для ребёнка. Используйте родительский код.</p>';
          return;
        }

        currentCode = code;
        familyId = data.family_id;
        
        document.getElementById('authStatus').innerHTML = `<p class="success">✅ Добро пожаловать, ${data.family_name}!</p>`;
        document.getElementById('topBar').style.display = 'flex';
        document.getElementById('privacyNotice').style.display = 'none';
        document.getElementById('mainApp').style.display = 'block';

        await loadChildren();
        renderTopBar();
        
        // Автоматически открываем профиль первого ребёнка
        if (childrenData && childrenData.length > 0) {
          const firstChildId = childrenData[0].id;
          selectedChildId = firstChildId;
          localStorage.setItem('selectedChildId', firstChildId);
          switchChild(firstChildId);
        }

      } catch (err) {
        document.getElementById('authStatus').innerHTML = `<p class="error">Ошибка сети: ${err.message}</p>`;
      }
    }

    async function loadChildren() {
      try {
        const res = await fetch(`${API_URL}/api/children/list`, {
          headers: { 'X-Invite-Code': currentCode }
        });

        const data = await res.json();
        
        if (!Array.isArray(data.children)) {
          document.getElementById('childrenList').innerHTML = '<p class="error">Ошибка загрузки детей</p>';
          return;
        }

        childrenData = data.children;

        if (data.children.length === 0) {
          document.getElementById('childrenList').innerHTML = '<p>Детей пока нет. Нажмите "+" чтобы добавить.</p>';
          return;
        }

        document.getElementById('childrenList').innerHTML = data.children.map(child => `
          <div class="child-item child-card" style="position: relative; padding-left: 50px;">
            <button onclick="event.stopPropagation(); editChild('${child.id}')" style="position: absolute; top: 15px; left: 15px; background: #4CAF50; color: white; border: none; padding: 8px 12px; border-radius: 8px; cursor: pointer; font-size: 18px; box-shadow: 0 2px 4px rgba(0,0,0,0.2); z-index: 10;">✏️</button>
            <div onclick="showChildPersonalView('${child.id}')" style="cursor: pointer;">
              <strong>${child.name}</strong> (${child.role}, ${child.age} лет)<br>
              Баланс: ${child.balance} ⭐ | На проверке: ${child.pending_balance} ⭐<br>
              Код ребёнка: <code>${child.invite_code}</code>
              ${child.ai_description ? `<div style="margin-top: 10px; padding: 10px; background: #f0f8ff; border-left: 3px solid #4CAF50; border-radius: 4px; font-size: 13px; color: #333;">✨ ${child.ai_description}</div>` : '<div style="margin-top: 8px; color: #999; font-size: 13px; font-style: italic;">✨ AI-профиль не настроен</div>'}
            </div>
          </div>
        `).join('');

      } catch (err) {
        document.getElementById('childrenList').innerHTML = `<p class="error">Ошибка: ${err.message}</p>`;
      }
    }


    // ============================
    // ПЕРСОНАЛЬНАЯ СТРАНИЦА РЕБЁНКА
    // ============================
    

    function showChildPersonalView(childId) {
      selectedChildId = childId;
      
      // Скрываем общий view
      document.getElementById('childrenList').style.display = 'none';
      document.getElementById('pendingTasks').parentElement.style.display = 'none';
      document.getElementById('rewardPurchasesDashboard').style.display = 'none';
      document.getElementById('historyList').parentElement.style.display = 'none';
      document.getElementById('activeDreamsContainer').style.display = 'none';
      
      // Показываем персональный view
      document.getElementById('childPersonalView').style.display = 'block';
      
      loadChildPersonalData(childId);
    }

    function backToChildrenList() {
      selectedChildId = null;
      
      // Показываем общий view
      document.getElementById('childrenList').style.display = 'block';
      document.getElementById('pendingTasks').parentElement.style.display = 'block';
      document.getElementById('rewardPurchasesDashboard').style.display = 'block';
      document.getElementById('historyList').parentElement.style.display = 'block';
      document.getElementById('activeDreamsContainer').style.display = 'block';
      
      // Скрываем персональный view
      document.getElementById('childPersonalView').style.display = 'none';
    }

    async function loadChildPersonalData(childId) {
      try {
        // Загружаем данные ребёнка
        const childRes = await fetch(`${API_URL}/api/children/${childId}`, {
          headers: { 'X-Invite-Code': currentCode }
        });
        
        if (!childRes.ok) throw new Error('Ошибка загрузки данных ребёнка');
        
        const childData = await childRes.json();
        const child = childData.child;
        
        // Отображаем заголовок
        // Отображаем заголовок и карточки
        document.getElementById('childPersonalHeader').innerHTML = `
          <!-- Заголовок ребёнка -->
          <div style="padding: 20px; margin-bottom: 20px;">
            <h2 style="font-family: 'Plus Jakarta Sans', Arial, sans-serif; font-weight: 800; font-size: 24px; letter-spacing: -0.02em; color: #FFFFFF; margin: 0;">
              ${child.name} <span style="color: #666; font-weight: 400; font-size: 16px;">(${child.role}, ${child.age} лет)</span>
            </h2>
            <div style="color: #666; margin-top: 8px; font-size: 14px;">
              Код ребёнка: <span style="font-family: monospace; color: #A78BFA;">${child.invite_code}</span>
            </div>
          </div>
          
          <!-- Баланс -->
          <div style="margin: 20px; padding: 24px; 
                      background: rgba(15, 14, 23, 0.6); 
                      backdrop-filter: blur(20px); 
                      border: 1px solid rgba(167, 139, 250, 0.3); 
                      border-radius: 16px; 
                      box-shadow: inset 0 1px 0 0 rgba(167, 139, 250, 0.1);">
            <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 12px;">
              <span style="font-size: 24px;">💰</span>
              <h3 style="font-family: 'Plus Jakarta Sans', Arial, sans-serif; font-weight: 800; font-size: 14px; text-transform: uppercase; letter-spacing: 0.1em; color: #FFFFFF; margin: 0;">
                Баланс
              </h3>
            </div>
            <div style="font-size: 48px; font-weight: 800; background: linear-gradient(135deg, #4ADE80 0%, #22C55E 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; text-align: center; font-family: 'Plus Jakarta Sans', Arial, sans-serif;">
              ${child.balance} ⭐
            </div>
          </div>
          
          <!-- На проверке -->
          <div style="margin: 20px; padding: 24px; 
                      background: rgba(15, 14, 23, 0.6); 
                      backdrop-filter: blur(20px); 
                      border: 1px solid rgba(251, 191, 36, 0.3); 
                      border-radius: 16px; 
                      box-shadow: inset 0 1px 0 0 rgba(251, 191, 36, 0.1);">
            <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 12px;">
              <span style="font-size: 24px;">⏳</span>
              <h3 style="font-family: 'Plus Jakarta Sans', Arial, sans-serif; font-weight: 800; font-size: 14px; text-transform: uppercase; letter-spacing: 0.1em; color: #FFFFFF; margin: 0;">
                На проверке
              </h3>
            </div>
            <div style="font-size: 48px; font-weight: 800; background: linear-gradient(135deg, #FBBF24 0%, #F59E0B 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; text-align: center; font-family: 'Plus Jakarta Sans', Arial, sans-serif;">
              ${child.pending_balance} ⭐
            </div>
          </div>
        `;
        // Загружаем миссии ребёнка
        await loadChildPersonalTasks(childId);
        
        // Загружаем награды ребёнка
        await loadChildPersonalRewards(childId);
        
        // Загружаем мечту ребёнка
        await loadChildPersonalDream(childId);
        
        // Обновляем pending мечты на главной
        await loadPendingDreams();
        
      } catch (err) {
        alert(`Ошибка: ${err.message}`);
        backToChildrenList();
      }
    }

    async function loadChildPersonalTasks(childId) {
      try {
        const res = await fetch(`${API_URL}/api/tasks/list`, {
          headers: { 'X-Invite-Code': currentCode }
        });
        
        if (!res.ok) throw new Error('Ошибка загрузки миссий');
        
        const data = await res.json();
        const childTasks = (data.tasks || []).filter(t => t.child_id === childId && t.status !== 'ARCHIVED');
        
        const list = document.getElementById('childPersonalTasks');
        
        if (childTasks.length === 0) {
          list.innerHTML = '<div class="empty-state">Нет миссий</div>';
          return;
        }
        
        const idleTasks = childTasks.filter(t => t.status === 'IDLE');
        const waitingTasks = childTasks.filter(t => t.status === 'WAITING');
        
        let html = '';
        
        if (idleTasks.length > 0) {
          html += '<h3>📋 Назначенные миссии</h3>';
          html += idleTasks.map(t => `
            <div class="task-item status-${t.status}">
              <span style="font-size: 24px; margin-right: 10px;">${t.icon}</span>
              <strong>${t.title}</strong><br>
              ${t.description || ''}<br>
              Награда: <strong>${t.reward_amount} ⭐</strong>
            </div>
          `).join('');
        }
        
        if (waitingTasks.length > 0) {
          html += '<h3 style="margin-top: 20px;">⏳ На проверке</h3>';
          html += waitingTasks.map(t => `
            <div class="task-item status-${t.status}">
              <span style="font-size: 24px; margin-right: 10px;">${t.icon}</span>
              <strong>${t.title}</strong><br>
              ${t.description || ''}<br>
              Награда: <strong>${t.reward_amount} ⭐</strong><br>
              <button onclick="handleTaskAction('${t.id}', 'confirm')" style="background: #4CAF50; color: white; margin-top: 10px;">
                ✅ Подтвердить
              </button>
              <button onclick="handleTaskAction('${t.id}', 'reject')" style="background: #f44336; color: white; margin-top: 10px;">
                ❌ Отклонить
              </button>
            </div>
          `).join('');
        }
        
        list.innerHTML = html;
        
      } catch (err) {
        document.getElementById('childPersonalTasks').innerHTML = 
          `<p class="error">Ошибка: ${err.message}</p>`;
      }
    }

    async function loadChildPersonalRewards(childId) {
      try {
        const res = await fetch(`${API_URL}/api/rewards/purchases/family`, {
          headers: { 'X-Invite-Code': currentCode }
        });
        
        if (!res.ok) throw new Error('Ошибка загрузки наград');
        
        const data = await res.json();
        const childRewards = (data.purchases || []).filter(p => p.child_id === childId && p.status === 'pending');
        
        const list = document.getElementById('childPersonalRewards');
        
        if (childRewards.length === 0) {
          list.innerHTML = '<div class="empty-state">Нет купленных наград</div>';
          return;
        }
        
        list.innerHTML = childRewards.map(p => `
          <div style="padding: 15px; margin: 10px 0; border: 2px solid #FF9800; background: #fff8e1; border-radius: 8px;">
            <span style="font-size: 32px; margin-right: 10px;">${p.reward_icon}</span>
            <strong>${p.reward_title}</strong> за <strong>${p.price} ⭐</strong>
            <div style="color: #666; font-size: 14px; margin-top: 5px;">
              ${new Date(p.purchased_at).toLocaleString('ru-RU')}
            </div>
            <div style="color: #FF9800; font-weight: bold; margin-top: 5px;">
              ⏳ Ожидает выдачи
            </div>
          </div>
        `).join('');
        
      } catch (err) {
        document.getElementById('childPersonalRewards').innerHTML = 
          `<p class="error">Ошибка: ${err.message}</p>`;
      }

    // === AI ФУНКЦИИ ДЛЯ ПРОФИЛЯ РЕБЁНКА ===
    
    window.showChildAiQuestionForm = function() {
      document.getElementById('childAiQuestionForm').style.display = 'block';
      document.getElementById('childAiQuestionInput').focus();
    }
    
    window.hideChildAiQuestionForm = function() {
      document.getElementById('childAiQuestionForm').style.display = 'none';
      document.getElementById('childAiQuestionInput').value = '';
    }
    
    function showChildAiResult(title, content) {
      document.getElementById('childAiResultTitle').textContent = title;
      document.getElementById('childAiResultContent').innerHTML = content;
      document.getElementById('childAiResultContainer').style.display = 'block';
    }
    
    function hideChildAiResult() {
      document.getElementById('childAiResultContainer').style.display = 'none';
    }
    
    function copyChildAiResult() {
      const content = document.getElementById('childAiResultContent').innerText;
      navigator.clipboard.writeText(content).then(() => {
        alert('✅ Результат скопирован!');
      }).catch(() => {
        alert('❌ Не удалось скопировать');
      });
    }
    
    window.generateChildAiReport = async function(period) {
      if (!selectedChildId) {
        alert('❌ Ошибка: ребёнок не выбран');
        return;
      }
      
      const title = period === 'week' ? '📊 Отчёт за неделю' : '📈 Отчёт за месяц';
      
      document.getElementById('childAiLoadingIndicator').style.display = 'block';
      showChildAiResult(title, '');
      
      try {
        const res = await fetch(`${API_URL}/api/ai-assistant/generate`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-Invite-Code': currentCode
          },
          body: JSON.stringify({
            type: 'report',
            period: period,
            child_id: selectedChildId
          })
        });
        
        const data = await res.json();
        
        document.getElementById('childAiLoadingIndicator').style.display = 'none';
        
        if (!res.ok) {
          showChildAiResult(title, `❌ Ошибка: ${data.error || 'Неизвестная ошибка'}`);
          return;
        }
        
        showChildAiResult(title, data.result.replace(/\n/g, '<br>'));
        
      } catch (err) {
        document.getElementById('childAiLoadingIndicator').style.display = 'none';
        showChildAiResult(title, `❌ Ошибка: ${err.message}`);
      }
    }
    
    window.generateChildAiIdeas = async function(ideaType) {
      if (!selectedChildId) {
        alert('❌ Ошибка: ребёнок не выбран');
        return;
      }
      
      const title = ideaType === 'rewards' ? '🎁 Идеи наград' : '🎯 Идеи миссий';
      
      document.getElementById('childAiLoadingIndicator').style.display = 'block';
      showChildAiResult(title, '');
      
      try {
        const res = await fetch(`${API_URL}/api/ai-assistant/generate`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-Invite-Code': currentCode
          },
          body: JSON.stringify({
            type: 'ideas',
            ideaType: ideaType,
            child_id: selectedChildId
          })
        });
        
        const data = await res.json();
        
        document.getElementById('childAiLoadingIndicator').style.display = 'none';
        
        if (!res.ok) {
          showChildAiResult(title, `❌ Ошибка: ${data.error || 'Неизвестная ошибка'}`);
          return;
        }
        
        showChildAiResult(title, data.result.replace(/\n/g, '<br>'));
        
      } catch (err) {
        document.getElementById('childAiLoadingIndicator').style.display = 'none';
        showChildAiResult(title, `❌ Ошибка: ${err.message}`);
      }
    }
    
    window.askChildAiQuestion = async function() {
      if (!selectedChildId) {
        alert('❌ Ошибка: ребёнок не выбран');
        return;
      }
      
      const question = document.getElementById('childAiQuestionInput').value.trim();
      
      if (!question) {
        alert('❌ Введите вопрос');
        return;
      }
      
      hideChildAiQuestionForm();
      
      const title = '💬 Ответ на вопрос';
      
      document.getElementById('childAiLoadingIndicator').style.display = 'block';
      showChildAiResult(title, '');
      
      try {
        const res = await fetch(`${API_URL}/api/ai-assistant/generate`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-Invite-Code': currentCode
          },
          body: JSON.stringify({
            type: 'question',
            question: question,
            child_id: selectedChildId
          })
        });
        
        const data = await res.json();
        
        document.getElementById('childAiLoadingIndicator').style.display = 'none';
        
        if (!res.ok) {
          showChildAiResult(title, `❌ Ошибка: ${data.error || 'Неизвестная ошибка'}`);
          return;
        }
        
        showChildAiResult(title, data.result.replace(/\n/g, '<br>'));
        
      } catch (err) {
        document.getElementById('childAiLoadingIndicator').style.display = 'none';
        showChildAiResult(title, `❌ Ошибка: ${err.message}`);
      }
    }

    }



    // ============================
    // МЕЧТЫ ДЕТЕЙ (РОДИТЕЛЬ)
    // ============================

    async function loadPendingDreams() {
      // Проверяем все input'ы с именами dreamGoal_*
      const activeElement = document.activeElement;
      if (activeElement && activeElement.id && activeElement.id.startsWith('dreamGoal_')) {
        console.log('Пропускаем обновление - пользователь вводит сумму');
        return;
      }
      
      try {
        const res = await fetch(`${API_URL}/api/dreams/pending`, {
          headers: { 'X-Invite-Code': currentCode }
        });
        
        if (!res.ok) throw new Error('Ошибка загрузки мечт');
        
        const data = await res.json();
        const dashboard = document.getElementById('pendingDreamsDashboard');
        
        if (!data.dreams || data.dreams.length === 0) {
          dashboard.innerHTML = '';
          return;
        }
        
        const html = `
          <div style="margin: 20px 0;">
            <h3>💭 Мечты детей (ожидают подтверждения)</h3>
            ${data.dreams.map(d => `
              <div class="dream-pending-item">
                <strong>${d.child_name}</strong> создал(а) мечту:
                <div style="font-size: 18px; font-weight: bold; margin: 10px 0;">
                  🎯 "${d.title}"
                </div>
                <div class="dream-goal-form">
                  <label>Цель:</label>
                  <input type="number" id="dreamGoal_${d.id}" class="dream-goal-input" placeholder="Сумма" min="1" max="1000000">
                  <span>⭐</span>
                  <button class="dream-goal-button" onclick="setDreamGoal('${d.id}')">
                    ✅ Установить
                  </button>
                </div>
              </div>
            `).join('')}
          </div>
        `;
        
        dashboard.innerHTML = html;
        
      } catch (err) {
        console.error('Ошибка загрузки pending мечт:', err);
      }
    }

    async function setDreamGoal(dreamId) {
      const input = document.getElementById(`dreamGoal_${dreamId}`);
      const amount = parseInt(input.value);
      
      if (!amount || amount < 1 || amount > 1000000) {
        alert('Введите сумму от 1 до 1000000');
        return;
      }
      
      try {
        const res = await fetch(`${API_URL}/api/dreams/set-goal`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-Invite-Code': currentCode
          },
          body: JSON.stringify({ dream_id: dreamId, target_amount: amount })
        });
        
        if (!res.ok) {
          const err = await res.json();
          alert(`Ошибка: ${err.error}`);
          return;
        }
        
        const data = await res.json();
        
        loadPendingDreams();
        loadActiveDreams();
        
        // Если мы на персональной странице ребёнка - обновляем её
        if (selectedChildId) {
          loadChildPersonalDream(selectedChildId);
        }
        
      } catch (err) {
        alert(`Ошибка: ${err.message}`);
      }
    }


    async function loadActiveDreams() {
      try {
        const res = await fetch(`${API_URL}/api/dreams/active`, {
          headers: { 'X-Invite-Code': currentCode }
        });

        if (!res.ok) throw new Error('Ошибка загрузки мечт');

        const data = await res.json();
        const container = document.getElementById('activeDreamsContainer');

        if (!data.dreams || data.dreams.length === 0) {
          container.innerHTML = '';
          return;
        }

        const html = data.dreams.map(dream => {
          const progress = Math.min(100, Math.round((dream.current_amount / dream.target_amount) * 100));
          return `
            <div style="background: #f0f9ff; padding: 15px; border-radius: 8px; margin-bottom: 10px; border-left: 4px solid #0ea5e9;">
              <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                <h3 style="margin: 0;">🎯 ${dream.child_name}: ${dream.title}</h3>
              </div>
              <div style="background: #e0f2fe; height: 20px; border-radius: 10px; overflow: hidden; margin-bottom: 8px;">
                <div style="background: linear-gradient(90deg, #0ea5e9, #06b6d4); height: 100%; width: ${progress}%; transition: width 0.3s;"></div>
              </div>
              <div style="text-align: center; font-size: 16px; font-weight: bold;">
                ${dream.current_amount} / ${dream.target_amount} ⭐ (${progress}%)
              </div>
            </div>
          `;
        }).join('');

        container.innerHTML = html;

      } catch (err) {
        console.error('Ошибка загрузки активных мечт:', err);
      }
    }


    async function loadChildPersonalDream(childId) {
      try {
        const res = await fetch(`${API_URL}/api/dreams/active`, {
          headers: { 'X-Invite-Code': currentCode }
        });
        
        if (!res.ok) throw new Error('Ошибка загрузки мечт');
        
        const data = await res.json();
        const childDream = (data.dreams || []).find(d => d.child_id === childId);
        
        const container = document.getElementById('childPersonalDream');
        
        if (!childDream) {
          container.innerHTML = '';
          return;
        }
        
        const progress = Math.min(100, Math.round((childDream.current_amount / childDream.target_amount) * 100));
        
        container.innerHTML = `
          <div style="margin: 20px; padding: 24px; 
                      background: rgba(15, 14, 23, 0.6); 
                      backdrop-filter: blur(20px); 
                      border: 1px solid rgba(167, 139, 250, 0.3); 
                      border-radius: 16px; 
                      box-shadow: inset 0 1px 0 0 rgba(167, 139, 250, 0.1);">
            <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 16px;">
              <span style="font-size: 24px;">🎯</span>
              <h3 style="font-family: 'Plus Jakarta Sans', Arial, sans-serif; font-weight: 800; font-size: 14px; text-transform: uppercase; letter-spacing: 0.1em; color: #FFFFFF; margin: 0;">
                Мечта: ${childDream.title}
              </h3>
            </div>
            
            <!-- Прогресс-бар -->
            <div style="width: 100%; height: 16px; background: rgba(0, 0, 0, 0.4); border-radius: 999px; overflow: hidden; margin-bottom: 16px;">
              <div style="width: ${progress}%; height: 100%; background: linear-gradient(90deg, #A78BFA 0%, #818CF8 100%); border-radius: 999px; transition: width 0.5s cubic-bezier(0.4, 0, 0.2, 1);"></div>
            </div>
            
            <!-- Цифры -->
            <div style="text-align: center; font-size: 24px; font-weight: 800; color: #FFFFFF; font-family: 'Plus Jakarta Sans', Arial, sans-serif;">
              ${childDream.current_amount} / ${childDream.target_amount} ⭐
            </div>
            <div style="text-align: center; color: #A78BFA; margin-top: 8px; font-size: 14px; font-weight: 600;">
              Прогресс: ${progress}%
            </div>
          </div>
        `;
      } catch (err) {
        console.error('Ошибка загрузки мечты ребёнка:', err);
      }
    }


    // Загрузка купленных наград детей
    async function loadPendingRewardPurchases() {
      try {
        const res = await fetch(`${API_URL}/api/rewards/purchases/family`, {
          headers: { 'X-Invite-Code': currentCode }
        });
        
        if (!res.ok) throw new Error('Ошибка загрузки покупок');
        
        const data = await res.json();
        const dashboard = document.getElementById('rewardPurchasesDashboard');
        
        if (!data.purchases || data.purchases.length === 0) {
          dashboard.innerHTML = '';
          return;
        }
        
        const html = `
          <div style="margin: 20px 0;">
            <h3>🎁 Покупки детей</h3>
            ${data.purchases.map(p => `
              <div style="padding: 15px; margin: 10px 0; border: 2px solid #FF9800; background: #fff8e1; border-radius: 8px;">
                <span style="font-size: 32px; margin-right: 10px;">${p.reward_icon}</span>
                <strong>${p.child_name}</strong> купил(а):
                <strong>${p.reward_title}</strong> за <strong>${p.price} ⭐</strong>
                <div style="color: #666; font-size: 14px; margin-top: 5px;">
                  ${new Date(p.purchased_at).toLocaleString('ru-RU')}
                </div>
                <div style="color: #FF9800; font-weight: bold; margin-top: 5px;">
                  ⏳ Ожидает выдачи
                </div>
              </div>
            `).join('')}
          </div>
        `;
        
        dashboard.innerHTML = html;
        
      } catch (err) {
        console.error('Ошибка загрузки покупок:', err);
      }
    }

    async function loadPendingTasks() {
      try {
        const res = await fetch(`${API_URL}/api/tasks/list`, {
          headers: { 'X-Invite-Code': currentCode }
        });

        const data = await res.json();
        
        if (!Array.isArray(data.tasks)) {
          document.getElementById('pendingTasks').innerHTML = '<p class="error">Ошибка загрузки задач</p>';
          return;
        }

        const pending = data.tasks.filter(t => t.status === 'WAITING');

        if (pending.length === 0) {
          document.getElementById('pendingTasks').innerHTML = '<p>Нет задач на проверке</p>';
          return;
        }

        document.getElementById('pendingTasks').innerHTML = pending.map(task => `
          <div class="task-item">
            <strong>${task.title}</strong> — ${task.reward_amount} ⭐<br>
            ${task.description || ''}<br>
            <button onclick="confirmTask('${task.id}', 'confirm')">✅ Подтвердить</button>
            <button onclick="confirmTask('${task.id}', 'reject')">❌ Отклонить</button>
          </div>
        `).join('');



      } catch (err) {
        document.getElementById('pendingTasks').innerHTML = `<p class="error">Ошибка: ${err.message}</p>`;
      }
    }

    async function confirmTask(taskId, action) {
      try {
        const res = await fetch(`${API_URL}/api/tasks/confirm`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-Invite-Code': currentCode
          },
          body: JSON.stringify({ task_id: taskId, action })
        });

        const data = await res.json();
        
        
        loadPendingTasks();
        loadPendingRewardPurchases();
        loadHistory();
        loadChildren();
        renderTopBar();

      } catch (err) {
        alert('Ошибка: ' + err.message);
      }
    }

    setInterval(() => {
      if (currentCode) {
        loadPendingTasks();
        loadPendingRewardPurchases();
        loadPendingDreams();
        loadHistory();
        loadChildren();
        renderTopBar();
      }
    }, 5000);

    // ============================
    // МАГАЗИН НАГРАД
    // ============================

    function toggleAddRewardForm() {
      const form = document.getElementById('addRewardForm');
      form.style.display = form.style.display === 'block' ? 'none' : 'block';
      if (form.style.display === 'block') {
        document.getElementById('rewardTitle').value = '';
        document.getElementById('rewardDescription').value = '';
        document.getElementById('rewardPrice').value = '';
        document.getElementById('rewardIsPermanent').checked = false;
      }
    }

    async function loadRewards() {
      try {
        const res = await fetch(`${API_URL}/api/rewards/list`, {
          headers: { 'X-Invite-Code': currentCode }
        });
        const data = await res.json();
        if (!Array.isArray(data.rewards)) {
          document.getElementById('rewardsList').innerHTML = '<p class="error">Ошибка загрузки наград</p>';
          return;
        }
        const rewardsList = document.getElementById('rewardsList');
        if (data.rewards.length === 0) {
          rewardsList.innerHTML = '<div class="empty-state">Наград пока нет. Нажмите \'+\' чтобы добавить.</div>';
          return;
        }
        rewardsList.innerHTML = data.rewards.map(reward => `
          <div class="task-item" style="position: relative;">
            <button class="delete-button" onclick="deleteReward('${reward.id}')">✕</button>
            <div style="display: flex; align-items: center; gap: 10px;">
              <span style="font-size: 32px;">${reward.icon || '🎁'}</span>
              <div style="flex: 1;">
                <strong>${reward.title}</strong>
                <div style="font-size: 14px; color: #666;">${reward.description || ''}</div>
                <div style="margin-top: 5px;">
                  <span style="font-weight: bold; color: #4CAF50;">${reward.price} ⭐</span>
                  ${reward.is_permanent ? '<span style="margin-left: 10px; font-size: 12px; color: #999;">📌 Постоянный</span>' : '<span style="margin-left: 10px; font-size: 12px; color: #999;">🔄 Разовый</span>'}
                </div>
              </div>
            </div>
          </div>
        `).join('');
      } catch (err) {
        document.getElementById('rewardsList').innerHTML = `<p class="error">Ошибка: ${err.message}</p>`;
      }
    }

    async function createReward() {
      const title = document.getElementById('rewardTitle').value.trim();
      const description = document.getElementById('rewardDescription').value.trim();
      const price = parseInt(document.getElementById('rewardPrice').value);
      const isPermanent = document.getElementById('rewardIsPermanent').checked;
      if (!title) {
        alert('Введите название награды');
        return;
      }
      if (!price || price < 1 || price > 10000) {
        alert('Цена должна быть от 1 до 10000');
        return;
      }
      try {
        const res = await fetch(`${API_URL}/api/rewards/create`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-Invite-Code': currentCode
          },
          body: JSON.stringify({ title, description, price, is_permanent: isPermanent, child_id: selectedChildId })
        });
        const data = await res.json();
        if (data.error) {
          alert('Ошибка: ' + data.error);
          return;
        }
        toggleAddRewardForm();
        // Перезагружаем награды для выбранного ребёнка
        if (selectedChildId) {
          loadFilteredRewards(selectedChildId);
        } else {
          loadRewards();
        }
      } catch (err) {
        alert('Ошибка создания награды: ' + err.message);
      }
    }


    // 🎯 ФИЛЬТРАЦИЯ НАГРАД ПО РЕБЁНКУ
    async function loadFilteredRewards(childId) {
      try {
        const res = await fetch(`${API_URL}/api/rewards/list`, {
          headers: { 'X-Invite-Code': currentCode }
        });
        const data = await res.json();
        if (!Array.isArray(data.rewards)) {
          document.getElementById('rewardsList').innerHTML = '<p class="error">Ошибка загрузки наград</p>';
          return;
        }
        
        // Фильтруем награды по ребёнку
        const childRewards = data.rewards.filter(r => r.child_id === childId);
        
        const rewardsList = document.getElementById('rewardsList');
        if (childRewards.length === 0) {
          rewardsList.innerHTML = '<div class="empty-state">У этого ребёнка пока нет наград.</div>';
          return;
        }
        
        rewardsList.innerHTML = childRewards.map(reward => `
          <div class="task-item" style="position: relative;">
            <button class="delete-button" onclick="deleteReward('${reward.id}')">✕</button>
            <div style="display: flex; align-items: center; gap: 10px;">
              <span style="font-size: 32px;">${reward.icon || '🎁'}</span>
              <div style="flex: 1;">
                <strong>${reward.title}</strong>
                <div style="font-size: 14px; color: #666;">${reward.description || ''}</div>
                <div style="margin-top: 5px;">
                  <span style="font-weight: bold; color: #4CAF50;">${reward.price} ⭐</span>
                  ${reward.is_permanent ? '<span style="margin-left: 10px; font-size: 12px; color: #999;">📌 Постоянный</span>' : '<span style="margin-left: 10px; font-size: 12px; color: #999;">🔄 Разовый</span>'}
                </div>
              </div>
            </div>
          </div>
        `).join('');
      } catch (err) {
        document.getElementById('rewardsList').innerHTML = `<p class="error">Ошибка: ${err.message}</p>`;
      }
    }

    // Загрузка профиля ребёнка
    async function loadChildProfile(childId) {
      try {
        // Найти данные ребёнка
        const child = childrenData.find(c => c.id === childId);
        if (!child) return;
        
        // Загрузить данные профиля
        const res = await fetch(`${API_URL}/api/auth/whoami?child_id=${childId}`, {
          headers: { 'X-Invite-Code': currentCode }
        });
        if (!res.ok) throw new Error('Ошибка загрузки профиля');
        const data = await res.json();
        
        // Получить награды
        const rewardsRes = await fetch(`${API_URL}/api/rewards/received?child_id=${childId}`, {
          headers: { 'X-Invite-Code': child.invite_code }
        });
        const rewardsData = await rewardsRes.json();
        
        // Получить миссии
        const tasksRes = await fetch(`${API_URL}/api/tasks/list?child_id=${childId}`, {
          headers: { 'X-Invite-Code': child.invite_code }
        });
        const tasksData = await tasksRes.json();
        
        // Обновить UI
        document.getElementById('profileName').textContent = data.name || child.name || 'Ребёнок';
        document.getElementById('profileBalance').textContent = child.balance || 0;
        document.getElementById('profileMissionsCount').textContent = 
          (tasksData.tasks || []).filter(t => t.status === 'CONFIRMED').length;
        document.getElementById('profileRewardsCount').textContent = rewardsData.count || 0;
        document.getElementById('profileChildCode').textContent = child.invite_code || 'Код не найден';
        document.getElementById('profileTotalEarned').textContent = (tasksData.tasks || []).filter(t => t.status === 'CONFIRMED').reduce((sum, t) => sum + (t.reward_amount || 0), 0);
        
        // Обновить прогресс-бар и уровень
        const missionsCount = (tasksData.tasks || []).filter(t => t.status === 'CONFIRMED').length;
        const levels = [
          { name: 'Новичок', icon: '❤️', min: 0, max: 24, next: 'Опытного' },
          { name: 'Опытный', icon: '💎', min: 25, max: 49, next: 'Мастера' },
          { name: 'Мастер', icon: '🏔️', min: 50, max: 74, next: 'Эксперта' },
          { name: 'Эксперт', icon: '🌟', min: 75, max: 99, next: 'Легенды' },
          { name: 'Легенда', icon: '🚀', min: 100, max: Infinity, next: null }
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
        
        // Обновить прозрачность маркеров уровней
        document.getElementById('marker0').style.opacity = missionsCount >= 0 ? '1' : '0.3';
        document.getElementById('marker25').style.opacity = missionsCount >= 25 ? '1' : '0.3';
        document.getElementById('marker50').style.opacity = missionsCount >= 50 ? '1' : '0.3';
        document.getElementById('marker75').style.opacity = missionsCount >= 75 ? '1' : '0.3';
        document.getElementById('marker100').style.opacity = missionsCount >= 100 ? '1' : '0.3';
        
        document.getElementById('profileProgressNext').textContent = 
          currentLevel.next 
            ? `До ${currentLevel.next}: ${remaining} миссий` 
            : 'Максимальный уровень!';
      } catch (e) {
        console.error('Ошибка загрузки профиля:', e);
      }
    }
    async function deleteReward(rewardId) {
      if (!confirm('Удалить эту награду?')) return;
      try {
        const res = await fetch(`${API_URL}/api/rewards/delete`, {
          method: 'DELETE',
          headers: {
            'Content-Type': 'application/json',
            'X-Invite-Code': currentCode
          },
          body: JSON.stringify({ reward_id: rewardId })
        });
        const data = await res.json();
        if (data.error) {
          alert('Ошибка: ' + data.error);
          return;
        }
        loadRewards();
      } catch (err) {
        alert('Ошибка удаления награды: ' + err.message);
      }
    }

  
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
              <div style="font-size: 11px; color: #888;">${ref.used_by_family_id ? '✅ Использован: ' + (ref.used_by_name || 'Другая семья') : '🔓 Доступен'}</div>
              <div class="ref-code">${ref.invite_code}</div>
              ${ref.used_by_family_id ? '' : '<button class="copy-btn" onclick="copyText(\''+ref.invite_code+'\')">Копировать</button>'}
            </div>
          `).join('');
        }
      } catch (e) { container.innerHTML = 'Ошибка загрузки'; }
    }

    function copyText(text) {
      navigator.clipboard.writeText(text);
      alert('Код скопирован!');
    }

    // ============================
    // AI ПОМОЩНИК
    // ============================

    function showAiQuestionForm() {
      document.getElementById('aiQuestionForm').style.display = 'block';
      document.getElementById('aiQuestionInput').focus();
    }

    function hideAiQuestionForm() {
      document.getElementById('aiQuestionForm').style.display = 'none';
      document.getElementById('aiQuestionInput').value = '';
    }

    function showAiResult(title) {
      document.getElementById('aiResultTitle').textContent = title;
      document.getElementById('aiResultContainer').style.display = 'block';
      document.getElementById('aiLoadingIndicator').style.display = 'block';
      document.getElementById('aiResultContent').style.display = 'none';
    }

    function hideAiResult() {
      document.getElementById('aiResultContainer').style.display = 'none';
    }

    async function generateAiReport(period) {
      const title = period === 'week' ? '📊 Отчёт за неделю' : '📈 Отчёт за месяц';
      showAiResult(title);

      try {
        const res = await fetch(`${API_URL}/api/ai-assistant/generate`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-Invite-Code': currentCode
          },
          body: JSON.stringify({ type: 'report', period: period })
        });

        const data = await res.json();
        if (!res.ok) throw new Error(data.error || 'Ошибка генерации');

        document.getElementById('aiLoadingIndicator').style.display = 'none';
        document.getElementById('aiResultContent').style.display = 'block';
        document.getElementById('aiResultContent').textContent = data.result;
      } catch (err) {
        document.getElementById('aiLoadingIndicator').style.display = 'none';
        document.getElementById('aiResultContent').style.display = 'block';
        document.getElementById('aiResultContent').textContent = '❌ Ошибка: ' + err.message;
      }
    }

    async function generateAiIdeas(ideaType) {
      const title = ideaType === 'rewards' ? '🎁 Идеи наград' : '🎯 Идеи миссий';
      showAiResult(title);

      try {
        const res = await fetch(`${API_URL}/api/ai-assistant/generate`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-Invite-Code': currentCode
          },
          body: JSON.stringify({ type: 'ideas', ideaType: ideaType })
        });

        const data = await res.json();
        if (!res.ok) throw new Error(data.error || 'Ошибка генерации');

        document.getElementById('aiLoadingIndicator').style.display = 'none';
        document.getElementById('aiResultContent').style.display = 'block';
        document.getElementById('aiResultContent').textContent = data.result;
      } catch (err) {
        document.getElementById('aiLoadingIndicator').style.display = 'none';
        document.getElementById('aiResultContent').style.display = 'block';
        document.getElementById('aiResultContent').textContent = '❌ Ошибка: ' + err.message;
      }
    }

    async function askAiQuestion() {
      const question = document.getElementById('aiQuestionInput').value.trim();
      if (!question) { alert('Введите вопрос'); return; }

      hideAiQuestionForm();
      showAiResult('💬 Ответ на вопрос');

      try {
        const res = await fetch(`${API_URL}/api/ai-assistant/generate`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-Invite-Code': currentCode
          },
          body: JSON.stringify({ type: 'question', question: question })
        });

        const data = await res.json();
        if (!res.ok) throw new Error(data.error || 'Ошибка генерации');

        document.getElementById('aiLoadingIndicator').style.display = 'none';
        document.getElementById('aiResultContent').style.display = 'block';
        document.getElementById('aiResultContent').textContent = data.result;
      } catch (err) {
        document.getElementById('aiLoadingIndicator').style.display = 'none';
        document.getElementById('aiResultContent').style.display = 'block';
        document.getElementById('aiResultContent').textContent = '❌ Ошибка: ' + err.message;
      }
    }



// ========================================
// ВТОРОЙ БЛОК СКРИПТОВ
// ========================================

    // Открыть модальное окно настроек
    function openSettingsModal() {
      document.getElementById('settingsModal').style.display = 'block';
      loadReferralsModal();
    }

    // Закрыть модальное окно настроек
    function closeSettingsModal() {
      document.getElementById('settingsModal').style.display = 'none';
    }

    // Загрузить коды в модальное окно
    async function loadReferralsModal() {
      const container = document.getElementById('referralsModalList');
      
      try {
        const res = await fetch(`${API_URL}/api/referrals/my`, {
          headers: { 'X-Invite-Code': currentCode }
        });

        if (!res.ok) throw new Error('Ошибка загрузки кодов');

        const data = await res.json();
        const referrals = data.referrals || [];

        if (referrals.length === 0) {
          container.innerHTML = '<p style="text-align: center; color: #999;">Нет доступных кодов приглашения</p>';
          return;
        }

        container.innerHTML = referrals.map(ref => `
          <div style="background: #f9f9f9; border: 1px solid #ddd; border-radius: 12px; padding: 15px; margin-bottom: 15px;">
            <div style="display: flex; align-items: center; gap: 15px;">
              <div style="width: 50px; height: 50px; border-radius: 50%; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); display: flex; align-items: center; justify-content: center; font-size: 24px;">👥</div>
              <div style="flex: 1;">
                <strong>${ref.used_by_name || 'Не активирован'}</strong><br>
                <code style="font-family: monospace; font-size: 16px; color: #24a1de; font-weight: bold;">${ref.invite_code}</code>
                ${ref.used_by_name ? '<br><span style="color: #4CAF50; font-size: 12px;">✅ Активирован</span>' : '<br><span style="color: #999; font-size: 12px;">⏳ Ожидает активации</span>'}
              </div>
              <div style="display: flex; gap: 10px;">
                <button onclick="copyToClipboard('${ref.invite_code}')" style="background: none; border: none; font-size: 24px; cursor: pointer;" title="Копировать">📋</button>
                <button onclick="shareCode('${ref.invite_code}', 'Family Wallet')" style="background: none; border: none; font-size: 24px; cursor: pointer;" title="Поделиться">🔗</button>
              </div>
            </div>
          </div>
        `).join('');

      } catch (err) {
        container.innerHTML = `<p style="color: red;">Ошибка: ${err.message}</p>`;
      }
    }

    // Копировать в буфер обмена
    function copyToClipboard(text) {
      navigator.clipboard.writeText(text).then(() => {
        alert('✅ Код скопирован: ' + text);
      }).catch(err => {
        alert('❌ Ошибка копирования: ' + err);
      });
    }

    // Поделиться кодом
    function shareCode(code, name) {
      if (navigator.share) {
        navigator.share({
          title: `Family Wallet — Код для ${name}`,
          text: `Присоединяйся к Family Wallet как ${name}! Код: ${code}`,
          url: window.location.href
        }).catch(err => console.log('Ошибка sharing:', err));
      } else {
        copyToClipboard(code);
        alert(`Код для ${name} скопирован! Поделись им с семьёй.`);
      }
    }

    // Удалить профиль родителя
    function deleteParentProfile() {
      if (confirm('⚠️ Вы уверены? Это удалит ВСЮ семью, всех детей, миссии и награды!')) {
        if (confirm('⚠️ ПОСЛЕДНЕЕ ПРЕДУПРЕЖДЕНИЕ! Отменить это действие будет НЕВОЗМОЖНО!')) {
          alert('🚧 Функция удаления профиля будет реализована позже');
        }
      }
    }

// ========================================
// CHILD BOTTOM NAVIGATION (ДИНАМИЧЕСКОЕ СОЗДАНИЕ)
// ========================================

function createChildBottomNavigation() {
  // Проверяем, не создана ли уже навигация
  if (document.getElementById('childBottomNavigation')) return;
  
  const navHTML = `
    <div id="childBottomNavigation">
      <button class="child-nav-btn active" data-tab="home" onclick="showChildTab('home')">
        <span style="font-size: 20px;">🏠</span>
        <span>ГЛАВНАЯ</span>
      </button>
      <button class="child-nav-btn" data-tab="missions" onclick="showChildTab('missions')">
        <span style="font-size: 20px;">🎯</span>
        <span>МИССИИ</span>
      </button>
      <button class="child-nav-btn" data-tab="shop" onclick="showChildTab('shop')">
        <span style="font-size: 20px;">🛍️</span>
        <span>МАГАЗИН</span>
      </button>
      <button class="child-nav-btn" data-tab="ai" onclick="showChildTab('ai')">
        <span style="font-size: 20px;">🤖</span>
        <span>ИИ</span>
      </button>
    </div>
  `;
  
  document.body.insertAdjacentHTML('beforeend', navHTML);
}

// Вызываем создание навигации при загрузке страницы
window.addEventListener('DOMContentLoaded', createChildBottomNavigation);


// ========================================
// ПОДТВЕРЖДЕНИЕ/ОТКЛОНЕНИЕ ЗАДАЧ (ДЛЯ РОДИТЕЛЯ)
// ========================================

async function handleTaskAction(taskId, action) {
  try {
    const endpoint = action === 'confirm' 
      ? `${API_URL}/api/tasks/${taskId}/confirm`
      : `${API_URL}/api/tasks/${taskId}/reject`;
    
    const res = await fetch(endpoint, {
      method: 'POST',
      headers: { 'X-Invite-Code': currentCode }
    });
    
    if (!res.ok) {
      const err = await res.json();
      alert('Ошибка: ' + (err.error || 'Неизвестная ошибка'));
      return;
    }
    
    const data = await res.json();
    alert(data.message || (action === 'confirm' ? '✅ Задача подтверждена!' : '❌ Задача отклонена'));
    
    // Перезагружаем данные ребёнка
    if (selectedChildId) {
      await loadChildren();
      renderTopBar();
      loadChildPersonalData(selectedChildId);
    }
    
  } catch (err) {
    alert('Ошибка сети: ' + err.message);
  }
}


// ========================================
// ПЕРЕКЛЮЧЕНИЕ ВКЛАДОК CHILD BOTTOM NAVIGATION
// ========================================

function showChildTab(tabId) {
  // Переключаем активную кнопку
  document.querySelectorAll('.child-nav-btn').forEach(btn => btn.classList.remove('active'));
  const targetBtn = document.querySelector(`[data-tab="${tabId}"]`);
  if (targetBtn) targetBtn.classList.add('active');
  
  // Логика показа контента (пока заглушка)
  console.log('Child tab:', tabId);
  
  // TODO: показывать/скрывать секции профиля ребёнка
}

