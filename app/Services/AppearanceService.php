<?php

namespace App\Services;

use App\Http\Requests\AppearanceRequest;
use App\Models\ThemeSetting;
use Exception;
use Spatie\Valuestore\Valuestore;

class AppearanceService
{
    protected $defaultColors = [
        'primary_color' => '#FF6A00',
        'bg_color' => '#FFFFFF',
        'text_color' => '#111827'
    ];

    public function list()
    {
        try {
            // Buscar cores personalizadas salvas
            $themeTokens = ThemeSetting::where('key', 'theme_tokens')->first();
            
            if ($themeTokens && $themeTokens->value) {
                $colors = json_decode($themeTokens->value, true);
                return [
                    'primary_color' => $colors['primary_color'] ?? $this->defaultColors['primary_color'],
                    'bg_color' => $colors['bg_color'] ?? $this->defaultColors['bg_color'],
                    'text_color' => $colors['text_color'] ?? $this->defaultColors['text_color'],
                ];
            }

            // Retornar cores padrão se não há customização
            return $this->defaultColors;
            
        } catch (Exception $exception) {
            return $this->defaultColors;
        }
    }

    public function update(AppearanceRequest $request)
    {
        try {
            $colors = [
                'primary_color' => $request->primary_color,
                'bg_color' => $request->bg_color,
                'text_color' => $request->text_color,
            ];

            // Buscar ou criar o registro theme_tokens
            $themeTokens = ThemeSetting::where('key', 'theme_tokens')->first();
            
            if ($themeTokens) {
                $themeTokens->update(['value' => json_encode($colors)]);
            } else {
                ThemeSetting::create([
                    'key' => 'theme_tokens',
                    'value' => json_encode($colors)
                ]);
            }

            return true;
            
        } catch (Exception $exception) {
            throw new Exception('Erro ao salvar as cores: ' . $exception->getMessage());
        }
    }

    public function restore()
    {
        try {
            // Buscar o registro theme_tokens
            $themeTokens = ThemeSetting::where('key', 'theme_tokens')->first();
            
            if ($themeTokens) {
                $themeTokens->update(['value' => json_encode($this->defaultColors)]);
            } else {
                ThemeSetting::create([
                    'key' => 'theme_tokens',
                    'value' => json_encode($this->defaultColors)
                ]);
            }

            return true;
            
        } catch (Exception $exception) {
            throw new Exception('Erro ao restaurar cores padrão: ' . $exception->getMessage());
        }
    }

    public function getCssVariables()
    {
        $colors = $this->list();
        
        return "
        :root {
            --token-primary: {$colors['primary_color']};
            --token-bg: {$colors['bg_color']};
            --token-text: {$colors['text_color']};
            --color-primary: var(--token-primary, {$this->defaultColors['primary_color']});
            --color-bg: var(--token-bg, {$this->defaultColors['bg_color']});
            --color-text: var(--token-text, {$this->defaultColors['text_color']});
        }
        body { background: var(--color-bg); color: var(--color-text); }
        .btn-primary { background: var(--color-primary); color: #fff; }
        .bg-primary { background: var(--color-primary) !important; }
        .text-primary { color: var(--color-primary) !important; }
        .border-primary { border-color: var(--color-primary) !important; }
        ";
    }
}
