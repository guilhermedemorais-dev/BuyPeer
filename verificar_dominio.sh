#!/bin/bash

# Script para verificar se o domínio buypeer.com.br está funcionando

echo "🔍 Verificando domínio buypeer.com.br..."

# Verificar DNS
echo "📡 Verificando DNS..."
nslookup buypeer.com.br

# Verificar se o site responde
echo "🌐 Testando acesso ao site..."
if curl -s -o /dev/null -w "%{http_code}" http://buypeer.com.br | grep -q "200\|301\|302"; then
    echo "✅ Site está funcionando!"
    echo "🌐 URL: http://buypeer.com.br"
    echo "🔐 Admin: http://buypeer.com.br/login"
    echo "📧 Login: admin@example.com"
    echo "🔑 Senha: admin123"
else
    echo "❌ Site ainda não está acessível"
    echo "📋 Verifique a configuração DNS no Hostinger"
    echo "📖 Consulte o arquivo CONFIGURACAO_DOMINIO.md"
fi

# Verificar HTTPS
echo "🔒 Testando HTTPS..."
if curl -s -o /dev/null -w "%{http_code}" https://buypeer.com.br | grep -q "200\|301\|302"; then
    echo "✅ HTTPS está funcionando!"
else
    echo "⚠️ HTTPS ainda não configurado"
fi
