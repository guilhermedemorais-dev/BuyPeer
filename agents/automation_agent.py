#!/usr/bin/env python3
"""
Agente de Automação Avançado - Executa comandos reais e navega no navegador
Faz TUDO automaticamente: servidor, navegador, testes, etc.
"""

import asyncio
import json
import logging
import os
import re
import subprocess
import time
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from datetime import datetime
import requests
from playwright.async_api import async_playwright, Browser, Page
import psutil

logger = logging.getLogger(__name__)

@dataclass
class AutomationTask:
    """Representa uma tarefa de automação"""
    id: str
    command: str
    description: str
    type: str  # server, browser, test, system
    status: str = "pending"
    result: Optional[Dict] = None
    timestamp: datetime = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()

class AutomationAgent:
    """
    Agente de Automação Avançado - Executa TUDO automaticamente
    """
    
    def __init__(self, project_path: str):
        self.project_path = project_path
        self.is_active = False
        self.status = "inactive"
        self.browser = None
        self.page = None
        self.server_process = None
        self.tasks_history = []
        
        # Configurações
        self.config = {
            'server_port': 8000,
            'server_host': '0.0.0.0',
            'browser_type': 'chromium',  # chromium, firefox, webkit
            'headless': False,
            'incognito': True,
            'timeout': 30000
        }
        
        logger.info("Agente de Automação Avançado inicializado")
    
    async def activate(self) -> Dict[str, Any]:
        """Ativa o agente de automação"""
        try:
            self.is_active = True
            self.status = "active"
            
            # Inicializar Playwright
            self.playwright = await async_playwright().start()
            
            logger.info("✅ Agente de Automação Avançado ativado com sucesso!")
            
            return {
                'status': 'success',
                'message': 'Agente de Automação Avançado ativado',
                'capabilities': [
                    'Execução automática de comandos',
                    'Controle de servidor Laravel',
                    'Navegação automática no navegador',
                    'Testes E2E reais',
                    'Screenshots automáticos',
                    'Relatórios detalhados'
                ]
            }
        except Exception as e:
            logger.error(f"❌ Erro ao ativar Agente de Automação: {e}")
            return {
                'status': 'error',
                'message': f'Erro ao ativar: {e}'
            }
    
    async def deactivate(self) -> Dict[str, Any]:
        """Desativa o agente de automação"""
        try:
            # Fechar navegador
            await self._close_browser()
            
            # Parar servidor
            await self._stop_server()
            
            # Fechar Playwright
            if hasattr(self, 'playwright'):
                await self.playwright.stop()
            
            self.is_active = False
            self.status = "inactive"
            return {
                'status': 'success',
                'message': 'Agente de Automação Avançado desativado'
            }
        except Exception as e:
            logger.error(f"Erro ao desativar: {e}")
            return {
                'status': 'error',
                'message': f'Erro ao desativar: {e}'
            }
    
    async def execute_command(self, command: str) -> Dict[str, Any]:
        """Executa um comando de automação"""
        try:
            logger.info(f"🤖 Executando comando: {command}")
            
            # Analisar comando
            if "servidor" in command.lower() or "laravel" in command.lower():
                return await self._handle_server_command(command)
            elif "navegador" in command.lower() or "browser" in command.lower():
                return await self._handle_browser_command(command)
            elif "teste" in command.lower() or "test" in command.lower():
                return await self._handle_test_command(command)
            elif "sistema" in command.lower() or "system" in command.lower():
                return await self._handle_system_command(command)
            else:
                return await self._handle_general_command(command)
                
        except Exception as e:
            logger.error(f"❌ Erro ao executar comando: {e}")
            return {
                'status': 'error',
                'message': f'Erro ao executar comando: {e}'
            }
    
    async def _handle_server_command(self, command: str) -> Dict[str, Any]:
        """Manipula comandos relacionados ao servidor"""
        try:
            if "iniciar" in command.lower() or "start" in command.lower():
                return await self._start_laravel_server()
            elif "parar" in command.lower() or "stop" in command.lower():
                return await self._stop_server()
            elif "status" in command.lower():
                return await self._check_server_status()
            else:
                return await self._start_laravel_server()
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
    
    async def _handle_browser_command(self, command: str) -> Dict[str, Any]:
        """Manipula comandos relacionados ao navegador"""
        try:
            if "abrir" in command.lower() or "open" in command.lower():
                return await self._open_browser()
            elif "navegar" in command.lower() or "navigate" in command.lower():
                return await self._navigate_to_site()
            elif "fechar" in command.lower() or "close" in command.lower():
                return await self._close_browser()
            else:
                return await self._open_browser()
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
    
    async def _handle_test_command(self, command: str) -> Dict[str, Any]:
        """Manipula comandos de teste"""
        try:
            if "frontend" in command.lower():
                return await self._test_frontend()
            elif "e2e" in command.lower():
                return await self._test_e2e()
            elif "performance" in command.lower():
                return await self._test_performance()
            else:
                return await self._test_frontend()
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
    
    async def _handle_system_command(self, command: str) -> Dict[str, Any]:
        """Manipula comandos do sistema"""
        try:
            if "status" in command.lower():
                return await self._get_system_status()
            elif "limpar" in command.lower() or "clear" in command.lower():
                return await self._clear_cache()
            else:
                return await self._get_system_status()
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
    
    async def _handle_general_command(self, command: str) -> Dict[str, Any]:
        """Manipula comandos gerais"""
        try:
            # Tentar executar como comando do sistema
            result = await self._run_system_command(command)
            return {
                'status': 'success',
                'message': f'Comando executado: {command}',
                'result': result
            }
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
    
    async def _start_laravel_server(self) -> Dict[str, Any]:
        """Inicia o servidor Laravel"""
        try:
            # Verificar se já está rodando
            server_status = await self._check_server_status()
            if server_status['running']:
                return {
                    'status': 'success',
                    'message': 'Servidor Laravel já está rodando',
                    'url': f'http://localhost:{self.config["server_port"]}'
                }
            
            # Iniciar servidor
            logger.info("🚀 Iniciando servidor Laravel...")
            
            command = f"cd {self.project_path} && php artisan serve --host={self.config['server_host']} --port={self.config['server_port']}"
            
            self.server_process = await asyncio.create_subprocess_shell(
                command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            # Aguardar servidor inicializar
            await asyncio.sleep(5)
            
            # Verificar se está rodando
            server_status = await self._check_server_status()
            if server_status['running']:
                return {
                    'status': 'success',
                    'message': 'Servidor Laravel iniciado com sucesso',
                    'url': f'http://localhost:{self.config["server_port"]}',
                    'pid': self.server_process.pid
                }
            else:
                return {
                    'status': 'error',
                    'message': 'Falha ao iniciar servidor Laravel'
                }
                
        except Exception as e:
            logger.error(f"Erro ao iniciar servidor: {e}")
            return {'status': 'error', 'message': str(e)}
    
    async def _stop_server(self) -> Dict[str, Any]:
        """Para o servidor Laravel"""
        try:
            if self.server_process:
                self.server_process.terminate()
                await self.server_process.wait()
                self.server_process = None
                logger.info("🛑 Servidor Laravel parado")
            
            return {
                'status': 'success',
                'message': 'Servidor Laravel parado'
            }
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
    
    async def _check_server_status(self) -> Dict[str, Any]:
        """Verifica status do servidor"""
        try:
            # Verificar processo
            if self.server_process and self.server_process.poll() is None:
                return {'running': True, 'pid': self.server_process.pid}
            
            # Verificar porta
            try:
                response = requests.get(f"http://localhost:{self.config['server_port']}", timeout=5)
                return {'running': True, 'status_code': response.status_code}
            except:
                return {'running': False}
                
        except Exception as e:
            return {'running': False, 'error': str(e)}
    
    async def _open_browser(self) -> Dict[str, Any]:
        """Abre o navegador"""
        try:
            if self.browser:
                return {
                    'status': 'success',
                    'message': 'Navegador já está aberto'
                }
            
            logger.info("🌐 Abrindo navegador...")
            
            # Configurar navegador
            browser_args = []
            if self.config['incognito']:
                browser_args.append('--incognito')
            
            self.browser = await self.playwright.chromium.launch(
                headless=self.config['headless'],
                args=browser_args
            )
            
            # Criar contexto
            context = await self.browser.new_context()
            self.page = await context.new_page()
            
            logger.info("✅ Navegador aberto com sucesso")
            
            return {
                'status': 'success',
                'message': 'Navegador aberto com sucesso',
                'browser_type': self.config['browser_type']
            }
            
        except Exception as e:
            logger.error(f"Erro ao abrir navegador: {e}")
            return {'status': 'error', 'message': str(e)}
    
    async def _close_browser(self) -> Dict[str, Any]:
        """Fecha o navegador"""
        try:
            if self.browser:
                await self.browser.close()
                self.browser = None
                self.page = None
                logger.info("🌐 Navegador fechado")
            
            return {
                'status': 'success',
                'message': 'Navegador fechado'
            }
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
    
    async def _navigate_to_site(self) -> Dict[str, Any]:
        """Navega para o site"""
        try:
            if not self.page:
                await self._open_browser()
            
            url = f"http://localhost:{self.config['server_port']}"
            logger.info(f"🌐 Navegando para: {url}")
            
            await self.page.goto(url, timeout=self.config['timeout'])
            
            # Aguardar carregamento
            await self.page.wait_for_load_state('networkidle')
            
            # Capturar screenshot
            screenshot_path = os.path.join(self.project_path, 'screenshots', f'navigation_{datetime.now().strftime("%Y%m%d_%H%M%S")}.png')
            os.makedirs(os.path.dirname(screenshot_path), exist_ok=True)
            await self.page.screenshot(path=screenshot_path)
            
            # Verificar elementos básicos
            title = await self.page.title()
            
            return {
                'status': 'success',
                'message': f'Site carregado com sucesso: {title}',
                'url': url,
                'title': title,
                'screenshot': screenshot_path
            }
            
        except Exception as e:
            logger.error(f"Erro ao navegar: {e}")
            return {'status': 'error', 'message': str(e)}
    
    async def _test_frontend(self) -> Dict[str, Any]:
        """Testa o frontend"""
        try:
            logger.info("🧪 Testando frontend...")
            
            # Garantir que navegador está aberto
            if not self.page:
                await self._navigate_to_site()
            
            tests = []
            
            # Teste 1: Verificar se página carrega
            try:
                title = await self.page.title()
                tests.append({
                    'name': 'Carregamento da página',
                    'status': 'passed',
                    'result': f'Título: {title}'
                })
            except Exception as e:
                tests.append({
                    'name': 'Carregamento da página',
                    'status': 'failed',
                    'result': str(e)
                })
            
            # Teste 2: Verificar elementos básicos
            try:
                # Verificar se há elementos de navegação
                nav_elements = await self.page.query_selector_all('nav, .navbar, .header')
                tests.append({
                    'name': 'Elementos de navegação',
                    'status': 'passed' if nav_elements else 'failed',
                    'result': f'Encontrados {len(nav_elements)} elementos'
                })
            except Exception as e:
                tests.append({
                    'name': 'Elementos de navegação',
                    'status': 'failed',
                    'result': str(e)
                })
            
            # Teste 3: Verificar responsividade
            try:
                # Testar em tamanho mobile
                await self.page.set_viewport_size({'width': 375, 'height': 667})
                await asyncio.sleep(2)
                
                # Verificar se elementos ainda estão visíveis
                visible_elements = await self.page.query_selector_all('*:visible')
                tests.append({
                    'name': 'Responsividade mobile',
                    'status': 'passed' if len(visible_elements) > 10 else 'failed',
                    'result': f'{len(visible_elements)} elementos visíveis'
                })
                
                # Voltar ao tamanho normal
                await self.page.set_viewport_size({'width': 1920, 'height': 1080})
            except Exception as e:
                tests.append({
                    'name': 'Responsividade mobile',
                    'status': 'failed',
                    'result': str(e)
                })
            
            # Capturar screenshot final
            screenshot_path = os.path.join(self.project_path, 'screenshots', f'frontend_test_{datetime.now().strftime("%Y%m%d_%H%M%S")}.png')
            await self.page.screenshot(path=screenshot_path)
            
            # Calcular resultados
            passed = len([t for t in tests if t['status'] == 'passed'])
            total = len(tests)
            success_rate = (passed / total) * 100 if total > 0 else 0
            
            return {
                'status': 'success',
                'message': f'Teste de frontend concluído: {passed}/{total} passaram',
                'tests': tests,
                'success_rate': success_rate,
                'screenshot': screenshot_path
            }
            
        except Exception as e:
            logger.error(f"Erro no teste de frontend: {e}")
            return {'status': 'error', 'message': str(e)}
    
    async def _test_e2e(self) -> Dict[str, Any]:
        """Testes E2E completos"""
        try:
            logger.info("🧪 Executando testes E2E...")
            
            # Garantir que navegador está aberto
            if not self.page:
                await self._navigate_to_site()
            
            tests = []
            
            # Teste de navegação
            try:
                # Tentar clicar em links de navegação
                links = await self.page.query_selector_all('a[href]')
                if links:
                    await links[0].click()
                    await asyncio.sleep(2)
                    tests.append({
                        'name': 'Navegação por links',
                        'status': 'passed',
                        'result': 'Navegação funcionando'
                    })
                else:
                    tests.append({
                        'name': 'Navegação por links',
                        'status': 'failed',
                        'result': 'Nenhum link encontrado'
                    })
            except Exception as e:
                tests.append({
                    'name': 'Navegação por links',
                    'status': 'failed',
                    'result': str(e)
                })
            
            # Teste de formulários
            try:
                forms = await self.page.query_selector_all('form')
                if forms:
                    tests.append({
                        'name': 'Formulários',
                        'status': 'passed',
                        'result': f'{len(forms)} formulários encontrados'
                    })
                else:
                    tests.append({
                        'name': 'Formulários',
                        'status': 'warning',
                        'result': 'Nenhum formulário encontrado'
                    })
            except Exception as e:
                tests.append({
                    'name': 'Formulários',
                    'status': 'failed',
                    'result': str(e)
                })
            
            # Capturar screenshot
            screenshot_path = os.path.join(self.project_path, 'screenshots', f'e2e_test_{datetime.now().strftime("%Y%m%d_%H%M%S")}.png')
            await self.page.screenshot(path=screenshot_path)
            
            # Calcular resultados
            passed = len([t for t in tests if t['status'] == 'passed'])
            total = len(tests)
            success_rate = (passed / total) * 100 if total > 0 else 0
            
            return {
                'status': 'success',
                'message': f'Testes E2E concluídos: {passed}/{total} passaram',
                'tests': tests,
                'success_rate': success_rate,
                'screenshot': screenshot_path
            }
            
        except Exception as e:
            logger.error(f"Erro nos testes E2E: {e}")
            return {'status': 'error', 'message': str(e)}
    
    async def _test_performance(self) -> Dict[str, Any]:
        """Testa performance"""
        try:
            logger.info("⚡ Testando performance...")
            
            if not self.page:
                await self._navigate_to_site()
            
            # Medir tempo de carregamento
            start_time = time.time()
            await self.page.reload()
            await self.page.wait_for_load_state('networkidle')
            load_time = time.time() - start_time
            
            # Verificar performance
            performance_data = await self.page.evaluate("""
                () => {
                    const perf = performance.getEntriesByType('navigation')[0];
                    return {
                        domContentLoaded: perf.domContentLoadedEventEnd - perf.domContentLoadedEventStart,
                        loadComplete: perf.loadEventEnd - perf.loadEventStart,
                        totalTime: perf.loadEventEnd - perf.navigationStart
                    };
                }
            """)
            
            # Capturar screenshot
            screenshot_path = os.path.join(self.project_path, 'screenshots', f'performance_test_{datetime.now().strftime("%Y%m%d_%H%M%S")}.png')
            await self.page.screenshot(path=screenshot_path)
            
            return {
                'status': 'success',
                'message': 'Teste de performance concluído',
                'load_time': load_time,
                'performance_data': performance_data,
                'screenshot': screenshot_path
            }
            
        except Exception as e:
            logger.error(f"Erro no teste de performance: {e}")
            return {'status': 'error', 'message': str(e)}
    
    async def _get_system_status(self) -> Dict[str, Any]:
        """Obtém status do sistema"""
        try:
            # Status do servidor
            server_status = await self._check_server_status()
            
            # Status do navegador
            browser_status = self.browser is not None
            
            # Uso de recursos
            cpu_percent = psutil.cpu_percent()
            memory = psutil.virtual_memory()
            
            return {
                'status': 'success',
                'message': 'Status do sistema obtido',
                'server': server_status,
                'browser': browser_status,
                'system': {
                    'cpu_percent': cpu_percent,
                    'memory_percent': memory.percent,
                    'memory_available': memory.available
                }
            }
            
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
    
    async def _clear_cache(self) -> Dict[str, Any]:
        """Limpa cache do sistema"""
        try:
            # Limpar cache do Laravel
            await self._run_system_command("php artisan cache:clear")
            await self._run_system_command("php artisan config:clear")
            await self._run_system_command("php artisan view:clear")
            
            return {
                'status': 'success',
                'message': 'Cache limpo com sucesso'
            }
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
    
    async def _run_system_command(self, command: str) -> Dict[str, Any]:
        """Executa comando do sistema"""
        try:
            process = await asyncio.create_subprocess_shell(
                command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=self.project_path
            )
            
            stdout, stderr = await process.communicate()
            
            return {
                'success': process.returncode == 0,
                'output': stdout.decode(),
                'error': stderr.decode() if stderr else None,
                'return_code': process.returncode
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    async def execute_tasks(self, tasks: List) -> Dict[str, Any]:
        """Executa tarefas de automação"""
        try:
            results = []
            
            for task in tasks:
                logger.info(f"🤖 Executando tarefa: {task.title}")
                
                # Executar comando baseado na tarefa
                result = await self.execute_command(task.title)
                
                task_result = {
                    'task_id': task.id,
                    'title': task.title,
                    'status': 'completed',
                    'result': result
                }
                results.append(task_result)
            
            return {
                'status': 'success',
                'message': f'{len(results)} tarefas de automação concluídas',
                'results': results
            }
        except Exception as e:
            logger.error(f"❌ Erro ao executar tarefas: {e}")
            return {
                'status': 'error',
                'message': f'Erro ao executar tarefas: {e}'
            }
    
    def get_status(self) -> Dict[str, Any]:
        """Retorna status atual do agente"""
        return {
            'active': self.is_active,
            'status': self.status,
            'server_running': self.server_process is not None,
            'browser_open': self.browser is not None,
            'tasks_executed': len(self.tasks_history)
        }

# Função de teste
async def test_automation_agent():
    """Testa o agente de automação"""
    automation_agent = AutomationAgent(os.getcwd())
    
    # Ativar
    result = await automation_agent.activate()
    print("Ativação:", json.dumps(result, indent=2, default=str))
    
    # Executar comando de teste
    result = await automation_agent.execute_command("iniciar servidor laravel e testar frontend")
    print("Resultado:", json.dumps(result, indent=2, default=str))
    
    # Status
    status = automation_agent.get_status()
    print("Status:", json.dumps(status, indent=2, default=str))
    
    # Desativar
    await automation_agent.deactivate()

if __name__ == "__main__":
    asyncio.run(test_automation_agent())
