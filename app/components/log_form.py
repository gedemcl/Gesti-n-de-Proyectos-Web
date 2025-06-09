import reflex as rx
from app.states.project_state import ProjectState


def log_form() -> rx.Component:
    return rx.el.dialog(
        rx.el.div(
            rx.el.form(
                rx.el.h3(
                    "Añadir Entrada de Bitácora",
                    class_name="text-xl font-semibold mb-4 text-gray-800",
                ),
                rx.el.label(
                    "Descripción de la Acción",
                    html_for="log_action_description",
                    class_name="text-sm font-medium text-gray-700",
                ),
                rx.el.textarea(
                    name="action",
                    id="log_action_description",
                    placeholder="Describe la acción realizada o el evento ocurrido",
                    class_name="w-full p-2 mt-1 mb-4 border border-gray-300 rounded-md focus:ring-indigo-500 focus:border-indigo-500 h-24",
                ),
                rx.el.div(
                    rx.el.button(
                        "Cancelar",
                        type="button",
                        on_click=ProjectState.toggle_log_form_dialog,
                        class_name="px-4 py-2 text-sm font-medium text-gray-700 bg-gray-100 rounded-md hover:bg-gray-200 transition-colors",
                    ),
                    rx.el.button(
                        "Añadir Entrada",
                        type="submit",
                        class_name="px-4 py-2 ml-2 text-sm font-medium text-white bg-indigo-600 rounded-md hover:bg-indigo-700 transition-colors",
                    ),
                    class_name="flex justify-end mt-4",
                ),
                on_submit=ProjectState.add_manual_log_entry,
                reset_on_submit=True,
                class_name="bg-white p-6 rounded-lg shadow-xl w-full max-w-md",
            ),
            class_name="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 p-4 z-50",
        ),
        open=ProjectState.show_log_form_dialog,
    )