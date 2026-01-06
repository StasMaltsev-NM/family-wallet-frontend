#!/bin/bash
set -e

echo "🚀 ПОЛНЫЙ ДЕПЛОЙ FAMILY WALLET"
echo "=============================="

# BACKEND
echo ""
echo "📦 1. Обновляем BACKEND..."
cd ~/Desktop/FAMILY_WALLET_MVP/backend

curl -sL -o worker.js "https://www.genspark.ai/api/files/s/ItrqbSIX?token=Z0FBQUFBQnBXRVhJTkhxRWdXS0gxUUZULUhfXzhnNE01WWFBRWt3YXdxVWV2Q1dtZGFRRFljc2x0STBsMXBqeldOM29HWF95aXFuTjFQSVdDS19IWWdWUzRiaGZNQUZHRm9XVjNJZExYanY1RVZpbHliQTExVUFVVWxTMVVIQUNCUlpLVnlFUHhWTndWcHdpcl9LXzJxVXAzLXN5V0Ezel9ONnp3VUhmVkp5VjR1LU9qSFdpNVEwRkR2UVU2cW4wa1RjUll1bVVRbzZoeVc0SEJJbW5lSjhkWGpqUGxJTXpiM2Q1RV9KTXFhQ1lDZmw4RGl1WFVGNWZGeldiak1RY1QzTWZOMmtlWGFwSDhoWkNPUEpDQXNtand5aXlLVGdnOFE9PQ"

echo "✅ worker.js скачан"
echo "Первые 3 строки:"
head -3 worker.js

if grep -q "detail.*Access denied" worker.js; then
    echo "❌ ОШИБКА: Токен истёк! worker.js не скачался!"
    exit 1
fi

echo ""
echo "☁️ Деплоим Worker..."
npx wrangler deploy

echo ""
echo "✅ Worker задеплоен!"

# FRONTEND
echo ""
echo "🎨 2. Обновляем FRONTEND..."
cd ~/Desktop/FAMILY_WALLET_MVP/frontend

# Kids
curl -sL -o kids.html "https://www.genspark.ai/api/files/s/f7jBoiDR?token=Z0FBQUFBQnBXRVhOdUpKbjJRcDA5eGdwbE5Fc3pyeGlVV0s2VWhEZjkzQ1h4OF9oUHdVdkZqdExUWk9XeFozb0YzblpuVWRtSEo2cFFoUFVXMGlDc3pLOEJZa3VBNWN5LXh1dFIxYkpaTmo3MURKaXdhQk0zZWtVam13LTFhclNjU2J1d2szdVcwcThZV1ByeXA5RkNJVHlCUEhyQnItNnRRR0R5YmctVkRJRFlRMkRrQVpPdmoxN2s2QTg4QW9sSFlVaEh4Mm1xTUxVTTVoaVh2bVVHaC1sVGd5dmxkc2l5d0dUWUhVNElmdzdpcEdJRmJCSkl5TnZGS1dtQUlTSGtrVldDMmc2U0t1WVdNUDBIX0ZDZ2wybk93WW1MT1hWM2c9PQ"

# Parent
curl -sL -o parent.html "https://www.genspark.ai/api/files/s/wo1jNdLl?token=Z0FBQUFBQnBXRVhUT0tnLTJwMmNfcmxhQmNxY2oza09mVVZQTUtJckRZLUw5LU5HYXZrVkhzM0lCcm1jMkYwNG1ZU0pjazZzcnJ6eFBveWthUnNuZ1FVdmREZjFyQ3lYVU1aa2tGQkd3cFlBUXRMcHFrY1l2dzVsSG5YLVZzQnc2YjB2RWtkR21GcDQ0V0RobWxXejZ5QUVibHpjLVdfV1hBYWZvU2lKSUQ1TkszZWg0Y20zYU1ZLWttb3FjZ2xCM3EtcXh6LThtcWFMeTZ2SmZ3Y2dJTGIwcmxpY0huVFRFd2VhZkE5b21aRjVyS1JPbnBZMGowZEVUZXVZUmloV3RCLWZDZ29CWjhyOXpRU3NjSDE2UWRJRjZ2RGpfUEJYUXc9PQ"

echo "✅ HTML файлы скачаны"
echo "kids.html (первые 3 строки):"
head -3 kids.html

if grep -q "detail.*Access denied" kids.html; then
    echo "❌ ОШИБКА: Токен истёк! kids.html не скачался!"
    exit 1
fi

echo ""
echo "☁️ Деплоим Frontend..."
npx wrangler pages deploy . --project-name=family-wallet-stas-v1 --branch=main --commit-dirty=true

echo ""
echo "=============================="
echo "🎉 ДЕПЛОЙ ЗАВЕРШЁН!"
echo "=============================="
echo ""
echo "🧪 Проверяем API:"
echo ""
curl -s https://family-wallet-api.maltsevstas21.workers.dev/api/wallet/balance | jq '.'
echo ""
echo "✅ Если видишь 'pending' (не 'pending_balance') - ВСЁ РАБОТАЕТ!"
