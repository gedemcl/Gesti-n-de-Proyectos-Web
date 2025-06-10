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
from app.db_models import (
    DBUser,
    DBProject,
    DBTask,
    DBLogEntry,
)

rx.Model.create_all()


def index() -> rx.Component:
    return rx.cond(
        AuthState.is_logged_in,
        dashboard_page(),
        login_page(),
    )


app = rx.App(
    theme=rx.theme(appearance="light"),
    stylesheets=[
        "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css"
    ],
)
app.add_page(
    index,
    route="/",
    on_load=[
        AuthState.check_login_status,
        ProjectState.load_all_data,
    ],
    title="Gestión de Proyectos IMA",
)
app.add_page(
    dashboard_page,
    route="/dashboard",
    on_load=[
        AuthState.check_login_status,
        ProjectState.load_all_data,
    ],
    title="Dashboard | Gestión Proyectos",
)
app.add_page(
    proyectos_page,
    route="/proyectos",
    on_load=[
        AuthState.check_login_status,
        ProjectState.load_all_data,
    ],
    title="Proyectos | Gestión Proyectos",
)
app.add_page(
    proyecto_detail_page,
    route="/proyectos/[project_id]",
    on_load=[
        AuthState.check_login_status,
        ProjectState.load_all_data,
        ProjectState.load_project_for_detail_page,
    ],
    title="Detalle Proyecto | Gestión Proyectos",
)
app.add_page(
    bitacora_page,
    route="/bitacora",
    on_load=[
        AuthState.check_login_status,
        ProjectState.load_all_data,
    ],
    title="Bitácora | Gestión Proyectos",
)
app.add_page(
    admin_page,
    route="/admin",
    on_load=[
        AuthState.check_login_status,
        ProjectState.load_all_data,
        AuthState.specific_admin_check,
    ],
    title="Administración | Gestión Proyectos",
)
app.add_page(
    ayuda_page,
    route="/ayuda",
    on_load=[
        AuthState.check_login_status,
        ProjectState.load_all_data,
    ],
    title="Ayuda | Gestión Proyectos",
)