#!/usr/bin/env python3
"""
Orquestrador Principal - Sistema de Agentes BuyPeer
Gerencia todos os agentes e MCPs de forma centralizada
"""

import asyncio
import json
import logging
import os
from typing import Dict, Any, List, Optional
from datetime import datetime

# Importar módulos do sistema
from .mcp_config import mcp_manager
from .communication import communication_hub
from .architect import ArchitectAgent
from .base_agent import BaseAgent

logger = logging.getLogger(__name__)

class AgentOrchestrator:
    """
    Orquestrador Principal do Sistema de Agentes
    Gerencia todos os agentes e MCPs de forma centralizada
    """
    
    def __init__(self, project_path: str = None):
        self.project_path = project_path or os.getcwd()
        self.is_active = False
        self.architect = None
        self.agents = {}
        self.mcp_manager = mcp_manager
        self.communication_hub = communication_hub
        
        logger.info("🎼 Agent Orchestrator inicializado")
    
    async def initialize(self) -> Dict[str, Any]:
        """Inicializa o orquestrador e todos os sistemas"""
        try:
            logger.info("🚀 Inicializando Agent Orchestrator...")
            
            # 1. Inicializar MCP Manager
            mcp_result = await self.mcp_manager.initialize()
            logger.info(f"🔧 MCP Manager: {mcp_result['status']}")
            
            # 2. Inicializar Communication Hub
            self.communication_hub.is_active = True
            logger.info("🔗 Communication Hub ativado")
            
            # 3. Inicializar Architect Agent
            self.architect = ArchitectAgent(self.project_path)
            architect_result = await self.architect.activate()
            logger.info(f"🏗️ Architect Agent: {architect_result['status']}")
            
            # 4. Registrar agentes básicos
            await self._register_basic_agents()
            
            self.is_active = True
            
            return {
                'status': 'success',
                'message': 'Agent Orchestrator inicializado com sucesso',
                'mcp_status': mcp_result,
                'architect_status': architect_result,
                'registered_agents': list(self.agents.keys())
            }
            
        except Exception as e:
            logger.error(f"❌ Erro ao inicializar Agent Orchestrator: {e}")
            return {
                'status': 'error',
                'message': f'Erro na inicialização: {e}'
            }
    
    async def _register_basic_agents(self):
        """Registra agentes básicos no sistema"""
        try:
            # Aqui você pode importar e registrar agentes específicos
            # Por enquanto, vamos criar agentes básicos
            
            basic_agents = {
                'backend': {
                    'name': 'Backend Agent',
                    'capabilities': ['APIs', 'Modelos', 'Controllers', 'Migrações']
                },
                'frontend': {
                    'name': 'Frontend Agent',
                    'capabilities': ['Vue.js', 'UI/UX', 'Componentes', 'Responsividade']
                },
                'devops': {
                    'name': 'DevOps Agent',
                    'capabilities': ['Deploy', 'Docker', 'CI/CD', 'Monitoramento']
                },
                'qa': {
                    'name': 'QA Agent',
                    'capabilities': ['Testes', 'Validação', 'Performance', 'Segurança']
                },
                'payments': {
                    'name': 'Payments Agent',
                    'capabilities': ['Gateways', 'Transações', 'Webhooks', 'Compliance']
                },
                'security': {
                    'name': 'Security Agent',
                    'capabilities': ['Autenticação', 'Autorização', 'PCI', 'LGPD']
                },
                'data': {
                    'name': 'Data Agent',
                    'capabilities': ['Analytics', 'Relatórios', 'Dashboards', 'Otimização']
                }
            }
            
            for agent_id, agent_info in basic_agents.items():
                # Criar agente básico
                agent = BasicAgent(agent_id, agent_info['name'], agent_info['capabilities'])
                
                # Ativar agente
                await agent.activate()
                
                # Registrar no orquestrador
                self.agents[agent_id] = agent
                
                logger.info(f"✅ Agente {agent_id} registrado")
            
        except Exception as e:
            logger.error(f"❌ Erro ao registrar agentes básicos: {e}")
    
    async def process_request(self, request: str) -> Dict[str, Any]:
        """Processa uma solicitação usando o Architect Agent"""
        try:
            if not self.is_active:
                return {
                    'status': 'error',
                    'message': 'Agent Orchestrator não está ativo'
                }
            
            logger.info(f"📋 Processando solicitação: {request}")
            
            # 1. Analisar solicitação com Architect
            analysis_result = await self.architect.analyze_request(request)
            
            if analysis_result['status'] != 'success':
                return analysis_result
            
            # 2. Executar plano de análise
            execution_result = await self.architect.execute_analysis_plan(analysis_result)
            
            # 3. Coletar resultados
            results = await self._collect_results()
            
            return {
                'status': 'success',
                'message': 'Solicitação processada com sucesso',
                'analysis': analysis_result['analysis'],
                'execution': execution_result,
                'results': results
            }
            
        except Exception as e:
            logger.error(f"❌ Erro ao processar solicitação: {e}")
            return {
                'status': 'error',
                'message': f'Erro no processamento: {e}'
            }
    
    async def _collect_results(self) -> Dict[str, Any]:
        """Coleta resultados de todos os agentes"""
        results = {}
        
        for agent_id, agent in self.agents.items():
            try:
                status = await agent.get_status()
                results[agent_id] = status
            except Exception as e:
                logger.warning(f"⚠️ Erro ao coletar status do agente {agent_id}: {e}")
                results[agent_id] = {'error': str(e)}
        
        return results
    
    async def get_system_status(self) -> Dict[str, Any]:
        """Obtém status completo do sistema"""
        return {
            'status': 'success',
            'orchestrator_active': self.is_active,
            'mcp_manager_initialized': self.mcp_manager.is_initialized,
            'communication_hub_active': self.communication_hub.is_active,
            'architect_active': self.architect.is_active if self.architect else False,
            'registered_agents': list(self.agents.keys()),
            'agent_status': await self._collect_results(),
            'available_mcps': await self.mcp_manager.list_available_mcps() if self.mcp_manager.is_initialized else []
        }
    
    async def shutdown(self) -> Dict[str, Any]:
        """Desliga o orquestrador e todos os agentes"""
        try:
            logger.info("🔄 Desligando Agent Orchestrator...")
            
            # Desativar agentes
            for agent_id, agent in self.agents.items():
                try:
                    await agent.deactivate()
                    logger.info(f"✅ Agente {agent_id} desativado")
                except Exception as e:
                    logger.warning(f"⚠️ Erro ao desativar agente {agent_id}: {e}")
            
            # Desativar architect
            if self.architect:
                await self.architect.deactivate()
                logger.info("✅ Architect Agent desativado")
            
            # Desativar communication hub
            self.communication_hub.is_active = False
            logger.info("✅ Communication Hub desativado")
            
            self.is_active = False
            
            return {
                'status': 'success',
                'message': 'Agent Orchestrator desligado com sucesso'
            }
            
        except Exception as e:
            logger.error(f"❌ Erro ao desligar Agent Orchestrator: {e}")
            return {
                'status': 'error',
                'message': f'Erro no desligamento: {e}'
            }

