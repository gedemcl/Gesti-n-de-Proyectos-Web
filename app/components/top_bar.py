import reflex as rx
from app.states.auth_state import AuthState


def top_bar() -> rx.Component:
    return rx.el.header(
        rx.el.div(
            rx.el.image(
                src="/professional_logo_ilustre.png",
                alt="Logo Municipalidad de Arica",
                class_name="h-8 w-auto",
            ),
            class_name="flex items-center space-x-2",
        ),
        rx.el.div(
            rx.el.span(
                AuthState.current_user_display_name,
                class_name="text-gray-700 font-medium",
            ),
            class_name="flex items-center space-x-2",
        ),
        class_name="flex justify-between items-center bg-white border-b h-14 px-4 fixed top-0 left-64 right-0 z-10 shadow-sm",
    )
