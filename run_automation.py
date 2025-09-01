#!/usr/bin/env python3
"""
Script Principal de Automação BuyPeer
Executa comandos automaticamente usando o Agente de Automação
"""

import asyncio
import json
import sys
import os

# Adicionar o diretório agents ao path
sys.path.append(os.path.join(os.path.dirname(__file__), 'agents'))

from automation_agent import AutomationAgent

async def main():
    """Função principal"""
    print("🤖 SISTEMA DE AUTOMAÇÃO BUYPEER")
    print("=" * 50)
    print("🎯 Digite comandos e o sistema fará TUDO automaticamente!")
    print("💡 Exemplos:")
    print("   - 'iniciar servidor laravel'")
    print("   - 'abrir navegador e testar frontend'")
    print("   - 'executar testes e2e completos'")
    print("   - 'verificar status do sistema'")
    print("   - 'sair' para encerrar")
    print("=" * 50)
    
    # Inicializar agente de automação
    automation_agent = AutomationAgent(os.getcwd())
    
    # Ativar agente
    print("🔄 Ativando agente de automação...")
    activation = await automation_agent.activate()
    
    if activation['status'] == 'success':
        print("✅ Agente ativado com sucesso!")
        print(f"🚀 Capacidades: {', '.join(activation['capabilities'])}")
    else:
        print(f"❌ Erro ao ativar agente: {activation['message']}")
        return
    
    print("\n🎯 Digite seu comando:")
    
    try:
        while True:
            # Ler comando do usuário
            command = input("\n📝 Comando: ").strip()
            
            if command.lower() in ['sair', 'exit', 'quit']:
                break
            
            if not command:
                continue
            
            print(f"\n🤖 Executando: {command}")
            print("⏳ Aguarde...")
            
            # Executar comando
            try:
                result = await automation_agent.execute_command(command)
            except Exception as e:
                result = {
                    'status': 'error',
                    'message': f'Erro ao executar comando: {e}'
                }
            
            # Mostrar resultado
            print(f"\n📊 RESULTADO:")
            print("-" * 30)
            
            if result['status'] == 'success':
                print(f"✅ {result['message']}")
                
                # Mostrar detalhes específicos baseado no tipo de comando
                if 'servidor' in command.lower():
                    if 'url' in result:
                        print(f"🌐 URL: {result['url']}")
                    if 'pid' in result:
                        print(f"🆔 PID: {result['pid']}")
                
                elif 'navegador' in command.lower() or 'browser' in command.lower():
                    if 'url' in result:
                        print(f"🌐 URL: {result['url']}")
                    if 'title' in result:
                        print(f"📄 Título: {result['title']}")
                    if 'screenshot' in result:
                        print(f"📸 Screenshot: {result['screenshot']}")
                
                elif 'teste' in command.lower() or 'test' in command.lower():
                    if 'tests' in result:
                        print(f"🧪 Testes executados:")
                        for test in result['tests']:
                            status_icon = "✅" if test['status'] == 'passed' else "❌"
                            print(f"   {status_icon} {test['name']}: {test['result']}")
                    
                    if 'success_rate' in result:
                        print(f"📈 Taxa de sucesso: {result['success_rate']}%")
                    
                    if 'screenshot' in result:
                        print(f"📸 Screenshot: {result['screenshot']}")
                
                elif 'sistema' in command.lower() or 'system' in command.lower():
                    if 'server' in result:
                        server_status = "🟢 Rodando" if result['server']['running'] else "🔴 Parado"
                        print(f"🚀 Servidor: {server_status}")
                    
                    if 'browser' in result:
                        browser_status = "🟢 Aberto" if result['browser'] else "🔴 Fechado"
                        print(f"🌐 Navegador: {browser_status}")
                    
                    if 'system' in result:
                        sys_info = result['system']
                        print(f"💻 CPU: {sys_info['cpu_percent']}%")
                        print(f"🧠 Memória: {sys_info['memory_percent']}%")
                
                # Mostrar resultado completo se houver
                if 'result' in result:
                    print(f"📋 Detalhes: {result['result']}")
                    
            else:
                print(f"❌ Erro: {result['message']}")
            
            print("-" * 30)
            
    except KeyboardInterrupt:
        print("\n\n🛑 Interrompido pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro: {e}")
    finally:
        # Desativar agente
        print("\n🔄 Desativando agente...")
        await automation_agent.deactivate()
        print("✅ Sistema encerrado!")

if __name__ == "__main__":
    asyncio.run(main())
