import reflex as rx
from app.pages.login_page import login_page
from app.pages.dashboard_page import dashboard_page
from app.pages.proyectos_page import proyectos_page
from app.pages.proyecto_detail_page import (
    proyecto_detail_page,
)
from app.pages.bitacora_page import bitacora_page
from app.pages.admin_page import admin_page
from app.pages.ayuda_page import ayuda_page
from app.states.auth_state import AuthState
from app.states.project_state import ProjectState


@rx.event
async def initial_load_event():
    """Initial load event to set up the database and initial data."""
    auth_state = await AuthState.get_state()
    await auth_state.on_load_create_admin_if_not_exists()
    project_state = await ProjectState.get_state()
    await project_state.on_load_populate_initial_data()
    await auth_state.check_login_status()
    return AuthState.finish_loading


def index() -> rx.Component:
    """The main entry point of the app."""
    return rx.cond(
        AuthState.is_loading,
        rx.el.div(
            rx.el.div(
                rx.el.i(
                    class_name="fas fa-spinner fa-spin text-5xl text-indigo-500"
                ),
                rx.el.p(
                    "Inicializando aplicación...",
                    class_name="mt-4 text-lg text-gray-600",
                ),
                class_name="text-center",
            ),
            class_name="flex items-center justify-center h-screen bg-gray-50",
        ),
        rx.cond(
            AuthState.is_logged_in,
            dashboard_page(),
            login_page(),
        ),
    )


app = rx.App(
    theme=rx.theme(appearance="light"),
    stylesheets=[
        "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css"
    ],
    head_components=[
        rx.el.link(
            rel="icon",
            href="/professional_logo_ilustre.png",
            type="image/png",
        )
    ],
)
app.add_page(
    index,
    route="/",
    on_load=initial_load_event,
    title="Gestión de Proyectos IMA",
)
app.add_page(
    dashboard_page,
    route="/dashboard",
    on_load=initial_load_event,
    title="Dashboard | Gestión Proyectos",
)
app.add_page(
    proyectos_page,
    route="/proyectos",
    on_load=initial_load_event,
    title="Proyectos | Gestión Proyectos",
)
app.add_page(
    proyecto_detail_page,
    route="/proyectos/[project_id]",
    on_load=[
        initial_load_event,
        ProjectState.load_project_for_detail_page,
    ],
    title="Detalle Proyecto | Gestión Proyectos",
)
app.add_page(
    bitacora_page,
    route="/bitacora",
    on_load=initial_load_event,
    title="Bitácora | Gestión Proyectos",
)
app.add_page(
    admin_page,
    route="/admin",
    on_load=[
        initial_load_event,
        AuthState.specific_admin_check,
    ],
    title="Administración | Gestión Proyectos",
)
app.add_page(
    ayuda_page,
    route="/ayuda",
    on_load=initial_load_event,
    title="Ayuda | Gestión Proyectos",
)