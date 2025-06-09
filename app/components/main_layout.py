import reflex as rx
from app.components.sidebar import sidebar
from app.components.change_password_dialog import (
    change_password_dialog,
)
from app.states.auth_state import AuthState


def main_layout(content: rx.Component) -> rx.Component:
    return rx.el.div(
        change_password_dialog(),
        sidebar(),
        rx.cond(
            AuthState.sidebar_open,
            rx.el.div(
                on_click=AuthState.toggle_sidebar,
                class_name="fixed inset-0 bg-gray-900/80 z-20 lg:hidden",
            ),
            rx.el.span(),
        ),
        rx.el.div(
            rx.el.header(
                rx.el.button(
                    rx.el.i(class_name="fas fa-bars"),
                    on_click=AuthState.toggle_sidebar,
                    class_name="p-2 rounded-md text-gray-700 hover:bg-gray-100 lg:hidden",
                ),
                class_name="sticky top-0 z-10 flex h-16 flex-shrink-0 items-center border-b border-gray-200 bg-white px-4 shadow-sm sm:px-6 lg:hidden",
            ),
            rx.el.main(content, class_name="flex-1"),
            class_name="flex flex-col flex-1 lg:ml-64 transition-all duration-300 ease-in-out",
        ),
        class_name="flex min-h-screen bg-gray-100",
    )