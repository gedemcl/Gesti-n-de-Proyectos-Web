import reflex as rx
from app.states.auth_state import AuthState


def add_user_dialog() -> rx.Component:
    return rx.el.dialog(
        rx.el.div(
            rx.el.form(
                rx.el.h3(
                    "Agregar Nuevo Usuario",
                    class_name="text-xl font-semibold mb-6 text-gray-800",
                ),
                rx.el.div(
                    rx.el.label(
                        "RUT del Usuario* (Ej: 12345678-9)",
                        html_for="new_username",
                        class_name="text-sm font-medium text-gray-700",
                    ),
                    rx.el.input(
                        name="new_username",
                        id="new_username",
                        placeholder="12345678-9",
                        class_name="w-full p-2 mt-1 border border-gray-300 rounded-md focus:ring-indigo-500 focus:border-indigo-500",
                        required=True,
                    ),
                    class_name="mb-4",
                ),
                rx.el.div(
                    rx.el.label(
                        "Email",
                        html_for="new_user_email",
                        class_name="text-sm font-medium text-gray-700",
                    ),
                    rx.el.input(
                        name="new_user_email",
                        id="new_user_email",
                        type="email",
                        placeholder="usuario@example.com",
                        class_name="w-full p-2 mt-1 border border-gray-300 rounded-md focus:ring-indigo-500 focus:border-indigo-500",
                    ),
                    class_name="mb-4",
                ),
                rx.el.div(
                    rx.el.label(
                        "Teléfono",
                        html_for="new_user_phone",
                        class_name="text-sm font-medium text-gray-700",
                    ),
                    rx.el.input(
                        name="new_user_phone",
                        id="new_user_phone",
                        placeholder="Ej: +56912345678",
                        class_name="w-full p-2 mt-1 border border-gray-300 rounded-md focus:ring-indigo-500 focus:border-indigo-500",
                    ),
                    class_name="mb-4",
                ),
                rx.el.div(
                    rx.el.label(
                        "Información de Contacto Adicional",
                        html_for="new_user_contact_info",
                        class_name="text-sm font-medium text-gray-700",
                    ),
                    rx.el.textarea(
                        name="new_user_contact_info",
                        id="new_user_contact_info",
                        placeholder="Ej: Departamento, oficina, etc.",
                        class_name="w-full p-2 mt-1 border border-gray-300 rounded-md focus:ring-indigo-500 focus:border-indigo-500 h-20",
                    ),
                    class_name="mb-4",
                ),
                rx.el.div(
                    rx.el.label(
                        "Roles",
                        class_name="text-sm font-medium text-gray-700 mb-1",
                    ),
                    rx.el.div(
                        rx.el.input(
                            type="checkbox",
                            name="new_user_assign_admin_role",
                            id="new_user_assign_admin_role",
                            class_name="mr-2 focus:ring-indigo-500",
                        ),
                        rx.el.label(
                            "Administrador",
                            html_for="new_user_assign_admin_role",
                            class_name="text-sm text-gray-700",
                        ),
                        class_name="flex items-center mb-1",
                    ),
                    rx.el.div(
                        rx.el.input(
                            type="checkbox",
                            name="new_user_assign_user_role",
                            id="new_user_assign_user_role",
                            class_name="mr-2 focus:ring-indigo-500",
                        ),
                        rx.el.label(
                            "Usuario Estándar",
                            html_for="new_user_assign_user_role",
                            class_name="text-sm text-gray-700",
                        ),
                        class_name="flex items-center",
                    ),
                    class_name="mb-4",
                ),
                rx.cond(
                    AuthState.new_user_generated_password
                    != "",
                    rx.el.div(
                        rx.el.p(
                            "Usuario Creado - Contraseña Temporal:",
                            class_name="text-sm font-medium text-gray-700",
                        ),
                        rx.el.p(
                            AuthState.new_user_generated_password,
                            class_name="text-sm text-green-600 bg-green-50 p-2 rounded-md select-all",
                        ),
                        class_name="mb-4",
                    ),
                    rx.el.span(),
                ),
                rx.el.div(
                    rx.el.button(
                        "Cerrar",
                        type="button",
                        on_click=AuthState.toggle_add_user_dialog,
                        class_name="px-4 py-2 text-sm font-medium text-gray-700 bg-gray-100 rounded-md hover:bg-gray-200 transition-colors",
                    ),
                    rx.el.button(
                        "Crear Usuario",
                        type="submit",
                        class_name="px-4 py-2 ml-2 text-sm font-medium text-white bg-indigo-600 rounded-md hover:bg-indigo-700 transition-colors",
                    ),
                    class_name="flex justify-end mt-6",
                ),
                on_submit=AuthState.add_user,
                reset_on_submit=False,
                class_name="bg-white p-6 rounded-lg shadow-xl w-full max-w-md",
            ),
            class_name="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 p-4 z-50 overflow-y-auto",
        ),
        open=AuthState.show_add_user_dialog,
    )