class BasicAgent(BaseAgent):
    """
    Agente básico para demonstração
    Pode ser substituído por agentes especializados
    """
    
    def __init__(self, agent_id: str, agent_name: str, capabilities: List[str]):
        super().__init__(agent_name)
        self.agent_id = agent_id
        self.capabilities = capabilities
    
    async def _initialize_capabilities(self):
        """Inicializa capacidades do agente básico"""
        logger.info(f"🔧 {self.agent_name} - Capacidades: {self.capabilities}")
    
    async def execute_task(self, task_description: str, parameters: Dict[str, Any] = None) -> Dict[str, Any]:
        """Executa uma tarefa básica"""
        try:
            logger.info(f"🚀 {self.agent_name} executando: {task_description}")
            
            # Simular execução da tarefa
            await asyncio.sleep(1)
            
            # Salvar contexto
            await self.save_context(f"task_{self.agent_id}_{datetime.now().timestamp()}", {
                'description': task_description,
                'parameters': parameters,
                'agent': self.agent_name,
                'timestamp': datetime.now().isoformat()
            })
            
            result = {
                'status': 'success',
                'message': f'Tarefa executada por {self.agent_name}',
                'task_description': task_description,
                'agent_id': self.agent_id,
                'execution_time': '1s'
            }
            
            # Registrar tarefa
            await self.log_task(task_description, result)
            
            return result
            
        except Exception as e:
            logger.error(f"❌ Erro ao executar tarefa em {self.agent_name}: {e}")
            return {
                'status': 'error',
                'message': f'Erro na execução: {e}'
            }

# Instância global do orquestrador
orchestrator = AgentOrchestrator()

async def main():
    """Função principal para teste do orquestrador"""
    try:
        # Inicializar orquestrador
        result = await orchestrator.initialize()
        print("Inicialização:", json.dumps(result, indent=2))
        
        # Processar solicitação de teste
        test_request = "Preciso implementar um sistema de cupons de desconto"
        result = await orchestrator.process_request(test_request)
        print("Processamento:", json.dumps(result, indent=2))
        
        # Obter status do sistema
        status = await orchestrator.get_system_status()
        print("Status:", json.dumps(status, indent=2))
        
        # Desligar orquestrador
        await orchestrator.shutdown()
        
    except Exception as e:
        logger.error(f"❌ Erro no teste: {e}")

if __name__ == "__main__":
    asyncio.run(main())
