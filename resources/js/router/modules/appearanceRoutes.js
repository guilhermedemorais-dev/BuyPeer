import AppearanceComponent from "../../components/admin/appearance/AppearanceComponent";

export default [
    {
        path: "/admin/appearance",
        component: AppearanceComponent,
        name: "admin.appearance",
        meta: {
            isFrontend: false,
            auth: true,
            permissionUrl: "appearance",
            breadcrumb: "appearance",
        },
    },
    {
        path: "/admin/settings/theme-style",
        component: AppearanceComponent,
        name: "admin.settings.theme-style",
        meta: {
            isFrontend: false,
            auth: true,
            permissionUrl: "appearance",
            breadcrumb: "settings.theme-style",
        },
    }
];
