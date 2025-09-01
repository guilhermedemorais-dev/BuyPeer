#!/usr/bin/env python3
"""
Script de Teste - Sistema de Agentes Orquestrado BuyPeer
Demonstra o funcionamento do sistema com MCPs e OpenAI
"""

import asyncio
import json
import logging
import sys
import os

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Adicionar diretório agents ao path
sys.path.append(os.path.join(os.path.dirname(__file__), 'agents'))

# Importar sistema de agentes
from agents import initialize_system, process_request, get_system_status, shutdown_system

async def test_system():
    """Testa o sistema completo de agentes"""
    
    print("🚀 TESTE DO SISTEMA DE AGENTES ORQUESTRADO")
    print("=" * 50)
    
    try:
        # 1. Inicializar sistema
        print("\n1️⃣ INICIALIZANDO SISTEMA...")
        init_result = await initialize_system()
        print(f"✅ Resultado: {json.dumps(init_result, indent=2)}")
        
        if init_result['status'] != 'success':
            print("❌ Falha na inicialização do sistema")
            return
        
        # 2. Obter status do sistema
        print("\n2️⃣ STATUS DO SISTEMA...")
        status = await get_system_status()
        print(f"✅ Status: {json.dumps(status, indent=2)}")
        
        # 3. Testar solicitações
        test_requests = [
            "Preciso implementar um sistema de cupons de desconto",
            "Criar uma API para gerenciar produtos",
            "Implementar autenticação com Sanctum",
            "Configurar testes automatizados",
            "Otimizar performance do banco de dados"
        ]
        
        print("\n3️⃣ TESTANDO SOLICITAÇÕES...")
        for i, request in enumerate(test_requests, 1):
            print(f"\n📋 Teste {i}: {request}")
            result = await process_request(request)
            print(f"✅ Resultado: {json.dumps(result, indent=2)}")
            
            # Aguardar um pouco entre as solicitações
            await asyncio.sleep(1)
        
        # 4. Desligar sistema
        print("\n4️⃣ DESLIGANDO SISTEMA...")
        shutdown_result = await shutdown_system()
        print(f"✅ Resultado: {json.dumps(shutdown_result, indent=2)}")
        
        print("\n🎉 TESTE CONCLUÍDO COM SUCESSO!")
        
    except Exception as e:
        logger.error(f"❌ Erro no teste: {e}")
        print(f"❌ Erro: {e}")

async def test_mcp_integration():
    """Testa integração específica com MCPs"""
    
    print("\n🔧 TESTE DE INTEGRAÇÃO COM MCPs")
    print("=" * 40)
    
    try:
        # Inicializar sistema
        await initialize_system()
        
        # Testar MCPs específicos
        from agents.mcp_config import mcp_manager
        
        # Listar MCPs disponíveis
        mcps = await mcp_manager.list_available_mcps()
        print(f"✅ MCPs disponíveis: {json.dumps(mcps, indent=2)}")
        
        # Testar operações específicas
        test_operations = [
            ('filesystem', 'list_directory', {'path': '.'}),
            ('git', 'status', {}),
            ('context7', 'save', {'key': 'test', 'data': {'message': 'Teste MCP'}})
        ]
        
        for mcp_name, operation, params in test_operations:
            print(f"\n🔧 Testando MCP {mcp_name} - {operation}")
            result = await mcp_manager.execute_mcp_command(mcp_name, operation, **params)
            print(f"✅ Resultado: {json.dumps(result, indent=2)}")
        
        # Desligar sistema
        await shutdown_system()
        
    except Exception as e:
        logger.error(f"❌ Erro no teste MCP: {e}")

async def test_agent_communication():
    """Testa comunicação entre agentes"""
    
    print("\n📨 TESTE DE COMUNICAÇÃO ENTRE AGENTES")
    print("=" * 45)
    
    try:
        # Inicializar sistema
        await initialize_system()
        
        from agents.communication import communication_hub
        
        # Testar criação de tarefas
        task_result = await communication_hub.create_task(
            description="Teste de comunicação entre agentes",
            agent_type="backend",
            priority="high"
        )
        print(f"✅ Tarefa criada: {json.dumps(task_result, indent=2)}")
        
        # Testar delegação de tarefa
        if task_result['status'] == 'success':
            delegate_result = await communication_hub.delegate_task(task_result['task_id'])
            print(f"✅ Tarefa delegada: {json.dumps(delegate_result, indent=2)}")
        
        # Testar envio de mensagem
        message_result = await communication_hub.send_message(
            from_agent="test_agent",
            to_agent="backend",
            message_type="test_message",
            content={"test": "data"}
        )
        print(f"✅ Mensagem enviada: {json.dumps(message_result, indent=2)}")
        
        # Obter resumo da comunicação
        summary = await communication_hub.get_communication_summary()
        print(f"✅ Resumo: {json.dumps(summary, indent=2)}")
        
        # Desligar sistema
        await shutdown_system()
        
    except Exception as e:
        logger.error(f"❌ Erro no teste de comunicação: {e}")

async def main():
    """Função principal"""
    
    print("🎼 SISTEMA DE AGENTES ORQUESTRADO BUYPEER")
    print("Integração com MCPs e OpenAI")
    print("=" * 60)
    
    # Executar testes
    await test_system()
    await test_mcp_integration()
    await test_agent_communication()
    
    print("\n🎉 TODOS OS TESTES CONCLUÍDOS!")

if __name__ == "__main__":
    asyncio.run(main())
