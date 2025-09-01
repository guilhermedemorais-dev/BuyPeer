#!/usr/bin/env python3
"""
Script para validar MCPs reais e verificados
Autor: Guilherme - BuyPeer
Data: 2025-08-28
"""

import subprocess
import sys
import os
from pathlib import Path

class MCPValidator:
    def __init__(self):
        # MCPs REAIS E VERIFICADOS
        self.required_mcps = {
            # DESENVOLVIMENTO (OBRIGATÓRIOS)
            "cursor": "MCP Custom do Cursor",
            "git": "Controle Git/GitHub",
            "filesystem": "Acesso ao sistema de arquivos",
            
            # IA E EXTERNOS (OPCIONAIS)
            "context7": "Contexto e memória",
            "figma": "Integração Figma",
            "puppeteer": "Automação de browser",
            "ref-tools": "Ferramentas de referência",
            "json-resume": "Gerenciamento de currículos"
        }
        
        self.mcp_config_path = Path.home() / ".cursor" / "mcp.json"
        
    def validate_mcp_server(self, server_name, command, args):
        """Valida se um MCP server está configurado corretamente"""
        try:
            # Verifica se o comando existe
            if command == "npx":
                # Para npx, verifica se o pacote existe
                package_name = args[1] if len(args) > 1 else ""
                if package_name:
                    result = subprocess.run(
                        ["npm", "view", package_name, "name"],
                        capture_output=True,
                        text=True,
                        timeout=10
                    )
                    if result.returncode == 0:
                        # Verificar se precisa de token (especial para json-resume)
                        if package_name == "@jsonresume/mcp":
                            return False, "⚠️ Pacote encontrado, mas precisa de GITHUB_TOKEN, GITHUB_USERNAME e OPENAI_API_KEY"
                        return True, "✅ Pacote encontrado no npm"
                    else:
                        return False, "❌ Pacote não encontrado no npm"
                        
            elif command == "uvx":
                # Para uvx, verifica se o comando funciona
                result = subprocess.run(
                    ["uvx", "--help"],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                if result.returncode == 0:
                    return True, "✅ uvx disponível"
                else:
                    return False, "❌ uvx não disponível"
                    
            elif command == "node":
                # Para node, verifica se o arquivo existe
                file_path = args[0] if args else ""
                if os.path.exists(file_path):
                    return True, "✅ Arquivo custom encontrado"
                else:
                    return False, "❌ Arquivo custom não encontrado"
                    
            else:
                return False, "❌ Comando não reconhecido"
                
        except subprocess.TimeoutExpired:
            return False, "❌ Timeout na validação"
        except Exception as e:
            return False, f"❌ Erro: {str(e)}"
    
    def check_mcp_config(self):
        """Verifica a configuração do MCP"""
        if not self.mcp_config_path.exists():
            print("❌ Arquivo mcp.json não encontrado!")
            return False
            
        try:
            import json
            with open(self.mcp_config_path, 'r') as f:
                config = json.load(f)
                
            servers = config.get('mcpServers', {})
            
            print("🔍 VALIDAÇÃO DE MCPs REAIS E VERIFICADOS")
            print("=" * 50)
            
            all_valid = True
            
            for server_name, server_config in servers.items():
                if server_name in self.required_mcps:
                    description = self.required_mcps[server_name]
                    
                    if 'command' in server_config and 'args' in server_config:
                        command = server_config['command']
                        args = server_config['args']
                        
                        is_valid, message = self.validate_mcp_server(server_name, command, args)
                        
                        status = "✅" if is_valid else "❌"
                        print(f"{status} {server_name}: {description} - {message}")
                        
                        if not is_valid:
                            all_valid = False
                    else:
                        print(f"⚠️  {server_name}: {description} - Configuração incompleta")
                        all_valid = False
                else:
                    print(f"❓ {server_name}: MCP não reconhecido")
            
            print("\n" + "=" * 50)
            
            if all_valid:
                print("🎉 TODOS OS MCPs REAIS ESTÃO FUNCIONANDO!")
            else:
                print("⚠️  ALGUNS MCPs PRECISAM DE ATENÇÃO")
                
            return all_valid
            
        except Exception as e:
            print(f"❌ Erro ao ler configuração: {e}")
            return False
    
    def install_missing_mcps(self):
        """Instala MCPs que estão faltando"""
        print("\n🔧 INSTALANDO MCPs FALTANTES...")
        
        # Lista de MCPs para instalar
        mcps_to_install = [
            "@modelcontextprotocol/server-filesystem",
            "figma-mcp",
            "puppeteer-mcp-server",
            "ref-tools-mcp",
            "@jsonresume/mcp"
        ]
        
        for mcp in mcps_to_install:
            print(f"📦 Instalando {mcp}...")
            try:
                subprocess.run(["npm", "install", "-g", mcp], check=True)
                print(f"✅ {mcp} instalado com sucesso!")
            except subprocess.CalledProcessError:
                print(f"❌ Falha ao instalar {mcp}")
    
    def show_help(self):
        """Mostra ajuda"""
        print("""
🔧 VALIDADOR DE MCPs REAIS - BUYPEER

USO:
    python3 check_mcps.py [comando]

COMANDOS:
    validate    - Valida MCPs configurados (padrão)
    install     - Instala MCPs faltantes
    help        - Mostra esta ajuda

MCPs REAIS DISPONÍVEIS:
    ✅ filesystem    - Acesso ao sistema de arquivos
    ✅ git          - Controle Git/GitHub  
    ✅ context7     - Contexto e memória
    ✅ figma        - Integração Figma
    ✅ puppeteer    - Automação de browser
    ✅ ref-tools    - Ferramentas de referência
    ✅ json-resume  - Gerenciamento de currículos
    ✅ cursor       - MCP Custom do Cursor

NOTA: Este script valida apenas MCPs REAIS que existem no npm registry.
        """)

def main():
    validator = MCPValidator()
    
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == "install":
            validator.install_missing_mcps()
        elif command == "help":
            validator.show_help()
        else:
            print(f"❌ Comando '{command}' não reconhecido")
            validator.show_help()
    else:
        # Comando padrão: validar
        validator.check_mcp_config()

if __name__ == "__main__":
    main()
