import reflex as rx
from app.models import LogEntry as LogEntryType


def log_entry_item(log_entry: LogEntryType) -> rx.Component:
    return rx.el.div(
        rx.el.p(
            log_entry["formatted_timestamp"],
            class_name="text-xs text-gray-500 font-mono mr-2 flex-shrink-0 w-36",
        ),
        rx.el.div(
            rx.el.p(
                log_entry["action"],
                class_name="text-sm text-gray-700 break-words",
            ),
            rx.el.p(
                f"Usuario: {log_entry['user']}",
                class_name="text-xs text-gray-500 mt-0.5",
            ),
            class_name="flex-grow",
        ),
        class_name="py-2 px-3 border-b border-gray-100 flex items-start hover:bg-gray-50",
        key=log_entry["id"],
    )