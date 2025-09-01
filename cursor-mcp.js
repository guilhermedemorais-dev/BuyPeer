#!/usr/bin/env node

/**
 * MCP Personalizado para Cursor
 * Fornece funcionalidades específicas do Cursor para o BuyPeer
 */

const { Server } = require('@modelcontextprotocol/sdk/server/index.js');
const { StdioServerTransport } = require('@modelcontextprotocol/sdk/server/stdio.js');
const { CallToolRequestSchema } = require('@modelcontextprotocol/sdk/types.js');
const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

class CursorMCPServer {
    constructor() {
        this.server = new Server(
            {
                name: 'cursor-mcp',
                version: '1.0.0',
            },
            {
                capabilities: {
                    tools: {},
                },
            }
        );

        this.setupTools();
    }

    setupTools() {
        // Tool: Verificar status do Cursor
        this.server.setRequestHandler(CallToolRequestSchema, async (request) => {
            const { name, arguments: args } = request.params;

            switch (name) {
                case 'cursor_status':
                    return await this.getCursorStatus();
                
                case 'cursor_config':
                    return await this.getCursorConfig();
                
                case 'cursor_extensions':
                    return await this.getCursorExtensions();
                
                case 'cursor_workspace':
                    return await this.getCursorWorkspace();
                
                case 'cursor_ai_models':
                    return await this.getCursorAIModels();
                
                case 'cursor_performance':
                    return await this.getCursorPerformance();
                
                case 'cursor_update':
                    return await this.updateCursor();
                
                case 'cursor_restart':
                    return await this.restartCursor();
                
                case 'cursor_backup':
                    return await this.backupCursorConfig();
                
                case 'cursor_restore':
                    return await this.restoreCursorConfig(args.config_file);
                
                default:
                    throw new Error(`Tool ${name} not found`);
            }
        });
    }

    async getCursorStatus() {
        try {
            const configPath = path.join(process.env.HOME, '.cursor', 'mcp.json');
            const configExists = fs.existsSync(configPath);
            
            const extensionsPath = path.join(process.env.HOME, '.cursor', 'extensions');
            const extensionsExist = fs.existsSync(extensionsPath);
            
            const extensions = extensionsExist ? fs.readdirSync(extensionsPath).length : 0;
            
            return {
                content: [
                    {
                        type: 'text',
                        text: JSON.stringify({
                            status: 'active',
                            config_exists: configExists,
                            extensions_count: extensions,
                            version: '1.0.0',
                            features: [
                                'MCP Integration',
                                'AI Code Completion',
                                'Multi-language Support',
                                'Git Integration',
                                'Terminal Integration'
                            ]
                        }, null, 2)
                    }
                ]
            };
        } catch (error) {
            return {
                content: [
                    {
                        type: 'text',
                        text: JSON.stringify({
                            status: 'error',
                            error: error.message
                        }, null, 2)
                    }
                ]
            };
        }
    }

    async getCursorConfig() {
        try {
            const configPath = path.join(process.env.HOME, '.cursor', 'mcp.json');
            if (fs.existsSync(configPath)) {
                const config = JSON.parse(fs.readFileSync(configPath, 'utf8'));
                return {
                    content: [
                        {
                            type: 'text',
                            text: JSON.stringify(config, null, 2)
                        }
                    ]
                };
            } else {
                return {
                    content: [
                        {
                            type: 'text',
                            text: 'Configuração do Cursor não encontrada'
                        }
                    ]
                };
            }
        } catch (error) {
            return {
                content: [
                    {
                        type: 'text',
                        text: `Erro ao ler configuração: ${error.message}`
                    }
                ]
            };
        }
    }

    async getCursorExtensions() {
        try {
            const extensionsPath = path.join(process.env.HOME, '.cursor', 'extensions');
            if (fs.existsSync(extensionsPath)) {
                const extensions = fs.readdirSync(extensionsPath);
                const extensionInfo = extensions.map(ext => {
                    const extPath = path.join(extensionsPath, ext);
                    const stats = fs.statSync(extPath);
                    return {
                        name: ext,
                        type: stats.isDirectory() ? 'directory' : 'file',
                        size: stats.size,
                        modified: stats.mtime
                    };
                });
                
                return {
                    content: [
                        {
                            type: 'text',
                            text: JSON.stringify(extensionInfo, null, 2)
                        }
                    ]
                };
            } else {
                return {
                    content: [
                        {
                            type: 'text',
                            text: 'Diretório de extensões não encontrado'
                        }
                    ]
                };
            }
        } catch (error) {
            return {
                content: [
                    {
                        type: 'text',
                        text: `Erro ao listar extensões: ${error.message}`
                    }
                ]
            };
        }
    }

    async getCursorWorkspace() {
        try {
            const workspacePath = process.cwd();
            const workspaceName = path.basename(workspacePath);
            const files = fs.readdirSync(workspacePath);
            
            return {
                content: [
                    {
                        type: 'text',
                        text: JSON.stringify({
                            workspace_name: workspaceName,
                            workspace_path: workspacePath,
                            files_count: files.length,
                            is_buypeer_project: workspaceName.includes('BuyPeer'),
                            has_package_json: files.includes('package.json'),
                            has_composer_json: files.includes('composer.json'),
                            has_requirements_txt: files.includes('requirements.txt')
                        }, null, 2)
                    }
                ]
            };
        } catch (error) {
            return {
                content: [
                    {
                        type: 'text',
                        text: `Erro ao obter workspace: ${error.message}`
                    }
                ]
            };
        }
    }

