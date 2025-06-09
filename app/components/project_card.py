import reflex as rx
from app.states.project_state import ProjectState
from app.models import Project as ProjectType


def project_card(project: ProjectType) -> rx.Component:
    static_base_class = "rounded-lg shadow-md transition-all duration-150 flex flex-col border"
    overdue_class = f"{static_base_class} bg-red-50 border-red-300 hover:bg-red-100"
    due_soon_class = f"{static_base_class} bg-yellow-50 border-yellow-300 hover:bg-yellow-100"
    default_class = f"{static_base_class} bg-white border-gray-200 hover:bg-gray-50"
    card_classes = rx.cond(
        project["is_overdue"],
        overdue_class,
        rx.cond(
            project["is_due_soon"],
            due_soon_class,
            default_class,
        ),
    )
    return rx.el.div(
        rx.el.div(
            rx.el.h3(
                project["name"],
                class_name="text-lg font-semibold text-indigo-700 truncate",
            ),
            rx.el.p(
                f"Responsable: {project['responsible']}",
                class_name="text-sm text-gray-600",
            ),
            rx.el.p(
                f"Inicio: {project['start_date']}",
                class_name="text-xs text-gray-500",
            ),
            rx.el.p(
                f"Vence: {project['due_date']}",
                class_name="text-xs text-gray-500",
            ),
            rx.cond(
                project["is_overdue"],
                rx.el.span(
                    "VENCIDO",
                    class_name="text-xs font-bold text-red-600 mt-1 inline-block",
                ),
                rx.cond(
                    project["is_due_soon"],
                    rx.el.span(
                        "VENCE PRONTO",
                        class_name="text-xs font-bold text-yellow-600 mt-1 inline-block",
                    ),
                    rx.el.span(""),
                ),
            ),
            class_name="flex-grow cursor-pointer p-4",
            on_click=lambda: rx.redirect(
                f"/proyectos/{project['id']}"
            ),
        ),
        rx.el.div(
            rx.el.button(
                rx.el.i(class_name="fas fa-edit"),
                on_click=lambda: ProjectState.toggle_project_form_dialog(
                    project["id"]
                ),
                class_name="p-2 text-sm text-blue-600 hover:text-blue-800 transition-colors",
            ),
            rx.el.button(
                rx.el.i(class_name="fas fa-trash-alt"),
                on_click=lambda: ProjectState.delete_project(
                    project["id"]
                ),
                class_name="p-2 text-sm text-red-600 hover:text-red-800 transition-colors",
            ),
            class_name="p-2 border-t border-gray-200 flex justify-end items-center",
        ),
        class_name=card_classes,
        key=project["id"],
    )