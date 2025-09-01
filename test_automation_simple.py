#!/usr/bin/env python3
"""
Teste simples do agente de automação
"""

import asyncio
import sys
import os

# Adicionar o diretório agents ao path
sys.path.append(os.path.join(os.path.dirname(__file__), 'agents'))

async def test_automation():
    """Testa o agente de automação"""
    try:
        from automation_agent import AutomationAgent
        print("✅ Importação bem-sucedida!")
        
        # Criar instância
        agent = AutomationAgent(os.getcwd())
        print("✅ Instância criada!")
        
        # Ativar agente
        activation = await agent.activate()
        print(f"✅ Ativação: {activation}")
        
        # Testar comando simples
        result = await agent.execute_command("verificar status do sistema")
        print(f"✅ Resultado: {result}")
        
        # Desativar agente
        await agent.deactivate()
        print("✅ Teste concluído!")
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_automation())
