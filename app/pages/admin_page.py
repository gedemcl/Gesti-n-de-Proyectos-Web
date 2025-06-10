import reflex as rx
from app.components.main_layout import main_layout
from app.states.auth_state import AuthState
from app.components.add_user_dialog import add_user_dialog
from app.components.user_table_item import user_table_item


def admin_page_content() -> rx.Component:
    return rx.el.div(
        add_user_dialog(),
        rx.el.h1(
            "Administración de Usuarios",
            class_name="text-3xl font-bold text-gray-800 mb-6",
        ),
        rx.el.div(
            rx.el.button(
                rx.el.i(class_name="fas fa-plus mr-2"),
                "Añadir Nuevo Usuario",
                on_click=AuthState.toggle_add_user_dialog,
                class_name="px-4 py-2 bg-indigo-600 text-white font-semibold rounded-md shadow-md hover:bg-indigo-700 transition-colors flex items-center",
            ),
            class_name="mb-6 flex justify-end",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.label(
                    "Filtrar por nombre:",
                    html_for="filter_user_username_input",
                    class_name="text-sm font-medium text-gray-700 mr-2",
                ),
                rx.el.input(
                    id="filter_user_username_input",
                    placeholder="Nombre de usuario",
                    on_change=AuthState.set_filter_user_username,
                    class_name="p-2 border border-gray-300 rounded-md focus:ring-indigo-500 focus:border-indigo-500 text-sm",
                    default_value=AuthState.filter_user_username,
                ),
                class_name="flex items-center",
            ),
            rx.el.div(
                rx.el.label(
                    "Filtrar por rol:",
                    html_for="filter_user_role_select",
                    class_name="text-sm font-medium text-gray-700 mr-2",
                ),
                rx.el.select(
                    rx.el.option("Todos", value="todos"),
                    rx.el.option("Admin", value="admin"),
                    rx.el.option("User", value="user"),
                    id="filter_user_role_select",
                    value=AuthState.filter_user_role,
                    on_change=AuthState.set_filter_user_role,
                    class_name="p-2 border border-gray-300 rounded-md focus:ring-indigo-500 focus:border-indigo-500 text-sm",
                ),
                class_name="flex items-center",
            ),
            class_name="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6 p-4 border-y border-gray-200 bg-gray-50 items-end",
        ),
        rx.el.div(
            rx.el.table(
                rx.el.thead(
                    rx.el.tr(
                        rx.el.th(
                            "Usuario",
                            class_name="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider",
                        ),
                        rx.el.th(
                            "Roles",
                            class_name="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider",
                        ),
                        rx.el.th(
                            "Email",
                            class_name="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider",
                        ),
                        rx.el.th(
                            "Teléfono",
                            class_name="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider",
                        ),
                        rx.el.th(
                            "Contacto Adicional",
                            class_name="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider",
                        ),
                        rx.el.th(
                            "Acciones",
                            class_name="px-4 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider",
                        ),
                    ),
                    class_name="bg-gray-100",
                ),
                rx.el.tbody(
                    rx.foreach(
                        AuthState.filtered_users,
                        user_table_item,
                    ),
                    class_name="bg-white divide-y divide-gray-200",
                ),
                class_name="min-w-full shadow-md rounded-lg overflow-hidden",
            ),
            rx.cond(
                AuthState.filtered_users.length() == 0,
                rx.el.p(
                    "No se encontraron usuarios que coincidan con los filtros.",
                    class_name="text-center text-gray-500 py-4",
                ),
                rx.el.span(),
            ),
            class_name="overflow-x-auto",
        ),
        class_name="p-6",
        on_mount=AuthState.load_users,
    )


def admin_page() -> rx.Component:
    return main_layout(admin_page_content())