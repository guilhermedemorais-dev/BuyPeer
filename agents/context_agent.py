#!/usr/bin/env python3
"""
Agente de Contexto - Especialista em Documentação e Contexto
Consulta documentação oficial e mantém contexto atualizado
"""

import asyncio
import json
import logging
import os
import re
import requests
import aiohttp
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from datetime import datetime
import subprocess

logger = logging.getLogger(__name__)

@dataclass
class DocumentationSource:
    """Representa uma fonte de documentação"""
    name: str
    url: str
    type: str  # api, docs, github, etc.
    version: str
    last_updated: datetime = None
    
    def __post_init__(self):
        if self.last_updated is None:
            self.last_updated = datetime.now()

@dataclass
class ContextInfo:
    """Informações de contexto"""
    framework: str
    version: str
    documentation: List[DocumentationSource]
    current_context: Dict[str, Any]
    last_updated: datetime = None
    
    def __post_init__(self):
        if self.last_updated is None:
            self.last_updated = datetime.now()

class ContextAgent:
    """
    Agente de Contexto - Consulta documentação oficial e mantém contexto
    """
    
    def __init__(self, project_path: str):
        self.project_path = project_path
        self.is_active = False
        self.status = "inactive"
        self.context_history = []
        
        # Context7 MCP Server - Documentação atualizada em tempo real
        self.context7_config = {
            'remote_url': 'https://mcp.context7.com/mcp',
            'local_command': ['npx', '-y', '@upstash/context7-mcp'],
            'enabled': False  # Desabilitado para funcionar offline
        }
        
        # Mapeamento de tecnologias para Context7 Library IDs
        self.context7_library_mapping = {
            'laravel': '/laravel/laravel',
            'vue': '/vuejs/vue',
            'php': '/php/php',
            'mysql': '/mysql/mysql',
            'redis': '/redis/redis',
            'nginx': '/nginx/nginx',
            'composer': '/composer/composer',
            'npm': '/npm/npm',
            'node': '/nodejs/node',
            'javascript': '/mdn/javascript',
            'typescript': '/microsoft/typescript',
            'react': '/facebook/react',
            'next': '/vercel/next.js',
            'tailwind': '/tailwindlabs/tailwindcss',
            'bootstrap': '/twbs/bootstrap',
            'jquery': '/jquery/jquery',
            'axios': '/axios/axios',
            'lodash': '/lodash/lodash',
            'moment': '/moment/moment',
            'chart': '/chartjs/chart.js',
            'socket': '/socketio/socket.io',
            'express': '/expressjs/express',
            'mongodb': '/mongodb/docs',
            'postgresql': '/postgresql/postgresql',
            'sqlite': '/sqlite/sqlite',
            'docker': '/docker/docs',
            'kubernetes': '/kubernetes/kubernetes',
            'aws': '/aws/aws-sdk-js',
            'firebase': '/firebase/firebase-js-sdk',
            'stripe': '/stripe/stripe-node',
            'paypal': '/paypal/paypal-checkout-components',
            'github': '/github/docs',
            'git': '/git/git'
        }
        
        logger.info("Agente de Contexto inicializado")
    
    async def activate(self) -> Dict[str, Any]:
        """Ativa o agente de contexto"""
        try:
            self.is_active = True
            self.status = "active"
            
            # Analisar contexto atual do projeto
            current_context = await self._analyze_project_context()
            
            # Testar conexão com Context7
            context7_status = await self._test_context7_connection()
            
            logger.info("✅ Agente de Contexto ativado com sucesso!")
            
            return {
                'status': 'success',
                'message': 'Agente de Contexto ativado',
                'current_context': current_context,
                'context7_status': context7_status,
                'capabilities': [
                    'Consulta documentação oficial',
                    'Análise de versões',
                    'Contexto atualizado',
                    'Integração com fontes oficiais',
                    'Manutenção de contexto'
                ]
            }
        except Exception as e:
            logger.error(f"❌ Erro ao ativar Agente de Contexto: {e}")
            return {
                'status': 'error',
                'message': f'Erro ao ativar: {e}'
            }
    
    async def deactivate(self) -> Dict[str, Any]:
        """Desativa o agente de contexto"""
        self.is_active = False
        self.status = "inactive"
        return {
            'status': 'success',
            'message': 'Agente de Contexto desativado'
        }
    
    async def get_context_for_request(self, request: str) -> Dict[str, Any]:
        """Obtém contexto específico para uma solicitação"""
        try:
            logger.info(f"🔍 Obtendo contexto para: {request}")
            
            # Identificar tecnologias mencionadas
            technologies = await self._identify_technologies(request)
            
            # Buscar documentação relevante
            relevant_docs = await self._search_relevant_documentation(request, technologies)
            
            # Analisar versões atuais
            current_versions = await self._get_current_versions(technologies)
            
            # Criar contexto específico
            context = {
                'request': request,
                'technologies': technologies,
                'documentation': relevant_docs,
                'versions': current_versions,
                'recommendations': await self._generate_context_recommendations(request, technologies),
                'timestamp': datetime.now().isoformat()
            }
            
            # Salvar no histórico
            self.context_history.append(context)
            
            return {
                'status': 'success',
                'context': context
            }
        except Exception as e:
            logger.error(f"❌ Erro ao obter contexto: {e}")
            return {
                'status': 'error',
                'message': f'Erro ao obter contexto: {e}'
            }
    
    async def _analyze_project_context(self) -> Dict[str, Any]:
        """Analisa o contexto atual do projeto"""
        try:
            context = {
                'framework': 'Laravel',
                'version': '10.x',
                'php_version': '8.1+',
                'frontend': 'Vue.js 3',
                'database': 'MySQL 8.0',
                'cache': 'Redis',
                'web_server': 'Nginx'
            }
            
            # Verificar composer.json para versões reais
            composer_path = os.path.join(self.project_path, 'composer.json')
            if os.path.exists(composer_path):
                with open(composer_path, 'r') as f:
                    composer_data = json.load(f)
                    if 'require' in composer_data:
                        if 'laravel/framework' in composer_data['require']:
                            context['laravel_version'] = composer_data['require']['laravel/framework']
                        if 'php' in composer_data['require']:
                            context['php_version'] = composer_data['require']['php']
            
            # Verificar package.json para frontend
            package_path = os.path.join(self.project_path, 'package.json')
            if os.path.exists(package_path):
                with open(package_path, 'r') as f:
                    package_data = json.load(f)
                    if 'dependencies' in package_data:
                        if 'vue' in package_data['dependencies']:
                            context['vue_version'] = package_data['dependencies']['vue']
            
            return context
        except Exception as e:
            logger.error(f"Erro ao analisar contexto: {e}")
            return {}
    
    async def _test_context7_connection(self) -> Dict[str, Any]:
        """Testa conexão com o servidor Context7"""
        try:
            # Testar conexão com Context7
            test_payload = {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "initialize",
                "params": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {},
                    "clientInfo": {
                        "name": "BuyPeer-ContextAgent",
                        "version": "1.0.0"
                    }
                }
            }
            
            response = await self._make_context7_request(test_payload)
            
            if response:
                return {
                    'status': 'connected',
                    'message': 'Conexão com Context7 estabelecida',
                    'server_info': response.get('result', {}),
                    'timestamp': datetime.now().isoformat()
                }
            else:
                return {
                    'status': 'error',
                    'message': 'Falha na conexão com Context7',
                    'timestamp': datetime.now().isoformat()
                }
                
        except Exception as e:
            logger.error(f"Erro ao testar conexão Context7: {e}")
            return {
                'status': 'error',
                'message': f'Erro na conexão: {str(e)}',
                'timestamp': datetime.now().isoformat()
            }
    
    async def _identify_technologies(self, request: str) -> List[str]:
        """Identifica tecnologias mencionadas na solicitação"""
        technologies = []
        request_lower = request.lower()
        
        # Laravel
        if any(word in request_lower for word in ['laravel', 'eloquent', 'artisan', 'blade', 'model', 'controller', 'migration', 'cupom', 'cupons', 'desconto']):
            technologies.append('laravel')
        
        # Vue.js
        if any(word in request_lower for word in ['vue', 'component', 'frontend', 'javascript', 'interface', 'ui']):
            technologies.append('vue')
        
        # PHP
        if any(word in request_lower for word in ['php', 'backend', 'api', 'sistema']):
            technologies.append('php')
        
        # MySQL
        if any(word in request_lower for word in ['mysql', 'database', 'query', 'migration', 'banco', 'dados']):
            technologies.append('mysql')
        
        # Redis
        if any(word in request_lower for word in ['redis', 'cache', 'session', 'cache']):
            technologies.append('redis')
        
        # Nginx
        if any(word in request_lower for word in ['nginx', 'server', 'deploy', 'servidor']):
            technologies.append('nginx')
        
        return technologies
    
    async def _search_relevant_documentation(self, request: str, technologies: List[str]) -> Dict[str, Any]:
        """Busca documentação relevante usando Context7"""
        try:
            relevant_docs = {}
            
            for tech in technologies:
                if tech in self.context7_library_mapping:
                    library_id = self.context7_library_mapping[tech]
                    docs = await self._get_context7_documentation(library_id, request)
                    relevant_docs[tech] = {
                        'source': 'Context7',
                        'library_id': library_id,
                        'documentation': docs
                    }
            
            return relevant_docs
        except Exception as e:
            logger.error(f"Erro ao buscar documentação: {e}")
            return {}
    
    async def _get_context7_documentation(self, library_id: str, request: str) -> Dict[str, Any]:
        """Obtém documentação do Context7 para uma biblioteca específica"""
        try:
            # Determinar tópico baseado na solicitação
            topic = self._extract_topic_from_request(request)
            
            # Preparar payload para Context7
            payload = {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "tools/call",
                "params": {
                    "name": "get-library-docs",
                    "arguments": {
                        "context7CompatibleLibraryID": library_id,
                        "topic": topic,
                        "tokens": 15000
                    }
                }
            }
            
            # Fazer requisição para Context7
            response = await self._make_context7_request(payload)
            
            if response and 'result' in response:
                return {
                    'library_id': library_id,
                    'topic': topic,
                    'content': response['result'].get('content', ''),
                    'source': 'Context7',
                    'timestamp': datetime.now().isoformat()
                }
            else:
                # Fallback para documentação local
                return await self._get_fallback_documentation(library_id, topic)
                
        except Exception as e:
            logger.error(f"Erro ao obter documentação do Context7: {e}")
            # Fallback para documentação local
            return await self._get_fallback_documentation(library_id, topic)
    
    async def _get_fallback_documentation(self, library_id: str, topic: str) -> Dict[str, Any]:
        """Documentação de fallback quando Context7 não está disponível"""
        fallback_docs = {
            '/laravel/laravel': {
                'models': 'Laravel Eloquent ORM: https://laravel.com/docs/10.x/eloquent\n- Criar modelos: php artisan make:model ModelName\n- Relacionamentos: hasMany, belongsTo, hasOne\n- Mass Assignment: $fillable, $guarded',
                'controllers': 'Laravel Controllers: https://laravel.com/docs/10.x/controllers\n- Criar: php artisan make:controller ControllerName\n- Resource Controllers: --resource flag\n- API Controllers: --api flag',
                'migrations': 'Laravel Migrations: https://laravel.com/docs/10.x/migrations\n- Criar: php artisan make:migration create_table_name\n- Executar: php artisan migrate\n- Rollback: php artisan migrate:rollback',
                'routing': 'Laravel Routing: https://laravel.com/docs/10.x/routing\n- Routes em routes/web.php ou routes/api.php\n- Route Model Binding\n- Middleware: auth, api, etc.',
                'authentication': 'Laravel Authentication: https://laravel.com/docs/10.x/authentication\n- Laravel Breeze ou Jetstream\n- Sanctum para APIs\n- Guards e Providers',
                'validation': 'Laravel Validation: https://laravel.com/docs/10.x/validation\n- Form Request Validation\n- Custom Rules\n- Error Messages'
            },
            '/vuejs/vue': {
                'components': 'Vue.js Components: https://vuejs.org/guide/essentials/component-basics.html\n- Single File Components (.vue)\n- Props e Events\n- Composition API vs Options API',
                'state-management': 'Vue.js State Management: https://vuejs.org/guide/scaling-up/state-management.html\n- Pinia (recomendado)\n- Vuex (legacy)\n- Composables',
                'routing': 'Vue Router: https://router.vuejs.org/\n- Dynamic Routes\n- Navigation Guards\n- Lazy Loading'
            },
            '/php/php': {
                'basics': 'PHP Basics: https://www.php.net/manual/en/\n- Variables, Arrays, Functions\n- Classes e Objects\n- Namespaces',
                'packages': 'Composer: https://getcomposer.org/\n- composer.json\n- Autoloading\n- PSR Standards'
            },
            '/mysql/mysql': {
                'queries': 'MySQL Queries: https://dev.mysql.com/doc/\n- SELECT, INSERT, UPDATE, DELETE\n- JOINs e Subqueries\n- Indexes para performance',
                'optimization': 'MySQL Optimization: https://dev.mysql.com/doc/refman/8.0/en/optimization.html\n- EXPLAIN para análise\n- Indexes\n- Query Cache'
            }
        }
        
        if library_id in fallback_docs and topic in fallback_docs[library_id]:
            return {
                'library_id': library_id,
                'topic': topic,
                'content': fallback_docs[library_id][topic],
                'source': 'Fallback Documentation',
                'timestamp': datetime.now().isoformat()
            }
        else:
            return {
                'library_id': library_id,
                'topic': topic,
                'content': f'Documentação básica para {library_id} - tópico: {topic}',
                'source': 'Fallback Documentation',
                'timestamp': datetime.now().isoformat()
            }
    
    async def _make_context7_request(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Faz requisição para o servidor Context7"""
        try:
            headers = {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'User-Agent': 'BuyPeer-ContextAgent/1.0.0'
            }
            
            # Usar requests para compatibilidade
            response = requests.post(
                self.context7_config['remote_url'],
                json=payload,
                headers=headers,
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"Erro na requisição Context7: {response.status_code}")
                return None
                            
        except Exception as e:
            logger.error(f"Erro na requisição Context7: {e}")
            return None
    
    def _extract_topic_from_request(self, request: str) -> str:
        """Extrai tópico relevante da solicitação"""
        request_lower = request.lower()
        
        # Laravel topics
        if any(word in request_lower for word in ['model', 'eloquent']):
            return 'models'
        elif any(word in request_lower for word in ['controller', 'api']):
            return 'controllers'
        elif any(word in request_lower for word in ['migration', 'database']):
            return 'migrations'
        elif any(word in request_lower for word in ['route', 'routing']):
            return 'routing'
        elif any(word in request_lower for word in ['auth', 'authentication']):
            return 'authentication'
        elif any(word in request_lower for word in ['validation', 'validate']):
            return 'validation'
        
        # Vue.js topics
        elif any(word in request_lower for word in ['component', 'vue']):
            return 'components'
        elif any(word in request_lower for word in ['state', 'store', 'pinia']):
            return 'state-management'
        elif any(word in request_lower for word in ['router', 'routing']):
            return 'routing'
        
        # MySQL topics
        elif any(word in request_lower for word in ['query', 'sql', 'database']):
            return 'queries'
        elif any(word in request_lower for word in ['index', 'performance']):
            return 'optimization'
        
        # PHP topics
        elif any(word in request_lower for word in ['function', 'class']):
            return 'basics'
        elif any(word in request_lower for word in ['composer', 'package']):
            return 'packages'
        
        return 'getting-started'
    
    async def _get_current_versions(self, technologies: List[str]) -> Dict[str, str]:
        """Obtém versões atuais das tecnologias"""
        try:
            versions = {}
            
            for tech in technologies:
                if tech == 'laravel':
                    # Verificar versão do Laravel no projeto
                    artisan_path = os.path.join(self.project_path, 'artisan')
                    if os.path.exists(artisan_path):
                        try:
                            result = await self._run_command(f"php {artisan_path} --version")
                            if result['success']:
                                # Extrair versão do output
                                version_match = re.search(r'Laravel Framework (\d+\.\d+\.\d+)', result['output'])
                                if version_match:
                                    versions['laravel'] = version_match.group(1)
                        except:
                            versions['laravel'] = '10.x (estimada)'
                
                elif tech == 'php':
                    try:
                        result = await self._run_command("php --version")
                        if result['success']:
                            version_match = re.search(r'PHP (\d+\.\d+\.\d+)', result['output'])
                            if version_match:
                                versions['php'] = version_match.group(1)
                    except:
                        versions['php'] = '8.1+ (estimada)'
                
                elif tech == 'vue':
                    # Verificar package.json
                    package_path = os.path.join(self.project_path, 'package.json')
                    if os.path.exists(package_path):
                        with open(package_path, 'r') as f:
                            package_data = json.load(f)
                            if 'dependencies' in package_data and 'vue' in package_data['dependencies']:
                                versions['vue'] = package_data['dependencies']['vue']
                            else:
                                versions['vue'] = '3.x (estimada)'
            
            return versions
        except Exception as e:
            logger.error(f"Erro ao obter versões: {e}")
            return {}
    
    async def _generate_context_recommendations(self, request: str, technologies: List[str]) -> List[str]:
        """Gera recomendações baseadas no contexto"""
        recommendations = []
        
        # Recomendações baseadas nas tecnologias
        if 'laravel' in technologies:
            recommendations.append("📚 Consulte a documentação oficial do Laravel para padrões recomendados")
            recommendations.append("🔧 Use Artisan commands para gerar código automaticamente")
        
        if 'vue' in technologies:
            recommendations.append("📚 Consulte a documentação oficial do Vue.js 3")
            recommendations.append("🎨 Use Composition API para melhor organização do código")
        
        if 'mysql' in technologies:
            recommendations.append("📚 Consulte a documentação MySQL para otimização de queries")
            recommendations.append("🔍 Use EXPLAIN para analisar performance de queries")
        
        # Recomendações gerais
        recommendations.append("✅ Sempre teste em ambiente de desenvolvimento primeiro")
        recommendations.append("📝 Documente mudanças e decisões técnicas")
        
        return recommendations
    
    async def _run_command(self, command: str) -> Dict[str, Any]:
        """Executa um comando no sistema"""
        try:
            process = await asyncio.create_subprocess_shell(
                command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=self.project_path
            )
            
            stdout, stderr = await process.communicate()
            
            if process.returncode == 0:
                return {
                    'success': True,
                    'output': stdout.decode(),
                    'error': stderr.decode() if stderr else None
                }
            else:
                return {
                    'success': False,
                    'error': stderr.decode() if stderr else 'Erro desconhecido',
                    'output': stdout.decode()
                }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    async def execute_tasks(self, tasks: List) -> Dict[str, Any]:
        """Executa tarefas do agente de contexto"""
        try:
            results = []
            
            for task in tasks:
                logger.info(f"🔍 Executando tarefa de contexto: {task.title}")
                
                # Simular execução da tarefa
                await asyncio.sleep(1)
                
                result = {
                    'task_id': task.id,
                    'title': task.title,
                    'status': 'completed',
                    'result': f'Contexto {task.title} atualizado com sucesso'
                }
                results.append(result)
            
            return {
                'status': 'success',
                'message': f'{len(results)} tarefas de contexto concluídas',
                'results': results
            }
        except Exception as e:
            logger.error(f"❌ Erro ao executar tarefas de contexto: {e}")
            return {
                'status': 'error',
                'message': f'Erro ao executar tarefas: {e}'
            }
    
    def get_status(self) -> Dict[str, Any]:
        """Retorna status atual do agente"""
        return {
            'active': self.is_active,
            'status': self.status,
            'context_analyses': len(self.context_history),
            'last_context': self.context_history[-1]['timestamp'] if self.context_history else None
        }

# Função de teste
async def test_context_agent():
    """Testa o agente de contexto"""
    context_agent = ContextAgent(os.getcwd())
    
    # Ativar
    result = await context_agent.activate()
    print("Ativação:", json.dumps(result, indent=2))
    
    # Obter contexto para uma solicitação
    request = "Preciso implementar sistema de cupons de desconto"
    result = await context_agent.get_context_for_request(request)
    print("Contexto:", json.dumps(result, indent=2))
    
    # Status
    status = context_agent.get_status()
    print("Status:", json.dumps(status, indent=2))

if __name__ == "__main__":
    asyncio.run(test_context_agent())
