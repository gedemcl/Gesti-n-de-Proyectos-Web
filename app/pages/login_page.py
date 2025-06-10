import reflex as rx
from app.states.auth_state import AuthState


def login_page() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.h2(
                    "Login en el Sistema",
                    class_name="text-2xl font-bold text-gray-800 mb-2 text-center",
                ),
                rx.el.p(
                    "Sistema De Gestión de Proyectos y Tareas",
                    class_name="text-sm text-gray-600 mb-6 text-center",
                ),
                rx.el.form(
                    rx.el.div(
                        rx.el.label(
                            "RUT (Ej: 12345678-9)",
                            html_for="login_username",
                            class_name="block text-sm font-medium text-gray-700 mb-1",
                        ),
                        rx.el.input(
                            name="username",
                            id="login_username",
                            type="text",
                            placeholder="12345678-9",
                            class_name="w-full p-2 border border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500",
                            required=True,
                        ),
                        class_name="mb-4",
                    ),
                    rx.el.div(
                        rx.el.label(
                            "Contraseña",
                            html_for="login_password",
                            class_name="block text-sm font-medium text-gray-700 mb-1",
                        ),
                        rx.el.input(
                            name="password",
                            id="login_password",
                            type="password",
                            placeholder="Contraseña",
                            class_name="w-full p-2 border border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500",
                            required=True,
                        ),
                        class_name="mb-6",
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
                            "ACCEDER",
                            type="submit",
                            class_name="w-full px-6 py-2.5 bg-blue-600 text-white font-semibold rounded-md shadow-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-opacity-50 transition-colors",
                        ),
                        class_name="mb-4",
                    ),
                    on_submit=AuthState.login,
                    class_name="w-full",
                ),
                class_name="w-full md:w-1/2 p-8 md:p-12 flex flex-col justify-center bg-white rounded-l-lg",
            ),
            rx.el.div(
                rx.el.image(
                    src="/arica_professional_logo.png",
                    alt="Logo Municipalidad de Arica",
                    class_name="w-40 h-auto md:w-48 object-contain mx-auto",
                ),
                rx.el.p(
                    "Ilustre Municipalidad de Arica",
                    class_name="text-white text-center mt-6 text-lg font-semibold",
                ),
                rx.el.p(
                    "Compromiso y Gestión",
                    class_name="text-indigo-200 text-center text-sm",
                ),
                class_name="w-full md:w-1/2 bg-indigo-700 flex flex-col items-center justify-center p-8 rounded-r-lg",
            ),
            class_name="flex flex-col md:flex-row bg-white rounded-lg shadow-2xl w-full max-w-4xl mx-auto overflow-hidden",
        ),
        class_name="min-h-screen bg-gray-100 flex items-center justify-center p-4",
    )