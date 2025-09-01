#!/usr/bin/env python3
"""
Agente Base - Classe base para todos os agentes especializados
Fornece funcionalidades comuns e integração com MCPs
"""

import asyncio
import json
import logging
import os
from typing import Dict, Any, List, Optional
from abc import ABC, abstractmethod
from datetime import datetime

# Importar módulos do sistema
from .mcp_config import mcp_manager
from .communication import communication_hub

logger = logging.getLogger(__name__)

class BaseAgent(ABC):
    """
    Classe base para todos os agentes especializados
    Fornece funcionalidades comuns e integração com MCPs
    """
    
    def __init__(self, agent_name: str, project_path: str = None):
        self.agent_name = agent_name
        self.project_path = project_path or os.getcwd()
        self.is_active = False
        self.status = "inactive"
        self.mcp_manager = mcp_manager
        self.communication_hub = communication_hub
        self.task_history = []
        self.capabilities = []
        
        logger.info(f"🤖 {self.agent_name} inicializado")
    
    async def activate(self) -> Dict[str, Any]:
        """Ativa o agente e registra no Communication Hub"""
        try:
            self.is_active = True
            self.status = "active"
            
            # Registrar no Communication Hub
            await self.communication_hub.register_agent(self.agent_name, self)
            
            # Inicializar capacidades específicas do agente
            await self._initialize_capabilities()
            
            logger.info(f"✅ {self.agent_name} ativado com sucesso!")
            
            return {
                'status': 'success',
                'message': f'{self.agent_name} ativado',
                'capabilities': self.capabilities,
                'mcp_integration': self.mcp_manager.is_initialized
            }
        except Exception as e:
            logger.error(f"❌ Erro ao ativar {self.agent_name}: {e}")
            return {
                'status': 'error',
                'message': f'Erro ao ativar: {e}'
            }
    
    async def deactivate(self) -> Dict[str, Any]:
        """Desativa o agente"""
        self.is_active = False
        self.status = "inactive"
        return {
            'status': 'success',
            'message': f'{self.agent_name} desativado'
        }
    
    @abstractmethod
    async def _initialize_capabilities(self):
        """Inicializa capacidades específicas do agente (deve ser implementado)"""
        pass
    
    @abstractmethod
    async def execute_task(self, task_description: str, parameters: Dict[str, Any] = None) -> Dict[str, Any]:
        """Executa uma tarefa específica (deve ser implementado)"""
        pass
    
    async def get_status(self) -> Dict[str, Any]:
        """Retorna status atual do agente"""
        return {
            'agent_name': self.agent_name,
            'active': self.is_active,
            'status': self.status,
            'capabilities': self.capabilities,
            'tasks_completed': len(self.task_history),
            'mcp_available': self.mcp_manager.is_initialized
        }
    
    async def use_mcp(self, mcp_name: str, operation: str, **kwargs) -> Dict[str, Any]:
        """Usa um MCP específico para executar uma operação"""
        try:
            if not self.mcp_manager.is_initialized:
                return {
                    'status': 'error',
                    'message': 'MCP Manager não inicializado'
                }
            
            result = await self.mcp_manager.execute_mcp_command(mcp_name, operation, **kwargs)
            
            logger.info(f"🔧 {self.agent_name} usou MCP {mcp_name} - {operation}")
            
            return result
            
        except Exception as e:
            logger.error(f"❌ Erro ao usar MCP {mcp_name}: {e}")
            return {
                'status': 'error',
                'message': f'Erro no MCP: {e}'
            }
    
    async def read_file(self, file_path: str) -> Dict[str, Any]:
        """Lê um arquivo usando MCP Filesystem"""
        return await self.use_mcp('filesystem', 'read_file', path=file_path)
    
    async def write_file(self, file_path: str, content: str) -> Dict[str, Any]:
        """Escreve em um arquivo usando MCP Filesystem"""
        return await self.use_mcp('filesystem', 'write_file', path=file_path, content=content)
    
    async def list_directory(self, directory_path: str) -> Dict[str, Any]:
        """Lista conteúdo de um diretório usando MCP Filesystem"""
        return await self.use_mcp('filesystem', 'list_directory', path=directory_path)
    
    async def search_files(self, pattern: str, directory_path: str = None) -> Dict[str, Any]:
        """Busca arquivos usando MCP Filesystem"""
        return await self.use_mcp('filesystem', 'search_files', pattern=pattern, path=directory_path or self.project_path)
    
    async def git_commit(self, message: str, files: List[str] = None) -> Dict[str, Any]:
        """Faz commit usando MCP Git"""
        return await self.use_mcp('git', 'commit', message=message, files=files)
    
    async def git_push(self, branch: str = None) -> Dict[str, Any]:
        """Faz push usando MCP Git"""
        return await self.use_mcp('git', 'push', branch=branch)
    
    async def git_pull(self, branch: str = None) -> Dict[str, Any]:
        """Faz pull usando MCP Git"""
        return await self.use_mcp('git', 'pull', branch=branch)
    
    async def take_screenshot(self, url: str, name: str) -> Dict[str, Any]:
        """Tira screenshot usando MCP Puppeteer"""
        return await self.use_mcp('puppeteer', 'screenshot', url=url, name=name)
    
    async def test_ui(self, url: str, test_script: str) -> Dict[str, Any]:
        """Executa teste de UI usando MCP Puppeteer"""
        return await self.use_mcp('puppeteer', 'test_ui', url=url, script=test_script)
    
    async def get_figma_design(self, file_url: str, node_id: str) -> Dict[str, Any]:
        """Obtém design do Figma usando MCP Figma"""
        return await self.use_mcp('figma', 'get_design', file_url=file_url, node_id=node_id)
    
    async def save_context(self, key: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Salva contexto usando MCP Context7"""
        return await self.use_mcp('context7', 'save', key=key, data=data)
    
    async def load_context(self, key: str) -> Dict[str, Any]:
        """Carrega contexto usando MCP Context7"""
        return await self.use_mcp('context7', 'load', key=key)
    
    async def send_message(self, to_agent: str, message_type: str, content: Dict[str, Any]) -> Dict[str, Any]:
        """Envia mensagem para outro agente"""
        return await self.communication_hub.send_message(
            self.agent_name, to_agent, message_type, content
        )
    
    async def update_task_result(self, task_id: str, result: Dict[str, Any]) -> Dict[str, Any]:
        """Atualiza resultado de uma tarefa"""
        return await self.communication_hub.update_task_result(task_id, result)
    
    async def log_task(self, task_description: str, result: Dict[str, Any]):
        """Registra uma tarefa executada"""
        task_log = {
            'description': task_description,
            'result': result,
            'timestamp': datetime.now().isoformat(),
            'agent': self.agent_name
        }
        self.task_history.append(task_log)
        
        logger.info(f"📝 {self.agent_name} registrou tarefa: {task_description}")
    
    async def get_available_mcps(self) -> List[Dict[str, Any]]:
        """Obtém lista de MCPs disponíveis"""
        if not self.mcp_manager.is_initialized:
            return []
        
        return await self.mcp_manager.list_available_mcps()
    
    async def find_mcp_by_capability(self, capability: str) -> List[str]:
        """Encontra MCPs que possuem uma capacidade específica"""
        if not self.mcp_manager.is_initialized:
            return []
        
        return await self.mcp_manager.find_mcp_by_capability(capability)
    
    async def validate_mcp_requirements(self, required_capabilities: List[str]) -> Dict[str, Any]:
        """Valida se os MCPs necessários estão disponíveis"""
        missing_capabilities = []
        available_mcps = {}
        
        for capability in required_capabilities:
            matching_mcps = await self.find_mcp_by_capability(capability)
            if matching_mcps:
                available_mcps[capability] = matching_mcps
            else:
                missing_capabilities.append(capability)
        
        return {
            'status': 'success' if not missing_capabilities else 'warning',
            'available_capabilities': available_mcps,
            'missing_capabilities': missing_capabilities,
            'all_available': len(missing_capabilities) == 0
        }
    
    async def execute_with_mcp_fallback(self, primary_mcp: str, fallback_mcp: str, operation: str, **kwargs) -> Dict[str, Any]:
        """Executa operação com fallback para outro MCP"""
        try:
            # Tentar MCP primário
            result = await self.use_mcp(primary_mcp, operation, **kwargs)
            
            if result['status'] == 'success':
                return result
            
            # Se falhou, tentar MCP de fallback
            logger.warning(f"⚠️ {self.agent_name}: MCP {primary_mcp} falhou, tentando {fallback_mcp}")
            
            fallback_result = await self.use_mcp(fallback_mcp, operation, **kwargs)
            
            if fallback_result['status'] == 'success':
                fallback_result['used_fallback'] = True
                return fallback_result
            
            # Se ambos falharam
            return {
                'status': 'error',
                'message': f'Ambos MCPs falharam: {primary_mcp} e {fallback_mcp}',
                'primary_error': result.get('message'),
                'fallback_error': fallback_result.get('message')
            }
            
        except Exception as e:
            logger.error(f"❌ Erro no fallback MCP: {e}")
            return {
                'status': 'error',
                'message': f'Erro no fallback: {e}'
            }
    
    async def get_task_history(self) -> List[Dict[str, Any]]:
        """Obtém histórico de tarefas executadas"""
        return self.task_history
    
    async def clear_task_history(self) -> Dict[str, Any]:
        """Limpa histórico de tarefas"""
        self.task_history.clear()
        return {
            'status': 'success',
            'message': 'Histórico de tarefas limpo'
        }
    
    def __str__(self):
        return f"{self.agent_name} ({'Ativo' if self.is_active else 'Inativo'})"
    
    def __repr__(self):
        return f"<{self.agent_name}: {self.status}>"
