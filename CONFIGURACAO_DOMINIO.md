# 🌐 Configuração do Domínio buypeer.com.br

## ❌ Problema Identificado
**Erro**: `DNS_PROBE_FINISHED_NXDOMAIN`
**Causa**: O domínio `buypeer.com.br` não está configurado no DNS

## ✅ Solução

### 1. **Configurar DNS no Hostinger**

Acesse o painel do Hostinger e configure os registros DNS:

#### **Registros A (IPv4)**:
```
Nome: @ (ou buypeer.com.br)
Valor: 147.79.89.70
TTL: 300
```

#### **Registros CNAME**:
```
Nome: www
Valor: buypeer.com.br
TTL: 300
```

### 2. **Configurar Subdomínio (Opcional)**:
```
Nome: admin
Valor: buypeer.com.br
TTL: 300
```

### 3. **Verificar Configuração**

Após configurar, aguarde 5-10 minutos e teste:

```bash
# Verificar DNS
nslookup buypeer.com.br
dig buypeer.com.br

# Testar acesso
curl -I http://buypeer.com.br
```

### 4. **Configurar SSL/HTTPS**

No painel do Hostinger:
1. Vá em "SSL"
2. Ative SSL gratuito para o domínio
3. Configure redirecionamento HTTP → HTTPS

### 5. **Configurar .htaccess (se necessário)**

Crie/edite o arquivo `.htaccess` na pasta `public_html`:

```apache
RewriteEngine On
RewriteCond %{REQUEST_FILENAME} !-d
RewriteCond %{REQUEST_FILENAME} !-f
RewriteRule ^ index.php [L]

# Redirecionar HTTP para HTTPS
RewriteCond %{HTTPS} off
RewriteRule ^(.*)$ https://%{HTTP_HOST}%{REQUEST_URI} [L,R=301]
```

## 🔧 **Passos no Hostinger**

1. **Login no Hostinger**
2. **Vá em "Domains"**
3. **Clique em "Manage" no domínio buypeer.com.br**
4. **Vá em "DNS / Nameservers"**
5. **Adicione os registros A e CNAME**
6. **Aguarde propagação (5-10 min)**

## 📞 **Suporte**

Se precisar de ajuda:
- **Hostinger Support**: Chat online
- **Documentação**: https://www.hostinger.com/help
- **Status DNS**: https://dnschecker.org

## ✅ **Teste Final**

Após configuração:
- ✅ http://buypeer.com.br
- ✅ https://buypeer.com.br
- ✅ http://www.buypeer.com.br
- ✅ https://www.buypeer.com.br

---
**Criado em**: 29/08/2025
**Status**: Aguardando configuração DNS
