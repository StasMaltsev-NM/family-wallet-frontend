#!/bin/bash

echo "=== ИСПРАВЛЕНИЕ parent.html ==="

# Бэкап
cp parent.html parent.html.before-fix

# Патч 1: approve → confirm (если есть)
echo "Патч 1: approve → confirm"
grep -q "'approve'" parent.html && sed -i '' "s/'approve'/'confirm'/g" parent.html || echo "  approve уже исправлен"

# Патч 2: Добавить tab-home обновление (только если НЕТ дубля)
echo "Патч 2: tab-home обновление"
if ! grep -q "} else if (tabId === 'tab-home')" parent.html; then
  # Находим строку с tab-missions и добавляем ПОСЛЕ неё блок tab-home
  sed -i '' '/if (tabId === .tab-missions.) {/{
    n
    a\
      } else if (tabId === '"'"'tab-home'"'"') {\
        loadChildren();\
        loadPendingTasks();\
        loadHistory();
  }' parent.html
  echo "  ✅ Блок tab-home добавлен"
else
  echo "  ⚠️ Блок tab-home уже существует"
fi

echo ""
echo "✅ ГОТОВО!"
echo "Размер файла:"
ls -lh parent.html

echo ""
echo "Проверка содержимого:"
grep -A 5 "function showTab" parent.html | head -15

