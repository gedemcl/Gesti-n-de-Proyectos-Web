import reflex as rx
from app.states.project_state import ProjectState
from app.models import (
    VALID_PROJECT_STATUSES,
    Project as ProjectType,
)
from typing import cast


def project_form() -> rx.Component:
    return rx.el.dialog(
        rx.el.div(
            rx.el.form(
                rx.el.h3(
                    rx.cond(
                        ProjectState.editing_project_id
                        != None,
                        "Editar Proyecto",
                        "Añadir Nuevo Proyecto",
                    ),
                    class_name="text-xl font-semibold mb-6 text-gray-800",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.label(
                            "Nombre del Proyecto*",
                            html_for="name",
                            class_name="text-sm font-medium text-gray-700",
                        ),
                        rx.el.input(
                            name="name",
                            id="name",
                            default_value=rx.cond(
                                ProjectState.project_to_edit,
                                ProjectState.project_to_edit[
                                    "name"
                                ],
                                "",
                            ),
                            key=rx.cond(
                                ProjectState.editing_project_id
                                != None,
                                ProjectState.editing_project_id.to_string()
                                + "-name",
                                "new-project-name",
                            ),
                            placeholder="Ej: Implementación Sistema de Alertas",
                            class_name="w-full p-2 mt-1 border border-gray-300 rounded-md focus:ring-indigo-500 focus:border-indigo-500",
                            required=True,
                        ),
                        class_name="w-full md:w-1/2 px-2 mb-4",
                    ),
                    rx.el.div(
                        rx.el.label(
                            "Responsable*",
                            html_for="responsible",
                            class_name="text-sm font-medium text-gray-700",
                        ),
                        rx.el.input(
                            name="responsible",
                            id="responsible",
                            default_value=rx.cond(
                                ProjectState.project_to_edit,
                                ProjectState.project_to_edit[
                                    "responsible"
                                ],
                                "",
                            ),
                            key=rx.cond(
                                ProjectState.editing_project_id
                                != None,
                                ProjectState.editing_project_id.to_string()
                                + "-responsible",
                                "new-project-responsible",
                            ),
                            placeholder="Ej: Juan Pérez (autocompletar)",
                            class_name="w-full p-2 mt-1 border border-gray-300 rounded-md focus:ring-indigo-500 focus:border-indigo-500",
                            required=True,
                        ),
                        class_name="w-full md:w-1/2 px-2 mb-4",
                    ),
                    class_name="flex flex-wrap -mx-2",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.label(
                            "Fecha de Inicio*",
                            html_for="start_date",
                            class_name="text-sm font-medium text-gray-700",
                        ),
                        rx.el.input(
                            name="start_date",
                            id="start_date",
                            type="date",
                            default_value=rx.cond(
                                ProjectState.project_to_edit,
                                ProjectState.project_to_edit[
                                    "start_date"
                                ],
                                "",
                            ),
                            key=rx.cond(
                                ProjectState.editing_project_id
                                != None,
                                ProjectState.editing_project_id.to_string()
                                + "-start_date",
                                "new-project-start_date",
                            ),
                            class_name="w-full p-2 mt-1 border border-gray-300 rounded-md focus:ring-indigo-500 focus:border-indigo-500",
                            required=True,
                        ),
                        class_name="w-full md:w-1/2 px-2 mb-4",
                    ),
                    rx.el.div(
                        rx.el.label(
                            "Fecha Límite*",
                            html_for="due_date",
                            class_name="text-sm font-medium text-gray-700",
                        ),
                        rx.el.input(
                            name="due_date",
                            id="due_date",
                            type="date",
                            default_value=rx.cond(
                                ProjectState.project_to_edit,
                                ProjectState.project_to_edit[
                                    "due_date"
                                ],
                                "",
                            ),
                            key=rx.cond(
                                ProjectState.editing_project_id
                                != None,
                                ProjectState.editing_project_id.to_string()
                                + "-due_date",
                                "new-project-due_date",
                            ),
                            class_name="w-full p-2 mt-1 border border-gray-300 rounded-md focus:ring-indigo-500 focus:border-indigo-500",
                            required=True,
                        ),
                        class_name="w-full md:w-1/2 px-2 mb-4",
                    ),
                    class_name="flex flex-wrap -mx-2",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.label(
                            "Estado del Proyecto*",
                            html_for="status",
                            class_name="text-sm font-medium text-gray-700",
                        ),
                        rx.el.select(
                            rx.foreach(
                                VALID_PROJECT_STATUSES,
                                lambda s: rx.el.option(
                                    s.capitalize(), value=s
                                ),
                            ),
                            name="status",
                            id="status",
                            default_value=rx.cond(
                                ProjectState.project_to_edit,
                                ProjectState.project_to_edit[
                                    "status"
                                ],
                                VALID_PROJECT_STATUSES[0],
                            ),
                            key=rx.cond(
                                ProjectState.editing_project_id
                                != None,
                                ProjectState.editing_project_id.to_string()
                                + "-status",
                                "new-project-status",
                            ),
                            class_name="w-full p-2 mt-1 border border-gray-300 rounded-md focus:ring-indigo-500 focus:border-indigo-500",
                            required=True,
                        ),
                        class_name="w-full px-2 mb-4",
                    ),
                    class_name="flex flex-wrap -mx-2",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.label(
                            "Descripción del Proyecto",
                            html_for="description",
                            class_name="text-sm font-medium text-gray-700",
                        ),
                        rx.el.textarea(
                            name="description",
                            id="description",
                            default_value=rx.cond(
                                ProjectState.project_to_edit,
                                ProjectState.project_to_edit[
                                    "description"
                                ],
                                "",
                            ),
                            key=rx.cond(
                                ProjectState.editing_project_id
                                != None,
                                ProjectState.editing_project_id.to_string()
                                + "-description",
                                "new-project-description",
                            ),
                            placeholder="Breve descripción de los objetivos y alcance del proyecto.",
                            class_name="w-full p-2 mt-1 border border-gray-300 rounded-md focus:ring-indigo-500 focus:border-indigo-500 h-24",
                        ),
                        class_name="w-full px-2 mb-4",
                    ),
                    class_name="flex flex-wrap -mx-2",
                ),
                rx.cond(
                    ~(
                        ProjectState.editing_project_id
                        != None
                    ),
                    rx.el.div(
                        rx.el.h4(
                            "Añadir Tarea Inicial (Opcional)",
                            class_name="text-md font-semibold text-gray-700 mb-2 px-2",
                        ),
                        rx.el.div(
                            rx.el.label(
                                "Descripción de la Tarea",
                                html_for="new_task_description",
                                class_name="text-sm font-medium text-gray-700",
                            ),
                            rx.el.input(
                                name="new_task_description",
                                id="new_task_description",
                                placeholder="Ej: Definir alcance inicial del proyecto",
                                class_name="w-full p-2 mt-1 border border-gray-300 rounded-md focus:ring-indigo-500 focus:border-indigo-500",
                            ),
                            class_name="w-full md:w-2/3 px-2 mb-4",
                        ),
                        rx.el.div(
                            rx.el.label(
                                "Fecha Límite Tarea",
                                html_for="new_task_due_date",
                                class_name="text-sm font-medium text-gray-700",
                            ),
                            rx.el.input(
                                name="new_task_due_date",
                                id="new_task_due_date",
                                type="date",
                                class_name="w-full p-2 mt-1 border border-gray-300 rounded-md focus:ring-indigo-500 focus:border-indigo-500",
                            ),
                            class_name="w-full md:w-1/3 px-2 mb-4",
                        ),
                        class_name="flex flex-wrap -mx-2 border-t border-gray-200 pt-4 mt-4",
                    ),
                    rx.el.span(),
                ),
                rx.el.div(
                    rx.el.button(
                        "Cancelar",
                        type="button",
                        on_click=ProjectState.toggle_project_form_dialog,
                        class_name="px-4 py-2 text-sm font-medium text-gray-700 bg-gray-100 rounded-md hover:bg-gray-200 transition-colors",
                    ),
                    rx.el.button(
                        rx.cond(
                            ProjectState.editing_project_id
                            != None,
                            "Guardar Cambios",
                            "Crear Proyecto",
                        ),
                        type="submit",
                        class_name="px-4 py-2 ml-2 text-sm font-medium text-white bg-indigo-600 rounded-md hover:bg-indigo-700 transition-colors",
                    ),
                    class_name="flex justify-end mt-6",
                ),
                on_submit=ProjectState.save_project,
                reset_on_submit=True,
                class_name="bg-white p-6 rounded-lg shadow-xl w-full max-w-2xl",
            ),
            class_name="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 p-4 overflow-y-auto z-50",
        ),
        open=ProjectState.show_project_form_dialog,
    )