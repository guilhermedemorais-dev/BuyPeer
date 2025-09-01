#!/usr/bin/env python3
"""
Sistema de Comunicação Central entre Agentes
Gerencia comunicação e orquestração usando OpenAI
"""

import asyncio
import json
import logging
import os
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, asdict
from datetime import datetime
import openai

logger = logging.getLogger(__name__)

@dataclass
class Task:
    """Representa uma tarefa a ser executada"""
    id: str
    description: str
    agent_type: str
    priority: str = "normal"
    dependencies: List[str] = None
    parameters: Dict[str, Any] = None
    created_at: datetime = None
    status: str = "pending"
    result: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.dependencies is None:
            self.dependencies = []
        if self.parameters is None:
            self.parameters = {}
        if self.created_at is None:
            self.created_at = datetime.now()

@dataclass
class AgentMessage:
    """Mensagem entre agentes"""
    from_agent: str
    to_agent: str
    message_type: str
    content: Dict[str, Any]
    timestamp: datetime = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()

class CommunicationHub:
    """
    Hub central de comunicação entre agentes
    Usa OpenAI para interpretação de linguagem natural
    """
    
    def __init__(self, openai_api_key: str = None):
        self.openai_api_key = openai_api_key or os.getenv('OPENAI_API_KEY')
        self.tasks: Dict[str, Task] = {}
        self.messages: List[AgentMessage] = []
        self.agents: Dict[str, Any] = {}
        self.is_active = False
        
        # Configurar OpenAI (compatível com versões 0.x e 1.x)
        if self.openai_api_key:
            try:
                # Versão 0.x
                openai.api_key = self.openai_api_key
            except AttributeError:
                # Versão 1.x - não precisa configurar globalmente
                pass
        
        # Mapeamento de tipos de tarefas para agentes
        self.task_agent_mapping = {
            'backend': ['backend', 'data', 'security'],
            'frontend': ['frontend', 'qa'],
            'devops': ['devops', 'security'],
            'payments': ['payments', 'security', 'data'],
            'testing': ['qa', 'test_automation_agent'],
            'automation': ['automation_agent', 'test_automation_agent'],
            'context': ['context_agent'],
            'management': ['team_manager', 'architect']
        }
        
        logger.info("🔗 Communication Hub inicializado")
    
    async def register_agent(self, agent_name: str, agent_instance: Any) -> Dict[str, Any]:
        """Registra um agente no hub de comunicação"""
        try:
            self.agents[agent_name] = agent_instance
            logger.info(f"✅ Agente {agent_name} registrado no Communication Hub")
            
            return {
                'status': 'success',
                'message': f'Agente {agent_name} registrado com sucesso',
                'registered_agents': list(self.agents.keys())
            }
        except Exception as e:
            logger.error(f"❌ Erro ao registrar agente {agent_name}: {e}")
            return {
                'status': 'error',
                'message': f'Erro no registro: {e}'
            }
    
    async def analyze_request_with_openai(self, request: str) -> Dict[str, Any]:
        """Analisa uma solicitação usando OpenAI para determinar agentes necessários"""
        try:
            if not self.openai_api_key:
                return {
                    'status': 'error',
                    'message': 'OpenAI API key não configurada'
                }
            
            # Prompt para análise da solicitação
            prompt = f"""
            Analise a seguinte solicitação e determine quais agentes especializados são necessários para executá-la.
            
            Solicitação: {request}
            
            Agentes disponíveis:
            - architect: Orquestrador principal, análise de requisitos
            - backend: Desenvolvimento backend (Laravel, PHP, APIs)
            - frontend: Desenvolvimento frontend (Vue.js, CSS, UI/UX)
            - devops: Infraestrutura, deploy, CI/CD
            - payments: Gateways de pagamento, integrações financeiras
            - qa: Testes de qualidade, validação
            - security: Segurança, compliance, autenticação
            - data: Análise de dados, relatórios, banco de dados
            - automation_agent: Automação de processos
            - test_automation_agent: Testes automatizados
            - context_agent: Memória e contexto
            - team_manager: Coordenação entre agentes
            
            Responda em JSON com a seguinte estrutura:
            {{
                "analysis": "Análise detalhada da solicitação",
                "required_agents": ["lista", "de", "agentes", "necessários"],
                "task_breakdown": [
                    {{
                        "agent": "nome_do_agente",
                        "task": "descrição da tarefa específica",
                        "priority": "high|normal|low",
                        "dependencies": ["tarefas", "que", "devem", "vir", "antes"]
                    }}
                ],
                "estimated_complexity": "low|medium|high",
                "recommendations": ["recomendações", "adicionais"]
            }}
            """
            
            # Chamada para OpenAI (versão 1.x)
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": "Você é um analista especializado em arquitetura de software e coordenação de equipes de desenvolvimento."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.3,
                    max_tokens=1000
                )
                
                # Parse da resposta
                analysis_result = json.loads(response.choices[0].message.content)
            except AttributeError:
                # Fallback para versão mais recente da OpenAI
                client = openai.OpenAI(api_key=self.openai_api_key)
                response = client.chat.completions.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": "Você é um analista especializado em arquitetura de software e coordenação de equipes de desenvolvimento."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.3,
                    max_tokens=1000
                )
                
                # Parse da resposta
                analysis_result = json.loads(response.choices[0].message.content)
            
            return {
                'status': 'success',
                'analysis': analysis_result
            }
            
        except Exception as e:
            logger.error(f"❌ Erro na análise OpenAI: {e}")
            return {
                'status': 'error',
                'message': f'Erro na análise: {e}'
            }
    
    async def create_task(self, description: str, agent_type: str, **kwargs) -> Dict[str, Any]:
        """Cria uma nova tarefa"""
        try:
            task_id = f"task_{len(self.tasks) + 1}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            task = Task(
                id=task_id,
                description=description,
                agent_type=agent_type,
                priority=kwargs.get('priority', 'normal'),
                dependencies=kwargs.get('dependencies', []),
                parameters=kwargs.get('parameters', {})
            )
            
            self.tasks[task_id] = task
            
            logger.info(f"📋 Tarefa criada: {task_id} - {description}")
            
            return {
                'status': 'success',
                'task_id': task_id,
                'task': asdict(task)
            }
        except Exception as e:
            logger.error(f"❌ Erro ao criar tarefa: {e}")
            return {
                'status': 'error',
                'message': f'Erro na criação: {e}'
            }
    
    async def delegate_task(self, task_id: str) -> Dict[str, Any]:
        """Delega uma tarefa para o agente apropriado"""
        try:
            task = self.tasks.get(task_id)
            if not task:
                return {
                    'status': 'error',
                    'message': f'Tarefa {task_id} não encontrada'
                }
            
            # Verificar se o agente está registrado
            if task.agent_type not in self.agents:
                return {
                    'status': 'error',
                    'message': f'Agente {task.agent_type} não registrado'
                }
            
            # Enviar mensagem para o agente
            message = AgentMessage(
                from_agent="communication_hub",
                to_agent=task.agent_type,
                message_type="task_execution",
                content={
                    'task_id': task_id,
                    'description': task.description,
                    'parameters': task.parameters
                }
            )
            
            self.messages.append(message)
            
            # Atualizar status da tarefa
            task.status = "delegated"
            
            logger.info(f"📤 Tarefa {task_id} delegada para {task.agent_type}")
            
            return {
                'status': 'success',
                'message': f'Tarefa delegada para {task.agent_type}',
                'task_id': task_id
            }
            
        except Exception as e:
            logger.error(f"❌ Erro ao delegar tarefa: {e}")
            return {
                'status': 'error',
                'message': f'Erro na delegação: {e}'
            }
    
    async def send_message(self, from_agent: str, to_agent: str, message_type: str, content: Dict[str, Any]) -> Dict[str, Any]:
        """Envia uma mensagem entre agentes"""
        try:
            message = AgentMessage(
                from_agent=from_agent,
                to_agent=to_agent,
                message_type=message_type,
                content=content
            )
            
            self.messages.append(message)
            
            logger.info(f"📨 Mensagem enviada: {from_agent} -> {to_agent} ({message_type})")
            
            return {
                'status': 'success',
                'message_id': len(self.messages),
                'message': {
                    'from_agent': message.from_agent,
                    'to_agent': message.to_agent,
                    'message_type': message.message_type,
                    'content': message.content,
                    'timestamp': message.timestamp.isoformat() if message.timestamp else None
                }
            }
            
        except Exception as e:
            logger.error(f"❌ Erro ao enviar mensagem: {e}")
            return {
                'status': 'error',
                'message': f'Erro no envio: {e}'
            }
    
    async def get_task_status(self, task_id: str) -> Dict[str, Any]:
        """Obtém o status de uma tarefa"""
        task = self.tasks.get(task_id)
        if not task:
            return {
                'status': 'error',
                'message': f'Tarefa {task_id} não encontrada'
            }
        
        return {
            'status': 'success',
            'task': {
                'id': task.id,
                'description': task.description,
                'agent_type': task.agent_type,
                'priority': task.priority,
                'dependencies': task.dependencies,
                'parameters': task.parameters,
                'created_at': task.created_at.isoformat() if task.created_at else None,
                'status': task.status,
                'result': task.result
            }
        }
    
    async def update_task_result(self, task_id: str, result: Dict[str, Any]) -> Dict[str, Any]:
        """Atualiza o resultado de uma tarefa"""
        try:
            task = self.tasks.get(task_id)
            if not task:
                return {
                    'status': 'error',
                    'message': f'Tarefa {task_id} não encontrada'
                }
            
            task.result = result
            task.status = "completed"
            
            logger.info(f"✅ Resultado da tarefa {task_id} atualizado")
            
            return {
                'status': 'success',
                'message': 'Resultado atualizado com sucesso'
            }
            
        except Exception as e:
            logger.error(f"❌ Erro ao atualizar resultado: {e}")
            return {
                'status': 'error',
                'message': f'Erro na atualização: {e}'
            }
    
    async def get_communication_summary(self) -> Dict[str, Any]:
        """Obtém um resumo da comunicação"""
        return {
            'status': 'success',
            'summary': {
                'total_tasks': len(self.tasks),
                'pending_tasks': len([t for t in self.tasks.values() if t.status == "pending"]),
                'completed_tasks': len([t for t in self.tasks.values() if t.status == "completed"]),
                'total_messages': len(self.messages),
                'registered_agents': list(self.agents.keys())
            }
        }

# Instância global do Communication Hub
communication_hub = CommunicationHub()
