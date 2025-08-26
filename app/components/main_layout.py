import reflex as rx
from app.components.sidebar import sidebar
from app.components.change_password_dialog import (
    change_password_dialog,
)
from app.components.top_bar import top_bar


def main_layout(content: rx.Component) -> rx.Component:
    return rx.el.div(
        change_password_dialog(),
        sidebar(),
        rx.el.div(
            top_bar(),
            rx.el.main(
                content,
                class_name="pt-16 p-6 flex-1",
            ),
            class_name="ml-64 flex flex-col flex-1 transition-all duration-300 ease-in-out",
        ),
        class_name="flex min-h-screen bg-gray-100",
    )