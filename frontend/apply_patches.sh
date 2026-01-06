#!/bin/bash

echo "=== ПРИМЕНЕНИЕ ПАТЧЕЙ К parent.html ==="

# Бэкап
cp parent.html parent.html.before-patches

# Патч 1: approve → confirm
echo "Патч 1: approve → confirm"
sed -i '' "s/'approve'/'confirm'/g" parent.html

# Патч 2: Добавить обновление tab-home
echo "Патч 2: Добавить обновление tab-home"
sed -i '' '/if (tabId === .tab-missions.) {/a\
      } else if (tabId === '"'"'tab-home'"'"') {\
        loadChildren();\
        loadPendingTasks();\
        loadHistory();\
' parent.html

echo "✅ Патчи применены!"
echo "Размер файла:"
ls -lh parent.html