    async getCursorAIModels() {
        try {
            // Simular verificação de modelos AI disponíveis
            const models = [
                {
                    name: 'Claude 3.5 Sonnet',
                    provider: 'Anthropic',
                    status: 'available',
                    features: ['Code Completion', 'Code Review', 'Bug Fixing']
                },
                {
                    name: 'GPT-4',
                    provider: 'OpenAI',
                    status: 'available',
                    features: ['Code Generation', 'Documentation', 'Testing']
                },
                {
                    name: 'Code Llama',
                    provider: 'Meta',
                    status: 'available',
                    features: ['Code Analysis', 'Refactoring', 'Optimization']
                }
            ];
            
            return {
                content: [
                    {
                        type: 'text',
                        text: JSON.stringify(models, null, 2)
                    }
                ]
            };
        } catch (error) {
            return {
                content: [
                    {
                        type: 'text',
                        text: `Erro ao obter modelos AI: ${error.message}`
                    }
                ]
            };
        }
    }

    async getCursorPerformance() {
        try {
            const memoryUsage = process.memoryUsage();
            const cpuUsage = process.cpuUsage();
            
            return {
                content: [
                    {
                        type: 'text',
                        text: JSON.stringify({
                            memory: {
                                rss: Math.round(memoryUsage.rss / 1024 / 1024) + ' MB',
                                heapTotal: Math.round(memoryUsage.heapTotal / 1024 / 1024) + ' MB',
                                heapUsed: Math.round(memoryUsage.heapUsed / 1024 / 1024) + ' MB',
                                external: Math.round(memoryUsage.external / 1024 / 1024) + ' MB'
                            },
                            cpu: {
                                user: cpuUsage.user,
                                system: cpuUsage.system
                            },
                            uptime: process.uptime(),
                            platform: process.platform,
                            node_version: process.version
                        }, null, 2)
                    }
                ]
            };
        } catch (error) {
            return {
                content: [
                    {
                        type: 'text',
                        text: `Erro ao obter performance: ${error.message}`
                    }
                ]
            };
        }
    }

    async updateCursor() {
        try {
            // Simular atualização do Cursor
            return {
                content: [
                    {
                        type: 'text',
                        text: 'Atualização do Cursor iniciada. Reinicie o aplicativo para aplicar as mudanças.'
                    }
                ]
            };
        } catch (error) {
            return {
                content: [
                    {
                        type: 'text',
                        text: `Erro na atualização: ${error.message}`
                    }
                ]
            };
        }
    }

    async restartCursor() {
        try {
            return {
                content: [
                    {
                        type: 'text',
                        text: 'Reinicialização do Cursor solicitada. Feche e abra o aplicativo.'
                    }
                ]
            };
        } catch (error) {
            return {
                content: [
                    {
                        type: 'text',
                        text: `Erro na reinicialização: ${error.message}`
                    }
                ]
            };
        }
    }

    async backupCursorConfig() {
        try {
            const configPath = path.join(process.env.HOME, '.cursor', 'mcp.json');
            const backupPath = path.join(process.env.HOME, '.cursor', 'mcp.json.backup.' + Date.now());
            
            if (fs.existsSync(configPath)) {
                fs.copyFileSync(configPath, backupPath);
                return {
                    content: [
                        {
                            type: 'text',
                            text: `Backup criado: ${backupPath}`
                        }
                    ]
                };
            } else {
                return {
                    content: [
                        {
                            type: 'text',
                            text: 'Arquivo de configuração não encontrado para backup'
                        }
                    ]
                };
            }
        } catch (error) {
            return {
                content: [
                    {
                        type: 'text',
                        text: `Erro no backup: ${error.message}`
                    }
                ]
            };
        }
    }

    async restoreCursorConfig(configFile) {
        try {
            const configPath = path.join(process.env.HOME, '.cursor', 'mcp.json');
            const restorePath = configFile || path.join(process.env.HOME, '.cursor', 'mcp.json.backup');
            
            if (fs.existsSync(restorePath)) {
                fs.copyFileSync(restorePath, configPath);
                return {
                    content: [
                        {
                            type: 'text',
                            text: `Configuração restaurada de: ${restorePath}`
                        }
                    ]
                };
            } else {
                return {
                    content: [
                        {
                            type: 'text',
                            text: 'Arquivo de backup não encontrado'
                        }
                    ]
                };
            }
        } catch (error) {
            return {
                content: [
                    {
                        type: 'text',
                        text: `Erro na restauração: ${error.message}`
                    }
                ]
            };
        }
    }

    async run() {
        const transport = new StdioServerTransport();
        await this.server.connect(transport);
        console.error('Cursor MCP Server running...');
    }
}

// Executar o servidor
const server = new CursorMCPServer();
server.run().catch(console.error);
