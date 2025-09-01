#!/usr/bin/env python3
"""
Sistema de Agentes BuyPeer - Script Principal
Executa o time virtual de desenvolvimento automaticamente
"""

import asyncio
import json
import os
import sys
from agents.team_manager import TeamManager

async def main():
    """Função principal"""
    print("🚀 Sistema de Agentes BuyPeer")
    print("=" * 50)
    
    # Inicializar o gerenciador de time
    manager = TeamManager()
    
    # Ativar todo o time
    print("\n🔄 Ativando time completo...")
    result = await manager.activate_team()
    
    if result['status'] == 'success':
        print("✅ Time ativado com sucesso!")
        
        # Mostrar agentes ativos
        print("\n👥 Agentes Ativos:")
        for name, agent_result in result['agents'].items():
            status = "✅" if agent_result['status'] == 'success' else "❌"
            print(f"  {status} {name.capitalize()}")
        
        # Loop principal
        while True:
            print("\n" + "=" * 50)
            print("🎯 Digite sua solicitação (ou 'sair' para encerrar):")
            print("Exemplos:")
            print("  - 'Preciso implementar sistema de cupons de desconto'")
            print("  - 'O checkout está quebrando, preciso corrigir'")
            print("  - 'Quero otimizar a performance do site'")
            print("  - 'sair' para encerrar")
            
            request = input("\n📝 Sua solicitação: ").strip()
            
            if request.lower() in ['sair', 'exit', 'quit']:
                break
            
            if not request:
                continue
            
            print(f"\n🔧 Processando: {request}")
            print("⏳ Aguarde, os agentes estão trabalhando...")
            
            # Processar solicitação
            result = await manager.process_request(request)
            
            if result['status'] == 'success':
                print("\n📊 RESULTADO:")
                print("-" * 30)
                
                # Mostrar contexto
                if 'context' in result and result['context']['status'] == 'success':
                    context = result['context']['context']
                    print(f"🔍 Contexto Analisado:")
                    print(f"  📚 Tecnologias: {', '.join(context['technologies'])}")
                    if context['versions']:
                        print(f"  📦 Versões: {context['versions']}")
                    if context['recommendations']:
                        print(f"  💡 Recomendações:")
                        for rec in context['recommendations'][:3]:  # Mostrar apenas 3
                            print(f"    - {rec}")
                    print()
                
                # Mostrar análise
                analysis = result['analysis']
                print(f"📋 Requisitos identificados: {len(analysis['requirements'])}")
                print(f"⏱️ Tempo estimado: {analysis['estimated_time']}")
                
                # Mostrar tarefas delegadas
                print(f"\n🔧 Tarefas delegadas:")
                for agent, tasks in analysis['delegated_tasks'].items():
                    print(f"  👨‍💻 {agent.capitalize()}:")
                    for task in tasks:
                        print(f"    - {task}")
                
                # Mostrar riscos
                if analysis['risks']:
                    print(f"\n⚠️ Riscos identificados:")
                    for risk in analysis['risks']:
                        print(f"  - {risk}")
                
                # Mostrar recomendações
                if analysis['recommendations']:
                    print(f"\n💡 Recomendações:")
                    for rec in analysis['recommendations']:
                        print(f"  - {rec}")
                
                # Mostrar resultados da execução
                print(f"\n✅ Execução das tarefas:")
                for agent, agent_result in result['results'].items():
                    if agent_result['status'] == 'success':
                        print(f"  ✅ {agent.capitalize()}: {len(agent_result['results'])} tarefas concluídas")
                    else:
                        print(f"  ❌ {agent.capitalize()}: Erro na execução")
                
                # Mostrar relatório final
                report = result['report']
                print(f"\n📈 Relatório Final:")
                print(f"  📊 Total de tarefas: {report['summary']['total_tasks']}")
                print(f"  ✅ Tarefas concluídas: {report['summary']['completed_tasks']}")
                print(f"  📈 Taxa de sucesso: {report['summary']['success_rate']:.1f}%")
                
                if report['recommendations']:
                    print(f"\n🎯 Próximos passos:")
                    for step in report['recommendations']:
                        print(f"  - {step}")
                
            else:
                print(f"❌ Erro: {result['message']}")
        
        # Parar o time
        print("\n🛑 Parando time...")
        await manager.stop_team()
        print("✅ Time parado com sucesso!")
        
    else:
        print(f"❌ Erro ao ativar time: {result['message']}")

if __name__ == "__main__":
    # Criar diretório de logs se não existir
    os.makedirs('logs', exist_ok=True)
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n🛑 Sistema interrompido pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro no sistema: {e}")
        sys.exit(1)
