import reflex as rx
from app.components.main_layout import main_layout
from app.states.project_state import ProjectState
from app.components.log_entry_item import log_entry_item
from app.models import VALID_PROJECT_STATUSES


def bitacora_filters() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.label(
                "Filtrar por estado del proyecto:",
                html_for="log_filter_project_status",
                class_name="text-sm font-medium text-gray-700 mr-2",
            ),
            rx.el.select(
                rx.el.option(
                    "Todos los Estados", value="todos"
                ),
                rx.foreach(
                    VALID_PROJECT_STATUSES,
                    lambda s: rx.el.option(
                        s.capitalize(), value=s
                    ),
                ),
                id="log_filter_project_status",
                value=ProjectState.filter_log_project_status,
                on_change=ProjectState.set_filter_log_project_status,
                class_name="p-2 border border-gray-300 rounded-md focus:ring-indigo-500 focus:border-indigo-500 text-sm",
            ),
            class_name="flex items-center",
        ),
        rx.el.div(
            rx.el.label(
                "Buscar en acción:",
                html_for="log_filter_action_text",
                class_name="text-sm font-medium text-gray-700 mr-2",
            ),
            rx.el.input(
                id="log_filter_action_text",
                placeholder="Texto en la acción...",
                on_change=ProjectState.set_filter_log_action_text,
                class_name="p-2 border border-gray-300 rounded-md focus:ring-indigo-500 focus:border-indigo-500 text-sm",
                default_value=ProjectState.filter_log_action_text,
            ),
            class_name="flex items-center",
        ),
        rx.el.button(
            "Limpiar Filtros de Bitácora",
            on_click=ProjectState.clear_log_filters,
            class_name="px-3 py-2 bg-gray-200 text-gray-700 font-semibold rounded-md hover:bg-gray-300 transition-colors text-sm",
        ),
        class_name="grid grid-cols-1 md:grid-cols-3 gap-4 p-4 border-b border-gray-200 bg-gray-50 items-end",
    )


def bitacora_general_content() -> rx.Component:
    return rx.el.div(
        rx.el.h1(
            "Bitácora General de Actividad",
            class_name="text-3xl font-bold text-gray-800 mb-6",
        ),
        bitacora_filters(),
        rx.el.div(
            rx.cond(
                ProjectState.filtered_log_entries.length()
                > 0,
                rx.el.div(
                    rx.foreach(
                        ProjectState.filtered_log_entries,
                        log_entry_item,
                    ),
                    class_name="bg-white rounded-lg shadow divide-y divide-gray-100",
                ),
                rx.el.p(
                    "No hay entradas en la bitácora que coincidan con los filtros.",
                    class_name="text-gray-500 text-center py-10",
                ),
            ),
            class_name="max-h-[calc(100vh-220px)] overflow-y-auto mt-4",
        ),
        class_name="p-6",
    )


def bitacora_page() -> rx.Component:
    return main_layout(bitacora_general_content())