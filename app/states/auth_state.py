import reflex as rx
from app.models import User as UserType
from app.db_models import DBUser
import random
import string
from typing import cast
import sqlalchemy
import json


class AuthState(rx.State):
    error_message: str = ""
    is_logged_in: bool = False
    current_user_id: int | None = None
    current_user_display_name: str = ""
    current_user_roles: list[str] = []
    show_add_user_dialog: bool = False
    new_user_generated_password: str = ""
    filter_user_username: str = ""
    filter_user_role: str = "todos"
    show_change_password_dialog: bool = False
    _initial_admin_created: bool = False

    @rx.event
    def on_load_create_admin_if_not_exists(self):
        if self._initial_admin_created:
            return
        with rx.session() as session:
            admin_user = (
                session.exec(
                    sqlalchemy.select(DBUser).where(
                        DBUser.username == "17011128-1"
                    )
                )
                .scalars()
                .first()
            )
            if not admin_user:
                new_admin = DBUser(
                    username="17011128-1",
                    password="17011128-1",
                    email="luis.contreras@municipalidadarica.cl",
                    phone="987423535",
                    contact_info="Administración General",
                    temp_password=False,
                )
                new_admin.roles = ["admin", "user"]
                session.add(new_admin)
                session.commit()
                print("Initial admin user created.")
            self._initial_admin_created = True

    def _is_valid_rut(self, rut: str) -> bool:
        rut_cleaned = (
            rut.upper().replace(".", "").replace("-", "")
        )
        if not rut_cleaned[:-1].isdigit() or not (
            rut_cleaned[-1].isdigit()
            or rut_cleaned[-1] == "K"
        ):
            return False
        body = rut_cleaned[:-1]
        dv_input = rut_cleaned[-1]
        if not 1 <= len(body) <= 8:
            return False
        reversed_digits = [int(d) for d in reversed(body)]
        multipliers = [2, 3, 4, 5, 6, 7]
        total = 0
        for i, digit in enumerate(reversed_digits):
            total += digit * multipliers[i % 6]
        remainder = total % 11
        expected_dv_num = 11 - remainder
        expected_dv: str
        if expected_dv_num == 11:
            expected_dv = "0"
        elif expected_dv_num == 10:
            expected_dv = "K"
        else:
            expected_dv = str(expected_dv_num)
        return dv_input == expected_dv

    @rx.var
    def is_admin(self) -> bool:
        return "admin" in self.current_user_roles

    @rx.event
    def login(self, form_data: dict):
        username_input = form_data.get("username", "")
        password_input = form_data.get("password", "")
        self.error_message = ""
        if not self._is_valid_rut(username_input):
            self.error_message = "Formato de RUT inválido. Use el formato 12345678-9."
            self.is_logged_in = False
            return rx.toast(
                self.error_message,
                duration=3000,
                position="top-center",
            )
        with rx.session() as session:
            user_db = (
                session.exec(
                    sqlalchemy.select(DBUser).where(
                        DBUser.username == username_input
                    )
                )
                .scalars()
                .first()
            )
            if (
                user_db
                and user_db.password == password_input
            ):
                self.is_logged_in = True
                self.current_user_id = user_db.id
                self.current_user_display_name = (
                    user_db.username
                )
                self.current_user_roles = user_db.roles
                if user_db.temp_password:
                    user_db.temp_password = False
                    session.add(user_db)
                    session.commit()
                    yield rx.toast(
                        "Bienvenido. Por seguridad, se recomienda cambiar su contraseña.",
                        duration=5000,
                        position="top-center",
                    )
                return rx.redirect("/dashboard")
        self.error_message = "RUT o contraseña incorrectos."
        self.is_logged_in = False
        self.current_user_id = None
        self.current_user_display_name = ""
        self.current_user_roles = []
        return rx.toast(
            self.error_message,
            duration=3000,
            position="top-center",
        )

    @rx.event
    def logout(self):
        self.is_logged_in = False
        self.current_user_id = None
        self.current_user_display_name = ""
        self.current_user_roles = []
        self.error_message = ""
        self.show_change_password_dialog = False
        return rx.redirect("/")

    @rx.event
    def check_login_status(self):
        if not self.is_logged_in:
            return rx.redirect("/")
        return None

    @rx.event
    def toggle_add_user_dialog(self):
        if not self.is_admin:
            return rx.toast(
                "Acción no permitida.", duration=3000
            )
        self.show_add_user_dialog = (
            not self.show_add_user_dialog
        )
        if self.show_add_user_dialog:
            self.new_user_generated_password = ""

    @rx.event
    def add_user(self, form_data: dict):
        if not self.is_admin:
            return rx.toast(
                "No tiene permisos para agregar usuarios.",
                duration=3000,
            )
        username = form_data.get("new_username", "").strip()
        email = form_data.get("new_user_email", "").strip()
        phone = form_data.get("new_user_phone", "").strip()
        contact_info = form_data.get(
            "new_user_contact_info", ""
        ).strip()
        assign_admin = form_data.get(
            "new_user_assign_admin_role", False
        )
        assign_user = form_data.get(
            "new_user_assign_user_role", True
        )
        if not username:
            return rx.toast(
                "El RUT del usuario no puede estar vacío.",
                duration=3000,
            )
        if not self._is_valid_rut(username):
            return rx.toast(
                f"El RUT '{username}' no es válido. Use el formato 12345678-9.",
                duration=3000,
            )
        with rx.session() as session:
            existing_user = (
                session.exec(
                    sqlalchemy.select(DBUser).where(
                        DBUser.username == username
                    )
                )
                .scalars()
                .first()
            )
            if existing_user:
                return rx.toast(
                    f"El usuario con RUT '{username}' ya existe.",
                    duration=3000,
                )
            roles_list = []
            if assign_admin:
                roles_list.append("admin")
            if assign_user:
                roles_list.append("user")
            if not roles_list:
                return rx.toast(
                    "El usuario debe tener al menos un rol.",
                    duration=3000,
                )
            password_chars = (
                string.ascii_letters + string.digits
            )
            generated_password = "".join(
                random.choices(password_chars, k=10)
            )
            new_db_user = DBUser(
                username=username,
                password=generated_password,
                email=email if email else None,
                phone=phone if phone else None,
                contact_info=(
                    contact_info if contact_info else None
                ),
                temp_password=True,
            )
            new_db_user.roles = roles_list
            session.add(new_db_user)
            session.commit()
        self.new_user_generated_password = (
            generated_password
        )
        return rx.toast(
            f"Usuario con RUT '{username}' creado.",
            duration=5000,
        )

    @rx.event
    async def specific_admin_check(self):
        if not self.is_logged_in:
            yield rx.redirect("/")
            return
        if not self.is_admin:
            yield rx.toast(
                "Acceso denegado. Esta sección es solo para administradores.",
                duration=4000,
                position="top-center",
            )
            yield rx.redirect("/dashboard")
            return
        return

    @rx.var
    def filtered_users(self) -> list[UserType]:
        with rx.session() as session:
            query = sqlalchemy.select(DBUser)
            current_filter_username_val = (
                self.filter_user_username
            )
            current_filter_role_val = self.filter_user_role
            if current_filter_username_val:
                query = query.where(
                    DBUser.username.ilike(
                        f"%{current_filter_username_val}%"
                    )
                )
            db_users_result = (
                session.exec(
                    query.order_by(DBUser.username)
                )
                .scalars()
                .all()
            )
            processed_users: list[UserType] = []
            for db_user in db_users_result:
                user_roles = db_user.roles
                if (
                    current_filter_role_val != "todos"
                    and current_filter_role_val
                    not in user_roles
                ):
                    continue
                processed_users.append(
                    {
                        "id": db_user.id,
                        "username": db_user.username,
                        "password": "",
                        "roles": user_roles,
                        "email": db_user.email,
                        "phone": db_user.phone,
                        "contact_info": db_user.contact_info,
                        "temp_password": db_user.temp_password,
                    }
                )
            return processed_users

    def set_filter_user_username(self, username: str):
        self.filter_user_username = username.strip()

    def set_filter_user_role(self, role: str):
        self.filter_user_role = role

    @rx.event
    def toggle_change_password_dialog(self):
        self.show_change_password_dialog = (
            not self.show_change_password_dialog
        )
        if self.show_change_password_dialog:
            self.error_message = ""

    @rx.event
    def change_password_current_user(self, form_data: dict):
        if (
            not self.is_logged_in
            or self.current_user_id is None
        ):
            self.error_message = (
                "No hay un usuario logueado."
            )
            return rx.toast(
                self.error_message,
                duration=3000,
                position="top-center",
            )
        current_password = form_data.get(
            "current_password_input", ""
        )
        new_password = form_data.get(
            "new_password_input", ""
        )
        confirm_new_password = form_data.get(
            "confirm_new_password_input", ""
        )
        self.error_message = ""
        with rx.session() as session:
            user_to_update = session.get(
                DBUser, self.current_user_id
            )
            if not user_to_update:
                self.error_message = (
                    "Error: Usuario no encontrado."
                )
                return rx.toast(
                    self.error_message,
                    duration=3000,
                    position="top-center",
                )
            if user_to_update.password != current_password:
                self.error_message = (
                    "La contraseña actual es incorrecta."
                )
                return
            if not new_password:
                self.error_message = "La nueva contraseña no puede estar vacía."
                return
            if new_password != confirm_new_password:
                self.error_message = (
                    "Las nuevas contraseñas no coinciden."
                )
                return
            user_to_update.password = new_password
            user_to_update.temp_password = False
            session.add(user_to_update)
            session.commit()
        self.show_change_password_dialog = False
        return rx.toast(
            "Contraseña actualizada exitosamente.",
            duration=3000,
            position="top-center",
        )