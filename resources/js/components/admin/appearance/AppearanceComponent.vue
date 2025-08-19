<template>
    <div id="appearance" class="db-card db-tab-div active">
        <div class="db-card-header border-none">
            <h3 class="db-card-title">{{ $t("menu.appearance") }}</h3>
        </div>
        <div class="db-card-body">
            <form @submit.prevent="save">
                <div class="row">
                    <div class="col-12">
                        <div class="db-field-wrap mb-6">
                            <label for="primary_color" class="db-field-title required">
                                Cor Primária
                            </label>
                            <div class="flex items-center gap-4">
                                <input
                                    v-model="form.primary_color"
                                    v-bind:class="errors.primary_color ? 'invalid' : ''"
                                    id="primary_color"
                                    type="color"
                                    class="db-field-control w-20 h-12 rounded-lg border cursor-pointer"
                                />
                                <input
                                    v-model="form.primary_color"
                                    v-bind:class="errors.primary_color ? 'invalid' : ''"
                                    type="text"
                                    class="db-field-control flex-1"
                                    placeholder="#FF6A00"
                                />
                            </div>
                            <small class="db-field-alert" v-if="errors.primary_color">
                                {{ errors.primary_color[0] }}
                            </small>
                        </div>
                    </div>

                    <div class="col-12">
                        <div class="db-field-wrap mb-6">
                            <label for="bg_color" class="db-field-title required">
                                Cor de Fundo
                            </label>
                            <div class="flex items-center gap-4">
                                <input
                                    v-model="form.bg_color"
                                    v-bind:class="errors.bg_color ? 'invalid' : ''"
                                    id="bg_color"
                                    type="color"
                                    class="db-field-control w-20 h-12 rounded-lg border cursor-pointer"
                                />
                                <input
                                    v-model="form.bg_color"
                                    v-bind:class="errors.bg_color ? 'invalid' : ''"
                                    type="text"
                                    class="db-field-control flex-1"
                                    placeholder="#FFFFFF"
                                />
                            </div>
                            <small class="db-field-alert" v-if="errors.bg_color">
                                {{ errors.bg_color[0] }}
                            </small>
                        </div>
                    </div>

                    <div class="col-12">
                        <div class="db-field-wrap mb-6">
                            <label for="text_color" class="db-field-title required">
                                Cor do Texto
                            </label>
                            <div class="flex items-center gap-4">
                                <input
                                    v-model="form.text_color"
                                    v-bind:class="errors.text_color ? 'invalid' : ''"
                                    id="text_color"
                                    type="color"
                                    class="db-field-control w-20 h-12 rounded-lg border cursor-pointer"
                                />
                                <input
                                    v-model="form.text_color"
                                    v-bind:class="errors.text_color ? 'invalid' : ''"
                                    type="text"
                                    class="db-field-control flex-1"
                                    placeholder="#111827"
                                />
                            </div>
                            <small class="db-field-alert" v-if="errors.text_color">
                                {{ errors.text_color[0] }}
                            </small>
                        </div>
                    </div>

                    <div class="col-12">
                        <div class="db-field-wrap mb-6">
                            <h4 class="text-lg font-medium mb-4">Pré-visualização</h4>
                            <div class="preview-container p-6 rounded-lg border" :style="previewStyle">
                                <div class="flex items-center gap-4 mb-4">
                                    <button 
                                        type="button" 
                                        class="px-4 py-2 rounded-lg font-medium btn-primary"
                                        :style="{ backgroundColor: form.primary_color, color: '#fff' }"
                                    >
                                        Botão Primário
                                    </button>
                                    <button 
                                        type="button" 
                                        class="px-4 py-2 rounded-lg border font-medium"
                                        :style="{ borderColor: form.primary_color, color: form.primary_color }"
                                    >
                                        Botão Secundário
                                    </button>
                                </div>
                                <p class="mb-2" :style="{ color: form.text_color }">
                                    <strong>Este é um exemplo</strong> de como as cores aparecerão no sistema.
                                </p>
                                <p class="text-sm" :style="{ color: form.text_color + '80' }">
                                    Texto secundário com transparência aplicada.
                                </p>
                            </div>
                        </div>
                    </div>

                    <div class="col-12">
                        <div class="flex items-center gap-4">
                            <button 
                                type="submit" 
                                class="db-btn py-2 text-white bg-primary"
                                :disabled="loading.isActive"
                            >
                                <i class="lab lab-fill-save"></i>
                                <span>{{ $t("button.save") }}</span>
                            </button>
                            
                            <button 
                                type="button" 
                                @click="restore"
                                class="db-btn py-2 text-gray-600 bg-gray-100"
                                :disabled="loading.isActive"
                            >
                                <i class="lab lab-line-refresh"></i>
                                <span>Restaurar Padrão</span>
                            </button>
                        </div>
                    </div>
                </div>
            </form>
        </div>
    </div>
