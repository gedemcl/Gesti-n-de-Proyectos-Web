import reflex as rx
from app.components.main_layout import main_layout


def ayuda_page_content() -> rx.Component:
    return rx.el.div(
        rx.el.h1(
            "Ayuda y Contacto Técnico",
            class_name="text-3xl font-bold text-gray-800 mb-6",
        ),
        rx.el.div(
            rx.el.h2(
                "Preguntas Frecuentes (FAQ)",
                class_name="text-xl font-semibold text-gray-700 mb-3",
            ),
            rx.el.div(
                rx.el.h3(
                    "¿Cómo creo un nuevo proyecto?",
                    class_name="font-medium text-gray-700",
                ),
                rx.el.p(
                    "Diríjase a la sección 'Proyectos' y haga clic en el botón '+ Añadir Nuevo Proyecto'. Complete el formulario con los detalles requeridos.",
                    class_name="text-gray-600 mb-3",
                ),
                rx.el.h3(
                    "¿Cómo gestiono las tareas de un proyecto?",
                    class_name="font-medium text-gray-700",
                ),
                rx.el.p(
                    "Seleccione un proyecto de la lista en la sección 'Proyectos'. En el panel de detalles del proyecto, encontrará la sección de 'Tareas' donde podrá añadir, editar, eliminar y cambiar el estado de las tareas.",
                    class_name="text-gray-600 mb-3",
                ),
                rx.el.h3(
                    "¿Qué es la bitácora?",
                    class_name="font-medium text-gray-700",
                ),
                rx.el.p(
                    "La bitácora registra automáticamente las acciones importantes realizadas en los proyectos (creación, edición, eliminación de proyectos/tareas). También puede añadir entradas manuales para un seguimiento detallado.",
                    class_name="text-gray-600 mb-3",
                ),
                class_name="space-y-4",
            ),
            class_name="bg-white p-6 rounded-lg shadow mb-8",
        ),
        rx.el.div(
            rx.el.h2(
                "Contacto Técnico",
                class_name="text-xl font-semibold text-gray-700 mb-3",
            ),
            rx.el.p(
                "Si necesita asistencia técnica o tiene alguna consulta, por favor contacte a:",
                class_name="text-gray-600",
            ),
            rx.el.ul(
                rx.el.li("Departamento de Informática"),
                rx.el.li(
                    "Correo: soporte.ti@municipalidadarica.cl"
                ),
                rx.el.li("Teléfono: (Por definir)"),
                class_name="list-disc list-inside text-gray-600 space-y-1 mt-2",
            ),
            class_name="bg-white p-6 rounded-lg shadow",
        ),
        class_name="p-6",
    )


def ayuda_page() -> rx.Component:
    return main_layout(ayuda_page_content())