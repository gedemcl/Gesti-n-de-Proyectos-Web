import reflex as rx
from app.models import User as UserType


def user_table_item(user: UserType) -> rx.Component:
    return rx.el.tr(
        rx.el.td(
            user["username"],
            class_name="px-4 py-3 text-sm text-gray-700 border-b border-gray-200",
        ),
        rx.el.td(
            rx.foreach(
                user["roles"],
                lambda role: rx.el.span(
                    role,
                    class_name=rx.cond(
                        role == "admin",
                        "capitalize px-2 py-0.5 text-xs font-semibold rounded-full mr-1 bg-blue-100 text-blue-800",
                        "capitalize px-2 py-0.5 text-xs font-semibold rounded-full mr-1 bg-green-100 text-green-800",
                    ),
                ),
            ),
            class_name="px-4 py-3 text-sm text-gray-700 border-b border-gray-200",
        ),
        rx.el.td(
            user["email"],
            class_name="px-4 py-3 text-sm text-gray-700 border-b border-gray-200",
        ),
        rx.el.td(
            user["phone"],
            class_name="px-4 py-3 text-sm text-gray-700 border-b border-gray-200",
        ),
        rx.el.td(
            user["contact_info"],
            class_name="px-4 py-3 text-sm text-gray-700 border-b border-gray-200",
        ),
        rx.el.td(
            rx.el.button(
                rx.el.i(class_name="fas fa-edit"),
                class_name="p-2 text-sm text-blue-600 hover:text-blue-800 transition-colors",
                disabled=True,
            ),
            rx.el.button(
                rx.el.i(class_name="fas fa-trash-alt"),
                class_name="p-2 text-sm text-red-600 hover:text-red-800 transition-colors",
                disabled=True,
            ),
            class_name="px-4 py-3 text-sm text-gray-700 border-b border-gray-200 text-right",
        ),
        key=user["id"],
        class_name="hover:bg-gray-50",
    )