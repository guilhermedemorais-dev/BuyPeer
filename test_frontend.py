#!/usr/bin/env python3
"""
Script para testar o frontend do BuyPeer
Executa testes automatizados no navegador
"""

import asyncio
import json
import sys
import os

# Adicionar o diretório agents ao path
sys.path.append(os.path.join(os.path.dirname(__file__), 'agents'))

from test_automation_agent import TestAutomationAgent

async def test_buypeer_frontend():
    """Testa o frontend do BuyPeer"""
    print("🧪 TESTE AUTOMATIZADO - BUYPEER FRONTEND")
    print("=" * 50)
    
    # Inicializar agente de testes
    test_agent = TestAutomationAgent(os.getcwd())
    
    # Ativar agente
    print("🔄 Ativando agente de testes...")
    activation = await test_agent.activate()
    
    if activation['status'] == 'success':
        print("✅ Agente ativado com sucesso!")
        print(f"🌐 Navegadores disponíveis: {list(activation['browser_status'].keys())}")
    else:
        print(f"❌ Erro ao ativar agente: {activation['message']}")
        return
    
    # Verificar se o servidor está rodando
    print("\n🔍 Verificando servidor local...")
    try:
        import requests
        response = requests.get("http://localhost:8000", timeout=5)
        if response.status_code == 200:
            print("✅ Servidor Laravel rodando em http://localhost:8000")
        else:
            print(f"⚠️ Servidor respondendo com status: {response.status_code}")
    except Exception as e:
        print(f"❌ Erro ao conectar com servidor: {e}")
        print("💡 Certifique-se de que o servidor está rodando: php artisan serve")
        return
    
    # Executar testes E2E
    print("\n🧪 Executando testes E2E...")
    print("🌐 Abrindo navegador...")
    
    test_result = await test_agent.run_test_suite("ecommerce_basic")
    
    if test_result['status'] == 'success':
        print("✅ Testes concluídos com sucesso!")
        
        # Mostrar resumo
        report = test_result['report']
        summary = report['summary']
        
        print(f"\n📊 RESUMO DOS TESTES:")
        print(f"   Total de testes: {summary['total_tests']}")
        print(f"   ✅ Passaram: {summary['passed']}")
        print(f"   ❌ Falharam: {summary['failed']}")
        print(f"   ⚠️ Erros: {summary['errors']}")
        print(f"   📈 Taxa de sucesso: {summary['success_rate']}%")
        
        # Mostrar detalhes dos testes
        print(f"\n📋 DETALHES DOS TESTES:")
        for result in test_result['results']:
            status_icon = "✅" if result['status'] == 'passed' else "❌"
            print(f"   {status_icon} {result['test_id']}: {result['status']} ({result['duration']:.2f}s)")
            if result.get('screenshot_path'):
                print(f"      📸 Screenshot: {result['screenshot_path']}")
        
        # Recomendações
        print(f"\n💡 RECOMENDAÇÕES:")
        if summary['success_rate'] >= 80:
            print("   🎉 Frontend funcionando bem!")
        elif summary['success_rate'] >= 60:
            print("   ⚠️ Alguns problemas detectados, verificar logs")
        else:
            print("   🚨 Problemas críticos detectados, revisão necessária")
            
    else:
        print(f"❌ Erro nos testes: {test_result['message']}")
    
    # Desativar agente
    await test_agent.deactivate()
    print("\n🏁 Teste concluído!")

if __name__ == "__main__":
    asyncio.run(test_buypeer_frontend())
