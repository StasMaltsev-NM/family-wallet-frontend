#!/bin/bash

# ============================
# FAMILY WALLET MVP - DEPLOY SCRIPT
# Автоматический деплой backend + frontend
# ============================

set -e  # Остановка при ошибке

echo "🚀 FAMILY WALLET MVP - АВТОДЕПЛОЙ"
echo "=================================="

# ============================
# 1️⃣ BACKEND DEPLOY
# ============================

echo ""
echo "📦 ШАГ 1: Скачиваем backend файлы..."
cd ~/Desktop/FAMILY_WALLET_MVP
mkdir -p backend
cd backend

curl -sL -o worker.js "https://www.genspark.ai/api/files/s/QeJ5fw2G?token=Z0FBQUFBQnBXQ3dhZzJkMlc1c3k2dWUxSklxX3NoRzBlU3BHN3RPY011UjZ6OUp5bWhfckR1WGJuNUZHanlDMldPNjN6VGdjczBhQlJDeXFnUTdLOFBpUTRHTkNMMWFYV3JPaG9yN1JoWWhCN2ZIQVd6Nk9EOVhuU1JrVlVuT1VYeEI5Y25HdkxDNUdrUTc3LW1WWTdYazVDSkNyc0JDczBMcHEwRW42S2dVcjlZSUtCdWE5LVhqR2ZQNVREOGZYemptZ2RKTzhJdURqV2czSUlrRGRJSWV1THFmOTZFVk10V2xVdGh3MUlwUnhHNlNrQ292ZS1RQzNxeE96ZWxUWWRXRDh3R094VXdSTDFIWHhINW5wUHJSVGdWRXhsOUNQVnc9PQ"

curl -sL -o schema.sql "https://www.genspark.ai/api/files/s/FhU68Ypk?token=Z0FBQUFBQnBXQzA3eE5hUXljT20zdVBpcjdHV1FJaE9JZXlVRmRmSTJ4M1hxN1h4RHNUY1lkdEpmM1VjVXN3VHpzYThyRGE2QW1xOWtaRE5mV20ya3RFUjBEMzlyazZHVkNrVkF4ODRZdG1VZHNBTmlCcFgyZ2l6dU1jR2d4T1hSdHI1X0FESFhWb29vbFFVdHNhdU9Xb1VLUDZpRDVhTG1NX21HSWFBYWF5bzJVcGtXMmxhZndvd0FQTTJ3b29fVm1GWmN3QW1BNjFoXzFXWkxJQjRSeFd5ZHpKXzRpSUxncU04dkkxdXVpc3czbGlpT1NueHVGb2FaZlRHLW9ETXRvNlQ1VExHeFhPTmJYX3F3RkNSV2Z6TUJPU0lGOTgzU3c9PQ"

curl -sL -o wrangler.toml "https://www.genspark.ai/api/files/s/sFBQVVmn?token=Z0FBQUFBQnBXQzBfSHh5T0o2aXJaR191YXpfS2xNcFp3aFJxMWthOWRaYXEtbzFRM3pOaXN4eG1lYmgxRE0yVllMVzFzcDEzZGgyLXFvOWg0N3VCb3dBUHpoYXBrb0l5SWQ5WDlkY3FrcGFwMHRpTUxwTzV6eWZsMGxpSl9iVTc4eFlWbnBIVXcxTmZOVkRCT1Y1ZXEyNmM4R0hQcG5ZOENsZDlmS2FkcUI4S1dUSzdIX1ZWM3U3aWNhd0FSSG80RmVPSDZfZFNNREMzLVZUam1DSzY3dXU0NENsZnY0NWhPa1JRLTlLN0NsZUFBWk1LOHNIakNPQUZETFE5Y2RTdnJNSVR4ZFBtWEZfdFlJbE1oX0x0dnF3Y2ZIRjcwcDI4N1E9PQ"

echo "✅ Файлы скачаны!"

# ============================
# 2️⃣ D1 DATABASE SETUP
# ============================

echo ""
echo "🗄️ ШАГ 2: Проверяем D1 базу данных..."

# Проверяем, есть ли уже database_id в wrangler.toml
if grep -q "YOUR_D1_DATABASE_ID" wrangler.toml; then
    echo "⚠️  D1 база не создана!"
    echo ""
    echo "ВЫПОЛНИ ВРУЧНУЮ:"
    echo "1. npx wrangler d1 create family_wallet_db"
    echo "2. Скопируй database_id из вывода"
    echo "3. Вставь в wrangler.toml вместо YOUR_D1_DATABASE_ID"
    echo "4. Запусти скрипт снова"
    echo ""
    exit 1
else
    echo "✅ D1 база уже настроена!"
fi

# ============================
# 3️⃣ APPLY SCHEMA
# ============================

echo ""
echo "📊 ШАГ 3: Применяем схему БД..."
npx wrangler d1 execute family_wallet_db --file=./schema.sql
echo "✅ Схема применена!"

# ============================
# 4️⃣ DEPLOY WORKER
# ============================

echo ""
echo "☁️ ШАГ 4: Деплоим Worker..."
npx wrangler deploy
echo "✅ Worker задеплоен!"

# ============================
# 5️⃣ FRONTEND DEPLOY
# ============================

echo ""
echo "🎨 ШАГ 5: Скачиваем и деплоим frontend..."
cd ~/Desktop/FAMILY_WALLET_MVP
mkdir -p frontend
cd frontend

curl -sL -o kids.html "https://www.genspark.ai/api/files/s/AHLCehzN?token=Z0FBQUFBQnBXQ3dXSm9WRU03ZXhKeXdEdlFjTk9XeFFfTHo5enRTRmxKNDZtTUNnbHZNV29EY3hRajZpQ01XREJDV3hpMEJnc2drVVhnS1NBV2l5bTZ1elRXa19FRE5mekRpbTY4YWJVTXplVzNlLThnekNOcGJudjJvWUk0ZXlqNzFubkp6WFNod2JQLXVfVVlmNk41dl9uNFFRdUJZbFF0blBZM1VHeEtvOXRHYTNaVlA2cFVnSTFMcWs1Q0FfQkRrR2tlVVV6S1l4UnhyUXJfazNhc3FScE53OFExXzFxYnZoYm5KbUxvaXBRT3NjdUpBa0k3YUYwVUgwdjF5ekRWVVR5N2s0anNrQU5pMEwySkgtRHBqTXY1LVJZNXY2RFE9PQ"

echo "✅ kids.html скачан!"

echo ""
echo "☁️ Деплоим frontend на Cloudflare Pages..."
npx wrangler pages deploy . --project-name=family-wallet-stas-v1 --branch=main

echo ""
echo "=================================="
echo "🎉 ДЕПЛОЙ ЗАВЕРШЁН!"
echo "=================================="
echo ""
echo "📱 Детское приложение: https://family-wallet-stas-v1.pages.dev"
echo "⚙️  Backend API: https://family-wallet-api.ТвойАккаунт.workers.dev"
echo ""
echo "🔧 ВАЖНО: Замени API_BASE в kids.html на реальный URL Worker!"
echo ""
