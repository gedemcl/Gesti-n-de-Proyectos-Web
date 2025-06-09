import reflex as rx
from app.states.auth_state import AuthState


def sidebar_link(
    text: str, href: str, icon_class: str
) -> rx.Component:
    return rx.el.a(
        rx.el.i(
            class_name=f"{icon_class} mr-3 w-5 text-center"
        ),
        text,
        href=href,
        class_name="flex items-center px-4 py-2.5 text-sm font-medium text-gray-700 rounded-lg hover:bg-blue-100 hover:text-blue-700 transition-colors",
    )


def sidebar() -> rx.Component:
    return rx.el.aside(
        rx.el.div(
            rx.el.div(
                rx.el.image(
                    src="/professional_logo_ilustre.png",
                    alt="Logo Municipalidad de Arica",
                    class_name="h-16 w-auto mx-auto mt-4 mb-2",
                ),
                class_name="p-4 border-b border-gray-200",
            ),
            rx.el.nav(
                sidebar_link(
                    "Dashboard",
                    "/dashboard",
                    "fas fa-tachometer-alt",
                ),
                sidebar_link(
                    "Proyectos",
                    "/proyectos",
                    "fas fa-project-diagram",
                ),
                sidebar_link(
                    "Bitácora General",
                    "/bitacora",
                    "fas fa-history",
                ),
                rx.cond(
                    AuthState.is_admin,
                    sidebar_link(
                        "Administración",
                        "/admin",
                        "fas fa-users-cog",
                    ),
                    rx.el.span(),
                ),
                sidebar_link(
                    "Ayuda y Contacto",
                    "/ayuda",
                    "fas fa-question-circle",
                ),
                class_name="flex-grow p-4 space-y-1",
            ),
            rx.el.div(
                rx.el.button(
                    rx.el.i(class_name="fas fa-key mr-2"),
                    "Cambiar Contraseña",
                    on_click=AuthState.toggle_change_password_dialog,
                    class_name="w-full flex items-center justify-center px-4 py-2.5 text-sm font-medium text-blue-600 bg-blue-50 rounded-lg hover:bg-blue-100 transition-colors mb-2",
                ),
                rx.el.button(
                    rx.el.i(
                        class_name="fas fa-sign-out-alt mr-2"
                    ),
                    "Cerrar Sesión",
                    on_click=AuthState.logout,
                    class_name="w-full flex items-center justify-center px-4 py-2.5 text-sm font-medium text-red-600 bg-red-50 rounded-lg hover:bg-red-100 transition-colors",
                ),
                class_name="p-4 border-t border-gray-200",
            ),
            class_name="flex flex-col h-full bg-white shadow-lg",
        ),
        class_name=rx.cond(
            AuthState.sidebar_open,
            "fixed top-0 left-0 z-30 w-64 h-screen bg-white border-r border-gray-200 transition-transform duration-300 ease-in-out lg:translate-x-0 translate-x-0",
            "fixed top-0 left-0 z-30 w-64 h-screen bg-white border-r border-gray-200 transition-transform duration-300 ease-in-out lg:translate-x-0 -translate-x-full",
        ),
    )