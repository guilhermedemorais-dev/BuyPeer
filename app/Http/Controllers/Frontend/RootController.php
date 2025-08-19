<?php

namespace App\Http\Controllers\Frontend;


use App\Enums\Status;
use App\Models\Analytic;
use App\Models\ThemeSetting;
use App\Http\Controllers\Controller;
use App\Services\AppearanceService;

class RootController extends Controller
{
    public function index(): \Illuminate\Contracts\View\Factory|\Illuminate\Contracts\View\View|\Illuminate\Contracts\Foundation\Application
    {
        $analytics    = Analytic::with('analyticSections')->where(['status' => Status::ACTIVE])->get();
        $themeFavicon = ThemeSetting::where(['key' => 'theme_favicon_logo'])->first();
        $favIcon      = $themeFavicon?->faviconLogo ?? asset('images/required/theme-favicon-logo.png');
        
        // Injetar cores personalizadas
        $appearanceService = new AppearanceService();
        $customCss = $appearanceService->getCssVariables();
        
        return view('master', [
            'analytics' => $analytics, 
            'favicon' => $favIcon,
            'customCss' => $customCss
        ]);
    }
}
