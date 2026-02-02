// ============================
// FAMILY WALLET — WORKER API
// Cloudflare Worker для мультисемейной архитектуры
// ============================

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const path = url.pathname;

    // CORS headers
    const corsHeaders = {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type, X-Invite-Code',
    };

    // OPTIONS preflight
    if (request.method === 'OPTIONS') {
      return new Response(null, { headers: corsHeaders });
    }

    // Helper: JSON response
    const json = (data, status = 200) => {
      return new Response(JSON.stringify(data), {
        status,
        headers: { 'Content-Type': 'application/json', ...corsHeaders },
      });
    };

    // Helper: Error response
    const error = (message, code = 'ERROR', status = 400) => {
      return json({ error: message, code }, status);
    };

    try {
      // ============================
      // AUTH: Идентификация пользователя
      // ============================
      
      // GET /api/auth/whoami
      if (path === '/api/auth/whoami' && request.method === 'GET') {
        const inviteCode = request.headers.get('X-Invite-Code');
        
        if (!inviteCode) {
          return error('Отсутствует заголовок X-Invite-Code', 'NO_AUTH', 401);
        }

        // Проверяем родителя
        const family = await env.DB.prepare(
          'SELECT id, name, currency_name, currency_symbol FROM families WHERE invite_code = ?'
        ).bind(inviteCode).first();

        if (family) {
          return json({
            role: 'parent',
            family_id: family.id,
            family_name: family.name,
            currency: {
              name: family.currency_name,
              symbol: family.currency_symbol
            }
          });
        }

        // Проверяем ребёнка
        const child = await env.DB.prepare(
          'SELECT c.id, c.family_id, c.name, c.role, c.age, c.balance, c.pending_balance, f.currency_name, f.currency_symbol FROM children c JOIN families f ON c.family_id = f.id WHERE c.invite_code = ?'
        ).bind(inviteCode).first();

        if (child) {
          return json({
            role: 'child',
            family_id: child.family_id,
            child_id: child.id,
            name: child.name,
            age: child.age,
            balance: child.balance,
            pending_balance: child.pending_balance,
            currency: {
              name: child.currency_name,
              symbol: child.currency_symbol
            }
          });
        }

        return error('Неверный код приглашения', 'INVALID_CODE', 403);
      }

      // ============================
      // TASKS: Задачи
      // ============================

      // GET /api/tasks/list
      if (path === '/api/tasks/list' && request.method === 'GET') {
        const inviteCode = request.headers.get('X-Invite-Code');
        if (!inviteCode) return error('Требуется авторизация', 'NO_AUTH', 401);

        // Определяем роль
        const child = await env.DB.prepare(
          'SELECT id, family_id FROM children WHERE invite_code = ?'
        ).bind(inviteCode).first();

        const family = await env.DB.prepare(
          'SELECT id FROM families WHERE invite_code = ?'
        ).bind(inviteCode).first();

        let query;
        if (child) {
          // Ребёнок видит только свои задачи
          query = env.DB.prepare(
            "SELECT t.*, c.name AS child_name FROM tasks t LEFT JOIN children c ON c.id = t.child_id WHERE t.family_id = ? AND (t.child_id = ? OR t.child_id IS NULL) AND t.status != 'ARCHIVED' ORDER BY t.created_at DESC"
          ).bind(child.family_id, child.id);
        } else if (family) {
          // Родитель видит все задачи семьи
          query = env.DB.prepare(
            "SELECT t.*, c.name AS child_name FROM tasks t LEFT JOIN children c ON c.id = t.child_id WHERE t.family_id = ? AND t.status != 'ARCHIVED' ORDER BY t.created_at DESC"
          ).bind(family.id);
        } else {
          return error('Неверный код доступа', 'INVALID_CODE', 403);
        }

        const result = await query.all();
        return json({ tasks: result.results || [] });
      }


      // POST /api/magic/generate — генерация аватара через AI
      if (path === '/api/magic/generate' && request.method === 'POST') {
        const inviteCode = request.headers.get('X-Invite-Code');
        
        if (!inviteCode) {
          return error('Отсутствует заголовок X-Invite-Code', 'NO_AUTH', 401);
        }

        // Проверяем ребёнка
        const child = await env.DB.prepare(
          'SELECT c.id, c.name FROM children c WHERE c.invite_code = ?'
        ).bind(inviteCode).first();

        if (!child) {
          return error('Недействительный код', 'FORBIDDEN', 403);
        }

        const body = await request.json();
        const { world, photo } = body;

        if (!world) {
          return error('Не указан игровой мир', 'BAD_REQUEST', 400);
        }

        // Промпты для разных миров
        const prompts = {
          roblox: 'A cute kid character avatar in Roblox style, blocky 3D, colorful, simple shapes, friendly smile, standing pose, white background',
          ghibli: 'A beautiful kid character in Studio Ghibli anime style, hand-drawn animation, soft colors, gentle expression, magical atmosphere, watercolor background',
          anime: 'A cheerful kid character in modern anime style, big expressive eyes, colorful hair, dynamic pose, vibrant colors, clean background',
          minecraft: 'A kid character in Minecraft style, pixelated blocky design, cubic shapes, textured blocks, simple colors, standing on grass block'
        };

        const prompt = prompts[world] || prompts.roblox;

        try {
          // Генерация через Cloudflare AI (правильный формат)
          const inputs = {
            prompt: prompt,
            num_steps: 20
          };

          // Если загружено фото - добавляем в inputs для image-to-image
          if (photo) {
            // photo в формате data:image/...;base64,xxxxx
            // Извлекаем base64 часть и конвертируем в Uint8Array
            const base64Data = photo.split(',')[1]; // Убираем data:image/...;base64,
            const binaryString = atob(base64Data);
            const bytes = new Uint8Array(binaryString.length);
            for (let i = 0; i < binaryString.length; i++) {
              bytes[i] = binaryString.charCodeAt(i);
            }
            inputs.image = Array.from(bytes); // Cloudflare AI ожидает массив
          }

          // Выбираем модель в зависимости от наличия фото
          const model = photo 
            ? '@cf/runwayml/stable-diffusion-v1-5-img2img'  // image-to-image
            : '@cf/stabilityai/stable-diffusion-xl-base-1.0'; // text-to-image
          
          const aiResult = await env.AI.run(model, inputs);

          // Cloudflare AI возвращает ReadableStream - нужно прочитать
          let imageBlob;
          
          if (aiResult instanceof ReadableStream) {
            // Читаем stream
            const reader = aiResult.getReader();
            const chunks = [];
            
            while (true) {
              const { done, value } = await reader.read();
              if (done) break;
              chunks.push(value);
            }
            
            // Объединяем все чанки в один ArrayBuffer
            const totalLength = chunks.reduce((acc, chunk) => acc + chunk.length, 0);
            imageBlob = new Uint8Array(totalLength);
            let offset = 0;
            for (const chunk of chunks) {
              imageBlob.set(chunk, offset);
              offset += chunk.length;
            }
          } else {
            // Fallback если вдруг вернулся ArrayBuffer напрямую
            imageBlob = new Uint8Array(aiResult);
          }
          
          // Конвертируем ArrayBuffer в base64
          const uint8Array = new Uint8Array(imageBlob);
          let binaryString = '';
          const chunkSize = 8192;
          
          for (let i = 0; i < uint8Array.length; i += chunkSize) {
            const chunk = uint8Array.subarray(i, Math.min(i + chunkSize, uint8Array.length));
            binaryString += String.fromCharCode.apply(null, Array.from(chunk));
          }
          
          const base64Image = btoa(binaryString);

          // Проверка, что base64 не пустой
          if (base64Image.length < 100) {
            throw new Error('Generated image is empty or corrupted');
          }

          return json({
            success: true,
            image_url: `data:image/png;base64,${base64Image}`,
            world: world,
            child_name: child.name
          });

        } catch (aiError) {
          console.error('AI Generation Error:', aiError);
          return error('Ошибка генерации изображения: ' + aiError.message, 'AI_ERROR', 500);
        }
      }


      // POST /api/ai-assistant/generate
      if (path === '/api/ai-assistant/generate' && request.method === 'POST') {
        const inviteCode = request.headers.get('X-Invite-Code');
        if (!inviteCode) return error('Требуется авторизация', 'NO_AUTH', 401);

        const family = await env.DB.prepare('SELECT id, name FROM families WHERE invite_code = ?').bind(inviteCode).first();
        if (!family) return error('Только родители могут использовать AI помощник', 'FORBIDDEN', 403);

        const body = await request.json();
        const { type, period, ideaType, question, child_id } = body;

        try {
          const children = child_id 
            ? await env.DB.prepare('SELECT id, name, age, role, balance, ai_description FROM children WHERE family_id = ? AND id = ?').bind(family.id, child_id).all()
            : await env.DB.prepare('SELECT id, name, age, role, balance, ai_description FROM children WHERE family_id = ?').bind(family.id).all();
          const tasks = child_id
            ? await env.DB.prepare('SELECT * FROM tasks WHERE family_id = ? AND child_id = ? AND created_at >= datetime("now", "-30 days")').bind(family.id, child_id).all()
            : await env.DB.prepare('SELECT * FROM tasks WHERE family_id = ? AND created_at >= datetime("now", "-30 days")').bind(family.id).all();

          let context = `Семья: ${family.name}\nДети:\n`;
          children.results.forEach(child => {
            context += `- ${child.name} (${child.role}, ${child.age} лет, баланс: ${child.balance})\n`;
            if (child.ai_description) context += `  Описание: ${child.ai_description}\n`;
          });
          context += `\nМиссий за месяц: ${tasks.results.length}, выполнено: ${tasks.results.filter(t => t.status === 'CONFIRMED').length}\n`;

          let prompt = '';
          if (type === 'report') {
            prompt = `Создай отчёт за ${period === 'week' ? 'неделю' : 'месяц'}.\n${context}\nВключи активность детей, прогресс, рекомендации.`;
          } else if (type === 'ideas') {
            prompt = ideaType === 'rewards' 
              ? `Предложи 8 идей наград для детей.\n${context}\nУчитывай возраст, интересы, разные цены.`
              : `Предложи 8 идей миссий для детей.\n${context}\nУчитывай возраст, интересы, разную сложность.`;
          } else if (type === 'question') {
            prompt = `Ответь на вопрос родителя.\n${context}\nВопрос: ${question}`;
          }

          const response = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key=${env.GEMINI_API_KEY}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ contents: [{ parts: [{ text: prompt }] }] })
          });

          const aiData = await response.json();
          
          // Логирование ответа для отладки
          console.log('Gemini API response:', JSON.stringify(aiData));
          
          // Проверка структуры ответа
          if (!aiData.candidates || !aiData.candidates[0]) {
            console.error('Invalid Gemini response:', aiData);
            return error('Некорректный ответ от AI: ' + JSON.stringify(aiData), 'AI_INVALID_RESPONSE', 500);
          }
          
          const result = aiData.candidates[0].content.parts[0].text;
          return json({ result });

        } catch (aiError) {
          return error('Ошибка AI: ' + aiError.message, 'AI_ERROR', 500);
        }
      }

      // POST /api/tasks/complete
      if (path === '/api/tasks/complete' && request.method === 'POST') {
        const inviteCode = request.headers.get('X-Invite-Code');
        if (!inviteCode) return error('Требуется авторизация', 'NO_AUTH', 401);

        const body = await request.json();
        const { task_id } = body;

        if (!task_id) return error('Отсутствует task_id', 'INVALID_INPUT');

        // Проверяем ребёнка
        const child = await env.DB.prepare(
          'SELECT id, family_id, balance, pending_balance FROM children WHERE invite_code = ?'
        ).bind(inviteCode).first();

        if (!child) {
          return error('Только дети могут выполнять задачи', 'FORBIDDEN', 403);
        }

        // Проверяем задачу (идемпотентность + проверка что задача для этого ребёнка)
        const task = await env.DB.prepare(
          'SELECT * FROM tasks WHERE id = ? AND family_id = ? AND (child_id = ? OR child_id IS NULL)'
        ).bind(task_id, child.family_id, child.id).first();

        if (!task) {
          return error('Задача не найдена', 'NOT_FOUND', 404);
        }

        if (task.status === 'WAITING') {
          // Уже отправлена на проверку
          return json({ message: 'Задача уже отправлена на проверку', status: 'PENDING' });
        }

        if (task.status === 'CONFIRMED') {
          // Уже подтверждена
          return json({ message: 'Задача уже выполнена', status: 'CONFIRMED' });
        }

        // Обновляем статус задачи + pending_balance ребёнка
        await env.DB.prepare(
          "UPDATE tasks SET status = 'WAITING', updated_at = CURRENT_TIMESTAMP WHERE id = ?"
        ).bind(task_id).run();

        await env.DB.prepare(
          'UPDATE children SET pending_balance = pending_balance + ? WHERE id = ?'
        ).bind(task.reward_amount, child.id).run();

        return json({ 
          message: 'Задача отправлена на проверку',
          status: 'WAITING',
          pending_reward: task.reward_amount
        });
      }

      // POST /api/tasks/confirm (родитель подтверждает)
      if (path === '/api/tasks/confirm' && request.method === 'POST') {
        const inviteCode = request.headers.get('X-Invite-Code');
        if (!inviteCode) return error('Требуется авторизация', 'NO_AUTH', 401);

        const body = await request.json();
        const { task_id, action } = body;

        if (!task_id || !action) {
          return error('Отсутствует task_id или action', 'INVALID_INPUT');
        }

        // Проверяем родителя
        const family = await env.DB.prepare(
          'SELECT id FROM families WHERE invite_code = ?'
        ).bind(inviteCode).first();

        if (!family) {
          return error('Только родители могут подтверждать задачи', 'FORBIDDEN', 403);
        }

        // Проверяем задачу (идемпотентность)
        const task = await env.DB.prepare(
          'SELECT * FROM tasks WHERE id = ? AND family_id = ?'
        ).bind(task_id, family.id).first();

        if (!task) {
          return error('Задача не найдена', 'NOT_FOUND', 404);
        }

        if (task.status === 'CONFIRMED' || task.status === 'REJECTED') {
          return json({ message: 'Задача уже обработана', status: task.status });
        }

        if (task.status !== 'WAITING') {
          return error('Задача не ожидает подтверждения', 'INVALID_STATUS');
        }

        // Получаем ребёнка
        const child = await env.DB.prepare(
          'SELECT id, balance, pending_balance FROM children WHERE id = ? AND family_id = ?'
        ).bind(task.child_id, family.id).first();

        if (!child) {
          return error('Ребёнок не найден', 'NOT_FOUND', 404);
        }

        if (action === 'confirm') {
          const newBalance = child.balance + task.reward_amount;
          const newPending = child.pending_balance - task.reward_amount;

          await env.DB.prepare(
            'UPDATE children SET balance = ?, pending_balance = ? WHERE id = ?'
          ).bind(newBalance, newPending, child.id).run();

          await env.DB.prepare(
            "UPDATE tasks SET status = 'CONFIRMED', updated_at = CURRENT_TIMESTAMP WHERE id = ?"
          ).bind(task_id).run();

          await env.DB.prepare(
            'INSERT INTO task_ledger (id, family_id, child_id, task_id, type, amount, balance_before, balance_after) VALUES (?, ?, ?, ?, ?, ?, ?, ?)'
          ).bind(
            `ledger_${Date.now()}`,
            family.id,
            child.id,
            task_id,
            'TASK_CONFIRM',
            task.reward_amount,
            child.balance,
            newBalance
          ).run();

          return json({ 
            message: 'Задача подтверждена',
            status: 'CONFIRMED',
            new_balance: newBalance
          });
        } else if (action === 'reject') {
          const newPending = child.pending_balance - task.reward_amount;

          await env.DB.prepare(
            'UPDATE children SET pending_balance = ? WHERE id = ?'
          ).bind(newPending, child.id).run();

          await env.DB.prepare(
            "UPDATE tasks SET status = 'IDLE', updated_at = CURRENT_TIMESTAMP WHERE id = ?"
          ).bind(task_id).run();

          return json({ 
            message: 'Задача отклонена',
            status: 'REJECTED'
          });
        } else {
          return error('Неверное действие (confirm/reject)', 'INVALID_ACTION');
        }
      }

      // POST /api/tasks/create (родитель создаёт задачу)
      if (path === '/api/tasks/create' && request.method === 'POST') {
        const inviteCode = request.headers.get('X-Invite-Code');
        if (!inviteCode) return error('Требуется авторизация', 'NO_AUTH', 401);

        const family = await env.DB.prepare(
          'SELECT id FROM families WHERE invite_code = ?'
        ).bind(inviteCode).first();

        if (!family) {
          return error('Только родители могут создавать задачи', 'FORBIDDEN', 403);
        }

        const body = await request.json();
        const { child_id, title, description, reward_amount, recurring, recurring_days } = body;

        if (!child_id || !title || !reward_amount) {
          return error('Отсутствуют обязательные поля: child_id, title, reward_amount', 'INVALID_INPUT');
        }

        const child = await env.DB.prepare(
          'SELECT id FROM children WHERE id = ? AND family_id = ?'
        ).bind(child_id, family.id).first();

        if (!child) {
          return error('Ребёнок не найден в этой семье', 'NOT_FOUND', 404);
        }

        const taskId = `task_${Date.now()}_${Math.random().toString(36).substring(2, 6)}`;

        await env.DB.prepare(
          'INSERT INTO tasks (id, family_id, child_id, title, description, reward_amount, recurring, recurring_days, status) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)'
        ).bind(
          taskId,
          family.id,
          child_id,
          title,
          description || null,
          parseInt(reward_amount),
          recurring || null,
          recurring_days || null,
          'IDLE'
        ).run();

        return json({
          message: 'Задача создана',
          task: {
            id: taskId,
            title,
            reward_amount: parseInt(reward_amount)
          }
        });
      }

      // DELETE /api/tasks/delete (родитель удаляет задачу)
      if (path === '/api/tasks/delete' && request.method === 'DELETE') {
        const inviteCode = request.headers.get('X-Invite-Code');
        if (!inviteCode) return error('Требуется авторизация', 'NO_AUTH', 401);

        const family = await env.DB.prepare(
          'SELECT id FROM families WHERE invite_code = ?'
        ).bind(inviteCode).first();

        if (!family) {
          return error('Только родители могут удалять задачи', 'FORBIDDEN', 403);
        }

        const body = await request.json();
        const { task_id } = body;

        if (!task_id) {
          return error('Отсутствует task_id', 'INVALID_INPUT');
        }

        const task = await env.DB.prepare(
          'SELECT id FROM tasks WHERE id = ? AND family_id = ?'
        ).bind(task_id, family.id).first();

        if (!task) {
          return error('Задача не найдена', 'NOT_FOUND', 404);
        }

        await env.DB.prepare(
          "UPDATE tasks SET status = 'ARCHIVED', updated_at = CURRENT_TIMESTAMP WHERE id = ?"
        ).bind(task_id).run();

        return json({ message: 'Задача удалена' });
      }

      // GET /api/children/list
      if (path === '/api/children/list' && request.method === 'GET') {
        const inviteCode = request.headers.get('X-Invite-Code');
        if (!inviteCode) return error('Требуется авторизация', 'NO_AUTH', 401);

        const family = await env.DB.prepare(
          'SELECT id FROM families WHERE invite_code = ?'
        ).bind(inviteCode).first();

        if (!family) {
          return error('Только родители могут просматривать список детей', 'FORBIDDEN', 403);
        }

        const result = await env.DB.prepare(
          'SELECT id, name, role, age, balance, pending_balance, invite_code, child_number FROM children WHERE family_id = ? ORDER BY child_number ASC'
        ).bind(family.id).all();

        return json({ children: result.results || [] });
      }


      // GET /api/children/:child_id — детальная информация о ребёнке
      const childDetailMatch = path.match(/^\/api\/children\/([^\/]+)$/);
      if (childDetailMatch && request.method === 'GET') {
        const childId = childDetailMatch[1];
        const inviteCode = request.headers.get('X-Invite-Code');
        
        if (!inviteCode) {
          return error('Отсутствует заголовок X-Invite-Code', 'NO_AUTH', 401);
        }

        // Проверяем родителя
        const family = await env.DB.prepare(
          'SELECT id FROM families WHERE invite_code = ?'
        ).bind(inviteCode).first();

        if (!family) {
          return error('Только родитель может видеть детали', 'FORBIDDEN', 403);
        }

        // Получаем ребёнка с проверкой принадлежности к семье
        const child = await env.DB.prepare(`
          SELECT id, name, role, age, balance, pending_balance, invite_code, child_number
          FROM children
          WHERE id = ? AND family_id = ?
        `).bind(childId, family.id).first();

        if (!child) {
          return error('Ребёнок не найден', 'NOT_FOUND', 404);
        }

        return json({ child });
      }

      // POST /api/children/add
      if (path === '/api/children/add' && request.method === 'POST') {
        const inviteCode = request.headers.get('X-Invite-Code');
        if (!inviteCode) return error('Требуется авторизация', 'NO_AUTH', 401);

        const family = await env.DB.prepare(
          'SELECT id FROM families WHERE invite_code = ?'
        ).bind(inviteCode).first();

        if (!family) {
          return error('Только родители могут добавлять детей', 'FORBIDDEN', 403);
        }

        const body = await request.json();
        const { name, role, age, ai_description } = body;

        if (!name || !role || !age) {
          return error('Отсутствуют обязательные поля: name, role, age', 'INVALID_INPUT');
        }

        const childId = `child_${Date.now()}`;
        const childInviteCode = `KID_${name.toUpperCase().replace(/[^A-Z0-9]/g, '')}_${Math.random().toString(36).substring(2, 6).toUpperCase()}`;

        await env.DB.prepare(
          'INSERT INTO children (id, family_id, name, role, age, invite_code, balance, pending_balance, ai_description) VALUES (?, ?, ?, ?, ?, ?, 0, 0, ?)'
        ).bind(childId, family.id, name, role, parseInt(age), childInviteCode, ai_description || null).run();

        return json({
          message: 'Ребёнок добавлен',
          child: {
            id: childId,
            name,
            role,
            age: parseInt(age),
            invite_code: childInviteCode
          }
        });
      }

      // PUT /api/children/edit/:id
      if (path.startsWith('/api/children/edit/') && request.method === 'PUT') {
        const inviteCode = request.headers.get('X-Invite-Code');
        if (!inviteCode) return error('Требуется авторизация', 'NO_AUTH', 401);

        const family = await env.DB.prepare(
          'SELECT id FROM families WHERE invite_code = ?'
        ).bind(inviteCode).first();

        if (!family) {
          return error('Только родители могут редактировать детей', 'FORBIDDEN', 403);
        }

        const childId = path.split('/').pop();
        const body = await request.json();
        const { name, role, age, ai_description } = body;

        if (!name || !role || !age) {
          return error('Отсутствуют обязательные поля: name, role, age', 'INVALID_INPUT');
        }

        // Проверить что ребёнок принадлежит этой семье
        const child = await env.DB.prepare(
          'SELECT id FROM children WHERE id = ? AND family_id = ?'
        ).bind(childId, family.id).first();

        if (!child) {
          return error('Ребёнок не найден', 'NOT_FOUND', 404);
        }

        // Обновить данные ребёнка
        await env.DB.prepare(
          'UPDATE children SET name = ?, role = ?, age = ?, ai_description = ? WHERE id = ?'
        ).bind(name, role, parseInt(age), ai_description || null, childId).run();

        return json({
          message: 'Изменения сохранены',
          child: {
            id: childId,
            name,
            role,
            age: parseInt(age),
            ai_description
          }
        });
      }

      // ============================
      // REWARDS: Управление наградами
      // ============================

            // POST /api/rewards/init — инициализация таблиц rewards и reward_purchases (ADMIN)
      if (path === '/api/rewards/init' && request.method === 'POST') {
        try {
          // Создаём таблицу rewards
          await env.DB.prepare(`
            CREATE TABLE IF NOT EXISTS rewards (
              id TEXT PRIMARY KEY,
              family_id TEXT NOT NULL,
              title TEXT NOT NULL,
              description TEXT,
              price INTEGER NOT NULL CHECK (price >= 1 AND price <= 10000),
              icon TEXT DEFAULT '🎁',
              is_permanent INTEGER DEFAULT 0 CHECK (is_permanent IN (0, 1)),
              is_active INTEGER DEFAULT 1 CHECK (is_active IN (0, 1)),
              created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
              updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
          `).run();

          // Создаём индексы для rewards
          await env.DB.prepare(`
            CREATE INDEX IF NOT EXISTS idx_rewards_family ON rewards(family_id)
          `).run();

          await env.DB.prepare(`
            CREATE INDEX IF NOT EXISTS idx_rewards_active ON rewards(family_id, is_active)
          `).run();

          // Создаём таблицу reward_purchases
          await env.DB.prepare(`
            CREATE TABLE IF NOT EXISTS reward_purchases (
              id TEXT PRIMARY KEY,
              reward_id TEXT NOT NULL,
              child_id TEXT NOT NULL,
              family_id TEXT NOT NULL,
              reward_title TEXT NOT NULL,
              reward_icon TEXT,
              price INTEGER NOT NULL,
              status TEXT DEFAULT 'pending' CHECK (status IN ('pending', 'received')),
              purchased_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
              received_at TIMESTAMP
            )
          `).run();

          // Создаём индексы для reward_purchases
          await env.DB.prepare(`
            CREATE INDEX IF NOT EXISTS idx_purchases_child ON reward_purchases(child_id, status)
          `).run();

          await env.DB.prepare(`
            CREATE INDEX IF NOT EXISTS idx_purchases_family ON reward_purchases(family_id)
          `).run();

          return json({ message: 'Таблицы rewards и reward_purchases успешно созданы' });
        } catch (err) {
          return error(`Ошибка создания таблиц: ${err.message}`, 'DB_ERROR', 500);
        }
      }

      // GET /api/rewards/list — список наград семьи
      if (path === '/api/rewards/list' && request.method === 'GET') {
        const inviteCode = request.headers.get('X-Invite-Code');
        
        if (!inviteCode) {
          return error('Отсутствует заголовок X-Invite-Code', 'NO_AUTH', 401);
        }

        // Проверяем родителя
        let family = await env.DB.prepare(
          'SELECT id FROM families WHERE invite_code = ?'
        ).bind(inviteCode).first();

        // Если не родитель — проверяем ребёнка
        if (!family) {
          const child = await env.DB.prepare(
            'SELECT family_id FROM children WHERE invite_code = ?'
          ).bind(inviteCode).first();
          
          if (!child) {
            return error('Недействительный код', 'FORBIDDEN', 403);
          }
          
          // Используем family_id ребёнка
          family = { id: child.family_id };
        }

        // Получаем список наград
        const rewards = await env.DB.prepare(`
          SELECT id, family_id, title, description, price, icon, is_permanent, created_at, updated_at
          FROM rewards
          WHERE family_id = ? AND is_active = 1
          ORDER BY created_at DESC
        `).bind(family.id).all();

        return json({ rewards: rewards.results || [] });
      }

      // POST /api/rewards/create — создание награды (только родитель)
      if (path === '/api/rewards/create' && request.method === 'POST') {
        const inviteCode = request.headers.get('X-Invite-Code');
        
        if (!inviteCode) {
          return error('Отсутствует заголовок X-Invite-Code', 'NO_AUTH', 401);
        }

        // Проверяем родителя
        const family = await env.DB.prepare(
          'SELECT id FROM families WHERE invite_code = ?'
        ).bind(inviteCode).first();

        if (!family) {
          return error('Только родитель может создавать награды', 'FORBIDDEN', 403);
        }

        // Парсим тело запроса
        const body = await request.json();
        const { title, description, price, icon, is_permanent } = body;

        // Валидация
        if (!title || !price) {
          return error('Отсутствуют обязательные поля: title, price', 'INVALID_DATA', 400);
        }

        const priceInt = parseInt(price);
        if (isNaN(priceInt) || priceInt < 1 || priceInt > 10000) {
          return error('Цена должна быть от 1 до 10000', 'INVALID_DATA', 400);
        }

        // Генерируем ID
        const rewardId = `reward_${Date.now()}_${Math.random().toString(36).substring(2, 6)}`;

        // Создаём награду
        await env.DB.prepare(`
          INSERT INTO rewards (id, family_id, title, description, price, icon, is_permanent, is_active, created_at, updated_at)
          VALUES (?, ?, ?, ?, ?, ?, ?, 1, datetime('now'), datetime('now'))
        `).bind(
          rewardId,
          family.id,
          title,
          description || '',
          priceInt,
          icon || '🎁',
          is_permanent ? 1 : 0
        ).run();

        return json({
          message: 'Награда создана',
          reward: {
            id: rewardId,
            title,
            price: priceInt
          }
        });
      }

      // DELETE /api/rewards/delete — удаление награды (мягкое удаление)
      if (path === '/api/rewards/delete' && request.method === 'DELETE') {
        const inviteCode = request.headers.get('X-Invite-Code');
        
        if (!inviteCode) {
          return error('Отсутствует заголовок X-Invite-Code', 'NO_AUTH', 401);
        }

        // Проверяем родителя
        const family = await env.DB.prepare(
          'SELECT id FROM families WHERE invite_code = ?'
        ).bind(inviteCode).first();

        if (!family) {
          return error('Только родитель может удалять награды', 'FORBIDDEN', 403);
        }

        // Парсим тело запроса
        const body = await request.json();
        const { reward_id } = body;

        if (!reward_id) {
          return error('Отсутствует reward_id', 'INVALID_DATA', 400);
        }

        // Проверяем, что награда принадлежит семье
        const reward = await env.DB.prepare(
          'SELECT id FROM rewards WHERE id = ? AND family_id = ?'
        ).bind(reward_id, family.id).first();

        if (!reward) {
          return error('Награда не найдена', 'NOT_FOUND', 404);
        }

        // Мягкое удаление
        await env.DB.prepare(
          'UPDATE rewards SET is_active = 0, updated_at = datetime(\'now\') WHERE id = ?'
        ).bind(reward_id).run();

        return json({ message: 'Награда удалена' });
      }


      // POST /api/rewards/purchase — покупка награды (только ребёнок)
      if (path === '/api/rewards/purchase' && request.method === 'POST') {
        const inviteCode = request.headers.get('X-Invite-Code');
        
        if (!inviteCode) {
          return error('Отсутствует заголовок X-Invite-Code', 'NO_AUTH', 401);
        }

        const child = await env.DB.prepare(
          'SELECT id, family_id, name, balance FROM children WHERE invite_code = ?'
        ).bind(inviteCode).first();

        if (!child) {
          return error('Только ребёнок может покупать награды', 'FORBIDDEN', 403);
        }

        const body = await request.json();
        const { reward_id } = body;

        if (!reward_id) {
          return error('Отсутствует reward_id', 'INVALID_DATA', 400);
        }

        const reward = await env.DB.prepare(
          'SELECT id, family_id, title, icon, price, is_permanent FROM rewards WHERE id = ? AND family_id = ? AND is_active = 1'
        ).bind(reward_id, child.family_id).first();

        if (!reward) {
          return error('Награда не найдена или недоступна', 'NOT_FOUND', 404);
        }

        if (child.balance < reward.price) {
          return error('Недостаточно средств', 'INSUFFICIENT_BALANCE', 400);
        }

        const newBalance = child.balance - reward.price;
        await env.DB.prepare(
          'UPDATE children SET balance = ? WHERE id = ?'
        ).bind(newBalance, child.id).run();

        const purchaseId = `purchase_${Date.now()}_${Math.random().toString(36).substring(2, 6)}`;
        await env.DB.prepare(`
          INSERT INTO reward_purchases (id, reward_id, child_id, family_id, reward_title, reward_icon, price, status, purchased_at)
          VALUES (?, ?, ?, ?, ?, ?, ?, 'pending', datetime('now'))
        `).bind(
          purchaseId,
          reward.id,
          child.id,
          child.family_id,
          reward.title,
          reward.icon,
          reward.price
        ).run();

        if (reward.is_permanent === 0) {
          await env.DB.prepare(
            'UPDATE rewards SET is_active = 0 WHERE id = ?'
          ).bind(reward.id).run();
        }

        return json({
          message: 'Награда куплена',
          purchase: {
            id: purchaseId,
            reward_title: reward.title,
            price: reward.price
          },
          new_balance: newBalance
        });
      }

      // GET /api/rewards/purchases — список купленных наград ребёнка
      if (path === '/api/rewards/purchases' && request.method === 'GET') {
        const inviteCode = request.headers.get('X-Invite-Code');
        
        if (!inviteCode) {
          return error('Отсутствует заголовок X-Invite-Code', 'NO_AUTH', 401);
        }

        const child = await env.DB.prepare(
          'SELECT id FROM children WHERE invite_code = ?'
        ).bind(inviteCode).first();

        if (!child) {
          return error('Недействительный код', 'FORBIDDEN', 403);
        }

        const purchases = await env.DB.prepare(`
          SELECT id, reward_id, reward_title, reward_icon, price, status, purchased_at
          FROM reward_purchases
          WHERE child_id = ? AND status = 'pending'
          ORDER BY purchased_at DESC
        `).bind(child.id).all();

        return json({ purchases: purchases.results || [] });
      }

      // GET /api/rewards/received — count received rewards for profile
      if (path === '/api/rewards/received' && request.method === 'GET') {
        const inviteCode = request.headers.get('X-Invite-Code');
        
        if (!inviteCode) {
          return error('Отсутствует заголовок X-Invite-Code', 'NO_AUTH', 401);
        }

        const child = await env.DB.prepare(
          'SELECT id FROM children WHERE invite_code = ?'
        ).bind(inviteCode).first();

        if (!child) {
          return error('Недействительный код', 'FORBIDDEN', 403);
        }

        const received = await env.DB.prepare(`
          SELECT COUNT(*) as count
          FROM reward_purchases
          WHERE child_id = ? AND status = 'received'
        `).bind(child.id).first();

        return json({ count: received.count || 0 });
      }


      // GET /api/rewards/purchases/family — список покупок всех детей семьи (для родителя)
      if (path === '/api/rewards/purchases/family' && request.method === 'GET') {
        const inviteCode = request.headers.get('X-Invite-Code');
        
        if (!inviteCode) {
          return error('Отсутствует заголовок X-Invite-Code', 'NO_AUTH', 401);
        }

        // Проверяем родителя
        const family = await env.DB.prepare(
          'SELECT id FROM families WHERE invite_code = ?'
        ).bind(inviteCode).first();

        if (!family) {
          return error('Только родитель может видеть все покупки', 'FORBIDDEN', 403);
        }

        // Получаем покупки со статусом pending для всей семьи
        const purchases = await env.DB.prepare(`
          SELECT 
            rp.id,
            rp.child_id,
            rp.reward_title, 
            rp.reward_icon, 
            rp.price, 
            rp.status,
            rp.purchased_at,
            c.name as child_name
          FROM reward_purchases rp
          JOIN children c ON rp.child_id = c.id
          WHERE rp.family_id = ? AND rp.status = 'pending'
          ORDER BY rp.purchased_at DESC
        `).bind(family.id).all();

        return json({ purchases: purchases.results || [] });
      }

      // POST /api/rewards/confirm-received — подтверждение получения награды
      if (path === '/api/rewards/confirm-received' && request.method === 'POST') {
        const inviteCode = request.headers.get('X-Invite-Code');
        
        if (!inviteCode) {
          return error('Отсутствует заголовок X-Invite-Code', 'NO_AUTH', 401);
        }

        const child = await env.DB.prepare(
          'SELECT id FROM children WHERE invite_code = ?'
        ).bind(inviteCode).first();

        if (!child) {
          return error('Недействительный код', 'FORBIDDEN', 403);
        }

        const body = await request.json();
        const { purchase_id } = body;

        if (!purchase_id) {
          return error('Отсутствует purchase_id', 'INVALID_DATA', 400);
        }

        const purchase = await env.DB.prepare(
          'SELECT id FROM reward_purchases WHERE id = ? AND child_id = ? AND status = \'pending\''
        ).bind(purchase_id, child.id).first();

        if (!purchase) {
          return error('Покупка не найдена', 'NOT_FOUND', 404);
        }

        await env.DB.prepare(
          'UPDATE reward_purchases SET status = \'received\', received_at = datetime(\'now\') WHERE id = ?'
        ).bind(purchase_id).run();


        // Записываем событие для AI
        const purchaseData = await env.DB.prepare(
          'SELECT family_id FROM reward_purchases WHERE id = ?'
        ).bind(purchase_id).first();

        if (purchaseData) {
          await env.DB.prepare(
            'INSERT INTO events (event_type, payload, family_id, child_id, created_at) VALUES (?, ?, ?, ?, datetime(\'now\'))'
          ).bind(
            'reward_received',
            JSON.stringify({ purchase_id }),
            purchaseData.family_id,
            child.id
          ).run();
        }

        return json({ message: 'Награда отмечена как полученная' });
      }


      // POST /api/dreams/init — создание таблицы dreams
      if (path === '/api/dreams/init' && request.method === 'POST') {
        try {
          await env.DB.prepare(`
            CREATE TABLE IF NOT EXISTS dreams (
              id TEXT PRIMARY KEY,
              child_id TEXT NOT NULL,
              family_id TEXT NOT NULL,
              title TEXT NOT NULL,
              target_amount INTEGER,
              current_amount INTEGER DEFAULT 0,
              status TEXT DEFAULT 'pending' CHECK (status IN ('pending', 'active', 'completed', 'cancelled')),
              created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
              approved_at TIMESTAMP
            )
          `).run();

          await env.DB.prepare(`
            CREATE INDEX IF NOT EXISTS idx_dreams_child ON dreams(child_id, status)
          `).run();

          await env.DB.prepare(`
            CREATE INDEX IF NOT EXISTS idx_dreams_family ON dreams(family_id, status)
          `).run();

          return json({ message: 'Таблица dreams успешно создана' });
        } catch (err) {
          return error('Ошибка создания таблицы: ' + err.message, 'DB_ERROR', 500);
        }
      }


      // POST /api/dreams/migrate — миграция таблицы dreams (DROP + CREATE)
      if (path === '/api/dreams/migrate' && request.method === 'POST') {
        try {
          // Удаляем старую таблицу
          await env.DB.prepare('DROP TABLE IF EXISTS dreams').run();

          // Создаём заново
          await env.DB.prepare(`
            CREATE TABLE dreams (
              id TEXT PRIMARY KEY,
              child_id TEXT NOT NULL,
              family_id TEXT NOT NULL,
              title TEXT NOT NULL,
              target_amount INTEGER,
              current_amount INTEGER DEFAULT 0,
              status TEXT DEFAULT 'pending' CHECK (status IN ('pending', 'active', 'completed', 'cancelled')),
              created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
              approved_at TIMESTAMP
            )
          `).run();

          await env.DB.prepare(`
            CREATE INDEX idx_dreams_child ON dreams(child_id, status)
          `).run();

          await env.DB.prepare(`
            CREATE INDEX idx_dreams_family ON dreams(family_id, status)
          `).run();

          return json({ message: 'Таблица dreams пересоздана успешно' });
        } catch (err) {
          return error('Ошибка миграции: ' + err.message, 'DB_ERROR', 500);
        }
      }


      // POST /api/dreams/create — создание мечты (ребёнок)
      if (path === '/api/dreams/create' && request.method === 'POST') {
        const inviteCode = request.headers.get('X-Invite-Code');
        
        if (!inviteCode) {
          return error('Отсутствует заголовок X-Invite-Code', 'NO_AUTH', 401);
        }

        const child = await env.DB.prepare(
          'SELECT id, family_id FROM children WHERE invite_code = ?'
        ).bind(inviteCode).first();

        if (!child) {
          return error('Недействительный код ребёнка', 'FORBIDDEN', 403);
        }

        const body = await request.json();
        const { title } = body;

        if (!title || title.trim().length === 0) {
          return error('Название мечты обязательно', 'INVALID_DATA', 400);
        }

        // Проверяем что нет активной мечты
        const existingDream = await env.DB.prepare(
          'SELECT id FROM dreams WHERE child_id = ? AND status IN ("pending", "active")'
        ).bind(child.id).first();

        if (existingDream) {
          return error('У ребёнка уже есть активная мечта', 'INVALID_DATA', 400);
        }

        const dreamId = 'dream_' + Date.now() + '_' + Math.random().toString(36).substring(2, 8);

        await env.DB.prepare(`
          INSERT INTO dreams (id, child_id, family_id, title, status, created_at)
          VALUES (?, ?, ?, ?, 'pending', datetime('now'))
        `).bind(dreamId, child.id, child.family_id, title.trim()).run();

        return json({ 
          message: 'Мечта создана',
          dream: { id: dreamId, title: title.trim(), status: 'pending' }
        });
      }

      // GET /api/dreams/my — получить мечту ребёнка
      if (path === '/api/dreams/my' && request.method === 'GET') {
        const inviteCode = request.headers.get('X-Invite-Code');
        
        if (!inviteCode) {
          return error('Отсутствует заголовок X-Invite-Code', 'NO_AUTH', 401);
        }

        const child = await env.DB.prepare(
          'SELECT id FROM children WHERE invite_code = ?'
        ).bind(inviteCode).first();

        if (!child) {
          return error('Недействительный код ребёнка', 'FORBIDDEN', 403);
        }

        const dream = await env.DB.prepare(`
          SELECT id, title, target_amount, current_amount, status, created_at, approved_at
          FROM dreams
          WHERE child_id = ? AND status IN ('pending', 'active')
          ORDER BY created_at DESC
          LIMIT 1
        `).bind(child.id).first();

        return json({ dream: dream || null });
      }

      // DELETE /api/dreams/delete — удаление мечты (ребёнок)
      if (path === '/api/dreams/delete' && request.method === 'DELETE') {
        const inviteCode = request.headers.get('X-Invite-Code');
        
        if (!inviteCode) {
          return error('Отсутствует заголовок X-Invite-Code', 'NO_AUTH', 401);
        }

        const child = await env.DB.prepare(
          'SELECT id FROM children WHERE invite_code = ?'
        ).bind(inviteCode).first();

        if (!child) {
          return error('Недействительный код ребёнка', 'FORBIDDEN', 403);
        }

        const body = await request.json();
        const { dream_id } = body;

        if (!dream_id) {
          return error('Не указан ID мечты', 'INVALID_DATA', 400);
        }

        // Проверяем принадлежность
        const dream = await env.DB.prepare(
          'SELECT id FROM dreams WHERE id = ? AND child_id = ?'
        ).bind(dream_id, child.id).first();

        if (!dream) {
          return error('Мечта не найдена', 'NOT_FOUND', 404);
        }

        await env.DB.prepare(
          'UPDATE dreams SET status = "cancelled" WHERE id = ?'
        ).bind(dream_id).run();

        return json({ message: 'Мечта удалена' });
      }

      // GET /api/dreams/pending — список pending мечт для родителя
      if (path === '/api/dreams/pending' && request.method === 'GET') {
        const inviteCode = request.headers.get('X-Invite-Code');
        
        if (!inviteCode) {
          return error('Отсутствует заголовок X-Invite-Code', 'NO_AUTH', 401);
        }

        const family = await env.DB.prepare(
          'SELECT id FROM families WHERE invite_code = ?'
        ).bind(inviteCode).first();

        if (!family) {
          return error('Недействительный код родителя', 'FORBIDDEN', 403);
        }

        const dreams = await env.DB.prepare(`
          SELECT 
            d.id,
            d.child_id,
            d.title,
            d.status,
            d.created_at,
            c.name as child_name
          FROM dreams d
          JOIN children c ON d.child_id = c.id
          WHERE d.family_id = ? AND d.status = 'pending'
          ORDER BY d.created_at DESC
        `).bind(family.id).all();

        return json({ dreams: dreams.results || [] });
      }

      // POST /api/dreams/set-goal — установка цели родителем
      if (path === '/api/dreams/set-goal' && request.method === 'POST') {
        const inviteCode = request.headers.get('X-Invite-Code');
        
        if (!inviteCode) {
          return error('Отсутствует заголовок X-Invite-Code', 'NO_AUTH', 401);
        }

        const family = await env.DB.prepare(
          'SELECT id FROM families WHERE invite_code = ?'
        ).bind(inviteCode).first();

        if (!family) {
          return error('Только родитель может устанавливать цель', 'FORBIDDEN', 403);
        }

        const body = await request.json();
        const { dream_id, target_amount } = body;

        if (!dream_id || !target_amount) {
          return error('Не указан ID мечты или сумма', 'INVALID_DATA', 400);
        }

        const amount = parseInt(target_amount);
        if (isNaN(amount) || amount < 1 || amount > 1000000) {
          return error('Сумма должна быть от 1 до 1000000', 'INVALID_DATA', 400);
        }

        // Проверяем принадлежность к семье
        const dream = await env.DB.prepare(
          'SELECT id, child_id FROM dreams WHERE id = ? AND family_id = ? AND status = "pending"'
        ).bind(dream_id, family.id).first();

        if (!dream) {
          return error('Мечта не найдена', 'NOT_FOUND', 404);
        }

        // Получаем текущий баланс ребёнка
        const child = await env.DB.prepare(
          'SELECT balance FROM children WHERE id = ?'
        ).bind(dream.child_id).first();

        await env.DB.prepare(`
          UPDATE dreams 
          SET target_amount = ?, current_amount = ?, status = 'active', approved_at = datetime('now')
          WHERE id = ?
        `).bind(amount, child.balance, dream_id).run();

        return json({ message: 'Цель установлена' });
      }

      // GET /api/dreams/active — список активных мечт для родителя
      if (path === '/api/dreams/active' && request.method === 'GET') {
        const inviteCode = request.headers.get('X-Invite-Code');
        
        if (!inviteCode) {
          return error('Отсутствует заголовок X-Invite-Code', 'NO_AUTH', 401);
        }

        const family = await env.DB.prepare(
          'SELECT id FROM families WHERE invite_code = ?'
        ).bind(inviteCode).first();

        if (!family) {
          return error('Недействительный код родителя', 'FORBIDDEN', 403);
        }

        const dreams = await env.DB.prepare(`
          SELECT 
            d.id,
            d.child_id,
            d.title,
            d.target_amount,
            d.current_amount,
            d.status,
            c.name as child_name
          FROM dreams d
          JOIN children c ON d.child_id = c.id
          WHERE d.family_id = ? AND d.status = 'active'
          ORDER BY d.created_at DESC
        `).bind(family.id).all();

        return json({ dreams: dreams.results || [] });
      }

      // GET /api/referrals/my - Получить/Генерировать 3 кода (для родителя)
      if (path === '/api/referrals/my' && request.method === 'GET') {
        const inviteCode = request.headers.get('X-Invite-Code');
        const family = await env.DB.prepare('SELECT id FROM families WHERE invite_code = ?').bind(inviteCode).first();
        if (!family) return error('Forbidden', 'FORBIDDEN', 403);
        let refs = await env.DB.prepare('SELECT r.*, f.name as used_by_name FROM referrals r LEFT JOIN families f ON r.used_by_family_id = f.id WHERE r.referrer_family_id = ?').bind(family.id).all();
        if (refs.results.length === 0) {
          for (let i = 0; i < 3; i++) {
            const refCode = 'REF_' + Math.random().toString(36).substring(2, 8).toUpperCase();
            await env.DB.prepare('INSERT INTO referrals (id, referrer_family_id, invite_code) VALUES (?, ?, ?)').bind(`ref_${Date.now()}_${i}`, family.id, refCode).run();
          }
          refs = await env.DB.prepare('SELECT r.*, f.name as used_by_name FROM referrals r LEFT JOIN families f ON r.used_by_family_id = f.id WHERE r.referrer_family_id = ?').bind(family.id).all();
        }
        return new Response(JSON.stringify({ referrals: refs.results }), { headers: corsHeaders });
      }

      // POST /api/families/register - Регистрация новой семьи по коду
      if (path === '/api/families/register' && request.method === 'POST') {
        const { name, currency_name, currency_symbol, referral_code } = await request.json();
        const cleanCode = referral_code.trim().toUpperCase();
        const ref = await env.DB.prepare('SELECT * FROM referrals WHERE invite_code = ? AND used_by_family_id IS NULL').bind(cleanCode).first();
        if (!ref) return new Response(JSON.stringify({ error: 'Код недействителен', code: 'INVALID_REF' }), { status: 400, headers: corsHeaders });
        const newFamilyId = 'fam_' + Date.now();
        const newInviteCode = Math.random().toString(36).substring(2, 8).toUpperCase();
        await env.DB.batch([
          env.DB.prepare('INSERT INTO families (id, name, currency_name, currency_symbol, invite_code) VALUES (?, ?, ?, ?, ?)').bind(newFamilyId, name, currency_name, currency_symbol, newInviteCode),
          env.DB.prepare('UPDATE referrals SET used_by_family_id = ?, used_at = CURRENT_TIMESTAMP WHERE invite_code = ?').bind(newFamilyId, cleanCode)
        ]);
        return new Response(JSON.stringify({ message: 'Семья создана', invite_code: newInviteCode }), { headers: corsHeaders });
      }


      return error('Эндпоинт не найден', 'NOT_FOUND', 404);
    } catch (err) {
      console.error('Worker error:', err);
      return error(`Внутренняя ошибка: ${err.message}`, 'INTERNAL_ERROR', 500);
    }
  },
};
