import reflex as rx
from app.components.sidebar import sidebar
from app.components.change_password_dialog import (
    change_password_dialog,
)


def main_layout(content: rx.Component) -> rx.Component:
    return rx.el.div(
        change_password_dialog(),
        sidebar(),
        rx.el.main(
            content,
            class_name="ml-64 p-0 flex-1 transition-all duration-300 ease-in-out",
        ),
        class_name="flex min-h-screen bg-gray-100",
    )