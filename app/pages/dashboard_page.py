import reflex as rx
from app.components.main_layout import main_layout
from app.states.project_state import ProjectState
from app.models import VALID_PROJECT_STATUSES
from app.constants import RECHARTS_TOOLTIP_STYLE_CLASS_NAME


def status_summary_card(
    status_display: str,
    count: rx.Var[int] | int,
    color_class: str,
    status_filter: str = "todos",
) -> rx.Component:
    return rx.el.div(
        rx.el.h3(
            status_display,
            class_name="text-lg font-semibold text-gray-700",
        ),
        rx.el.p(
            count.to_string(),
            class_name=f"text-4xl font-bold {color_class}",
        ),
        class_name=rx.cond(
            status_filter != "todos",
            "bg-white p-6 rounded-lg shadow-md text-center cursor-pointer hover:scale-105 transition-transform",
            "bg-white p-6 rounded-lg shadow-md text-center",
        ),
        on_click=rx.cond(
            status_filter != "todos",
            ProjectState.filter_by_status_and_redirect(
                status_filter
            ),
            None,
        ),
    )


def dashboard_content() -> rx.Component:
    return rx.el.div(
        rx.el.h1(
            "Dashboard General",
            class_name="text-3xl font-bold text-gray-800 mb-6",
        ),
        rx.el.div(
            status_summary_card(
                "Total Proyectos",
                ProjectState.total_projects_count,
                "text-indigo-600",
            ),
            status_summary_card(
                "En Idea",
                ProjectState.projects_idea_count,
                "text-blue-500",
                "idea",
            ),
            status_summary_card(
                "En Diseño",
                ProjectState.projects_diseno_count,
                "text-purple-500",
                "diseño",
            ),
            status_summary_card(
                "En Ejecución",
                ProjectState.projects_ejecucion_count,
                "text-yellow-500",
                "ejecución",
            ),
            status_summary_card(
                "Finalizados",
                ProjectState.projects_finalizado_count,
                "text-green-500",
                "finalizado",
            ),
            status_summary_card(
                "Vencen Pronto (<7 días)",
                ProjectState.projects_due_soon_count,
                "text-orange-500",
            ),
            status_summary_card(
                "Vencidos",
                ProjectState.projects_overdue_count,
                "text-red-600",
            ),
            class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.h3(
                    "Proyectos por Responsable",
                    class_name="text-xl font-semibold text-gray-700 mb-4",
                ),
                rx.recharts.bar_chart(
                    rx.recharts.cartesian_grid(
                        horizontal=True,
                        vertical=False,
                        class_name="opacity-25",
                    ),
                    rx.recharts.graphing_tooltip(
                        class_name=RECHARTS_TOOLTIP_STYLE_CLASS_NAME
                    ),
                    rx.recharts.x_axis(
                        data_key="name",
                        type_="category",
                        axis_line=False,
                        tick_line=False,
                        custom_attrs={"fontSize": "12px"},
                    ),
                    rx.recharts.y_axis(
                        rx.recharts.label(
                            value="Nº Proyectos",
                            position="left",
                            custom_attrs={
                                "angle": 270,
                                "fontSize": "12px",
                                "fontWeight": "700",
                            },
                        ),
                        allow_decimals=False,
                        axis_line=False,
                        tick_line=False,
                        custom_attrs={"fontSize": "12px"},
                    ),
                    rx.recharts.bar(
                        data_key="projects",
                        fill="#005BBB",
                        radius=[4, 4, 0, 0],
                        name="Proyectos",
                    ),
                    rx.recharts.legend(
                        height=0,
                        layout="horizontal",
                        align="right",
                        icon_size=10,
                        icon_type="square",
                    ),
                    data=ProjectState.projects_by_responsible_data,
                    height=300,
                    bar_size=35,
                    margin={
                        "left": 20,
                        "right": 20,
                        "top": 5,
                        "bottom": 20,
                    },
                    width="100%",
                ),
                class_name="bg-white p-4 rounded-lg shadow w-full",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.h3(
                        "Proyectos por Estado",
                        class_name="text-xl font-semibold text-gray-700 mb-2",
                    ),
                    rx.el.select(
                        rx.el.option(
                            "Todos los Estados",
                            value="todos",
                        ),
                        rx.foreach(
                            VALID_PROJECT_STATUSES,
                            lambda s: rx.el.option(
                                s.capitalize(), value=s
                            ),
                        ),
                        value=ProjectState.dashboard_filter_project_status,
                        on_change=ProjectState.set_dashboard_filter_project_status,
                        class_name="p-2 border border-gray-300 rounded-md focus:ring-indigo-500 focus:border-indigo-500 text-sm mb-4",
                    ),
                    class_name="flex justify-between items-center",
                ),
                rx.recharts.bar_chart(
                    rx.recharts.cartesian_grid(
                        horizontal=True,
                        vertical=False,
                        class_name="opacity-25",
                    ),
                    rx.recharts.graphing_tooltip(
                        class_name=RECHARTS_TOOLTIP_STYLE_CLASS_NAME
                    ),
                    rx.recharts.x_axis(
                        data_key="name",
                        type_="category",
                        axis_line=False,
                        tick_line=False,
                        custom_attrs={"fontSize": "12px"},
                    ),
                    rx.recharts.y_axis(
                        rx.recharts.label(
                            value="Nº Proyectos",
                            position="left",
                            custom_attrs={
                                "angle": 270,
                                "fontSize": "12px",
                                "fontWeight": "700",
                            },
                        ),
                        allow_decimals=False,
                        axis_line=False,
                        tick_line=False,
                        custom_attrs={"fontSize": "12px"},
                    ),
                    rx.recharts.bar(
                        data_key="count",
                        fill="#FFC107",
                        radius=[4, 4, 0, 0],
                        name="Proyectos",
                    ),
                    rx.recharts.legend(
                        height=0,
                        layout="horizontal",
                        align="right",
                        icon_size=10,
                        icon_type="square",
                    ),
                    data=ProjectState.projects_by_status_dashboard_data,
                    height=300,
                    bar_size=35,
                    margin={
                        "left": 20,
                        "right": 20,
                        "top": 5,
                        "bottom": 20,
                    },
                    width="100%",
                ),
                class_name="bg-white p-4 rounded-lg shadow w-full",
            ),
            class_name="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8",
        ),
        rx.el.div(
            rx.el.h3(
                "Distribución de Proyectos por Estado (Gráfico Circular)",
                class_name="text-xl font-semibold text-gray-700 mt-8 mb-4",
            ),
            rx.el.div(
                rx.recharts.pie_chart(
                    rx.recharts.graphing_tooltip(
                        class_name=RECHARTS_TOOLTIP_STYLE_CLASS_NAME
                    ),
                    rx.recharts.pie(
                        data=ProjectState.project_status_distribution,
                        data_key="value",
                        name_key="name",
                        cx="50%",
                        cy="50%",
                        outer_radius=100,
                        fill="#8884d8",
                        label=True,
                    ),
                    rx.recharts.legend(
                        icon_size=10, icon_type="square"
                    ),
                    width="100%",
                    height=350,
                ),
                class_name="bg-white p-4 rounded-lg shadow",
            ),
            class_name="mt-8",
        ),
        rx.el.h2(
            "Actividad Reciente (Bitácora General)",
            class_name="text-2xl font-semibold text-gray-700 mb-4 mt-8",
        ),
        rx.el.div(
            rx.cond(
                ProjectState.recent_log_entries.length()
                > 0,
                rx.el.div(
                    rx.foreach(
                        ProjectState.recent_log_entries,
                        lambda log_entry: rx.el.div(
                            rx.el.p(
                                log_entry[
                                    "formatted_timestamp"
                                ],
                                class_name="text-xs text-gray-500 mr-2",
                            ),
                            rx.el.p(
                                log_entry["action"],
                                class_name="text-sm",
                            ),
                            rx.el.p(
                                f"Usuario: {log_entry['user']}",
                                class_name="text-xs text-gray-400",
                            ),
                            class_name="p-3 border-b border-gray-100 hover:bg-gray-50",
                            key=log_entry["id"],
                        ),
                    ),
                    class_name="bg-white rounded-lg shadow overflow-hidden",
                ),
                rx.el.p(
                    "No hay actividad reciente en la bitácora.",
                    class_name="text-gray-500",
                ),
            )
        ),
        class_name="p-6",
    )


def dashboard_page() -> rx.Component:
    return main_layout(dashboard_content())