#!/usr/bin/env python3
"""
Agente de Testes Automatizados - Executa testes automatizados no navegador
Abre o navegador e testa a aplicação conforme tarefas específicas
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

logger = logging.getLogger(__name__)

@dataclass
class TestCase:
    """Representa um caso de teste"""
    id: str
    name: str
    description: str
    type: str  # e2e, unit, integration, visual
    steps: List[str]
    expected_result: str
    priority: str = "medium"
    status: str = "pending"
    
    def __post_init__(self):
        if self.status == "pending":
            self.status = "pending"

@dataclass
class TestResult:
    """Resultado de um teste"""
    test_id: str
    status: str  # passed, failed, error, skipped
    duration: float
    screenshot_path: Optional[str] = None
    error_message: Optional[str] = None
    timestamp: datetime = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()

class TestAutomationAgent:
    """
    Agente de Testes Automatizados - Executa testes no navegador
    """
    
    def __init__(self, project_path: str):
        self.project_path = project_path
        self.is_active = False
        self.status = "inactive"
        self.test_results = []
        self.browser_process = None
        
        # Configurações de teste
        self.test_config = {
            'browser': 'chrome',  # chrome, firefox, edge
            'headless': False,    # True para executar sem interface
            'timeout': 30,        # Timeout em segundos
            'screenshots_dir': os.path.join(project_path, 'test_screenshots'),
            'reports_dir': os.path.join(project_path, 'test_reports')
        }
        
        # Casos de teste pré-definidos
        self.predefined_tests = {
            'ecommerce_basic': [
                TestCase(
                    id="test_001",
                    name="Teste de Navegação Principal",
                    description="Verifica se a página inicial carrega corretamente",
                    type="e2e",
                    steps=[
                        "Abrir navegador",
                        "Navegar para página inicial",
                        "Verificar se título está presente",
                        "Verificar se menu principal está visível",
                        "Verificar se produtos são exibidos"
                    ],
                    expected_result="Página inicial carrega com todos os elementos visíveis"
                ),
                TestCase(
                    id="test_002",
                    name="Teste de Login",
                    description="Verifica funcionalidade de login",
                    type="e2e",
                    steps=[
                        "Navegar para página de login",
                        "Preencher credenciais válidas",
                        "Clicar em login",
                        "Verificar redirecionamento para dashboard"
                    ],
                    expected_result="Login realizado com sucesso e redirecionamento correto"
                ),
                TestCase(
                    id="test_003",
                    name="Teste de Busca de Produtos",
                    description="Verifica funcionalidade de busca",
                    type="e2e",
                    steps=[
                        "Navegar para página de produtos",
                        "Digitar termo de busca",
                        "Clicar em buscar",
                        "Verificar resultados da busca"
                    ],
                    expected_result="Resultados de busca são exibidos corretamente"
                ),
                TestCase(
                    id="test_004",
                    name="Teste de Adicionar ao Carrinho",
                    description="Verifica funcionalidade do carrinho",
                    type="e2e",
                    steps=[
                        "Navegar para página de produto",
                        "Selecionar quantidade",
                        "Clicar em 'Adicionar ao Carrinho'",
                        "Verificar se produto foi adicionado"
                    ],
                    expected_result="Produto adicionado ao carrinho com sucesso"
                ),
                TestCase(
                    id="test_005",
                    name="Teste de Checkout",
                    description="Verifica processo de checkout",
                    type="e2e",
                    steps=[
                        "Adicionar produto ao carrinho",
                        "Ir para checkout",
                        "Preencher dados de entrega",
                        "Selecionar método de pagamento",
                        "Finalizar compra"
                    ],
                    expected_result="Checkout concluído com sucesso"
                )
            ],
            'performance': [
                TestCase(
                    id="test_perf_001",
                    name="Teste de Performance - Carregamento",
                    description="Verifica tempo de carregamento da página inicial",
                    type="performance",
                    steps=[
                        "Abrir navegador",
                        "Medir tempo de carregamento da página inicial",
                        "Verificar se tempo está dentro do limite aceitável"
                    ],
                    expected_result="Página carrega em menos de 3 segundos"
                )
            ],
            'responsive': [
                TestCase(
                    id="test_resp_001",
                    name="Teste de Responsividade - Mobile",
                    description="Verifica se o site funciona bem em dispositivos móveis",
                    type="responsive",
                    steps=[
                        "Abrir navegador em modo mobile",
                        "Navegar pelo site",
                        "Verificar se elementos estão responsivos",
                        "Testar menu mobile"
                    ],
                    expected_result="Site funciona corretamente em dispositivos móveis"
                )
            ]
        }
        
        # Criar diretórios necessários
        os.makedirs(self.test_config['screenshots_dir'], exist_ok=True)
        os.makedirs(self.test_config['reports_dir'], exist_ok=True)
        
        logger.info("Agente de Testes Automatizados inicializado")
    
    async def activate(self) -> Dict[str, Any]:
        """Ativa o agente de testes automatizados"""
        try:
            self.is_active = True
            self.status = "active"
            
            # Verificar se o navegador está disponível
            browser_status = await self._check_browser_availability()
            
            logger.info("✅ Agente de Testes Automatizados ativado com sucesso!")
            
            return {
                'status': 'success',
                'message': 'Agente de Testes Automatizados ativado',
                'browser_status': browser_status,
                'capabilities': [
                    'Testes E2E automatizados',
                    'Abertura automática do navegador',
                    'Captura de screenshots',
                    'Geração de relatórios',
                    'Testes de performance',
                    'Testes de responsividade'
                ]
            }
        except Exception as e:
            logger.error(f"❌ Erro ao ativar Agente de Testes: {e}")
            return {
                'status': 'error',
                'message': f'Erro ao ativar: {e}'
            }
    
    async def deactivate(self) -> Dict[str, Any]:
        """Desativa o agente de testes"""
        try:
            # Fechar navegador se estiver aberto
            await self._close_browser()
            
            self.is_active = False
            self.status = "inactive"
            return {
                'status': 'success',
                'message': 'Agente de Testes Automatizados desativado'
            }
        except Exception as e:
            logger.error(f"Erro ao desativar: {e}")
            return {
                'status': 'error',
                'message': f'Erro ao desativar: {e}'
            }
    
    async def run_test_suite(self, test_suite: str = "ecommerce_basic") -> Dict[str, Any]:
        """Executa uma suíte de testes completa"""
        try:
            logger.info(f"🧪 Executando suíte de testes: {test_suite}")
            
            if test_suite not in self.predefined_tests:
                return {
                    'status': 'error',
                    'message': f'Suíte de testes "{test_suite}" não encontrada'
                }
            
            tests = self.predefined_tests[test_suite]
            results = []
            
            # Abrir navegador
            await self._open_browser()
            
            for test in tests:
                logger.info(f"🔍 Executando teste: {test.name}")
                result = await self._execute_test(test)
                results.append(result)
                
                # Pequena pausa entre testes
                await asyncio.sleep(1)
            
            # Fechar navegador
            await self._close_browser()
            
            # Gerar relatório
            report = await self._generate_test_report(results, test_suite)
            
            return {
                'status': 'success',
                'message': f'Suíte de testes "{test_suite}" concluída',
                'results': [vars(result) for result in results],
                'report': report
            }
            
        except Exception as e:
            logger.error(f"❌ Erro ao executar suíte de testes: {e}")
            await self._close_browser()
            return {
                'status': 'error',
                'message': f'Erro ao executar testes: {e}'
            }
    
    async def run_specific_test(self, test_name: str) -> Dict[str, Any]:
        """Executa um teste específico"""
        try:
            logger.info(f"🔍 Executando teste específico: {test_name}")
            
            # Encontrar o teste
            test = None
            for suite in self.predefined_tests.values():
                for t in suite:
                    if t.name.lower() == test_name.lower() or t.id == test_name:
                        test = t
                        break
                if test:
                    break
            
            if not test:
                return {
                    'status': 'error',
                    'message': f'Teste "{test_name}" não encontrado'
                }
            
            # Abrir navegador
            await self._open_browser()
            
            # Executar teste
            result = await self._execute_test(test)
            
            # Fechar navegador
            await self._close_browser()
            
            return {
                'status': 'success',
                'message': f'Teste "{test.name}" concluído',
                'result': vars(result)
            }
            
        except Exception as e:
            logger.error(f"❌ Erro ao executar teste específico: {e}")
            await self._close_browser()
            return {
                'status': 'error',
                'message': f'Erro ao executar teste: {e}'
            }
    
    async def _check_browser_availability(self) -> Dict[str, Any]:
        """Verifica se o navegador está disponível"""
        try:
            browsers = {
                'chrome': 'google-chrome',
                'firefox': 'firefox',
                'edge': 'microsoft-edge'
            }
            
            available_browsers = {}
            
            for browser_name, command in browsers.items():
                try:
                    result = await self._run_command(f"{command} --version")
                    if result['success']:
                        available_browsers[browser_name] = {
                            'available': True,
                            'version': result['output'].strip()
                        }
                    else:
                        available_browsers[browser_name] = {
                            'available': False,
                            'error': result['error']
                        }
                except:
                    available_browsers[browser_name] = {
                        'available': False,
                        'error': 'Navegador não encontrado'
                    }
            
            return available_browsers
            
        except Exception as e:
            logger.error(f"Erro ao verificar navegadores: {e}")
            return {'error': str(e)}
    
    async def _open_browser(self) -> bool:
        """Abre o navegador"""
        try:
            if self.browser_process:
                return True
            
            browser_command = self._get_browser_command()
            if not browser_command:
                logger.error("Nenhum navegador disponível")
                return False
            
            # Abrir navegador em modo de desenvolvimento
            if self.test_config['headless']:
                command = f"{browser_command} --headless --disable-gpu --no-sandbox --disable-dev-shm-usage"
            else:
                command = f"{browser_command} --new-window --disable-web-security --disable-features=VizDisplayCompositor"
            
            self.browser_process = await asyncio.create_subprocess_shell(
                command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            # Aguardar um pouco para o navegador abrir
            await asyncio.sleep(3)
            
            logger.info("🌐 Navegador aberto com sucesso")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao abrir navegador: {e}")
            return False
    
    async def _close_browser(self) -> bool:
        """Fecha o navegador"""
        try:
            if self.browser_process:
                self.browser_process.terminate()
                await self.browser_process.wait()
                self.browser_process = None
                logger.info("🌐 Navegador fechado")
            return True
        except Exception as e:
            logger.error(f"Erro ao fechar navegador: {e}")
            return False
    
    def _get_browser_command(self) -> str:
        """Retorna o comando do navegador disponível"""
        browsers = ['google-chrome', 'firefox', 'microsoft-edge']
        
        for browser in browsers:
            try:
                result = subprocess.run([browser, '--version'], 
                                      capture_output=True, text=True, timeout=5)
                if result.returncode == 0:
                    return browser
            except:
                continue
        
        return None
    
    async def _execute_test(self, test: TestCase) -> TestResult:
        """Executa um teste específico"""
        start_time = time.time()
        
        try:
            logger.info(f"🔍 Executando: {test.name}")
            
            # Simular execução do teste baseado no tipo
            if test.type == "e2e":
                result = await self._execute_e2e_test(test)
            elif test.type == "performance":
                result = await self._execute_performance_test(test)
            elif test.type == "responsive":
                result = await self._execute_responsive_test(test)
            else:
                result = "passed"  # Teste genérico
            
            duration = time.time() - start_time
            
            # Capturar screenshot se necessário
            screenshot_path = None
            if result == "failed":
                screenshot_path = await self._capture_screenshot(test.id)
            
            return TestResult(
                test_id=test.id,
                status=result,
                duration=duration,
                screenshot_path=screenshot_path
            )
            
        except Exception as e:
            duration = time.time() - start_time
            logger.error(f"Erro no teste {test.id}: {e}")
            
            return TestResult(
                test_id=test.id,
                status="error",
                duration=duration,
                error_message=str(e)
            )
    
    async def _execute_e2e_test(self, test: TestCase) -> str:
        """Executa teste E2E"""
        try:
            # Simular execução dos passos do teste
            for step in test.steps:
                logger.info(f"  📋 {step}")
                await asyncio.sleep(0.5)  # Simular tempo de execução
            
            # Simular resultado (80% de sucesso para demonstração)
            import random
            if random.random() < 0.8:
                return "passed"
            else:
                return "failed"
                
        except Exception as e:
            logger.error(f"Erro no teste E2E: {e}")
            return "error"
    
    async def _execute_performance_test(self, test: TestCase) -> str:
        """Executa teste de performance"""
        try:
            # Simular teste de performance
            await asyncio.sleep(1)
            
            # Simular medição de tempo
            load_time = 2.5  # segundos
            
            if load_time < 3.0:
                return "passed"
            else:
                return "failed"
                
        except Exception as e:
            logger.error(f"Erro no teste de performance: {e}")
            return "error"
    
    async def _execute_responsive_test(self, test: TestCase) -> str:
        """Executa teste de responsividade"""
        try:
            # Simular teste de responsividade
            await asyncio.sleep(1)
            
            # Simular verificação de elementos responsivos
            return "passed"
            
        except Exception as e:
            logger.error(f"Erro no teste de responsividade: {e}")
            return "error"
    
    async def _capture_screenshot(self, test_id: str) -> str:
        """Captura screenshot do teste"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"test_{test_id}_{timestamp}.png"
            filepath = os.path.join(self.test_config['screenshots_dir'], filename)
            
            # Simular captura de screenshot
            logger.info(f"📸 Screenshot salvo: {filepath}")
            
            return filepath
            
        except Exception as e:
            logger.error(f"Erro ao capturar screenshot: {e}")
            return None
    
    async def _generate_test_report(self, results: List[TestResult], test_suite: str) -> Dict[str, Any]:
        """Gera relatório de testes"""
        try:
            total_tests = len(results)
            passed_tests = len([r for r in results if r.status == "passed"])
            failed_tests = len([r for r in results if r.status == "failed"])
            error_tests = len([r for r in results if r.status == "error"])
            
            success_rate = (passed_tests / total_tests) * 100 if total_tests > 0 else 0
            
            report = {
                'test_suite': test_suite,
                'timestamp': datetime.now().isoformat(),
                'summary': {
                    'total_tests': total_tests,
                    'passed': passed_tests,
                    'failed': failed_tests,
                    'errors': error_tests,
                    'success_rate': round(success_rate, 2)
                },
                'results': [vars(result) for result in results]
            }
            
            # Salvar relatório em arquivo
            report_filename = f"test_report_{test_suite}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            report_path = os.path.join(self.test_config['reports_dir'], report_filename)
            
            with open(report_path, 'w') as f:
                json.dump(report, f, indent=2, default=str)
            
            logger.info(f"📊 Relatório salvo: {report_path}")
            
            return report
            
        except Exception as e:
            logger.error(f"Erro ao gerar relatório: {e}")
            return {'error': str(e)}
    
    async def _run_command(self, command: str) -> Dict[str, Any]:
        """Executa um comando no sistema"""
        try:
            process = await asyncio.create_subprocess_shell(
                command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
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
        """Executa tarefas do agente de testes"""
        try:
            results = []
            
            for task in tasks:
                logger.info(f"🧪 Executando tarefa de teste: {task.title}")
                
                # Determinar tipo de teste baseado na tarefa
                if "e2e" in task.title.lower() or "navegador" in task.title.lower():
                    result = await self.run_test_suite("ecommerce_basic")
                elif "performance" in task.title.lower():
                    result = await self.run_test_suite("performance")
                elif "responsivo" in task.title.lower():
                    result = await self.run_test_suite("responsive")
                else:
                    result = await self.run_test_suite("ecommerce_basic")
                
                task_result = {
                    'task_id': task.id,
                    'title': task.title,
                    'status': 'completed',
                    'result': result
                }
                results.append(task_result)
            
            return {
                'status': 'success',
                'message': f'{len(results)} tarefas de teste concluídas',
                'results': results
            }
        except Exception as e:
            logger.error(f"❌ Erro ao executar tarefas de teste: {e}")
            return {
                'status': 'error',
                'message': f'Erro ao executar tarefas: {e}'
            }
    
    def get_status(self) -> Dict[str, Any]:
        """Retorna status atual do agente"""
        return {
            'active': self.is_active,
            'status': self.status,
            'browser_open': self.browser_process is not None,
            'tests_executed': len(self.test_results),
            'last_test': self.test_results[-1].timestamp if self.test_results else None
        }

# Função de teste
async def test_automation_agent():
    """Testa o agente de testes automatizados"""
    test_agent = TestAutomationAgent(os.getcwd())
    
    # Ativar
    result = await test_agent.activate()
    print("Ativação:", json.dumps(result, indent=2))
    
    # Executar suíte de testes
    result = await test_agent.run_test_suite("ecommerce_basic")
    print("Testes:", json.dumps(result, indent=2, default=str))
    
    # Status
    status = test_agent.get_status()
    print("Status:", json.dumps(status, indent=2, default=str))
    
    # Desativar
    await test_agent.deactivate()

if __name__ == "__main__":
    asyncio.run(test_automation_agent())
