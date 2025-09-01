#!/usr/bin/env python3
"""
Script para executar automação específica do BuyPeer
- Inicia servidor Laravel
- Roda testes automatizados
"""

import asyncio
import sys
import os

# Adicionar o diretório agents ao path
sys.path.append(os.path.join(os.path.dirname(__file__), 'agents'))

from automation_agent import AutomationAgent

async def main():
    """Função principal"""
    print("🚀 AUTOMAÇÃO BUYPEER - INICIANDO SERVIDOR E TESTES")
    print("=" * 60)
    
    # Inicializar agente de automação
    automation_agent = AutomationAgent(os.getcwd())
    
    try:
        # Ativar agente
        print("🔄 Ativando agente de automação...")
        activation = await automation_agent.activate()
        
        if activation['status'] == 'success':
            print("✅ Agente ativado com sucesso!")
        else:
            print(f"❌ Erro ao ativar agente: {activation['message']}")
            return
        
        # 1. Iniciar servidor Laravel
        print("\n🚀 INICIANDO SERVIDOR LARAVEL...")
        print("-" * 40)
        
        server_result = await automation_agent.execute_command("iniciar servidor laravel")
        
        if server_result['status'] == 'success':
            print(f"✅ {server_result['message']}")
            if 'url' in server_result:
                print(f"🌐 URL: {server_result['url']}")
            if 'pid' in server_result:
                print(f"🆔 PID: {server_result['pid']}")
        else:
            print(f"❌ Erro ao iniciar servidor: {server_result['message']}")
            return
        
        # Aguardar servidor inicializar completamente
        print("⏳ Aguardando servidor inicializar...")
        await asyncio.sleep(10)
        
        # 2. Verificar status do sistema
        print("\n📊 VERIFICANDO STATUS DO SISTEMA...")
        print("-" * 40)
        
        status_result = await automation_agent.execute_command("verificar status do sistema")
        
        if status_result['status'] == 'success':
            print("✅ Status do sistema:")
            if 'server' in status_result:
                server_status = "🟢 Rodando" if status_result['server']['running'] else "🔴 Parado"
                print(f"   🚀 Servidor: {server_status}")
            if 'system' in status_result:
                sys_info = status_result['system']
                print(f"   💻 CPU: {sys_info['cpu_percent']}%")
                print(f"   🧠 Memória: {sys_info['memory_percent']}%")
        else:
            print(f"❌ Erro ao verificar status: {status_result['message']}")
        
        # 3. Executar testes automatizados
        print("\n🧪 EXECUTANDO TESTES AUTOMATIZADOS...")
        print("-" * 40)
        
        test_result = await automation_agent.execute_command("executar testes e2e completos")
        
        if test_result['status'] == 'success':
            print(f"✅ {test_result['message']}")
            
            if 'tests' in test_result:
                print("🧪 Testes executados:")
                for test in test_result['tests']:
                    status_icon = "✅" if test['status'] == 'passed' else "❌"
                    print(f"   {status_icon} {test['name']}: {test['result']}")
            
            if 'success_rate' in test_result:
                print(f"📈 Taxa de sucesso: {test_result['success_rate']}%")
            
            if 'screenshot' in test_result:
                print(f"📸 Screenshot: {test_result['screenshot']}")
        else:
            print(f"❌ Erro nos testes: {test_result['message']}")
        
        # 4. Abrir navegador para verificar
        print("\n🌐 ABRINDO NAVEGADOR PARA VERIFICAÇÃO...")
        print("-" * 40)
        
        browser_result = await automation_agent.execute_command("abrir navegador e testar frontend")
        
        if browser_result['status'] == 'success':
            print(f"✅ {browser_result['message']}")
            if 'url' in browser_result:
                print(f"🌐 URL: {browser_result['url']}")
            if 'title' in browser_result:
                print(f"📄 Título: {browser_result['title']}")
        else:
            print(f"❌ Erro ao abrir navegador: {browser_result['message']}")
        
        print("\n" + "=" * 60)
        print("🎉 AUTOMAÇÃO CONCLUÍDA COM SUCESSO!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Erro durante a automação: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        # Desativar agente
        print("\n🔄 Desativando agente...")
        await automation_agent.deactivate()
        print("✅ Sistema encerrado!")

if __name__ == "__main__":
    asyncio.run(main())
