#!/bin/bash

# MCP Helper Script para BuyPeer
# Comandos rápidos para gerenciar MCPs

echo "🚀 MCP HELPER - BUYPEER"
echo "========================"
echo ""
echo "Comandos disponíveis:"
echo ""
echo "📋 VALIDAÇÃO:"
echo "  check-mcps          - Validação completa de MCPs"
echo "  validate-buypeer    - Validação específica do BuyPeer"
echo "  mcp-status          - Status rápido dos MCPs"
echo ""
echo "🔧 CONFIGURAÇÃO:"
echo "  mcp-edit            - Editar arquivo mcp.json"
echo "  mcp-backup          - Fazer backup da configuração"
echo "  mcp-restore         - Restaurar backup"
echo ""
echo "📊 RELATÓRIOS:"
echo "  mcp-report          - Relatório detalhado"
echo "  mcp-tokens          - Listar tokens faltantes"
echo "  mcp-missing         - Listar MCPs faltantes"
echo ""
echo "🔄 AÇÕES:"
echo "  mcp-reload          - Recarregar configuração"
echo "  mcp-test            - Testar MCPs básicos"
echo "  mcp-clean           - Limpar cache MCP"
echo ""
echo "🎯 CURSOR ESPECÍFICO:"
echo "  cursor-status       - Status do Cursor"
echo "  cursor-config       - Ver configuração"
echo "  cursor-extensions   - Listar extensões"
echo "  cursor-workspace    - Info do workspace"
echo "  cursor-ai-models    - Modelos AI disponíveis"
echo "  cursor-performance  - Performance do Cursor"
echo ""

# Função para editar mcp.json
mcp_edit() {
    echo "📝 Editando mcp.json..."
    nano ~/.cursor/mcp.json
}

# Função para backup
mcp_backup() {
    echo "💾 Fazendo backup da configuração MCP..."
    cp ~/.cursor/mcp.json ~/.cursor/mcp.json.backup.$(date +%Y%m%d_%H%M%S)
    echo "✅ Backup criado!"
}

# Função para restaurar
mcp_restore() {
    echo "🔄 Restaurando backup..."
    if [ -f ~/.cursor/mcp.json.backup ]; then
        cp ~/.cursor/mcp.json.backup ~/.cursor/mcp.json
        echo "✅ Backup restaurado!"
    else
        echo "❌ Backup não encontrado!"
    fi
}

# Função para relatório
mcp_report() {
    echo "📊 Gerando relatório detalhado..."
    python3 /home/guilherme/Documentos/BuyPeer-main/check_mcps.py
}

# Função para tokens faltantes
mcp_tokens() {
    echo "🔑 Tokens faltantes:"
    python3 /home/guilherme/Documentos/BuyPeer-main/check_mcps.py | grep -A 50 "🔑 TOKENS FALTANDO:" | grep -v "🔑 TOKENS FALTANDO:"
}

# Função para MCPs faltantes
mcp_missing() {
    echo "❌ MCPs faltantes:"
    python3 /home/guilherme/Documentos/BuyPeer-main/check_mcps.py | grep -A 50 "❌ MCPs FALTANDO:" | grep -v "❌ MCPs FALTANDO:"
}

# Função para recarregar
mcp_reload() {
    echo "🔄 Recarregando configuração MCP..."
    echo "Reinicie o Cursor para aplicar as mudanças!"
}

# Função para testar
mcp_test() {
    echo "🧪 Testando MCPs básicos..."
    echo "1. Verificando npx..."
    if command -v npx &> /dev/null; then
        echo "✅ npx disponível"
    else
        echo "❌ npx não encontrado"
    fi
    
    echo "2. Verificando arquivo mcp.json..."
    if [ -f ~/.cursor/mcp.json ]; then
        echo "✅ mcp.json encontrado"
    else
        echo "❌ mcp.json não encontrado"
    fi
    
    echo "3. Verificando Node.js..."
    if command -v node &> /dev/null; then
        echo "✅ Node.js disponível: $(node --version)"
    else
        echo "❌ Node.js não encontrado"
    fi
}

# Função para limpar cache
mcp_clean() {
    echo "🧹 Limpando cache MCP..."
    rm -rf ~/.npm/_npx
    echo "✅ Cache limpo!"
}

# Verificar argumento
case "$1" in
    "edit")
        mcp_edit
        ;;
    "backup")
        mcp_backup
        ;;
    "restore")
        mcp_restore
        ;;
    "report")
        mcp_report
        ;;
    "tokens")
        mcp_tokens
        ;;
    "missing")
        mcp_missing
        ;;
    "reload")
        mcp_reload
        ;;
    "test")
        mcp_test
        ;;
    "clean")
        mcp_clean
        ;;
    "cursor-status")
        echo "🎯 Status do Cursor:"
        node /home/guilherme/Documentos/BuyPeer-main/cursor-mcp.js cursor_status 2>/dev/null || echo "❌ MCP do Cursor não disponível"
        ;;
    "cursor-config")
        echo "🎯 Configuração do Cursor:"
        node /home/guilherme/Documentos/BuyPeer-main/cursor-mcp.js cursor_config 2>/dev/null || echo "❌ MCP do Cursor não disponível"
        ;;
    "cursor-extensions")
        echo "🎯 Extensões do Cursor:"
        node /home/guilherme/Documentos/BuyPeer-main/cursor-mcp.js cursor_extensions 2>/dev/null || echo "❌ MCP do Cursor não disponível"
        ;;
    "cursor-workspace")
        echo "🎯 Workspace do Cursor:"
        node /home/guilherme/Documentos/BuyPeer-main/cursor-mcp.js cursor_workspace 2>/dev/null || echo "❌ MCP do Cursor não disponível"
        ;;
    "cursor-ai-models")
        echo "🎯 Modelos AI do Cursor:"
        node /home/guilherme/Documentos/BuyPeer-main/cursor-mcp.js cursor_ai_models 2>/dev/null || echo "❌ MCP do Cursor não disponível"
        ;;
    "cursor-performance")
        echo "🎯 Performance do Cursor:"
        node /home/guilherme/Documentos/BuyPeer-main/cursor-mcp.js cursor_performance 2>/dev/null || echo "❌ MCP do Cursor não disponível"
        ;;
    *)
        echo "Uso: $0 [comando]"
        echo ""
        echo "Comandos: edit, backup, restore, report, tokens, missing, reload, test, clean"
        echo "Cursor: cursor-status, cursor-config, cursor-extensions, cursor-workspace, cursor-ai-models, cursor-performance"
        ;;
esac
