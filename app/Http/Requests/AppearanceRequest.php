<?php

namespace App\Http\Requests;

use Illuminate\Foundation\Http\FormRequest;

class AppearanceRequest extends FormRequest
{
    /**
     * Determine if the user is authorized to make this request.
     *
     * @return bool
     */
    public function authorize()
    {
        return true;
    }

    /**
     * Get the validation rules that apply to the request.
     *
     * @return array
     */
    public function rules()
    {
        return [
            'primary_color' => ['required', 'string', 'regex:/^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$/'],
            'bg_color' => ['required', 'string', 'regex:/^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$/'],
            'text_color' => ['required', 'string', 'regex:/^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$/'],
        ];
    }

    /**
     * Get custom attributes for validator errors.
     *
     * @return array
     */
    public function attributes()
    {
        return [
            'primary_color' => 'cor primária',
            'bg_color' => 'cor de fundo',
            'text_color' => 'cor do texto',
        ];
    }

    /**
     * Get the error messages for the defined validation rules.
     *
     * @return array
     */
    public function messages()
    {
        return [
            'regex' => 'A :attribute deve ser uma cor hexadecimal válida (ex: #FF6A00).',
            'required' => 'A :attribute é obrigatória.',
            'string' => 'A :attribute deve ser um texto válido.',
        ];
    }
}
