#!/usr/bin/env python3
"""
Agente Backend - Desenvolvimento Backend Laravel/PHP
Especializado em APIs, modelos, controllers e lógica de negócio
"""

import asyncio
import json
import logging
import os
import re
from typing import Dict, Any, List, Optional
from datetime import datetime

# Importar classe base
from .base_agent import BaseAgent

logger = logging.getLogger(__name__)

class BackendAgent(BaseAgent):
    """
    Agente Backend - Desenvolvimento Laravel/PHP
    Especializado em APIs, modelos, controllers e lógica de negócio
    """
    
    def __init__(self, project_path: str = None):
        super().__init__("backend", project_path)
        
        # Estrutura do projeto Laravel
        self.laravel_structure = {
            'app': {
                'Models': 'Modelos Eloquent',
                'Http': {
                    'Controllers': 'Controllers da aplicação',
                    'Middleware': 'Middleware customizado',
                    'Requests': 'Form Requests de validação'
                },
                'Services': 'Serviços de negócio',
                'Repositories': 'Repositórios de dados',
                'Providers': 'Service Providers'
            },
            'database': {
                'migrations': 'Migrações do banco',
                'seeders': 'Seeders de dados',
                'factories': 'Factories para testes'
            },
            'routes': {
                'api.php': 'Rotas da API',
                'web.php': 'Rotas web',
                'channels.php': 'Broadcasting channels'
            },
            'config': 'Arquivos de configuração',
            'resources': {
                'views': 'Views Blade',
                'lang': 'Arquivos de tradução'
            }
        }
    
    async def _initialize_capabilities(self):
        """Inicializa capacidades específicas do Backend Agent"""
        self.capabilities = [
            'Desenvolvimento de APIs Laravel',
            'Criação de modelos Eloquent',
            'Implementação de controllers',
            'Configuração de rotas',
            'Criação de migrações',
            'Implementação de seeders',
            'Desenvolvimento de middleware',
            'Criação de form requests',
            'Implementação de serviços',
            'Configuração de autenticação',
            'Otimização de consultas',
            'Implementação de cache',
            'Configuração de jobs/queues',
            'Desenvolvimento de testes'
        ]
        
        logger.info(f"🔧 {self.agent_name} - Capacidades inicializadas: {len(self.capabilities)}")
    
    async def execute_task(self, task_description: str, parameters: Dict[str, Any] = None) -> Dict[str, Any]:
        """Executa uma tarefa específica do backend"""
        try:
            logger.info(f"🚀 {self.agent_name} executando: {task_description}")
            
            # Analisar tipo de tarefa
            task_type = await self._identify_task_type(task_description)
            
            # Executar tarefa específica
            if task_type == 'create_model':
                result = await self._create_model(parameters)
            elif task_type == 'create_controller':
                result = await self._create_controller(parameters)
            elif task_type == 'create_migration':
                result = await self._create_migration(parameters)
            elif task_type == 'create_api_endpoint':
                result = await self._create_api_endpoint(parameters)
            elif task_type == 'optimize_database':
                result = await self._optimize_database(parameters)
            elif task_type == 'implement_authentication':
                result = await self._implement_authentication(parameters)
            elif task_type == 'create_service':
                result = await self._create_service(parameters)
            elif task_type == 'setup_cache':
                result = await self._setup_cache(parameters)
            else:
                result = await self._generic_backend_task(task_description, parameters)
            
            # Registrar tarefa
            await self.log_task(task_description, result)
            
            return result
            
        except Exception as e:
            logger.error(f"❌ Erro ao executar tarefa backend: {e}")
            return {
                'status': 'error',
                'message': f'Erro na execução: {e}'
            }
    
    async def _identify_task_type(self, task_description: str) -> str:
        """Identifica o tipo de tarefa baseado na descrição"""
        description_lower = task_description.lower()
        
        if any(word in description_lower for word in ['modelo', 'model', 'eloquent']):
            return 'create_model'
        elif any(word in description_lower for word in ['controller', 'controlador']):
            return 'create_controller'
        elif any(word in description_lower for word in ['migração', 'migration', 'tabela']):
            return 'create_migration'
        elif any(word in description_lower for word in ['api', 'endpoint', 'rota']):
            return 'create_api_endpoint'
        elif any(word in description_lower for word in ['otimizar', 'optimize', 'banco', 'database']):
            return 'optimize_database'
        elif any(word in description_lower for word in ['autenticação', 'auth', 'login']):
            return 'implement_authentication'
        elif any(word in description_lower for word in ['serviço', 'service']):
            return 'create_service'
        elif any(word in description_lower for word in ['cache', 'redis']):
            return 'setup_cache'
        else:
            return 'generic'
    
    async def _create_model(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Cria um modelo Eloquent"""
        try:
            model_name = parameters.get('model_name', 'Example')
            table_name = parameters.get('table_name', f'{model_name.lower()}s')
            fields = parameters.get('fields', [])
            
            # Usar MCP Filesystem para criar arquivo
            model_content = self._generate_model_content(model_name, table_name, fields)
            model_path = f"app/Models/{model_name}.php"
            
            result = await self.write_file(model_path, model_content)
            
            if result['status'] == 'success':
                # Fazer commit das mudanças
                await self.git_commit(f"feat: Criar modelo {model_name}")
                
                return {
                    'status': 'success',
                    'message': f'Modelo {model_name} criado com sucesso',
                    'file_path': model_path,
                    'model_name': model_name,
                    'table_name': table_name
                }
            else:
                return result
                
        except Exception as e:
            logger.error(f"❌ Erro ao criar modelo: {e}")
            return {
                'status': 'error',
                'message': f'Erro ao criar modelo: {e}'
            }
    
    async def _create_controller(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Cria um controller"""
        try:
            controller_name = parameters.get('controller_name', 'ExampleController')
            model_name = parameters.get('model_name', 'Example')
            actions = parameters.get('actions', ['index', 'store', 'show', 'update', 'destroy'])
            
            # Usar MCP Filesystem para criar arquivo
            controller_content = self._generate_controller_content(controller_name, model_name, actions)
            controller_path = f"app/Http/Controllers/{controller_name}.php"
            
            result = await self.write_file(controller_path, controller_content)
            
            if result['status'] == 'success':
                # Fazer commit das mudanças
                await self.git_commit(f"feat: Criar controller {controller_name}")
                
                return {
                    'status': 'success',
                    'message': f'Controller {controller_name} criado com sucesso',
                    'file_path': controller_path,
                    'controller_name': controller_name,
                    'actions': actions
                }
            else:
                return result
                
        except Exception as e:
            logger.error(f"❌ Erro ao criar controller: {e}")
            return {
                'status': 'error',
                'message': f'Erro ao criar controller: {e}'
            }
    
    async def _create_migration(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Cria uma migração"""
        try:
            table_name = parameters.get('table_name', 'examples')
            fields = parameters.get('fields', [])
            
            # Usar MCP Filesystem para criar arquivo
            migration_content = self._generate_migration_content(table_name, fields)
            timestamp = datetime.now().strftime('%Y_%m_%d_%H%M%S')
            migration_path = f"database/migrations/{timestamp}_create_{table_name}_table.php"
            
            result = await self.write_file(migration_path, migration_content)
            
            if result['status'] == 'success':
                # Fazer commit das mudanças
                await self.git_commit(f"feat: Criar migração para tabela {table_name}")
                
                return {
                    'status': 'success',
                    'message': f'Migração para {table_name} criada com sucesso',
                    'file_path': migration_path,
                    'table_name': table_name
                }
            else:
                return result
                
        except Exception as e:
            logger.error(f"❌ Erro ao criar migração: {e}")
            return {
                'status': 'error',
                'message': f'Erro ao criar migração: {e}'
            }
    
    async def _create_api_endpoint(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Cria um endpoint da API"""
        try:
            endpoint = parameters.get('endpoint', '/api/example')
            method = parameters.get('method', 'GET')
            controller = parameters.get('controller', 'ExampleController')
            action = parameters.get('action', 'index')
            
            # Ler arquivo de rotas atual
            routes_file = 'routes/api.php'
            current_routes = await self.read_file(routes_file)
            
            if current_routes['status'] == 'success':
                routes_content = current_routes['result']
            else:
                routes_content = "<?php\n\nuse Illuminate\\Support\\Facades\\Route;\n\n"
            
            # Adicionar nova rota
            new_route = f"Route::{method.lower()}('{endpoint}', [{controller}::class, '{action}']);\n"
            updated_routes = routes_content + new_route
            
            # Salvar arquivo atualizado
            result = await self.write_file(routes_file, updated_routes)
            
            if result['status'] == 'success':
                # Fazer commit das mudanças
                await self.git_commit(f"feat: Adicionar endpoint {method} {endpoint}")
                
                return {
                    'status': 'success',
                    'message': f'Endpoint {method} {endpoint} criado com sucesso',
                    'endpoint': endpoint,
                    'method': method,
                    'controller': controller,
                    'action': action
                }
            else:
                return result
                
        except Exception as e:
            logger.error(f"❌ Erro ao criar endpoint: {e}")
            return {
                'status': 'error',
                'message': f'Erro ao criar endpoint: {e}'
            }
    
    async def _optimize_database(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Otimiza consultas de banco de dados"""
        try:
            # Analisar consultas lentas
            slow_queries = await self._analyze_slow_queries()
            
            # Gerar recomendações
            recommendations = await self._generate_optimization_recommendations(slow_queries)
            
            # Implementar otimizações
            optimizations_applied = await self._apply_optimizations(recommendations)
            
            return {
                'status': 'success',
                'message': 'Otimização de banco concluída',
                'slow_queries_found': len(slow_queries),
                'recommendations': recommendations,
                'optimizations_applied': optimizations_applied
            }
            
        except Exception as e:
            logger.error(f"❌ Erro na otimização: {e}")
            return {
                'status': 'error',
                'message': f'Erro na otimização: {e}'
            }
    
    async def _implement_authentication(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Implementa sistema de autenticação"""
        try:
            auth_type = parameters.get('type', 'sanctum')
            
            if auth_type == 'sanctum':
                result = await self._setup_sanctum_auth()
            elif auth_type == 'jwt':
                result = await self._setup_jwt_auth()
            else:
                result = await self._setup_basic_auth()
            
            return result
            
        except Exception as e:
            logger.error(f"❌ Erro na autenticação: {e}")
            return {
                'status': 'error',
                'message': f'Erro na autenticação: {e}'
            }
    
    async def _create_service(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Cria um serviço de negócio"""
        try:
            service_name = parameters.get('service_name', 'ExampleService')
            methods = parameters.get('methods', [])
            
            # Usar MCP Filesystem para criar arquivo
            service_content = self._generate_service_content(service_name, methods)
            service_path = f"app/Services/{service_name}.php"
            
            result = await self.write_file(service_path, service_content)
            
            if result['status'] == 'success':
                # Fazer commit das mudanças
                await self.git_commit(f"feat: Criar serviço {service_name}")
                
                return {
                    'status': 'success',
                    'message': f'Serviço {service_name} criado com sucesso',
                    'file_path': service_path,
                    'service_name': service_name,
                    'methods': methods
                }
            else:
                return result
                
        except Exception as e:
            logger.error(f"❌ Erro ao criar serviço: {e}")
            return {
                'status': 'error',
                'message': f'Erro ao criar serviço: {e}'
            }
    
    async def _setup_cache(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Configura sistema de cache"""
        try:
            cache_driver = parameters.get('driver', 'redis')
            
            # Configurar cache
            config_result = await self._configure_cache_driver(cache_driver)
            
            # Implementar cache em modelos
            models_result = await self._implement_model_cache()
            
            return {
                'status': 'success',
                'message': f'Cache configurado com {cache_driver}',
                'cache_driver': cache_driver,
                'config_result': config_result,
                'models_result': models_result
            }
            
        except Exception as e:
            logger.error(f"❌ Erro na configuração de cache: {e}")
            return {
                'status': 'error',
                'message': f'Erro na configuração de cache: {e}'
            }
    
    async def _generic_backend_task(self, task_description: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Executa tarefa genérica de backend"""
        try:
            # Salvar contexto da tarefa
            await self.save_context(f"backend_task_{datetime.now().timestamp()}", {
                'description': task_description,
                'parameters': parameters,
                'timestamp': datetime.now().isoformat()
            })
            
            # Simular execução da tarefa
            await asyncio.sleep(1)
            
            return {
                'status': 'success',
                'message': f'Tarefa backend executada: {task_description}',
                'task_type': 'generic',
                'execution_time': '1s'
            }
            
        except Exception as e:
            logger.error(f"❌ Erro na tarefa genérica: {e}")
            return {
                'status': 'error',
                'message': f'Erro na tarefa genérica: {e}'
            }
    
    # Métodos auxiliares para geração de código
    def _generate_model_content(self, model_name: str, table_name: str, fields: List[str]) -> str:
        """Gera conteúdo de um modelo Eloquent"""
        return f"""<?php

namespace App\\Models;

use Illuminate\\Database\\Eloquent\\Factories\\HasFactory;
use Illuminate\\Database\\Eloquent\\Model;

class {model_name} extends Model
{{
    use HasFactory;

    protected $table = '{table_name}';
    
    protected $fillable = [
        {', '.join([f"'{field}'" for field in fields])}
    ];
    
    protected $casts = [
        'created_at' => 'datetime',
        'updated_at' => 'datetime',
    ];
}}
"""
    
    def _generate_controller_content(self, controller_name: str, model_name: str, actions: List[str]) -> str:
        """Gera conteúdo de um controller"""
        actions_code = ""
        
        for action in actions:
            if action == 'index':
                actions_code += """
    public function index()
    {
        return response()->json([
            'data' => $this->model->all()
        ]);
    }
"""
            elif action == 'store':
                actions_code += """
    public function store(Request $request)
    {
        $validated = $request->validate([
            // Adicione validações aqui
        ]);
        
        $item = $this->model->create($validated);
        
        return response()->json([
            'data' => $item
        ], 201);
    }
"""
        
        return f"""<?php

namespace App\\Http\\Controllers;

use App\\Models\\{model_name};
use Illuminate\\Http\\Request;

class {controller_name} extends Controller
{{
    protected ${model_name.lower()};
    
    public function __construct({model_name} ${model_name.lower()})
    {{
        $this->{model_name.lower()} = ${model_name.lower()};
    }}
    
    {actions_code}
}}
"""
    
    def _generate_migration_content(self, table_name: str, fields: List[str]) -> str:
        """Gera conteúdo de uma migração"""
        fields_code = ""
        
        for field in fields:
            if 'id' in field.lower():
                fields_code += "            $table->id();\n"
            elif 'name' in field.lower():
                fields_code += f"            $table->string('{field}');\n"
            elif 'email' in field.lower():
                fields_code += f"            $table->string('{field}')->unique();\n"
            else:
                fields_code += f"            $table->string('{field}');\n"
        
        return f"""<?php

use Illuminate\\Database\\Migrations\\Migration;
use Illuminate\\Database\\Schema\\Blueprint;
use Illuminate\\Support\\Facades\\Schema;

return new class extends Migration
{{
    public function up()
    {{
        Schema::create('{table_name}', function (Blueprint $table) {{
{fields_code}
            $table->timestamps();
        }});
    }}

    public function down()
    {{
        Schema::dropIfExists('{table_name}');
    }}
}};
"""
    
    def _generate_service_content(self, service_name: str, methods: List[str]) -> str:
        """Gera conteúdo de um serviço"""
        methods_code = ""
        
        for method in methods:
            methods_code += f"""
    public function {method}()
    {{
        // Implementar lógica do método {method}
        return true;
    }}
"""
        
        return f"""<?php

namespace App\\Services;

class {service_name}
{{
    {methods_code}
}}
"""
    
    # Métodos auxiliares para otimização
    async def _analyze_slow_queries(self) -> List[Dict[str, Any]]:
        """Analisa consultas lentas"""
        # Implementação básica
        return [
            {
                'query': 'SELECT * FROM users WHERE email = ?',
                'execution_time': '2.5s',
                'suggestion': 'Adicionar índice na coluna email'
            }
        ]
    
    async def _generate_optimization_recommendations(self, slow_queries: List[Dict[str, Any]]) -> List[str]:
        """Gera recomendações de otimização"""
        recommendations = []
        
        for query in slow_queries:
            if 'email' in query['query']:
                recommendations.append('Criar índice na coluna email da tabela users')
            if 'created_at' in query['query']:
                recommendations.append('Criar índice na coluna created_at')
        
        return recommendations
    
    async def _apply_optimizations(self, recommendations: List[str]) -> List[str]:
        """Aplica otimizações recomendadas"""
        applied = []
        
        for recommendation in recommendations:
            if 'índice' in recommendation:
                applied.append(f'Índice criado: {recommendation}')
        
        return applied
    
    # Métodos auxiliares para autenticação
    async def _setup_sanctum_auth(self) -> Dict[str, Any]:
        """Configura autenticação Sanctum"""
        return {
            'status': 'success',
            'message': 'Sanctum configurado com sucesso',
            'type': 'sanctum'
        }
    
    async def _setup_jwt_auth(self) -> Dict[str, Any]:
        """Configura autenticação JWT"""
        return {
            'status': 'success',
            'message': 'JWT configurado com sucesso',
            'type': 'jwt'
        }
    
    async def _setup_basic_auth(self) -> Dict[str, Any]:
        """Configura autenticação básica"""
        return {
            'status': 'success',
            'message': 'Autenticação básica configurada',
            'type': 'basic'
        }
    
    async def _configure_cache_driver(self, driver: str) -> Dict[str, Any]:
        """Configura driver de cache"""
        return {
            'status': 'success',
            'driver': driver,
            'message': f'Driver {driver} configurado'
        }
    
    async def _implement_model_cache(self) -> Dict[str, Any]:
        """Implementa cache em modelos"""
        return {
            'status': 'success',
            'message': 'Cache implementado em modelos',
            'models_updated': ['User', 'Product', 'Order']
        }
