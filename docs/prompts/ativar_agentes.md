# 🚀 Script de Ativação - Sistema de Agentes BuyPeer

## 🎯 **Comandos de Ativação**

### **Ativar Time Completo**
```
/ativar-time-completo
```
**Resultado:** Ativa todos os agentes e inicia o Arquiteto como coordenador.

---

### **Ativar Agentes Individuais**

#### **Agente Arquiteto (Obrigatório)**
```
/ativar-agente arquiteto
```
**Responsabilidades:** Coordenação geral, planejamento, delegação de tarefas.

#### **Agente Backend (Laravel)**
```
/ativar-agente backend
```
**Responsabilidades:** APIs, modelos, lógica de negócio, banco de dados.

#### **Agente Frontend (Vue.js)**
```
/ativar-agente frontend
```
**Responsabilidades:** Interfaces, componentes, UX, responsividade.

#### **Agente DevOps**
```
/ativar-agente devops
```
**Responsabilidades:** Ambiente, deploy, monitoramento, infraestrutura.

#### **Agente QA**
```
/ativar-agente qa
```
**Responsabilidades:** Testes, validação, qualidade, bugs.

#### **Agente Pagamentos**
```
/ativar-agente pagamentos
```
**Responsabilidades:** Gateways, webhooks, transações, segurança PCI.

#### **Agente Dados**
```
/ativar-agente dados
```
**Responsabilidades:** Analytics, dashboards, relatórios, BI.

#### **Agente Segurança**
```
/ativar-agente seguranca
```
**Responsabilidades:** Autenticação, HTTPS, validação, rate limiting.

---

## 📋 **Comandos de Gestão**

### **Status dos Agentes**
```
/status-agentes
```
**Mostra:** Quais agentes estão ativos e seu status atual.

### **Desativar Agente**
```
/desativar-agente [nome]
```
**Exemplo:** `/desativar-agente qa`

### **Reiniciar Agente**
```
/reiniciar-agente [nome]
```
**Exemplo:** `/reiniciar-agente backend`

### **Configurar Agente**
```
/configurar-agente [nome] [configuração]
```
**Exemplo:** `/configurar-agente backend "usar-laravel-10"`

---

## 🎯 **Exemplos de Uso**

### **Cenário 1: Desenvolvimento Completo**
```
Usuário: /ativar-time-completo
Sistema: ✅ Time ativado! Arquiteto coordenando...

Usuário: "Preciso implementar sistema de avaliações de produtos"
Arquiteto: 
📋 Analisando requisitos...
🔧 Delegando tarefas:
  - Backend: Criar modelo Review e API
  - Frontend: Criar componente de avaliações
  - QA: Testar fluxo de avaliações
  - Segurança: Validar inputs
⏱️ Estimativa: 2-3 dias
```

### **Cenário 2: Correção de Bug**
```
Usuário: /ativar-agente arquiteto
Usuário: /ativar-agente backend
Usuário: /ativar-agente qa

Usuário: "O checkout está quebrando quando o usuário não tem endereço"
Arquiteto: 
🚨 Bug identificado!
🔧 Delegando:
  - Backend: Corrigir validação de endereço
  - QA: Testar cenários sem endereço
⏱️ Correção: 2-4 horas
```

### **Cenário 3: Otimização**
```
Usuário: /ativar-agente arquiteto
Usuário: /ativar-agente backend
Usuário: /ativar-agente devops

Usuário: "O site está lento, preciso otimizar"
Arquiteto: 
⚡ Análise de performance...
🔧 Delegando:
  - Backend: Otimizar queries
  - DevOps: Configurar cache Redis
  - QA: Testar performance
📊 Métricas: Tempo de resposta, throughput
```

---

## 🔧 **Configurações Avançadas**

### **Configurar Ambiente**
```
/configurar-ambiente desenvolvimento
/configurar-ambiente producao
/configurar-ambiente staging
```

### **Configurar Banco de Dados**
```
/configurar-db mysql
/configurar-db postgresql
/configurar-db sqlite
```

### **Configurar Cache**
```
/configurar-cache redis
/configurar-cache memcached
/configurar-cache file
```

### **Configurar Pagamentos**
```
/configurar-pagamento stripe
/configurar-pagamento paypal
/configurar-pagamento mercadopago
```

---

## 📊 **Monitoramento**

### **Dashboard de Status**
```
/dashboard
```
**Mostra:**
- Agentes ativos
- Tasks em andamento
- Performance do sistema
- Bugs e issues
- Próximos passos

### **Relatório de Progresso**
```
/relatorio-progresso
```
**Gera relatório com:**
- Tasks completadas
- Tempo gasto
- Bugs corrigidos
- Performance atual
- Recomendações

---

## 🚨 **Comandos de Emergência**

### **Parar Todos os Agentes**
```
/parar-todos-agentes
```

### **Modo de Emergência**
```
/modo-emergencia
```
**Ativa apenas:** Arquiteto + Backend + DevOps

### **Rollback de Mudanças**
```
/rollback [commit-hash]
```

### **Backup de Emergência**
```
/backup-emergencia
```

---

## 🎯 **Como Começar**

1. **Ative o Arquiteto primeiro:**
   ```
   /ativar-agente arquiteto
   ```

2. **Descreva sua necessidade:**
   ```
   "Preciso implementar [funcionalidade]"
   ```

3. **O Arquiteto coordenará o time:**
   - Analisará requisitos
   - Delegará tarefas
   - Monitorará progresso
   - Reportará status

4. **Aprove as mudanças:**
   - Revise o código
   - Teste as funcionalidades
   - Valide a qualidade

---

**🎉 Pronto! Seu time virtual está configurado e pronto para desenvolver o BuyPeer!**
