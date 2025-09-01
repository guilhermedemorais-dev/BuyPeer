# Sistema de Agentes BuyPeer - Módulo Principal
# Arquitetura Orquestrada com MCPs e OpenAI

# Importar módulos do sistema
from .mcp_config import mcp_manager, MCPManager, MCPConfig
from .communication import communication_hub, CommunicationHub, Task, AgentMessage
from .base_agent import BaseAgent
from .architect import ArchitectAgent
from .orchestrator import orchestrator, AgentOrchestrator, BasicAgent

# Importar agentes especializados (mantidos para compatibilidade)
from .context_agent import ContextAgent
from .backend import BackendAgent
from .frontend import FrontendAgent
from .devops import DevOpsAgent
from .qa import QAAgent
from .test_automation_agent import TestAutomationAgent
from .automation_agent import AutomationAgent
from .payments import PaymentsAgent
from .data import DataAgent
from .security import SecurityAgent
from .team_manager import TeamManager

__version__ = "2.0.0"
__author__ = "BuyPeer Development Team"

# Exportar módulos principais do sistema orquestrado
__all__ = [
    # Sistema Orquestrado
    'mcp_manager',
    'MCPManager', 
    'MCPConfig',
    'communication_hub',
    'CommunicationHub',
    'Task',
    'AgentMessage',
    'BaseAgent',
    'ArchitectAgent',
    'orchestrator',
    'AgentOrchestrator',
    'BasicAgent',
    
    # Agentes Especializados (Legacy)
    'ContextAgent',
    'BackendAgent', 
    'FrontendAgent',
    'DevOpsAgent',
    'QAAgent',
    'TestAutomationAgent',
    'AutomationAgent',
    'PaymentsAgent',
    'DataAgent',
    'SecurityAgent',
    'TeamManager'
]

# Função de inicialização rápida do sistema
async def initialize_system(project_path: str = None):
    """
    Inicializa o sistema completo de agentes
    
    Args:
        project_path: Caminho do projeto (opcional)
    
    Returns:
        Dict com status da inicialização
    """
    try:
        result = await orchestrator.initialize()
        return result
    except Exception as e:
        return {
            'status': 'error',
            'message': f'Erro na inicialização do sistema: {e}'
        }

# Função para processar solicitações
async def process_request(request: str):
    """
    Processa uma solicitação usando o sistema orquestrado
    
    Args:
        request: Solicitação em linguagem natural
    
    Returns:
        Dict com resultado do processamento
    """
    try:
        result = await orchestrator.process_request(request)
        return result
    except Exception as e:
        return {
            'status': 'error',
            'message': f'Erro no processamento: {e}'
        }

# Função para obter status do sistema
async def get_system_status():
    """
    Obtém status completo do sistema
    
    Returns:
        Dict com status de todos os componentes
    """
    try:
        return await orchestrator.get_system_status()
    except Exception as e:
        return {
            'status': 'error',
            'message': f'Erro ao obter status: {e}'
        }

# Função para desligar o sistema
async def shutdown_system():
    """
    Desliga o sistema completo
    
    Returns:
        Dict com status do desligamento
    """
    try:
        return await orchestrator.shutdown()
    except Exception as e:
        return {
            'status': 'error',
            'message': f'Erro no desligamento: {e}'
        }
