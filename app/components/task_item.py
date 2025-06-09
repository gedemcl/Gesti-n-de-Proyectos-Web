import reflex as rx
from app.states.project_state import ProjectState
from app.models import Task as TaskType, VALID_STATUSES
from app.components.priority_badge import priority_badge
from app.components.status_badge import status_badge


def task_item(task: TaskType) -> rx.Component:
    task_id = task["id"]
    static_base_class = "p-3 rounded-md shadow-sm border"
    overdue_class = (
        f"{static_base_class} bg-red-50 border-red-200"
    )
    due_soon_class = f"{static_base_class} bg-yellow-50 border-yellow-200"
    default_class = (
        f"{static_base_class} bg-white border-gray-200"
    )
    item_classes = rx.cond(
        task["is_overdue"],
        overdue_class,
        rx.cond(
            task["is_due_soon"],
            due_soon_class,
            default_class,
        ),
    )
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.p(
                    task["description"],
                    class_name="text-gray-800 font-medium",
                ),
                rx.el.p(
                    f"Vence: {task['due_date']}",
                    class_name="text-xs text-gray-500 mt-1",
                ),
                rx.cond(
                    task["is_overdue"],
                    rx.el.span(
                        "VENCIDA",
                        class_name="text-xs font-bold text-red-500",
                    ),
                    rx.cond(
                        task["is_due_soon"],
                        rx.el.span(
                            "VENCE PRONTO",
                            class_name="text-xs font-bold text-yellow-500",
                        ),
                        rx.el.span(""),
                    ),
                ),
                class_name="flex-grow",
            ),
            rx.el.div(
                priority_badge(task["priority"]),
                status_badge(task["status"]),
                class_name="flex items-center space-x-2",
            ),
            class_name="flex justify-between items-start",
        ),
        rx.el.div(
            rx.el.select(
                rx.foreach(
                    VALID_STATUSES,
                    lambda s: rx.el.option(
                        s.capitalize(), value=s
                    ),
                ),
                value=task["status"],
                on_change=lambda new_status: ProjectState.change_task_status(
                    task_id, new_status
                ),
                class_name="text-xs p-1 border border-gray-300 rounded-md focus:ring-indigo-500 focus:border-indigo-500",
            ),
            rx.el.button(
                rx.el.i(class_name="fas fa-edit"),
                on_click=lambda: ProjectState.toggle_task_form_dialog(
                    task_id
                ),
                class_name="p-1 text-xs text-blue-500 hover:text-blue-700",
            ),
            rx.el.button(
                rx.el.i(class_name="fas fa-trash-alt"),
                on_click=lambda: ProjectState.delete_task(
                    task_id
                ),
                class_name="p-1 text-xs text-red-500 hover:text-red-700",
            ),
            class_name="flex items-center space-x-2 mt-2 pt-2 border-t border-gray-200",
        ),
        class_name=item_classes,
        key=task_id,
    )