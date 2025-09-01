#!/usr/bin/env python3
"""
Configuração Central de MCPs para o Sistema de Agentes BuyPeer
Gerencia conexões e funcionalidades dos MCPs disponíveis
"""

import json
import logging
import os
import subprocess
from pathlib import Path
from typing import Dict, Any, Optional, List
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class MCPConfig:
    """Configuração de um MCP específico"""
    name: str
    command: str
    args: List[str]
    env: Dict[str, str] = None
    description: str = ""
    capabilities: List[str] = None
    
    def __post_init__(self):
        if self.env is None:
            self.env = {}
        if self.capabilities is None:
            self.capabilities = []

class MCPManager:
    """
    Gerenciador central de MCPs
    Fornece interface unificada para todos os MCPs configurados
    """
    
    def __init__(self, mcp_config_path: str = None):
        self.mcp_config_path = mcp_config_path or str(Path.home() / '.cursor' / 'mcp.json')
        self.mcps: Dict[str, MCPConfig] = {}
        self.is_initialized = False
        
        # Mapeamento de funcionalidades por MCP
        self.mcp_capabilities = {
            'context7': {
                'description': 'Memória e contexto persistente',
                'capabilities': ['memória', 'contexto', 'histórico', 'sincronização']
            },
            'cursor': {
                'description': 'Controle do IDE Cursor',
                'capabilities': ['ide', 'workspace', 'extensões', 'configurações']
            },
            'git': {
                'description': 'Controle de versão Git/GitHub',
                'capabilities': ['commits', 'branches', 'merge', 'push', 'pull']
            },
            'filesystem': {
                'description': 'Acesso ao sistema de arquivos',
                'capabilities': ['leitura', 'escrita', 'busca', 'organização']
            },
            'figma': {
                'description': 'Integração com Figma',
                'capabilities': ['designs', 'assets', 'componentes', 'prototipagem']
            },
            'puppeteer': {
                'description': 'Automação de browser',
                'capabilities': ['testes', 'screenshots', 'scraping', 'simulação']
            },
            'ref-tools': {
                'description': 'Ferramentas de referência',
                'capabilities': ['documentação', 'refatoração', 'padrões', 'templates']
            },
            'json-resume': {
                'description': 'Gerenciamento de currículos',
                'capabilities': ['currículos', 'templates', 'exportação', 'formatação']
            }
        }
    
    async def initialize(self) -> Dict[str, Any]:
        """Inicializa o gerenciador de MCPs"""
        try:
            logger.info("🔧 Inicializando MCP Manager...")
            
            # Carregar configuração do arquivo
            await self._load_mcp_config()
            
            # Validar MCPs disponíveis
            validation_result = await self._validate_mcps()
            
            self.is_initialized = True
            
            return {
                'status': 'success',
                'message': 'MCP Manager inicializado com sucesso',
                'available_mcps': list(self.mcps.keys()),
                'validation': validation_result
            }
        except Exception as e:
            logger.error(f"❌ Erro ao inicializar MCP Manager: {e}")
            return {
                'status': 'error',
                'message': f'Erro na inicialização: {e}'
            }
    
    async def _load_mcp_config(self):
        """Carrega configuração dos MCPs do arquivo JSON"""
        try:
            with open(self.mcp_config_path, 'r') as f:
                config = json.load(f)
            
            for mcp_name, mcp_data in config['mcpServers'].items():
                mcp_config = MCPConfig(
                    name=mcp_name,
                    command=mcp_data['command'],
                    args=mcp_data.get('args', []),
                    env=mcp_data.get('env', {}),
                    description=self.mcp_capabilities.get(mcp_name, {}).get('description', ''),
                    capabilities=self.mcp_capabilities.get(mcp_name, {}).get('capabilities', [])
                )
                self.mcps[mcp_name] = mcp_config
                
            logger.info(f"✅ Carregados {len(self.mcps)} MCPs")
            
        except Exception as e:
            logger.error(f"❌ Erro ao carregar configuração MCP: {e}")
            raise
    
    async def _validate_mcps(self) -> Dict[str, Any]:
        """Valida se os MCPs estão funcionando corretamente"""
        validation_results = {}
        
        for mcp_name, mcp_config in self.mcps.items():
            try:
                # Verificar se o comando existe
                result = subprocess.run(
                    ['which', mcp_config.command],
                    capture_output=True,
                    text=True
                )
                
                if result.returncode == 0:
                    validation_results[mcp_name] = {
                        'status': 'available',
                        'command': mcp_config.command,
                        'description': mcp_config.description
                    }
                else:
                    validation_results[mcp_name] = {
                        'status': 'command_not_found',
                        'command': mcp_config.command,
                        'error': f'Comando {mcp_config.command} não encontrado'
                    }
                    
            except Exception as e:
                validation_results[mcp_name] = {
                    'status': 'error',
                    'error': str(e)
                }
        
        return validation_results
    
    async def get_mcp(self, mcp_name: str) -> Optional[MCPConfig]:
        """Retorna configuração de um MCP específico"""
        return self.mcps.get(mcp_name)
    
    async def list_available_mcps(self) -> List[Dict[str, Any]]:
        """Lista todos os MCPs disponíveis com suas capacidades"""
        return [
            {
                'name': name,
                'description': config.description,
                'capabilities': config.capabilities,
                'command': config.command
            }
            for name, config in self.mcps.items()
        ]
    
    async def find_mcp_by_capability(self, capability: str) -> List[str]:
        """Encontra MCPs que possuem uma capacidade específica"""
        matching_mcps = []
        
        for mcp_name, config in self.mcps.items():
            if capability.lower() in [cap.lower() for cap in config.capabilities]:
                matching_mcps.append(mcp_name)
        
        return matching_mcps
    
    async def execute_mcp_command(self, mcp_name: str, operation: str, **kwargs) -> Dict[str, Any]:
        """Executa uma operação específica em um MCP"""
        try:
            mcp_config = await self.get_mcp(mcp_name)
            if not mcp_config:
                return {
                    'status': 'error',
                    'message': f'MCP {mcp_name} não encontrado'
                }
            
            # Aqui implementaríamos a lógica específica para cada MCP
            # Por enquanto, retornamos uma estrutura básica
            return {
                'status': 'success',
                'mcp': mcp_name,
                'operation': operation,
                'result': f'Operação {operation} executada no MCP {mcp_name}',
                'kwargs': kwargs
            }
            
        except Exception as e:
            logger.error(f"❌ Erro ao executar comando MCP {mcp_name}: {e}")
            return {
                'status': 'error',
                'message': f'Erro na execução: {e}'
            }
    
    async def get_filesystem_operations(self) -> Dict[str, Any]:
        """Operações específicas do MCP Filesystem"""
        return {
            'read_file': 'Ler conteúdo de arquivo',
            'write_file': 'Escrever conteúdo em arquivo',
            'list_directory': 'Listar conteúdo de diretório',
            'search_files': 'Buscar arquivos por padrão',
            'create_directory': 'Criar diretório',
            'move_file': 'Mover/renomear arquivo'
        }
    
    async def get_git_operations(self) -> Dict[str, Any]:
        """Operações específicas do MCP Git"""
        return {
            'commit': 'Fazer commit de mudanças',
            'push': 'Enviar mudanças para repositório',
            'pull': 'Baixar mudanças do repositório',
            'branch': 'Gerenciar branches',
            'merge': 'Fazer merge de branches',
            'status': 'Verificar status do repositório'
        }
    
    async def get_puppeteer_operations(self) -> Dict[str, Any]:
        """Operações específicas do MCP Puppeteer"""
        return {
            'screenshot': 'Capturar screenshot de página',
            'navigate': 'Navegar para URL',
            'click': 'Clicar em elemento',
            'fill': 'Preencher formulário',
            'evaluate': 'Executar JavaScript',
            'test_ui': 'Executar testes de interface'
        }

# Instância global do MCP Manager
mcp_manager = MCPManager()
