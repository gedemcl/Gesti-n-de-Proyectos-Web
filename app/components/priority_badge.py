import reflex as rx
from app.models import PriorityType


def priority_badge(priority: PriorityType) -> rx.Component:
    return rx.match(
        priority,
        (
            "crítica",
            rx.el.span(
                priority,
                class_name="capitalize px-2 py-0.5 text-xs font-semibold rounded-full bg-red-100 text-red-800",
            ),
        ),
        (
            "alta",
            rx.el.span(
                priority,
                class_name="capitalize px-2 py-0.5 text-xs font-semibold rounded-full bg-orange-100 text-orange-800",
            ),
        ),
        (
            "media",
            rx.el.span(
                priority,
                class_name="capitalize px-2 py-0.5 text-xs font-semibold rounded-full bg-blue-100 text-blue-800",
            ),
        ),
        rx.el.span(
            priority,
            class_name="capitalize px-2 py-0.5 text-xs font-semibold rounded-full bg-gray-100 text-gray-800",
        ),
    )