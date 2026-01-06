#!/bin/bash

echo "=== ПАТЧИНГ parent.html ==="

cp parent.html parent.html.before-patch

echo "Патч 1: approve → confirm"
sed -i '' "s/'approve'/'confirm'/g" parent.html

echo "Патч 2: tab-home обновление"
awk '
/if \(tabId === .tab-missions.\) \{/ { print; in_block=1; next }
in_block && /loadAllTasks\(\);/ { print; print "      } else if (tabId === '\''tab-home'\'') {"; print "        loadChildren();"; print "        loadPendingTasks();"; print "        loadHistory();"; in_block=0; next }
{ print }
' parent.html > parent.html.tmp && mv parent.html.tmp parent.html

echo "Готово!"
ls -lh parent.html
grep -A 12 "function showTab" parent.html

