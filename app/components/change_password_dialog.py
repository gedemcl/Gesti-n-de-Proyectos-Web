import reflex as rx
from app.states.auth_state import AuthState


def change_password_dialog() -> rx.Component:
    return rx.el.dialog(
        rx.el.div(
            rx.el.form(
                rx.el.h3(
                    "Cambiar Contraseña",
                    class_name="text-xl font-semibold mb-6 text-gray-800",
                ),
                rx.el.div(
                    rx.el.label(
                        "Contraseña Actual*",
                        html_for="current_password_input",
                        class_name="text-sm font-medium text-gray-700",
                    ),
                    rx.el.input(
                        name="current_password_input",
                        id="current_password_input",
                        type="password",
                        placeholder="Ingrese su contraseña actual",
                        default_value=AuthState.current_password_input,
                        class_name="w-full p-2 mt-1 border border-gray-300 rounded-md focus:ring-indigo-500 focus:border-indigo-500",
                        required=True,
                    ),
                    class_name="mb-4",
                ),
                rx.el.div(
                    rx.el.label(
                        "Nueva Contraseña*",
                        html_for="new_password_input",
                        class_name="text-sm font-medium text-gray-700",
                    ),
                    rx.el.input(
                        name="new_password_input",
                        id="new_password_input",
                        type="password",
                        placeholder="Ingrese su nueva contraseña",
                        default_value=AuthState.new_password_input,
                        class_name="w-full p-2 mt-1 border border-gray-300 rounded-md focus:ring-indigo-500 focus:border-indigo-500",
                        required=True,
                    ),
                    class_name="mb-4",
                ),
                rx.el.div(
                    rx.el.label(
                        "Confirmar Nueva Contraseña*",
                        html_for="confirm_new_password_input",
                        class_name="text-sm font-medium text-gray-700",
                    ),
                    rx.el.input(
                        name="confirm_new_password_input",
                        id="confirm_new_password_input",
                        type="password",
                        placeholder="Confirme su nueva contraseña",
                        default_value=AuthState.confirm_new_password_input,
                        class_name="w-full p-2 mt-1 border border-gray-300 rounded-md focus:ring-indigo-500 focus:border-indigo-500",
                        required=True,
                    ),
                    class_name="mb-4",
                ),
                rx.cond(
                    AuthState.error_message != "",
                    rx.el.p(
                        AuthState.error_message,
                        class_name="text-sm text-red-600 mb-4 text-center",
                    ),
                    rx.el.span(),
                ),
                rx.el.div(
                    rx.el.button(
                        "Cancelar",
                        type="button",
                        on_click=AuthState.toggle_change_password_dialog,
                        class_name="px-4 py-2 text-sm font-medium text-gray-700 bg-gray-100 rounded-md hover:bg-gray-200 transition-colors",
                    ),
                    rx.el.button(
                        "Cambiar Contraseña",
                        type="submit",
                        class_name="px-4 py-2 ml-2 text-sm font-medium text-white bg-indigo-600 rounded-md hover:bg-indigo-700 transition-colors",
                    ),
                    class_name="flex justify-end mt-6",
                ),
                on_submit=AuthState.change_password_current_user,
                reset_on_submit=False,
                class_name="bg-white p-6 rounded-lg shadow-xl w-full max-w-md",
            ),
            class_name="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 p-4 z-50 overflow-y-auto",
        ),
        open=AuthState.show_change_password_dialog,
    )