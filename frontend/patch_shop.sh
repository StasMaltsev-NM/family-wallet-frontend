#!/bin/bash

WORKER_FILE="parent.html"

# Находим строки с tab-shop и заменяем заглушку на полный магазин
awk '
BEGIN { in_shop = 0; skip = 0 }

# Начало блока tab-shop
/<div id="tab-shop" class="tab-content">/ {
  in_shop = 1
  skip = 1
  print "    <div id=\"tab-shop\" class=\"tab-content\">"
  print "      <div class=\"section\" style=\"min-height: 400px; position: relative;\">"
  print "        <h2>Магазин наград</h2>"
  print "        <button class=\"add-button\" onclick=\"toggleAddRewardForm()\">+</button>"
  print "        "
  print "        <!-- Форма создания награды -->"
  print "        <div class=\"form-popup\" id=\"addRewardForm\">"
  print "          <input type=\"text\" id=\"rewardTitle\" placeholder=\"Название награды\" />"
  print "          <textarea id=\"rewardDescription\" placeholder=\"Описание награды\" rows=\"3\"></textarea>"
  print "          <input type=\"number\" id=\"rewardPrice\" placeholder=\"Цена (1-10000)\" min=\"1\" max=\"10000\" />"
  print "          <label style=\"display: flex; align-items: center; gap: 8px; margin: 10px 0;\">"
  print "            <input type=\"checkbox\" id=\"rewardIsPermanent\" />"
  print "            <span>Постоянный слот (остаётся после покупки)</span>"
  print "          </label>"
  print "          <button onclick=\"createReward()\">Создать награду</button>"
  print "          <button onclick=\"toggleAddRewardForm()\">Отмена</button>"
  print "        </div>"
  print ""
  print "        <!-- Список наград -->"
  print "        <div id=\"rewardsList\"></div>"
  print "      </div>"
  print "    </div>"
  next
}

# Внутри блока tab-shop — пропускаем старые строки до закрывающего </div>
in_shop == 1 {
  if (/<\/div>/ && skip == 1) {
    in_shop = 0
    skip = 0
  }
  next
}

# Все остальные строки — печатаем как есть
{ print }
' "$WORKER_FILE" > "${WORKER_FILE}.tmp"

# Заменяем файл
mv "${WORKER_FILE}.tmp" "$WORKER_FILE"

echo "✅ Патч применён! HTML структура магазина добавлена."
echo "📊 Новый размер файла:"
wc -l "$WORKER_FILE"
