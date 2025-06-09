import reflex as rx
from app.models import StatusType


def status_badge(status: StatusType) -> rx.Component:
    return rx.match(
        status,
        (
            "por hacer",
            rx.el.span(
                status,
                class_name="capitalize px-2 py-0.5 text-xs font-semibold rounded-full bg-gray-200 text-gray-700",
            ),
        ),
        (
            "en progreso",
            rx.el.span(
                status,
                class_name="capitalize px-2 py-0.5 text-xs font-semibold rounded-full bg-yellow-100 text-yellow-800",
            ),
        ),
        (
            "hecho",
            rx.el.span(
                status,
                class_name="capitalize px-2 py-0.5 text-xs font-semibold rounded-full bg-green-100 text-green-800",
            ),
        ),
        (
            "idea",
            rx.el.span(
                status,
                class_name="capitalize px-2 py-0.5 text-xs font-semibold rounded-full bg-blue-100 text-blue-800",
            ),
        ),
        (
            "diseño",
            rx.el.span(
                status,
                class_name="capitalize px-2 py-0.5 text-xs font-semibold rounded-full bg-purple-100 text-purple-800",
            ),
        ),
        (
            "ejecución",
            rx.el.span(
                status,
                class_name="capitalize px-2 py-0.5 text-xs font-semibold rounded-full bg-yellow-100 text-yellow-800",
            ),
        ),
        (
            "finalizado",
            rx.el.span(
                status,
                class_name="capitalize px-2 py-0.5 text-xs font-semibold rounded-full bg-green-100 text-green-800",
            ),
        ),
        rx.el.span(
            status,
            class_name="capitalize px-2 py-0.5 text-xs font-semibold rounded-full bg-gray-100 text-gray-800",
        ),
    )