# ROOT_ADMIN_REPORT

## Rotas / e /admin

**Rota raiz (/):**
- Controller: `RootController@index`
- Middleware: `installed`
- Nome: `home`

**Rota admin (/admin):**
- Mesmo controller: `RootController@index` (SPA)
- Mesmo middleware: `installed`
- Mesmo layout: `master.blade.php`

## APP_URL
```
5:APP_URL=http://127.0.0.1:8000
```

## Mix manifest
```json
{
    "/js/app.js": "/js/app.js?id=8ca14dcb0aebe5ec15c189e0dbf91046",
    "/js/manifest.js": "/js/manifest.js?id=0ecd257e36664d66810f5526fe58d7fc",
    "/css/app.css": "/css/app.css?id=9557d6022d40a7ed11c85166291df504",
    "/js/vendor.js": "/js/vendor.js?id=16e74c67172d23379134755519237144"
}
```

## Assets
```
-rw-rw-r-- 1 guilherme guilherme 7,8M ago 20 01:15 public/js/app.js
-rw-rw-r-- 1 guilherme guilherme 180K ago 20 01:15 public/css/app.css
```

## Testes de Rotas

**✅ /health:**
- Status: 200 OK
- Content-Type: text/plain
- Resposta: "OK:blade"

**✅ / (raiz):**
- Status: 200 OK
- Content-Type: text/html
- Layout: master.blade.php

**✅ /admin:**
- Status: 200 OK
- Content-Type: text/html
- Layout: master.blade.php (mesmo da raiz)

## Layouts Identificados

**Layout principal:**
- Arquivo: `resources/views/master.blade.php`
- Assets: `mix('css/app.css')` e `mix('js/app.js')`
- Div raiz: `<div id="app"></div>`

**Outros layouts:**
- `resources/views/installer/layouts/master.blade.php` (instalador)
- `resources/views/installer/site.blade.php` (instalador)

## JavaScript Resiliente

**Mount targets (ordem de prioridade):**
1. `#admin-app` (se existir)
2. `#site-app` (se existir)
3. `#app` (fallback padrão)

**Console log:** `[BuyPeer] mount on #app`

## Observações

- **Se /health mostra OK e / fica branco:** É problema de JS/asset
- **Se / renderiza e /admin não:** É problema específico do admin
- **Se ambas ficam brancas:** É problema global de assets

**Diagnóstico atual:**
- ✅ Laravel funcionando (rota /health responde)
- ✅ Assets compilados e servindo
- ✅ Layout único para ambas as rotas
- ✅ JavaScript resiliente implementado
- ✅ Cache limpo

**Próximos passos:**
1. Testar no navegador com DevTools aberto
2. Verificar console para mensagens de erro
3. Verificar se Vue.js está montando corretamente
4. Verificar se há erros de JavaScript
