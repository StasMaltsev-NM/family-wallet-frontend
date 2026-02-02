#!/bin/bash

# Цвета для вывода
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${YELLOW}🚀 ДЕПЛОЙ WORKER ЧЕРЕЗ CLOUDFLARE API${NC}"

# Проверим что файл существует
if [ ! -f "worker.js" ]; then
    echo -e "${RED}❌ worker.js не найден!${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Файл worker.js найден ($(wc -l < worker.js) строк)${NC}"

# Получим account_id и worker name из wrangler.toml
ACCOUNT_ID=$(grep -oP 'account_id\s*=\s*"\K[^"]+' ../wrangler.toml 2>/dev/null || echo "")
WORKER_NAME=$(grep -oP 'name\s*=\s*"\K[^"]+' ../wrangler.toml 2>/dev/null || echo "family-wallet-api")

if [ -z "$ACCOUNT_ID" ]; then
    echo -e "${YELLOW}⚠️  Account ID не найден в wrangler.toml${NC}"
    echo "Введи Account ID (найти в Cloudflare Dashboard → Workers):"
    read ACCOUNT_ID
fi

echo -e "${GREEN}📦 Worker: ${WORKER_NAME}${NC}"
echo -e "${GREEN}🔑 Account: ${ACCOUNT_ID}${NC}"

# Проверим API токен
if [ -z "$CLOUDFLARE_API_TOKEN" ]; then
    echo -e "${YELLOW}⚠️  CLOUDFLARE_API_TOKEN не установлен${NC}"
    echo "Введи API Token (создать в Cloudflare Dashboard → API Tokens):"
    read -s CF_TOKEN
    export CLOUDFLARE_API_TOKEN=$CF_TOKEN
fi

# Деплой через wrangler (попытка 1)
echo -e "${YELLOW}🔄 Попытка деплоя через wrangler...${NC}"
if npx wrangler deploy worker.js 2>/dev/null; then
    echo -e "${GREEN}✅ ДЕПЛОЙ УСПЕШЕН!${NC}"
    exit 0
fi

# Если wrangler не сработал — выводим инструкцию для ручного деплоя
echo -e "${RED}❌ Автоматический деплой не удался${NC}"
echo ""
echo -e "${YELLOW}📋 РУЧНОЙ ДЕПЛОЙ (через браузер):${NC}"
echo ""
echo "1. Открой: https://dash.cloudflare.com/"
echo "2. Перейди: Workers & Pages → ${WORKER_NAME}"
echo "3. Нажми: Quick Edit"
echo "4. Скопируй содержимое worker.js:"
echo ""
echo -e "${GREEN}   Команда для копирования:${NC}"
echo "   cat worker.js | pbcopy"
echo ""
echo "5. Вставь в редактор (Cmd+A, Cmd+V)"
echo "6. Нажми: Save and Deploy"
echo ""
echo -e "${YELLOW}Выполнить копирование в буфер обмена? (y/n)${NC}"
read -r response
if [[ "$response" =~ ^[Yy]$ ]]; then
    cat worker.js | pbcopy
    echo -e "${GREEN}✅ Содержимое скопировано в буфер обмена!${NC}"
    echo -e "${GREEN}   Теперь открой Dashboard и вставь (Cmd+V)${NC}"
fi

