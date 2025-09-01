#!/usr/bin/env python3
"""
Team Manager - Coordenador Principal dos Agentes BuyPeer
Gerencia e coordena todos os agentes automaticamente
"""

import asyncio
import json
import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime
import os
import sys

# Adicionar o diretório raiz ao path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.architect import ArchitectAgent
from agents.context_agent import ContextAgent
from agents.backend import BackendAgent
from agents.frontend import FrontendAgent
from agents.devops import DevOpsAgent
from agents.qa import QAAgent
from agents.test_automation_agent import TestAutomationAgent
from agents.automation_agent import AutomationAgent
from agents.payments import PaymentsAgent
from agents.data import DataAgent
from agents.security import SecurityAgent
from agents.context_agent import ContextAgent

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/team_manager.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

@dataclass
class Task:
    """Representa uma tarefa no sistema"""
    id: str
    title: str
    description: str
    agent: str
    priority: str = "medium"
    status: str = "pending"
    created_at: datetime = None
    completed_at: datetime = None
    estimated_time: str = "1-2 hours"
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()

@dataclass
class ProjectStatus:
    """Status do projeto"""
    total_tasks: int = 0
    completed_tasks: int = 0
    pending_tasks: int = 0
    bugs_found: int = 0
    bugs_fixed: int = 0
    performance_score: float = 0.0
    security_score: float = 0.0

