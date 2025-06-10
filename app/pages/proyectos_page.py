import reflex as rx
from app.states.project_state import ProjectState
from app.components.project_card import project_card
from app.components.project_form import project_form
from app.models import VALID_PROJECT_STATUSES
from app.components.main_layout import main_layout


def project_filters() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.label(
                "Estado:",
                html_for="project_filter_status",
                class_name="text-sm font-medium text-gray-700 mr-2",
            ),
            rx.el.select(
                rx.el.option("Todos", value="todos"),
                rx.foreach(
                    VALID_PROJECT_STATUSES,
                    lambda s: rx.el.option(
                        s.capitalize(), value=s
                    ),
                ),
                id="project_filter_status",
                value=ProjectState.filter_status,
                on_change=ProjectState.set_filter_status,
                class_name="p-2 border border-gray-300 rounded-md focus:ring-indigo-500 focus:border-indigo-500 text-sm",
            ),
            class_name="flex items-center",
        ),
        rx.el.div(
            rx.el.label(
                "Fecha Término (hasta):",
                html_for="project_filter_due_date",
                class_name="text-sm font-medium text-gray-700 mr-2",
            ),
            rx.el.input(
                id="project_filter_due_date",
                type="date",
                default_value=ProjectState.filter_due_date,
                on_change=ProjectState.set_filter_due_date,
                class_name="p-2 border border-gray-300 rounded-md focus:ring-indigo-500 focus:border-indigo-500 text-sm",
            ),
            class_name="flex items-center",
        ),
        rx.el.div(
            rx.el.label(
                "Responsable:",
                html_for="project_filter_responsible",
                class_name="text-sm font-medium text-gray-700 mr-2",
            ),
            rx.el.input(
                id="project_filter_responsible",
                placeholder="Nombre del responsable",
                default_value=ProjectState.filter_responsible,
                on_change=ProjectState.set_filter_responsible.debounce(
                    300
                ),
                class_name="p-2 border border-gray-300 rounded-md focus:ring-indigo-500 focus:border-indigo-500 text-sm",
            ),
            class_name="flex items-center",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.input(
                    type="checkbox",
                    id="due_soon_filter",
                    checked=ProjectState.filter_is_due_soon,
                    on_change=ProjectState.set_filter_is_due_soon,
                    class_name="mr-2",
                ),
                rx.el.label(
                    "Vence Pronto",
                    html_for="due_soon_filter",
                ),
                class_name="flex items-center",
            ),
            rx.el.div(
                rx.el.input(
                    type="checkbox",
                    id="overdue_filter",
                    checked=ProjectState.filter_is_overdue,
                    on_change=ProjectState.set_filter_is_overdue,
                    class_name="mr-2",
                ),
                rx.el.label(
                    "Vencido", html_for="overdue_filter"
                ),
                class_name="flex items-center",
            ),
            class_name="flex items-center space-x-4",
        ),
        rx.el.button(
            "Limpiar Filtros",
            on_click=ProjectState.clear_filters,
            class_name="px-3 py-2 bg-gray-200 text-gray-700 font-semibold rounded-md hover:bg-gray-300 transition-colors text-sm",
        ),
        class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4 mb-6 p-4 border-y border-gray-200 bg-gray-50 items-end",
    )


def proyectos_page_content() -> rx.Component:
    return rx.el.div(
        project_form(),
        rx.el.div(
            rx.el.h1(
                "Gestión de Proyectos",
                class_name="text-3xl font-bold text-gray-800",
            ),
            rx.el.button(
                rx.el.i(class_name="fas fa-plus mr-2"),
                "Añadir Nuevo Proyecto",
                on_click=lambda: ProjectState.toggle_project_form_dialog(
                    None
                ),
                class_name="px-4 py-2 bg-indigo-600 text-white font-semibold rounded-md shadow-md hover:bg-indigo-700 transition-colors flex items-center",
            ),
            class_name="flex justify-between items-center p-6 border-b border-gray-200 bg-white",
        ),
        rx.el.div(
            rx.el.input(
                placeholder="Buscar por nombre, responsable...",
                on_change=ProjectState.set_search_term.debounce(
                    300
                ),
                class_name="w-full p-3 mb-6 border border-gray-300 rounded-md focus:ring-indigo-500 focus:border-indigo-500",
                default_value=ProjectState.search_term,
            ),
            project_filters(),
            rx.el.div(
                rx.cond(
                    ProjectState.filtered_project_list.length()
                    > 0,
                    rx.el.div(
                        rx.foreach(
                            ProjectState.filtered_project_list,
                            project_card,
                        ),
                        class_name="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6",
                    ),
                    rx.el.p(
                        rx.cond(
                            (ProjectState.search_term != "")
                            | (
                                ProjectState.filter_status
                                != "todos"
                            )
                            | (
                                ProjectState.filter_due_date
                                != ""
                            )
                            | (
                                ProjectState.filter_responsible
                                != ""
                            ),
                            "No se encontraron proyectos que coincidan.",
                            "Aún no hay proyectos.",
                        ),
                        class_name="text-center text-gray-500 py-10",
                    ),
                ),
                class_name="flex-1 overflow-y-auto",
            ),
            class_name="p-6 bg-gray-50 flex-1 flex flex-col",
        ),
        class_name="flex flex-col h-full",
    )


def proyectos_page() -> rx.Component:
    return main_layout(proyectos_page_content())