import reflex as rx
from app.states.project_state import ProjectState
from app.models import (
    VALID_PRIORITIES,
    VALID_STATUSES,
    Task as TaskType,
)


def task_form() -> rx.Component:
    return rx.el.dialog(
        rx.el.div(
            rx.el.form(
                rx.el.h3(
                    rx.cond(
                        ProjectState.editing_task_id
                        != None,
                        "Editar Tarea",
                        "Añadir Nueva Tarea",
                    ),
                    class_name="text-xl font-semibold mb-4 text-gray-800",
                ),
                rx.el.label(
                    "Descripción",
                    html_for="task_description",
                    class_name="text-sm font-medium text-gray-700",
                ),
                rx.el.textarea(
                    name="description",
                    id="task_description",
                    default_value=rx.cond(
                        ProjectState.task_to_edit,
                        ProjectState.task_to_edit[
                            "description"
                        ],
                        "",
                    ),
                    key=rx.cond(
                        ProjectState.editing_task_id
                        != None,
                        ProjectState.editing_task_id.to_string()
                        + "-desc",
                        "new-task-desc",
                    ),
                    placeholder="Introduce la descripción de la tarea",
                    class_name="w-full p-2 mt-1 mb-3 border border-gray-300 rounded-md focus:ring-indigo-500 focus:border-indigo-500 h-24",
                ),
                rx.el.label(
                    "Fecha Límite",
                    html_for="task_due_date",
                    class_name="text-sm font-medium text-gray-700",
                ),
                rx.el.input(
                    name="due_date",
                    id="task_due_date",
                    type="date",
                    default_value=rx.cond(
                        ProjectState.task_to_edit,
                        ProjectState.task_to_edit[
                            "due_date"
                        ],
                        "",
                    ),
                    key=rx.cond(
                        ProjectState.editing_task_id
                        != None,
                        ProjectState.editing_task_id.to_string()
                        + "-due_date",
                        "new-task-due_date",
                    ),
                    class_name="w-full p-2 mt-1 mb-3 border border-gray-300 rounded-md focus:ring-indigo-500 focus:border-indigo-500",
                ),
                rx.el.label(
                    "Prioridad",
                    html_for="task_priority",
                    class_name="text-sm font-medium text-gray-700",
                ),
                rx.el.select(
                    rx.foreach(
                        VALID_PRIORITIES,
                        lambda p: rx.el.option(
                            p.capitalize(), value=p
                        ),
                    ),
                    name="priority",
                    id="task_priority",
                    default_value=rx.cond(
                        ProjectState.task_to_edit,
                        ProjectState.task_to_edit[
                            "priority"
                        ],
                        VALID_PRIORITIES[2],
                    ),
                    key=rx.cond(
                        ProjectState.editing_task_id
                        != None,
                        ProjectState.editing_task_id.to_string()
                        + "-priority",
                        "new-task-priority",
                    ),
                    class_name="w-full p-2 mt-1 mb-3 border border-gray-300 rounded-md focus:ring-indigo-500 focus:border-indigo-500",
                ),
                rx.el.label(
                    "Estado",
                    html_for="task_status",
                    class_name="text-sm font-medium text-gray-700",
                ),
                rx.el.select(
                    rx.foreach(
                        VALID_STATUSES,
                        lambda s: rx.el.option(
                            s.capitalize(), value=s
                        ),
                    ),
                    name="status",
                    id="task_status",
                    default_value=rx.cond(
                        ProjectState.task_to_edit,
                        ProjectState.task_to_edit["status"],
                        VALID_STATUSES[0],
                    ),
                    key=rx.cond(
                        ProjectState.editing_task_id
                        != None,
                        ProjectState.editing_task_id.to_string()
                        + "-status",
                        "new-task-status",
                    ),
                    class_name="w-full p-2 mt-1 mb-4 border border-gray-300 rounded-md focus:ring-indigo-500 focus:border-indigo-500",
                ),
                rx.el.div(
                    rx.el.button(
                        "Cancelar",
                        type="button",
                        on_click=ProjectState.toggle_task_form_dialog,
                        class_name="px-4 py-2 text-sm font-medium text-gray-700 bg-gray-100 rounded-md hover:bg-gray-200 transition-colors",
                    ),
                    rx.el.button(
                        "Guardar Tarea",
                        type="submit",
                        class_name="px-4 py-2 ml-2 text-sm font-medium text-white bg-indigo-600 rounded-md hover:bg-indigo-700 transition-colors",
                    ),
                    class_name="flex justify-end mt-4",
                ),
                on_submit=ProjectState.save_task,
                reset_on_submit=True,
                class_name="bg-white p-6 rounded-lg shadow-xl w-full max-w-md",
            ),
            class_name="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 p-4 z-50",
        ),
        open=ProjectState.show_task_form_dialog,
    )