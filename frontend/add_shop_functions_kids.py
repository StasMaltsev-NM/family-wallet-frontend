#!/usr/bin/env python3

with open('kids.html', 'r', encoding='utf-8') as f:
    content = f.read()

# JavaScript функции для магазина
shop_functions = """
    // ============================
    // МАГАЗИН НАГРАД
    // ============================

    async function loadShopRewards() {
      try {
        const res = await fetch(`${API_URL}/api/rewards/list`, {
          headers: { 'X-Invite-Code': currentCode }
        });
        
        if (!res.ok) throw new Error('Ошибка загрузки наград');
        
        const data = await res.json();
        const list = document.getElementById('shopRewardsList');
        
        if (!data.rewards || data.rewards.length === 0) {
          list.innerHTML = '<div class="empty-state">Пока нет доступных наград</div>';
          return;
        }
        
        list.innerHTML = data.rewards.map(reward => `
          <div class="reward-item">
            <span class="reward-icon">${reward.icon}</span>
            <div class="reward-info">
              <h3>${reward.title}</h3>
              <p>${reward.description || ''}</p>
              <div class="reward-price">${reward.price} ⭐</div>
              <button class="buy-button" onclick="purchaseReward('${reward.id}', ${reward.price})">
                Купить за ${reward.price} ⭐
              </button>
            </div>
          </div>
        `).join('');
        
      } catch (err) {
        document.getElementById('shopRewardsList').innerHTML = 
          `<p class="error">Ошибка: ${err.message}</p>`;
      }
    }

    async function purchaseReward(rewardId, price) {
      const currentBalance = parseInt(document.getElementById('balanceDisplay').innerText.split(':')[1]);
      
      if (currentBalance < price) {
        alert('Недостаточно средств!');
        return;
      }
      
      if (!confirm(`Купить эту награду за ${price} ⭐?`)) return;
      
      try {
        const res = await fetch(`${API_URL}/api/rewards/purchase`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-Invite-Code': currentCode
          },
          body: JSON.stringify({ reward_id: rewardId })
        });
        
        if (!res.ok) {
          const err = await res.json();
          alert(`Ошибка: ${err.error || 'Не удалось купить награду'}`);
          return;
        }
        
        const data = await res.json();
        alert(`✅ ${data.message}`);
        
        // Обновляем баланс и списки
        updateBalance(data.new_balance, 0);
        loadShopRewards();
        loadMyRewards();
        
      } catch (err) {
        alert(`Ошибка: ${err.message}`);
      }
    }

    async function loadMyRewards() {
      try {
        const res = await fetch(`${API_URL}/api/rewards/purchases`, {
          headers: { 'X-Invite-Code': currentCode }
        });
        
        if (!res.ok) throw new Error('Ошибка загрузки покупок');
        
        const data = await res.json();
        const list = document.getElementById('myRewardsList');
        
        if (!data.purchases || data.purchases.length === 0) {
          list.innerHTML = '<div class="empty-state">У тебя пока нет наград</div>';
          return;
        }
        
        list.innerHTML = data.purchases.map(purchase => `
          <div class="my-reward-item">
            <span class="reward-icon">${purchase.reward_icon}</span>
            <div class="reward-info">
              <h3>${purchase.reward_title}</h3>
              <div class="reward-price">${purchase.price} ⭐</div>
              <p style="color: #FF9800; font-weight: bold;">⏳ Ожидает выдачи</p>
              <button class="confirm-button" onclick="confirmReceived('${purchase.id}')">
                Получил награду ✅
              </button>
            </div>
          </div>
        `).join('');
        
      } catch (err) {
        document.getElementById('myRewardsList').innerHTML = 
          `<p class="error">Ошибка: ${err.message}</p>`;
      }
    }

    async function confirmReceived(purchaseId) {
      if (!confirm('Ты точно получил эту награду?')) return;
      
      try {
        const res = await fetch(`${API_URL}/api/rewards/confirm-received`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-Invite-Code': currentCode
          },
          body: JSON.stringify({ purchase_id: purchaseId })
        });
        
        if (!res.ok) {
          const err = await res.json();
          alert(`Ошибка: ${err.error}`);
          return;
        }
        
        const data = await res.json();
        alert(`✅ ${data.message}`);
        
        loadMyRewards();
        
      } catch (err) {
        alert(`Ошибка: ${err.message}`);
      }
    }
"""

# Найти где показываются секции после логина и добавить новые
content = content.replace(
    "document.getElementById('historySection').style.display = 'block';",
    """document.getElementById('historySection').style.display = 'block';
        document.getElementById('myRewardsSection').style.display = 'block';
        document.getElementById('shopSection').style.display = 'block';"""
)

# Добавить вызовы загрузки наград после логина
content = content.replace(
    "loadHistory();",
    """loadHistory();
        loadMyRewards();
        loadShopRewards();"""
)

# Вставить функции перед закрывающим </script>
content = content.replace('  </script>', shop_functions + '\n  </script>')

with open('kids.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("OK")
