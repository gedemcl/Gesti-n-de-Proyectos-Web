import reflex as rx
from app.states.project_state import ProjectState
from app.components.project_form import project_form
from app.components.task_item import task_item
from app.components.task_form import task_form
from app.components.log_entry_item import log_entry_item
from app.components.log_form import log_form
from app.components.main_layout import main_layout


def proyecto_detail_page_content() -> rx.Component:
    return rx.el.div(
        project_form(),
        task_form(),
        log_form(),
        rx.el.a(
            rx.el.i(class_name="fas fa-arrow-left mr-2"),
            "Volver a Proyectos",
            href="/proyectos",
            class_name="mb-6 inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-indigo-700 bg-indigo-100 hover:bg-indigo-200",
        ),
        rx.cond(
            ProjectState.selected_project,
            rx.el.div(
                rx.el.div(
                    rx.el.h2(
                        ProjectState.selected_project[
                            "name"
                        ],
                        class_name="text-3xl font-bold text-gray-800",
                    ),
                    rx.el.div(
                        rx.cond(
                            ProjectState.selected_project[
                                "is_overdue"
                            ],
                            rx.el.span(
                                rx.el.i(
                                    class_name="fas fa-exclamation-circle text-red-500 mr-1"
                                ),
                                "VENCIDO",
                                class_name="text-sm font-bold text-red-600 px-2 py-1 bg-red-100 rounded-full mr-2",
                            ),
                            rx.el.span(),
                        ),
                        rx.cond(
                            ProjectState.selected_project[
                                "is_due_soon"
                            ],
                            rx.el.span(
                                rx.el.i(
                                    class_name="fas fa-exclamation-triangle text-yellow-500 mr-1"
                                ),
                                "VENCE PRONTO",
                                class_name="text-sm font-bold text-yellow-600 px-2 py-1 bg-yellow-100 rounded-full mr-2",
                            ),
                            rx.el.span(),
                        ),
                        rx.el.button(
                            rx.el.i(
                                class_name="fas fa-edit mr-1"
                            ),
                            "Editar Proyecto",
                            on_click=lambda: ProjectState.toggle_project_form_dialog(
                                ProjectState.selected_project_id
                            ),
                            class_name="px-3 py-1.5 text-sm bg-blue-500 text-white rounded-md hover:bg-blue-600 transition-colors flex items-center",
                        ),
                        rx.el.button(
                            rx.el.i(
                                class_name="fas fa-trash-alt mr-1"
                            ),
                            "Eliminar Proyecto",
                            on_click=lambda: ProjectState.delete_project(
                                ProjectState.selected_project_id
                            ),
                            class_name="ml-2 px-3 py-1.5 text-sm bg-red-500 text-white rounded-md hover:bg-red-600 transition-colors flex items-center",
                        ),
                        class_name="flex items-center",
                    ),
                    class_name="flex justify-between items-center mb-6 pb-4 border-b border-gray-200",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.h3(
                            "Detalles del Proyecto",
                            class_name="text-xl font-semibold text-gray-700 mb-3",
                        ),
                        rx.el.p(
                            f"Responsable: {ProjectState.selected_project['responsible']}",
                            class_name="text-md text-gray-700 mb-1",
                        ),
                        rx.el.p(
                            "Temática: ",
                            rx.el.span(
                                ProjectState.selected_project[
                                    "category_name"
                                ],
                                class_name="font-semibold",
                            ),
                            class_name="text-md text-gray-700 mb-1",
                        ),
                        rx.el.div(
                            rx.el.span("Estado: "),
                            rx.el.span(
                                ProjectState.selected_project[
                                    "status"
                                ],
                                class_name="capitalize",
                            ),
                            class_name="text-md text-gray-700 mb-1",
                        ),
                        rx.el.p(
                            f"Fecha de Inicio: {ProjectState.selected_project['start_date']}",
                            class_name="text-md text-gray-700 mb-1",
                        ),
                        rx.el.p(
                            f"Fecha Límite: {ProjectState.selected_project['due_date']}",
                            class_name="text-md text-gray-700 mb-1",
                        ),
                        rx.el.h4(
                            "Descripción:",
                            class_name="text-md font-semibold text-gray-700 mt-3 mb-1",
                        ),
                        rx.el.p(
                            ProjectState.selected_project[
                                "description"
                            ],
                            class_name="text-md text-gray-600 mb-4 italic bg-gray-50 p-3 rounded-md",
                        ),
                        class_name="bg-white p-6 rounded-lg shadow-md mb-6 md:mb-0",
                    ),
                    rx.el.div(
                        rx.el.div(
                            rx.el.div(
                                rx.el.h3(
                                    "Tareas del Proyecto",
                                    class_name="text-xl font-semibold text-gray-700",
                                ),
                                rx.el.button(
                                    rx.el.i(
                                        class_name="fas fa-plus mr-1"
                                    ),
                                    "Añadir Tarea",
                                    on_click=lambda: ProjectState.toggle_task_form_dialog(
                                        None
                                    ),
                                    class_name="px-3 py-1.5 text-sm bg-green-500 text-white rounded-md hover:bg-green-600 transition-colors flex items-center",
                                ),
                                class_name="flex justify-between items-center mb-3",
                            ),
                            rx.el.div(
                                rx.cond(
                                    ProjectState.tasks_for_selected_project.length()
                                    > 0,
                                    rx.el.div(
                                        rx.foreach(
                                            ProjectState.tasks_for_selected_project,
                                            task_item,
                                        ),
                                        class_name="space-y-3",
                                    ),
                                    rx.el.p(
                                        "Aún no hay tareas para este proyecto.",
                                        class_name="text-sm text-gray-500 py-4 text-center",
                                    ),
                                ),
                                class_name="bg-gray-50 p-4 rounded-lg max-h-96 overflow-y-auto",
                            ),
                            class_name="mb-6",
                        ),
                        rx.el.div(
                            rx.el.div(
                                rx.el.h3(
                                    "Bitácora del Proyecto",
                                    class_name="text-xl font-semibold text-gray-700",
                                ),
                                rx.el.button(
                                    rx.el.i(
                                        class_name="fas fa-book mr-1"
                                    ),
                                    "Añadir Entrada Manual",
                                    on_click=ProjectState.toggle_log_form_dialog,
                                    class_name="px-3 py-1.5 text-sm bg-purple-500 text-white rounded-md hover:bg-purple-600 transition-colors flex items-center",
                                ),
                                class_name="flex justify-between items-center mb-3",
                            ),
                            rx.el.div(
                                rx.cond(
                                    ProjectState.logs_for_selected_project.length()
                                    > 0,
                                    rx.el.div(
                                        rx.foreach(
                                            ProjectState.logs_for_selected_project,
                                            log_entry_item,
                                        ),
                                        class_name="divide-y divide-gray-100",
                                    ),
                                    rx.el.p(
                                        "Aún no hay entradas de bitácora para este proyecto.",
                                        class_name="text-sm text-gray-500 py-4 text-center",
                                    ),
                                ),
                                class_name="bg-gray-50 p-4 rounded-lg max-h-96 overflow-y-auto",
                            ),
                        ),
                    ),
                    class_name="grid md:grid-cols-2 gap-6",
                ),
                class_name="p-6 bg-white rounded-lg shadow-xl overflow-y-auto flex-1",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.i(
                        class_name="fas fa-spinner fa-spin text-5xl text-gray-400 mb-4"
                    ),
                    rx.el.p(
                        "Cargando detalles del proyecto...",
                        class_name="text-gray-500 text-center text-lg",
                    ),
                    class_name="flex flex-col items-center justify-center h-full p-10",
                )
            ),
        ),
        class_name="p-6 flex flex-col h-full bg-gray-100",
    )


def proyecto_detail_page() -> rx.Component:
    return main_layout(proyecto_detail_page_content())