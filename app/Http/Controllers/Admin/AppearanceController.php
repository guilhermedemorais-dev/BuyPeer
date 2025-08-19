<?php

namespace App\Http\Controllers\Admin;

use App\Http\Controllers\Controller;
use App\Http\Requests\AppearanceRequest;
use App\Services\AppearanceService;
use Exception;
use Illuminate\Http\Request;

class AppearanceController extends Controller
{
    public AppearanceService $appearanceService;

    public function __construct(AppearanceService $appearanceService)
    {
        $this->appearanceService = $appearanceService;
    }

    public function index(): \Illuminate\Http\JsonResponse
    {
        try {
            return response()->json([
                'data' => $this->appearanceService->list()
            ]);
        } catch (Exception $exception) {
            return response()->json(['message' => $exception->getMessage()], 422);
        }
    }

    public function update(AppearanceRequest $request): \Illuminate\Http\JsonResponse
    {
        try {
            $this->appearanceService->update($request);
            return response()->json([
                'message' => 'Cores atualizadas com sucesso!'
            ]);
        } catch (Exception $exception) {
            return response()->json(['message' => $exception->getMessage()], 422);
        }
    }

    public function restore(): \Illuminate\Http\JsonResponse
    {
        try {
            $this->appearanceService->restore();
            return response()->json([
                'message' => 'Cores restauradas para o padrão!'
            ]);
        } catch (Exception $exception) {
            return response()->json(['message' => $exception->getMessage()], 422);
        }
    }
}
