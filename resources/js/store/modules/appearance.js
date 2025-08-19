import axios from "axios";

export const appearance = {
    namespaced: true,
    state: {
        colors: {
            primary_color: "#FF6A00",
            bg_color: "#FFFFFF", 
            text_color: "#111827"
        }
    },
    getters: {
        colors: function (state) {
            return state.colors;
        }
    },
    actions: {
        lists: function (context) {
            return new Promise((resolve, reject) => {
                // Detectar se estamos na rota theme-style
                const isThemeStyle = window.location.pathname.includes('/settings/theme-style');
                const url = isThemeStyle ? "admin/settings/theme-style" : "admin/appearance";
                
                axios.get(url).then((res) => {
                    context.commit("lists", res.data.data);
                    resolve(res);
                }).catch((err) => {
                    reject(err);
                });
            });
        },
        save: function (context, payload) {
            return new Promise((resolve, reject) => {
                // Detectar se estamos na rota theme-style
                const isThemeStyle = window.location.pathname.includes('/settings/theme-style');
                const url = isThemeStyle ? "admin/settings/theme-style" : "admin/appearance";
                
                axios.post(url, payload).then((res) => {
                    context.commit("lists", payload);
                    resolve(res);
                }).catch((err) => {
                    reject(err);
                });
            });
        },
        restore: function (context) {
            return new Promise((resolve, reject) => {
                // Detectar se estamos na rota theme-style
                const isThemeStyle = window.location.pathname.includes('/settings/theme-style');
                const url = isThemeStyle ? "admin/settings/theme-style/restore" : "admin/appearance/restore";
                
                axios.post(url).then((res) => {
                    const defaultColors = {
                        primary_color: "#FF6A00",
                        bg_color: "#FFFFFF",
                        text_color: "#111827"
                    };
                    context.commit("lists", defaultColors);
                    resolve(res);
                }).catch((err) => {
                    reject(err);
                });
            });
        }
    },
    mutations: {
        lists: function (state, payload) {
            state.colors = payload;
        }
    }
};
