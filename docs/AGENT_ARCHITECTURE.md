# 🎼 Arquitetura Orquestrada de Agentes BuyPeer

## Visão Geral

O sistema de agentes BuyPeer foi completamente refatorado para implementar uma **arquitetura orquestrada** que integra **MCPs (Model Context Protocol)** e **OpenAI** para processamento de linguagem natural.

## 🏗️ Arquitetura Principal

```
[ VOCÊ ]
   │
   ▼
[ CURSOR ]
   - Recebe sua solicitação em linguagem natural
   - Registra a task
   - Encaminha SEMPRE para o Architect
   │
   ▼
[ ARCHITECT (Orquestrador Principal) ]
   - Analisa a task usando a OpenAI API
   - Decide qual agente especializado deve assumir
   - Pode dividir em subtarefas e repassar
   │
   ├──> [ BACKEND ] → usa MCPs p/ código backend, API, DB
   ├──> [ FRONTEND ] → usa MCPs p/ UI, Vue.js, assets
   ├──> [ PAYMENTS ] → integra gateways (Stripe, Mercado Pago, etc.)
   ├──> [ DATA ] → queries, relatórios, integrações com Postgres/Redis
   ├──> [ DEVOPS ] → CI/CD, Docker, Nginx, Deploy
   ├──> [ QA ] → testes (unitários, e2e via Puppeteer)
   ├──> [ SECURITY ] → compliance, PCI, LGPD, segurança de API
   ├──> [ AUTOMATION_AGENT ] → fluxos automáticos de build/test
   ├──> [ CONTEXT_AGENT ] → memória contextual (usa context7 MCP)
   └──> [ TEAM_MANAGER ] → coordenação entre agentes

   │
   ▼
[ MCP SERVERS ]
   - Filesystem (ler/escrever arquivos)
   - Git (commits, branch, merge)
   - Figma (designs e mockups)
   - Puppeteer (testes automatizados UI)
   - Ref-tools (refatoração de código)
   - Json-resume (documentação estruturada)
   - Context7 (memória persistente)
   - Postgres / Redis (dados e cache)
   │
   ▼
[ INFRA / EXTERNO ]
   - GitHub repo
   - APIs de pagamentos
   - Serviços de entrega/logística
   - Cloud (VPS/Docker)
```

## 🔧 Componentes Principais

### 1. **AgentOrchestrator** (`agents/orchestrator.py`)
- **Função**: Orquestrador principal do sistema
- **Responsabilidades**:
  - Inicializar todos os componentes
  - Gerenciar ciclo de vida dos agentes
  - Coordenar comunicação entre agentes
  - Processar solicitações de alto nível

### 2. **ArchitectAgent** (`agents/architect.py`)
- **Função**: Orquestrador de análise e delegação
- **Responsabilidades**:
  - Analisar solicitações usando OpenAI
  - Identificar agentes necessários
  - Criar planos de execução
  - Delegar tarefas para agentes especializados

### 3. **CommunicationHub** (`agents/communication.py`)
- **Função**: Sistema de comunicação central
- **Responsabilidades**:
  - Gerenciar mensagens entre agentes
  - Criar e delegar tarefas
  - Integrar com OpenAI para análise
  - Manter histórico de comunicação

### 4. **MCPManager** (`agents/mcp_config.py`)
- **Função**: Gerenciador de MCPs
- **Responsabilidades**:
  - Carregar configuração de MCPs
  - Validar disponibilidade
  - Fornecer interface unificada
  - Gerenciar operações específicas

### 5. **BaseAgent** (`agents/base_agent.py`)
- **Função**: Classe base para todos os agentes
- **Responsabilidades**:
  - Fornecer funcionalidades comuns
  - Integração com MCPs
  - Comunicação entre agentes
  - Logging e histórico de tarefas

## 🚀 Fluxo de Execução

### 1. **Recepção da Solicitação**
```python
# Você faz uma solicitação em linguagem natural
request = "Preciso implementar um sistema de cupons de desconto"
```

### 2. **Análise pelo Architect**
```python
# Architect usa OpenAI para analisar
analysis = await architect.analyze_request(request)
# Resultado: Identifica necessidade de backend, frontend, payments, qa
```

### 3. **Delegação de Tarefas**
```python
# Architect cria tarefas específicas
tasks = [
    {"agent": "backend", "task": "Criar modelo Coupon"},
    {"agent": "payments", "task": "Integrar validação de cupons"},
    {"agent": "frontend", "task": "Criar interface de cupons"},
    {"agent": "qa", "task": "Testar funcionalidade"}
]
```

### 4. **Execução pelos Agentes**
```python
# Cada agente executa usando MCPs
backend_agent.use_mcp('filesystem', 'write_file', path='app/Models/Coupon.php')
backend_agent.use_mcp('git', 'commit', message='feat: Criar modelo Coupon')
```

### 5. **Consolidação de Resultados**
```python
# Architect coleta e consolida resultados
final_result = {
    'status': 'success',
    'components_created': ['Model', 'Controller', 'Migration'],
    'tests_passed': True,
    'deployment_ready': True
}
```