class TeamManager:
    """
    Gerenciador principal do time de agentes
    Coordena automaticamente todos os agentes
    """
    
    def __init__(self, project_path: str = None):
        self.project_path = project_path or os.getcwd()
        self.agents = {}
        self.tasks = []
        self.project_status = ProjectStatus()
        self.active = False
        
        # Inicializar agentes
        self._initialize_agents()
        
        logger.info("Team Manager inicializado com sucesso!")
    
    def _initialize_agents(self):
        """Inicializa todos os agentes"""
        try:
            self.agents = {
                'architect': ArchitectAgent(self.project_path),
                'context': ContextAgent(self.project_path),
                'backend': BackendAgent(self.project_path),
                'frontend': FrontendAgent(self.project_path),
                'devops': DevOpsAgent(self.project_path),
                'qa': QAAgent(self.project_path),
                'test_automation': TestAutomationAgent(self.project_path),
                'automation': AutomationAgent(self.project_path),
                'payments': PaymentsAgent(self.project_path),
                'data': DataAgent(self.project_path),
                'security': SecurityAgent(self.project_path)
            }
            logger.info(f"✅ {len(self.agents)} agentes inicializados")
        except Exception as e:
            logger.error(f"❌ Erro ao inicializar agentes: {e}")
    
    async def activate_team(self) -> Dict[str, Any]:
        """Ativa todo o time de agentes"""
        try:
            self.active = True
            results = {}
            
            # Ativar todos os agentes
            for name, agent in self.agents.items():
                logger.info(f"🔄 Ativando agente: {name}")
                result = await agent.activate()
                results[name] = result
            
            logger.info("🎉 Time completo ativado!")
            return {
                'status': 'success',
                'message': 'Time completo ativado com sucesso!',
                'agents': results
            }
        except Exception as e:
            logger.error(f"❌ Erro ao ativar time: {e}")
            return {
                'status': 'error',
                'message': f'Erro ao ativar time: {e}'
            }
    
    async def activate_specific_agent(self, agent_name: str) -> Dict[str, Any]:
        """Ativa um agente específico"""
        try:
            if agent_name not in self.agents:
                return {
                    'status': 'error',
                    'message': f'Agente {agent_name} não encontrado'
                }
            
            logger.info(f"🔄 Ativando agente específico: {agent_name}")
            result = await self.agents[agent_name].activate()
            
            return {
                'status': 'success',
                'message': f'Agente {agent_name} ativado com sucesso!',
                'agent': result
            }
        except Exception as e:
            logger.error(f"❌ Erro ao ativar agente {agent_name}: {e}")
            return {
                'status': 'error',
                'message': f'Erro ao ativar agente {agent_name}: {e}'
            }
    
    async def process_request(self, request: str) -> Dict[str, Any]:
        """Processa uma solicitação do usuário"""
        try:
            logger.info(f"📋 Processando solicitação: {request}")
            
            # O agente de contexto obtém documentação e contexto atualizado
            context_agent = self.agents['context']
            context_info = await context_agent.get_context_for_request(request)
            
            # O arquiteto analisa a solicitação com contexto atualizado
            architect = self.agents['architect']
            analysis = await architect.analyze_request(request)
            
            # Enriquecer análise com contexto
            if context_info['status'] == 'success':
                analysis['context'] = context_info['context']
            
            # Criar tarefas baseadas na análise
            tasks = await self._create_tasks_from_analysis(analysis)
            
            # Executar tarefas em paralelo
            results = await self._execute_tasks(tasks)
            
            # Gerar relatório final
            report = await self._generate_report(results)
            
            return {
                'status': 'success',
                'context': context_info,
                'analysis': analysis,
                'tasks': tasks,
                'results': results,
                'report': report
            }
        except Exception as e:
            logger.error(f"❌ Erro ao processar solicitação: {e}")
            return {
                'status': 'error',
                'message': f'Erro ao processar solicitação: {e}'
            }
    
    async def _create_tasks_from_analysis(self, analysis: Dict[str, Any]) -> List[Task]:
        """Cria tarefas baseadas na análise do arquiteto"""
        tasks = []
        task_id = 1
        
        for agent_name, agent_tasks in analysis.get('delegated_tasks', {}).items():
            for task_desc in agent_tasks:
                task = Task(
                    id=f"task_{task_id}",
                    title=task_desc,
                    description=task_desc,
                    agent=agent_name,
                    priority="high" if "crítico" in task_desc.lower() else "medium"
                )
                tasks.append(task)
                task_id += 1
        
        self.tasks.extend(tasks)
        return tasks
    
    async def _execute_tasks(self, tasks: List[Task]) -> Dict[str, Any]:
        """Executa as tarefas em paralelo"""
        results = {}
        
        # Agrupar tarefas por agente
        tasks_by_agent = {}
        for task in tasks:
            if task.agent not in tasks_by_agent:
                tasks_by_agent[task.agent] = []
            tasks_by_agent[task.agent].append(task)
        
        # Executar tarefas de cada agente
        for agent_name, agent_tasks in tasks_by_agent.items():
            if agent_name in self.agents:
                logger.info(f"🔧 Executando tarefas do agente: {agent_name}")
                agent = self.agents[agent_name]
                result = await agent.execute_tasks(agent_tasks)
                results[agent_name] = result
                
                # Atualizar status das tarefas
                for task in agent_tasks:
                    task.status = "completed"
                    task.completed_at = datetime.now()
        
        return results
    
    async def _generate_report(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Gera relatório final"""
        total_tasks = len(self.tasks)
        completed_tasks = len([t for t in self.tasks if t.status == "completed"])
        
        report = {
            'summary': {
                'total_tasks': total_tasks,
                'completed_tasks': completed_tasks,
                'success_rate': (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
            },
            'agent_results': results,
            'recommendations': [],
            'next_steps': []
        }
        
        # Gerar recomendações
        if completed_tasks == total_tasks:
            report['recommendations'].append("✅ Todas as tarefas foram concluídas com sucesso!")
            report['next_steps'].append("🚀 Pronto para deploy em produção")
        else:
            report['recommendations'].append("⚠️ Algumas tarefas ainda estão pendentes")
            report['next_steps'].append("🔧 Revisar tarefas pendentes")
        
        return report
    
    async def get_status(self) -> Dict[str, Any]:
        """Retorna status atual do time"""
        status = {
            'active': self.active,
            'agents': {},
            'tasks': {
                'total': len(self.tasks),
                'completed': len([t for t in self.tasks if t.status == "completed"]),
                'pending': len([t for t in self.tasks if t.status == "pending"])
            },
            'project_status': self.project_status
        }
        
        # Status de cada agente
        for name, agent in self.agents.items():
            status['agents'][name] = {
                'active': agent.is_active,
                'status': agent.get_status()
            }
        
        return status
    
    async def stop_team(self) -> Dict[str, Any]:
        """Para todo o time"""
        try:
            self.active = False
            for name, agent in self.agents.items():
                await agent.deactivate()
            
            logger.info("🛑 Time parado com sucesso!")
            return {
                'status': 'success',
                'message': 'Time parado com sucesso!'
            }
        except Exception as e:
            logger.error(f"❌ Erro ao parar time: {e}")
            return {
                'status': 'error',
                'message': f'Erro ao parar time: {e}'
            }

# Função principal para uso direto
async def main():
    """Função principal para teste"""
    manager = TeamManager()
    
    # Ativar time
    result = await manager.activate_team()
    print(json.dumps(result, indent=2, default=str))
    
    # Processar solicitação de exemplo
    request = "Preciso implementar um sistema de cupons de desconto"
    result = await manager.process_request(request)
    print(json.dumps(result, indent=2, default=str))
    
    # Status do time
    status = await manager.get_status()
    print(json.dumps(status, indent=2, default=str))

if __name__ == "__main__":
    asyncio.run(main())
