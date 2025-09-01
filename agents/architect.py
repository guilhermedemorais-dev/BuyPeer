#!/usr/bin/env python3
"""
Agente Arquiteto - Orquestrador Principal do Sistema BuyPeer
Analisa solicitações usando OpenAI e coordena outros agentes com MCPs
"""

import asyncio
import json
import logging
import os
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from datetime import datetime

# Importar módulos do sistema
from .mcp_config import mcp_manager
from .communication import communication_hub, Task

logger = logging.getLogger(__name__)

@dataclass
class Requirement:
    """Representa um requisito identificado"""
    id: str
    description: str
    priority: str
    complexity: str
    estimated_time: str
    dependencies: List[str] = None
    mcp_requirements: List[str] = None
    
    def __post_init__(self):
        if self.dependencies is None:
            self.dependencies = []
        if self.mcp_requirements is None:
            self.mcp_requirements = []

@dataclass
class Analysis:
    """Resultado da análise de uma solicitação"""
    request: str
    requirements: List[Requirement]
    delegated_tasks: Dict[str, List[str]]
    estimated_total_time: str
    risks: List[str]
    recommendations: List[str]
    mcp_usage: Dict[str, List[str]]
    created_at: datetime = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()

class ArchitectAgent:
    """
    Agente Arquiteto - Orquestrador Principal
    Usa OpenAI para análise e coordena agentes com MCPs
    """
    
    def __init__(self, project_path: str):
        self.project_path = project_path
        self.is_active = False
        self.status = "inactive"
        self.analysis_history = []
        self.mcp_manager = mcp_manager
        self.communication_hub = communication_hub
        
        # Padrões para identificação rápida de tipos de solicitações
        self.patterns = {
            'backend': [
                r'api|modelo|controller|banco|database|laravel|php',
                r'backend|servidor|serviço|lógica|negócio',
                r'crud|endpoint|rota|migration|seeder'
            ],
            'frontend': [
                r'interface|componente|página|vue|javascript|css',
                r'frontend|cliente|ui|ux|responsivo|mobile',
                r'formulário|botão|modal|tabela|gráfico'
            ],
            'devops': [
                r'deploy|servidor|ambiente|docker|nginx|apache',
                r'devops|infraestrutura|monitoramento|backup',
                r'produção|staging|ci/cd|github|actions'
            ],
            'qa': [
                r'teste|bug|erro|validação|qualidade|performance',
                r'qa|test|unitário|integração|e2e|cypress',
                r'corrigir|quebrando|lento|problema'
            ],
            'payments': [
                r'pagamento|stripe|paypal|gateway|transação',
                r'checkout|cartão|boleto|pix|webhook',
                r'cupom|desconto|promoção|frete'
            ],
            'security': [
                r'segurança|autenticação|autorização|https|ssl',
                r'vulnerabilidade|hack|ataque|proteção|validação',
                r'login|senha|token|jwt|sanctum'
            ],
            'data': [
                r'analytics|relatório|dashboard|métrica|dados',
                r'gráfico|estatística|venda|cliente|produto',
                r'export|import|excel|csv|pdf'
            ]
        }
        
        logger.info("🏗️ Agente Arquiteto inicializado")
    
    async def activate(self) -> Dict[str, Any]:
        """Ativa o agente arquiteto e inicializa MCPs"""
        try:
            self.is_active = True
            self.status = "active"
            
            # Inicializar MCP Manager
            mcp_result = await self.mcp_manager.initialize()
            if mcp_result['status'] != 'success':
                logger.warning(f"⚠️ MCP Manager não inicializado: {mcp_result['message']}")
            
            # Registrar no Communication Hub
            await self.communication_hub.register_agent('architect', self)
            
            # Analisar estrutura do projeto
            project_analysis = await self._analyze_project_structure()
            
            logger.info("✅ Agente Arquiteto ativado com sucesso!")
            
            return {
                'status': 'success',
                'message': 'Agente Arquiteto ativado',
                'project_analysis': project_analysis,
                'mcp_status': mcp_result,
                'capabilities': [
                    'Análise de requisitos com OpenAI',
                    'Orquestração de agentes',
                    'Integração com MCPs',
                    'Estimativa de tempo',
                    'Identificação de riscos',
                    'Recomendações técnicas'
                ]
            }
        except Exception as e:
            logger.error(f"❌ Erro ao ativar Agente Arquiteto: {e}")
            return {
                'status': 'error',
                'message': f'Erro ao ativar: {e}'
            }
    
    async def deactivate(self) -> Dict[str, Any]:
        """Desativa o agente arquiteto"""
        self.is_active = False
        self.status = "inactive"
        return {
            'status': 'success',
            'message': 'Agente Arquiteto desativado'
        }
    
    async def analyze_request(self, request: str) -> Dict[str, Any]:
        """Analisa uma solicitação usando OpenAI e cria plano de ação"""
        try:
            logger.info(f"📋 Analisando solicitação: {request}")
            
            # Usar OpenAI para análise detalhada
            openai_analysis = await self.communication_hub.analyze_request_with_openai(request)
            
            if openai_analysis['status'] != 'success':
                # Fallback para análise padrão
                logger.warning("⚠️ OpenAI não disponível, usando análise padrão")
                return await self._fallback_analysis(request)
            
            # Processar análise da OpenAI
            analysis_data = openai_analysis['analysis']
            
            # Identificar requisitos
            requirements = await self._process_openai_requirements(analysis_data)
            
            # Identificar MCPs necessários
            mcp_usage = await self._identify_mcp_requirements(request, requirements)
            
            # Delegar tarefas
            delegated_tasks = await self._delegate_tasks_from_analysis(analysis_data)
            
            # Calcular tempo estimado
            estimated_time = await self._estimate_time_from_analysis(analysis_data)
            
            # Identificar riscos
            risks = analysis_data.get('risks', [])
            
            # Gerar recomendações
            recommendations = analysis_data.get('recommendations', [])
            
            # Criar análise
            analysis = Analysis(
                request=request,
                requirements=requirements,
                delegated_tasks=delegated_tasks,
                estimated_total_time=estimated_time,
                risks=risks,
                recommendations=recommendations,
                mcp_usage=mcp_usage
            )
            
            # Salvar na história
            self.analysis_history.append(analysis)
            
            return {
                'status': 'success',
                'analysis': {
                    'request': analysis.request,
                    'requirements': [vars(req) for req in analysis.requirements] if analysis.requirements else [],
                    'delegated_tasks': analysis.delegated_tasks,
                    'estimated_time': analysis.estimated_total_time,
                    'risks': analysis.risks,
                    'recommendations': analysis.recommendations,
                    'mcp_usage': analysis.mcp_usage,
                    'created_at': analysis.created_at.isoformat()
                }
            }
        except Exception as e:
            logger.error(f"❌ Erro ao analisar solicitação: {e}")
            return {
                'status': 'error',
                'message': f'Erro na análise: {e}'
            }
    
    async def _fallback_analysis(self, request: str) -> Dict[str, Any]:
        """Análise de fallback quando OpenAI não está disponível"""
        try:
            # Identificar requisitos básicos
            requirements = await self._identify_requirements(request)
            
            # Delegar tarefas
            delegated_tasks = await self._delegate_tasks(request, requirements)
            
            # Calcular tempo estimado
            estimated_time = await self._estimate_time(requirements)
            
            # Identificar riscos
            risks = await self._identify_risks(request, requirements)
            
            # Gerar recomendações
            recommendations = await self._generate_recommendations(request, requirements)
            
            # Identificar MCPs necessários
            mcp_usage = await self._identify_mcp_requirements(request, requirements)
            
            # Criar análise
            analysis = Analysis(
                request=request,
                requirements=requirements,
                delegated_tasks=delegated_tasks,
                estimated_total_time=estimated_time,
                risks=risks,
                recommendations=recommendations,
                mcp_usage=mcp_usage
            )
            
            return {
                'status': 'success',
                'analysis': {
                    'request': analysis.request,
                    'requirements': [vars(req) for req in analysis.requirements] if analysis.requirements else [],
                    'delegated_tasks': analysis.delegated_tasks,
                    'estimated_time': analysis.estimated_total_time,
                    'risks': analysis.risks,
                    'recommendations': analysis.recommendations,
                    'mcp_usage': analysis.mcp_usage,
                    'created_at': analysis.created_at.isoformat()
                }
            }
        except Exception as e:
            logger.error(f"❌ Erro na análise de fallback: {e}")
            return {
                'status': 'error',
                'message': f'Erro na análise de fallback: {e}'
            }
    
    async def _process_openai_requirements(self, analysis_data: Dict[str, Any]) -> List[Requirement]:
        """Processa requisitos identificados pela OpenAI"""
        requirements = []
        
        for i, task_breakdown in enumerate(analysis_data.get('task_breakdown', [])):
            req = Requirement(
                id=f"req_{i+1}",
                description=task_breakdown.get('task', ''),
                priority=task_breakdown.get('priority', 'normal'),
                complexity=self._map_priority_to_complexity(task_breakdown.get('priority', 'normal')),
                estimated_time=self._estimate_time_from_complexity(task_breakdown.get('priority', 'normal')),
                dependencies=task_breakdown.get('dependencies', [])
            )
            requirements.append(req)
        
        return requirements
    
    async def _delegate_tasks_from_analysis(self, analysis_data: Dict[str, Any]) -> Dict[str, List[str]]:
        """Delega tarefas baseado na análise da OpenAI"""
        delegated_tasks = {}
        
        for task_breakdown in analysis_data.get('task_breakdown', []):
            agent = task_breakdown.get('agent', '')
            task = task_breakdown.get('task', '')
            
            if agent not in delegated_tasks:
                delegated_tasks[agent] = []
            
            delegated_tasks[agent].append(task)
        
        return delegated_tasks
    
    async def _estimate_time_from_analysis(self, analysis_data: Dict[str, Any]) -> str:
        """Estima tempo baseado na complexidade da análise"""
        complexity = analysis_data.get('estimated_complexity', 'medium')
        
        time_mapping = {
            'low': '1-2 horas',
            'medium': '4-8 horas',
            'high': '1-3 dias'
        }
        
        return time_mapping.get(complexity, '4-8 horas')
    
    async def _identify_mcp_requirements(self, request: str, requirements: List[Requirement]) -> Dict[str, List[str]]:
        """Identifica quais MCPs são necessários para a solicitação"""
        mcp_usage = {}
        
        # Mapear capacidades necessárias
        needed_capabilities = []
        
        # Análise baseada em palavras-chave
        request_lower = request.lower()
        
        if any(word in request_lower for word in ['arquivo', 'ler', 'escrever', 'buscar']):
            needed_capabilities.append('leitura')
            needed_capabilities.append('escrita')
        
        if any(word in request_lower for word in ['git', 'commit', 'push', 'pull']):
            needed_capabilities.append('commits')
            needed_capabilities.append('branches')
        
        if any(word in request_lower for word in ['teste', 'screenshot', 'automático']):
            needed_capabilities.append('testes')
            needed_capabilities.append('screenshots')
        
        if any(word in request_lower for word in ['design', 'figma', 'componente']):
            needed_capabilities.append('designs')
            needed_capabilities.append('componentes')
        
        if any(word in request_lower for word in ['memória', 'contexto', 'histórico']):
            needed_capabilities.append('memória')
            needed_capabilities.append('contexto')
        
        # Encontrar MCPs que fornecem essas capacidades
        for capability in needed_capabilities:
            matching_mcps = await self.mcp_manager.find_mcp_by_capability(capability)
            for mcp in matching_mcps:
                if mcp not in mcp_usage:
                    mcp_usage[mcp] = []
                mcp_usage[mcp].append(capability)
        
        return mcp_usage
    
    def _map_priority_to_complexity(self, priority: str) -> str:
        """Mapeia prioridade para complexidade"""
        mapping = {
            'high': 'high',
            'normal': 'medium',
            'low': 'low'
        }
        return mapping.get(priority, 'medium')
    
    def _estimate_time_from_complexity(self, priority: str) -> str:
        """Estima tempo baseado na prioridade"""
        mapping = {
            'high': '4-8 horas',
            'normal': '2-4 horas',
            'low': '1-2 horas'
        }
        return mapping.get(priority, '2-4 horas')
    
    async def _analyze_project_structure(self) -> Dict[str, Any]:
        """Analisa a estrutura atual do projeto usando MCPs"""
        try:
            structure = {
                'backend': {
                    'laravel_version': '10.x',
                    'php_version': '8.1+',
                    'database': 'MySQL',
                    'cache': 'Redis'
                },
                'frontend': {
                    'vue_version': '3.x',
                    'build_tool': 'Laravel Mix',
                    'ui_framework': 'Custom'
                },
                'devops': {
                    'server': 'VPS Hostinger',
                    'web_server': 'Nginx',
                    'containerization': 'Docker'
                }
            }
            
            # Usar MCP Filesystem para análise detalhada
            if self.mcp_manager.is_initialized:
                try:
                    # Listar estrutura de diretórios
                    fs_result = await self.mcp_manager.execute_mcp_command(
                        'filesystem', 'list_directory', path=self.project_path
                    )
                    
                    if fs_result['status'] == 'success':
                        structure['filesystem_analysis'] = fs_result['result']
                    
                except Exception as e:
                    logger.warning(f"⚠️ Erro ao usar MCP Filesystem: {e}")
            
            return structure
            
        except Exception as e:
            logger.error(f"❌ Erro ao analisar estrutura do projeto: {e}")
            return {'error': str(e)}
    
    async def _identify_requirements(self, request: str) -> List[Requirement]:
        """Identifica requisitos da solicitação (método legado)"""
        # Implementação básica para fallback
        requirements = []
        
        # Análise simples baseada em padrões
        for req_type, patterns in self.patterns.items():
            for pattern in patterns:
                if pattern in request.lower():
                    req = Requirement(
                        id=f"req_{len(requirements)+1}",
                        description=f"Implementar funcionalidade {req_type}",
                        priority="normal",
                        complexity="medium",
                        estimated_time="2-4 horas"
                    )
                    requirements.append(req)
                    break
        
        return requirements
    
    async def _delegate_tasks(self, request: str, requirements: List[Requirement]) -> Dict[str, List[str]]:
        """Delega tarefas para agentes (método legado)"""
        delegated_tasks = {}
        
        # Mapeamento básico baseado em padrões
        for req_type, patterns in self.patterns.items():
            for pattern in patterns:
                if pattern in request.lower():
                    if req_type not in delegated_tasks:
                        delegated_tasks[req_type] = []
                    delegated_tasks[req_type].append(f"Implementar {req_type}")
                    break
        
        return delegated_tasks
    
    async def _estimate_time(self, requirements: List[Requirement]) -> str:
        """Estima tempo total (método legado)"""
        total_hours = len(requirements) * 2
        return f"{total_hours}-{total_hours + 2} horas"
    
    async def _identify_risks(self, request: str, requirements: List[Requirement]) -> List[str]:
        """Identifica riscos (método legado)"""
        risks = []
        
        if 'pagamento' in request.lower():
            risks.append("Riscos de segurança em transações financeiras")
        
        if 'deploy' in request.lower():
            risks.append("Riscos de downtime durante deploy")
        
        if 'teste' in request.lower():
            risks.append("Riscos de bugs não detectados")
        
        return risks
    
    async def _generate_recommendations(self, request: str, requirements: List[Requirement]) -> List[str]:
        """Gera recomendações (método legado)"""
        recommendations = []
        
        if 'pagamento' in request.lower():
            recommendations.append("Implementar testes de segurança rigorosos")
        
        if 'deploy' in request.lower():
            recommendations.append("Usar ambiente de staging antes da produção")
        
        if 'teste' in request.lower():
            recommendations.append("Implementar testes automatizados")
        
        return recommendations
    
    async def execute_analysis_plan(self, analysis_result: Dict[str, Any]) -> Dict[str, Any]:
        """Executa o plano de análise criando e delegando tarefas"""
        try:
            logger.info("🚀 Executando plano de análise...")
            
            tasks_created = []
            tasks_delegated = []
            
            # Criar tarefas baseadas na análise
            for agent, tasks in analysis_result['analysis']['delegated_tasks'].items():
                for task_description in tasks:
                    # Criar tarefa no Communication Hub
                    task_result = await self.communication_hub.create_task(
                        description=task_description,
                        agent_type=agent,
                        priority='normal'
                    )
                    
                    if task_result['status'] == 'success':
                        task_id = task_result['task_id']
                        tasks_created.append(task_id)
                        
                        # Delegar tarefa
                        delegate_result = await self.communication_hub.delegate_task(task_id)
                        if delegate_result['status'] == 'success':
                            tasks_delegated.append(task_id)
            
            return {
                'status': 'success',
                'message': 'Plano de análise executado',
                'tasks_created': tasks_created,
                'tasks_delegated': tasks_delegated,
                'total_tasks': len(tasks_created)
            }
            
        except Exception as e:
            logger.error(f"❌ Erro ao executar plano de análise: {e}")
            return {
                'status': 'error',
                'message': f'Erro na execução: {e}'
            }
    
    async def get_analysis_summary(self) -> Dict[str, Any]:
        """Obtém resumo das análises realizadas"""
        return {
            'status': 'success',
            'summary': {
                'total_analyses': len(self.analysis_history),
                'recent_analyses': [
                    {
                        'request': analysis.request[:100] + '...' if len(analysis.request) > 100 else analysis.request,
                        'created_at': analysis.created_at.isoformat(),
                        'estimated_time': analysis.estimated_total_time
                    }
                    for analysis in self.analysis_history[-5:]  # Últimas 5 análises
                ],
                'mcp_status': self.mcp_manager.is_initialized,
                'communication_status': len(self.communication_hub.agents)
            }
        }