## 🔧 MCPs Integrados

### **MCPs Disponíveis**
1. **context7** - Memória e contexto persistente
2. **cursor** - Controle do IDE Cursor
3. **git** - Controle de versão Git/GitHub
4. **filesystem** - Acesso ao sistema de arquivos
5. **figma** - Integração com Figma
6. **puppeteer** - Automação de browser
7. **ref-tools** - Ferramentas de referência
8. **json-resume** - Gerenciamento de currículos

### **Operações por MCP**
```python
# Filesystem
await agent.read_file('app/Models/User.php')
await agent.write_file('app/Models/Coupon.php', content)
await agent.list_directory('resources/views')

# Git
await agent.git_commit('feat: Implementar sistema de cupons')
await agent.git_push('main')
await agent.git_pull('develop')

# Puppeteer
await agent.take_screenshot('http://localhost:8000', 'homepage')
await agent.test_ui('http://localhost:8000', test_script)

# Context7
await agent.save_context('cupon_system', {'status': 'implemented'})
await agent.load_context('cupon_system')
```

## 📋 Regras de Arquitetura

### 1. **Comunicação Centralizada**
- Você só se comunica diretamente com o Cursor
- Cursor registra sua solicitação como uma **task**
- Cursor SEMPRE encaminha para o **Architect**
- Architect decide qual agente executar

### 2. **Architect como Orquestrador**
- Architect analisa task em linguagem natural (OpenAI)
- Decide qual agente especializado deve assumir
- Pode dividir task em subtarefas
- Repassa para múltiplos agentes se necessário

### 3. **Agentes Especializados**
- Cada agente expõe funções claras para o Architect chamar
- Agentes podem consultar outros agentes se necessário
- Exemplo: `payments` pode acionar `security` para validar PCI

### 4. **Integração com MCPs**
- Todos os agentes usam MCPs para operações práticas
- `filesystem` → ler/escrever arquivos
- `git` → versionar e sincronizar código
- `puppeteer` → rodar testes de UI automatizados
- `context7` → manter contexto de longo prazo

### 5. **Uso da OpenAI**
- Toda interpretação em linguagem natural passa pela OpenAI
- Agentes são funções/módulos especializados
- OpenAI entende a task e traduz para chamada de agente + MCP

## 🎯 Benefícios da Nova Arquitetura

### **Redução de Tokens**
- Interpretação pesada apenas no Architect
- Cursor é apenas hub de entrada e saída
- Agentes + MCPs executam de forma modular

### **Modularidade**
- Cada agente tem responsabilidades específicas
- Fácil adição de novos agentes
- MCPs fornecem funcionalidades reutilizáveis

### **Escalabilidade**
- Sistema pode crescer horizontalmente
- Novos MCPs podem ser adicionados facilmente
- Agentes podem ser distribuídos em diferentes máquinas

### **Manutenibilidade**
- Código bem estruturado e documentado
- Separação clara de responsabilidades
- Testes automatizados para cada componente

## 🚀 Como Usar

### **Inicialização Rápida**
```python
from agents import initialize_system, process_request

# Inicializar sistema
await initialize_system()

# Processar solicitação
result = await process_request("Implementar sistema de cupons")
```

### **Uso Avançado**
```python
from agents.orchestrator import orchestrator

# Inicializar orquestrador
await orchestrator.initialize()

# Processar solicitação
result = await orchestrator.process_request("Criar API de produtos")

# Obter status
status = await orchestrator.get_system_status()

# Desligar
await orchestrator.shutdown()
```

### **Teste do Sistema**
```bash
python test_orchestrated_system.py
```

## 📁 Estrutura de Arquivos

```
agents/
├── __init__.py              # Módulo principal
├── orchestrator.py          # Orquestrador principal
├── architect.py             # Agente arquiteto
├── communication.py         # Hub de comunicação
├── mcp_config.py           # Gerenciador de MCPs
├── base_agent.py           # Classe base para agentes
├── backend.py              # Agente backend (legacy)
├── frontend.py             # Agente frontend (legacy)
├── devops.py               # Agente devops (legacy)
├── qa.py                   # Agente QA (legacy)
├── payments.py             # Agente payments (legacy)
├── security.py             # Agente security (legacy)
├── data.py                 # Agente data (legacy)
├── context_agent.py        # Agente contexto (legacy)
├── automation_agent.py     # Agente automação (legacy)
├── test_automation_agent.py # Agente testes (legacy)
└── team_manager.py         # Gerenciador de equipe (legacy)

docs/
└── AGENT_ARCHITECTURE.md   # Esta documentação

test_orchestrated_system.py # Script de teste
```

## 🔮 Próximos Passos

1. **Refatorar agentes legacy** para herdar de BaseAgent
2. **Implementar agentes especializados** mais robustos
3. **Adicionar mais MCPs** conforme necessário
4. **Criar interface web** para monitoramento
5. **Implementar testes automatizados** completos
6. **Documentar APIs** de cada agente
7. **Criar templates** para novos agentes

---

**🎉 Sistema Orquestrado Pronto para Produção!**