</template>

<script>
import LoadingComponent from "../components/LoadingComponent";
import alertService from "../../../services/alertService";

export default {
    name: "AppearanceComponent",
    components: {LoadingComponent},
    data() {
        return {
            loading: {
                isActive: false,
            },
            form: {
                primary_color: "#FF6A00",
                bg_color: "#FFFFFF",
                text_color: "#111827",
            },
            errors: {},
        }
    },
    computed: {
        previewStyle() {
            return {
                backgroundColor: this.form.bg_color,
                color: this.form.text_color,
            }
        }
    },
    mounted() {
        this.loading.isActive = true;
        this.$store.dispatch("appearance/lists").then(res => {
            this.form = {
                primary_color: res.data.data.primary_color,
                bg_color: res.data.data.bg_color,
                text_color: res.data.data.text_color,
            };
            this.loading.isActive = false;
        }).catch((err) => {
            this.loading.isActive = false;
        });
    },
    methods: {
        save: function () {
            this.loading.isActive = true;
            this.errors = {};
            
            this.$store.dispatch("appearance/save", {
                primary_color: this.form.primary_color,
                bg_color: this.form.bg_color,
                text_color: this.form.text_color,
            }).then((res) => {
                this.loading.isActive = false;
                alertService.successFlip(0, "Cores atualizadas com sucesso!");
                this.errors = {};
                // Aplicar as cores globalmente
                this.applyCssVariables();
            }).catch((err) => {
                this.loading.isActive = false;
                this.errors = err.response.data.errors || {};
            });
        },
        restore: function () {
            if (confirm('Tem certeza que deseja restaurar as cores padrão?')) {
                this.loading.isActive = true;
                this.$store.dispatch("appearance/restore").then((res) => {
                    this.loading.isActive = false;
                    alertService.successFlip(0, "Cores restauradas para o padrão!");
                    // Recarregar as cores
                    this.form = {
                        primary_color: "#FF6A00",
                        bg_color: "#FFFFFF",
                        text_color: "#111827",
                    };
                    this.applyCssVariables();
                }).catch((err) => {
                    this.loading.isActive = false;
                });
            }
        },
        applyCssVariables: function() {
            // Aplicar CSS variables globalmente
            const root = document.documentElement;
            root.style.setProperty('--token-primary', this.form.primary_color);
            root.style.setProperty('--token-bg', this.form.bg_color);
            root.style.setProperty('--token-text', this.form.text_color);
            root.style.setProperty('--color-primary', this.form.primary_color);
            root.style.setProperty('--color-bg', this.form.bg_color);
            root.style.setProperty('--color-text', this.form.text_color);
        }
    }
}
</script>

<style scoped>
.preview-container {
    transition: all 0.3s ease;
}

.btn-primary {
    transition: all 0.3s ease;
}

.db-field-control[type="color"] {
    padding: 0;
    border: 2px solid #e5e7eb;
}

.db-field-control[type="color"]::-webkit-color-swatch-wrapper {
    padding: 0;
}

.db-field-control[type="color"]::-webkit-color-swatch {
    border: none;
    border-radius: 0.5rem;
}
</style>
