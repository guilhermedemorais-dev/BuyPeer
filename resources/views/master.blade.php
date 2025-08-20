<!DOCTYPE html>
<html dir="ltr" lang="{{ str_replace('_', '-', app()->getLocale()) }}">

<head>
    <!-- REQUIRED META TAGS -->
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <script>
        try {
            document.documentElement.setAttribute('dir', 'ltr');
            const vuex = localStorage.getItem('vuex');
            if (vuex) {
                const state = JSON.parse(vuex);
                state.globalState = state.globalState || { lists: {} };
                state.globalState.lists = state.globalState.lists || {};
                state.globalState.lists.display_mode = 5; // force LTR
                localStorage.setItem('vuex', JSON.stringify(state));
            }
        } catch (e) {}
    </script>

    <!-- CUSTOM STYLE -->
    <link rel="stylesheet" href="{{ mix('css/app.css') }}">
    <link rel="stylesheet" href="{{ asset('themes/default/css/custom.css') }}">
    
    <!-- CUSTOM THEME COLORS -->
    @if(isset($customCss))
    <style>
        {!! $customCss !!}
    </style>
    @endif
    <!-- PAGE TITLE -->
    <title>{{ Settings::group('company')->get('company_name') }}</title>

    <!-- FAV ICON -->
    <link rel="icon" type="image" href="{{ $favicon }}">

    @if (!blank($analytics))
        @foreach ($analytics as $analytic)
            @if (!blank($analytic->analyticSections))
                @foreach ($analytic->analyticSections as $section)
                    @if ($section->section == \App\Enums\AnalyticSection::HEAD)
                        {!! $section->data !!}
                    @endif
                @endforeach
            @endif
        @endforeach
    @endif
    @laravelPWA
</head>

<body>
    @if (!blank($analytics))
        @foreach ($analytics as $analytic)
            @if (!blank($analytic->analyticSections))
                @foreach ($analytic->analyticSections as $section)
                    @if ($section->section == \App\Enums\AnalyticSection::BODY)
                        {!! $section->data !!}
                    @endif
                @endforeach
            @endif
        @endforeach
    @endif

    <!-- HEALTHCHECK_BUYPEER: se você vê este bloco, Blade está ok. Se a UI segue vazia, o problema é JS/mount/assets. -->
    <div id="__admin_healthcheck" style="padding:6px;border:1px dashed #aaa;margin:8px 0;background:#f0f0f0;color:#333;font-family:monospace;font-size:12px;">Blade OK - Vue.js deve montar em #app</div>
    <div id="app"></div>

    @if (!blank($analytics))
        @foreach ($analytics as $analytic)
            @if (!blank($analytic->analyticSections))
                @foreach ($analytic->analyticSections as $section)
                    @if ($section->section == \App\Enums\AnalyticSection::FOOTER)
                        {!! $section->data !!}
                    @endif
                @endforeach
            @endif
        @endforeach
    @endif

    <script>
        const APP_URL = "{{ env('MIX_HOST') }}";
        const APP_DEMO = "{{ env('MIX_DEMO') }}";
        const APP_KEY = "{{ env('MIX_API_KEY') }}";
    </script>

    <script src="{{ mix('js/app.js') }}"></script>
    <script src="{{ asset('themes/default/js/modal.js') }}"></script>
    <script src="{{ asset('themes/default/js/customScript.js') }}"></script>
    <script src="{{ asset('pwa/index.js') }}"></script>
    <script src="{{ asset('themes/default/js/tabs.js') }}"></script>

</body>

</html>
