import reflex as rx
from app.models import (
    Project as ProjectType,
    Task as TaskType,
    LogEntry as LogEntryType,
    StatusType,
    PriorityType,
    VALID_PRIORITIES,
    VALID_STATUSES,
    VALID_PROJECT_STATUSES,
)
from app.db_models import DBProject, DBTask, DBLogEntry
from typing import cast, Union
import datetime
from dateutil.parser import isoparse
from app.states.auth_state import AuthState
from collections import Counter
import sqlalchemy


class ProjectState(rx.State):
    editing_project_id: int | None = None
    show_project_form_dialog: bool = False
    selected_project_id: int | None = None
    editing_task_id: int | None = None
    show_task_form_dialog: bool = False
    show_log_form_dialog: bool = False
    search_term: str = ""
    filter_status: str = "todos"
    filter_due_date: str = ""
    filter_responsible: str = ""
    filter_log_project_status: str = "todos"
    filter_log_action_text: str = ""
    dashboard_filter_project_status: str = "todos"
    _initial_data_populated: bool = False

    @rx.event
    def on_load_populate_initial_data(self):
        if self._initial_data_populated:
            return
        with rx.session() as session:
            if (
                session.exec(sqlalchemy.select(DBProject))
                .scalars()
                .first()
            ):
                self._initial_data_populated = True
                return
            today = datetime.date.today()
            tomorrow = today + datetime.timedelta(days=1)
            yesterday = today - datetime.timedelta(days=1)
            in_a_week = today + datetime.timedelta(days=7)
            current_user_display_name = "Sistema"
            try:
                auth_s = self.get_state_sync(AuthState)
                if (
                    auth_s
                    and auth_s.current_user_display_name
                ):
                    current_user_display_name = (
                        auth_s.current_user_display_name
                    )
            except Exception:
                print(
                    "Warning: AuthState not available during initial data population. Using default user 'Sistema'."
                )
            project1_data = {
                "name": "Rediseño Sitio Web Principal",
                "responsible": "Alicia Pérez",
                "start_date": today
                - datetime.timedelta(days=10),
                "due_date": tomorrow,
                "status": "ejecución",
                "description": "Actualización completa de la plataforma web municipal.",
            }
            db_project1 = DBProject(**project1_data)
            session.add(db_project1)
            project2_data = {
                "name": "Desarrollo App Móvil Cliente VIP",
                "responsible": "Roberto García",
                "start_date": today
                - datetime.timedelta(days=30),
                "due_date": yesterday,
                "status": "diseño",
                "description": "Aplicación móvil para mejorar la comunicación con ciudadanos destacados.",
            }
            db_project2 = DBProject(**project2_data)
            session.add(db_project2)
            project3_data = {
                "name": "Campaña Marketing Q4",
                "responsible": "Laura Gómez",
                "start_date": today,
                "due_date": in_a_week,
                "status": "idea",
                "description": "Planificación y ejecución de la campaña de marketing para el último trimestre.",
            }
            db_project3 = DBProject(**project3_data)
            session.add(db_project3)
            project4_data = {
                "name": "Implementación Nuevo CRM",
                "responsible": "Alicia Pérez",
                "start_date": today
                - datetime.timedelta(days=5),
                "due_date": today
                + datetime.timedelta(days=20),
                "status": "ejecución",
                "description": "Migración e implementación del nuevo sistema CRM.",
            }
            db_project4 = DBProject(**project4_data)
            session.add(db_project4)
            project5_data = {
                "name": "Organización Evento Anual",
                "responsible": "Roberto García",
                "start_date": today,
                "due_date": today
                + datetime.timedelta(days=45),
                "status": "finalizado",
                "description": "Coordinación completa del evento anual de la municipalidad.",
            }
            db_project5 = DBProject(**project5_data)
            session.add(db_project5)
            session.flush()
            task1_data = {
                "project_id": db_project1.id,
                "description": "Diseñar mockups iniciales UX",
                "due_date": today,
                "status": "por hacer",
                "priority": "alta",
            }
            session.add(DBTask(**task1_data))
            task2_data = {
                "project_id": db_project1.id,
                "description": "Desarrollar prototipo de homepage interactivo",
                "due_date": tomorrow,
                "status": "en progreso",
                "priority": "crítica",
            }
            session.add(DBTask(**task2_data))
            task3_data = {
                "project_id": db_project2.id,
                "description": "Configurar servicios backend y base de datos",
                "due_date": today
                - datetime.timedelta(days=5),
                "status": "hecho",
                "priority": "media",
            }
            session.add(DBTask(**task3_data))
            task4_data = {
                "project_id": db_project3.id,
                "description": "Definir KPIs de campaña",
                "due_date": today
                + datetime.timedelta(days=6),
                "status": "por hacer",
                "priority": "alta",
            }
            session.add(DBTask(**task4_data))
            log1_data = {
                "project_id": db_project1.id,
                "action": "Proyecto 'Rediseño Sitio Web Principal' creado",
                "user": current_user_display_name,
            }
            session.add(DBLogEntry(**log1_data))
            log2_data = {
                "project_id": db_project2.id,
                "action": "Proyecto 'Desarrollo App Móvil Cliente VIP' creado",
                "user": current_user_display_name,
            }
            session.add(DBLogEntry(**log2_data))
            log3_data = {
                "project_id": db_project3.id,
                "action": "Proyecto 'Campaña Marketing Q4' creado",
                "user": current_user_display_name,
            }
            session.add(DBLogEntry(**log3_data))
            log4_data = {
                "project_id": db_project1.id,
                "action": "Tarea 'Diseñar mockups iniciales UX' añadida al proyecto 'Rediseño Sitio Web Principal'",
                "user": current_user_display_name,
            }
            session.add(DBLogEntry(**log4_data))
            log5_data = {
                "project_id": None,
                "action": "Usuario '17011128-1' inició sesión.",
                "user": "17011128-1",
            }
            session.add(DBLogEntry(**log5_data))
            session.commit()
            self._initial_data_populated = True
            print(
                "Initial project data populated into database."
            )

    @rx.event
    async def on_load(self) -> None:
        pass

    @rx.event
    async def load_project_for_detail_page(self):
        project_id_str = self.router.page.params.get(
            "project_id", ""
        )
        if project_id_str.isdigit():
            project_id = int(project_id_str)
            with rx.session() as session:
                project_db = session.get(
                    DBProject, project_id
                )
                if project_db:
                    self.selected_project_id = project_id
                else:
                    self.selected_project_id = None
                    yield rx.toast(
                        "Proyecto no encontrado.",
                        duration=3000,
                        position="top-center",
                    )
                    yield rx.redirect("/proyectos")
        else:
            self.selected_project_id = None
            yield rx.toast(
                "ID de proyecto inválido.",
                duration=3000,
                position="top-center",
            )
            yield rx.redirect("/proyectos")

    async def _add_log_entry_db(
        self,
        session,
        action: str,
        project_id: int | None = None,
    ):
        auth_state = await self.get_state(AuthState)
        current_user = (
            auth_state.current_user_display_name
            if auth_state.current_user_display_name
            else "Sistema"
        )
        db_log = DBLogEntry(
            project_id=project_id,
            action=action,
            user=current_user,
            timestamp=datetime.datetime.now(
                datetime.timezone.utc
            ),
        )
        session.add(db_log)

    def _map_dbproject_to_projecttype(
        self, db_project: DBProject
    ) -> ProjectType:
        return {
            "id": db_project.id,
            "name": db_project.name,
            "responsible": db_project.responsible,
            "start_date": db_project.start_date.strftime(
                "%Y-%m-%d"
            ),
            "due_date": db_project.due_date.strftime(
                "%Y-%m-%d"
            ),
            "status": cast(StatusType, db_project.status),
            "description": db_project.description or "",
            "is_overdue": self.is_date_overdue(
                db_project.due_date.strftime("%Y-%m-%d")
            ),
            "is_due_soon": self.is_date_due_soon(
                db_project.due_date.strftime("%Y-%m-%d"),
                days_threshold=7,
            ),
        }

    def _map_dbtask_to_tasktype(
        self, db_task: DBTask
    ) -> TaskType:
        due_date_str = db_task.due_date.strftime("%Y-%m-%d")
        status_str = cast(StatusType, db_task.status)
        return {
            "id": db_task.id,
            "project_id": db_task.project_id,
            "description": db_task.description,
            "due_date": due_date_str,
            "status": status_str,
            "priority": cast(
                PriorityType, db_task.priority
            ),
            "is_overdue": self.is_date_overdue(due_date_str)
            and status_str != "hecho",
            "is_due_soon": self.is_date_due_soon(
                due_date_str, days_threshold=7
            )
            and status_str != "hecho",
        }

    def _map_dblogentry_to_logentrytype(
        self, db_log: DBLogEntry
    ) -> LogEntryType:
        return {
            "id": db_log.id,
            "project_id": db_log.project_id,
            "timestamp": db_log.timestamp.isoformat(),
            "formatted_timestamp": self.format_timestamp(
                db_log.timestamp.isoformat()
            ),
            "action": db_log.action,
            "user": db_log.user,
        }

    @rx.var
    def filtered_project_list(self) -> list[ProjectType]:
        with rx.session() as session:
            query = sqlalchemy.select(DBProject)
            if self.filter_status != "todos":
                query = query.where(
                    DBProject.status == self.filter_status
                )
            if self.filter_due_date:
                try:
                    filter_date_obj = (
                        datetime.datetime.strptime(
                            self.filter_due_date, "%Y-%m-%d"
                        ).date()
                    )
                    query = query.where(
                        DBProject.due_date
                        <= filter_date_obj
                    )
                except ValueError:
                    pass
            if self.filter_responsible:
                query = query.where(
                    DBProject.responsible.ilike(
                        f"%{self.filter_responsible}%"
                    )
                )
            if self.search_term.strip():
                search_lower = self.search_term.lower()
                query = query.where(
                    sqlalchemy.or_(
                        DBProject.name.ilike(
                            f"%{search_lower}%"
                        ),
                        DBProject.responsible.ilike(
                            f"%{search_lower}%"
                        ),
                        DBProject.description.ilike(
                            f"%{search_lower}%"
                        ),
                    )
                )
            db_projects = (
                session.exec(query.order_by(DBProject.name))
                .scalars()
                .all()
            )
            return [
                self._map_dbproject_to_projecttype(p)
                for p in db_projects
            ]

    @rx.var
    def selected_project(self) -> ProjectType | None:
        if self.selected_project_id is None:
            return None
        with rx.session() as session:
            db_project = session.get(
                DBProject, self.selected_project_id
            )
            return (
                self._map_dbproject_to_projecttype(
                    db_project
                )
                if db_project
                else None
            )

    @rx.var
    def tasks_for_selected_project(self) -> list[TaskType]:
        if self.selected_project_id is None:
            return []
        with rx.session() as session:
            db_tasks = (
                session.exec(
                    sqlalchemy.select(DBTask).where(
                        DBTask.project_id
                        == self.selected_project_id
                    )
                )
                .scalars()
                .all()
            )
            mapped_tasks = [
                self._map_dbtask_to_tasktype(t)
                for t in db_tasks
            ]
            return sorted(
                mapped_tasks,
                key=lambda t: (
                    VALID_PRIORITIES.index(t["priority"]),
                    t["due_date"],
                ),
            )

    @rx.var
    def logs_for_selected_project(
        self,
    ) -> list[LogEntryType]:
        if self.selected_project_id is None:
            return []
        with rx.session() as session:
            db_logs = (
                session.exec(
                    sqlalchemy.select(DBLogEntry)
                    .where(
                        DBLogEntry.project_id
                        == self.selected_project_id
                    )
                    .order_by(DBLogEntry.timestamp.desc())
                )
                .scalars()
                .all()
            )
            return [
                self._map_dblogentry_to_logentrytype(log)
                for log in db_logs
            ]

    @rx.var
    def all_log_entries(self) -> list[LogEntryType]:
        with rx.session() as session:
            db_logs = (
                session.exec(
                    sqlalchemy.select(DBLogEntry).order_by(
                        DBLogEntry.timestamp.desc()
                    )
                )
                .scalars()
                .all()
            )
            return [
                self._map_dblogentry_to_logentrytype(log)
                for log in db_logs
            ]

    @rx.var
    def recent_log_entries(self) -> list[LogEntryType]:
        all_entries = self.all_log_entries
        return all_entries[:10]

    @rx.var
    def filtered_log_entries(self) -> list[LogEntryType]:
        logs_query = sqlalchemy.select(DBLogEntry)
        if self.filter_log_project_status != "todos":
            project_ids_with_status = sqlalchemy.select(
                DBProject.id
            ).where(
                DBProject.status
                == self.filter_log_project_status
            )
            logs_query = logs_query.where(
                DBLogEntry.project_id.in_(
                    project_ids_with_status
                )
            )
        if self.filter_log_action_text:
            logs_query = logs_query.where(
                DBLogEntry.action.ilike(
                    f"%{self.filter_log_action_text}%"
                )
            )
        with rx.session() as session:
            db_logs = (
                session.exec(
                    logs_query.order_by(
                        DBLogEntry.timestamp.desc()
                    )
                )
                .scalars()
                .all()
            )
            return [
                self._map_dblogentry_to_logentrytype(log)
                for log in db_logs
            ]

    @rx.var
    def project_to_edit(self) -> ProjectType | None:
        if self.editing_project_id is None:
            return None
        with rx.session() as session:
            db_project = session.get(
                DBProject, self.editing_project_id
            )
            return (
                self._map_dbproject_to_projecttype(
                    db_project
                )
                if db_project
                else None
            )

    @rx.var
    def task_to_edit(self) -> TaskType | None:
        if self.editing_task_id is None:
            return None
        with rx.session() as session:
            db_task = session.get(
                DBTask, self.editing_task_id
            )
            return (
                self._map_dbtask_to_tasktype(db_task)
                if db_task
                else None
            )

    @rx.event
    def toggle_project_form_dialog(
        self, project_id: int | None = None
    ):
        self.editing_project_id = project_id
        self.show_project_form_dialog = (
            not self.show_project_form_dialog
        )

    @rx.event
    async def save_project(self, form_data: dict):
        name = form_data.get("name", "").strip()
        responsible = form_data.get(
            "responsible", ""
        ).strip()
        start_date_str = form_data.get("start_date", "")
        due_date_str = form_data.get("due_date", "")
        status_str = form_data.get("status", "idea")
        description_str = form_data.get("description", "")
        if not all(
            [
                name,
                responsible,
                start_date_str,
                due_date_str,
                status_str,
            ]
        ):
            return rx.toast(
                "Nombre, responsable, fechas y estado del proyecto son obligatorios.",
                duration=3000,
            )
        try:
            start_date_obj = datetime.datetime.strptime(
                start_date_str, "%Y-%m-%d"
            ).date()
            due_date_obj = datetime.datetime.strptime(
                due_date_str, "%Y-%m-%d"
            ).date()
            if start_date_obj > due_date_obj:
                return rx.toast(
                    "La fecha de inicio no puede ser posterior a la fecha límite.",
                    duration=3000,
                )
        except ValueError:
            return rx.toast(
                "Formato de fecha inválido. Use YYYY-MM-DD.",
                duration=3000,
            )
        if status_str not in VALID_PROJECT_STATUSES:
            return rx.toast(
                f"Estado de proyecto inválido.",
                duration=3000,
            )
        project_action = "actualizado"
        saved_project_id: int | None = None
        with rx.session() as session:
            if self.editing_project_id is not None:
                db_project = session.get(
                    DBProject, self.editing_project_id
                )
                if not db_project:
                    return rx.toast(
                        "Proyecto no encontrado para editar.",
                        duration=3000,
                    )
                saved_project_id = self.editing_project_id
            else:
                db_project = DBProject()
                project_action = "creado"
            db_project.name = name
            db_project.responsible = responsible
            db_project.start_date = start_date_obj
            db_project.due_date = due_date_obj
            db_project.status = status_str
            db_project.description = description_str
            session.add(db_project)
            session.flush()
            if saved_project_id is None:
                saved_project_id = db_project.id
            await self._add_log_entry_db(
                session,
                f"Proyecto '{name}' {project_action}.",
                project_id=saved_project_id,
            )
            new_task_description = form_data.get(
                "new_task_description", ""
            ).strip()
            if (
                new_task_description
                and saved_project_id is not None
                and (project_action == "creado")
            ):
                new_task_due_date_str = form_data.get(
                    "new_task_due_date", due_date_str
                )
                try:
                    new_task_due_obj = (
                        datetime.datetime.strptime(
                            new_task_due_date_str,
                            "%Y-%m-%d",
                        ).date()
                    )
                except ValueError:
                    new_task_due_obj = due_date_obj
                db_task = DBTask(
                    project_id=saved_project_id,
                    description=new_task_description,
                    due_date=new_task_due_obj,
                    priority="media",
                    status="por hacer",
                )
                session.add(db_task)
                await self._add_log_entry_db(
                    session,
                    f"Tarea '{new_task_description}' creada para el proyecto '{name}'.",
                    project_id=saved_project_id,
                )
            session.commit()
        self.show_project_form_dialog = False
        self.editing_project_id = None
        return rx.toast(
            f"Proyecto '{name}' {project_action} exitosamente.",
            duration=3000,
        )

    @rx.event
    async def delete_project(self, project_id: int):
        with rx.session() as session:
            db_project = session.get(DBProject, project_id)
            if db_project:
                project_name = db_project.name
                tasks_to_delete = (
                    session.exec(
                        sqlalchemy.select(DBTask).where(
                            DBTask.project_id == project_id
                        )
                    )
                    .scalars()
                    .all()
                )
                for task in tasks_to_delete:
                    session.delete(task)
                logs_to_delete = (
                    session.exec(
                        sqlalchemy.select(DBLogEntry).where(
                            DBLogEntry.project_id
                            == project_id
                        )
                    )
                    .scalars()
                    .all()
                )
                for log_entry in logs_to_delete:
                    session.delete(log_entry)
                session.delete(db_project)
                await self._add_log_entry_db(
                    session,
                    f"Proyecto '{project_name}' eliminado.",
                    project_id=None,
                )
                session.commit()
                if self.selected_project_id == project_id:
                    self.selected_project_id = None
                    yield rx.redirect("/proyectos")
                yield rx.toast(
                    f"Proyecto '{project_name}' eliminado.",
                    duration=3000,
                )
            else:
                yield rx.toast(
                    "Proyecto no encontrado para eliminar.",
                    duration=3000,
                )

    @rx.event
    def select_project(self, project_id: int | None):
        self.selected_project_id = project_id
        self.show_task_form_dialog = False
        self.editing_task_id = None
        self.show_log_form_dialog = False

    @rx.event
    def toggle_task_form_dialog(
        self, task_id: int | None = None
    ):
        if (
            self.selected_project_id is None
            and task_id is None
        ):
            if task_id:
                with rx.session() as session:
                    task_db = session.get(DBTask, task_id)
                    if not task_db:
                        return rx.toast(
                            "Tarea no encontrada.",
                            duration=3000,
                        )
            else:
                return rx.toast(
                    "Por favor, selecciona primero un proyecto para añadir una tarea nueva.",
                    duration=3000,
                )
        self.editing_task_id = task_id
        self.show_task_form_dialog = (
            not self.show_task_form_dialog
        )

    @rx.event
    async def save_task(self, form_data: dict):
        description = form_data.get(
            "description", ""
        ).strip()
        due_date_str = form_data.get("due_date", "")
        priority_str = form_data.get("priority", "media")
        status_str = form_data.get("status", "por hacer")
        if priority_str not in VALID_PRIORITIES:
            return rx.toast(
                f"Prioridad inválida.", duration=3000
            )
        if status_str not in VALID_STATUSES:
            return rx.toast(
                f"Estado de tarea inválido.", duration=3000
            )
        current_project_id_for_task: int | None = None
        if self.editing_task_id is not None:
            with rx.session() as session:
                task_db = session.get(
                    DBTask, self.editing_task_id
                )
                if task_db:
                    current_project_id_for_task = (
                        task_db.project_id
                    )
                else:
                    return rx.toast(
                        "Tarea para editar no encontrada.",
                        duration=3000,
                    )
        else:
            current_project_id_for_task = (
                self.selected_project_id
            )
        if current_project_id_for_task is None:
            return rx.toast(
                "No hay contexto de proyecto para esta tarea. Seleccione un proyecto.",
                duration=3000,
            )
        if not all([description, due_date_str]):
            return rx.toast(
                "La descripción y la fecha límite de la tarea son obligatorias.",
                duration=3000,
            )
        try:
            due_date_obj = datetime.datetime.strptime(
                due_date_str, "%Y-%m-%d"
            ).date()
        except ValueError:
            return rx.toast(
                "Formato de fecha inválido para la tarea. Use YYYY-MM-DD.",
                duration=3000,
            )
        task_action = "actualizada"
        with rx.session() as session:
            if self.editing_task_id is not None:
                db_task = session.get(
                    DBTask, self.editing_task_id
                )
                if not db_task:
                    return rx.toast(
                        "Tarea no encontrada para editar.",
                        duration=3000,
                    )
            else:
                db_task = DBTask(
                    project_id=current_project_id_for_task
                )
                task_action = "creada"
            db_task.description = description
            db_task.due_date = due_date_obj
            db_task.priority = priority_str
            db_task.status = status_str
            session.add(db_task)
            await self._add_log_entry_db(
                session,
                f"Tarea '{description}' {task_action}.",
                project_id=current_project_id_for_task,
            )
            session.commit()
        self.show_task_form_dialog = False
        self.editing_task_id = None
        return rx.toast(
            f"Tarea '{description}' {task_action} exitosamente.",
            duration=3000,
        )

    @rx.event
    async def delete_task(self, task_id: int):
        with rx.session() as session:
            db_task = session.get(DBTask, task_id)
            if db_task:
                task_description = db_task.description
                project_id_for_log = db_task.project_id
                session.delete(db_task)
                await self._add_log_entry_db(
                    session,
                    f"Tarea '{task_description}' eliminada.",
                    project_id=project_id_for_log,
                )
                session.commit()
                return rx.toast(
                    f"Tarea '{task_description}' eliminada.",
                    duration=3000,
                )
            else:
                return rx.toast(
                    "Tarea no encontrada para eliminar.",
                    duration=3000,
                )

    @rx.event
    async def change_task_status(
        self, task_id: int, new_status_str: str
    ):
        if new_status_str not in VALID_STATUSES:
            return rx.toast(
                f"Estado de tarea inválido.", duration=3000
            )
        new_status = cast(StatusType, new_status_str)
        with rx.session() as session:
            db_task = session.get(DBTask, task_id)
            if db_task:
                old_status = db_task.status
                db_task.status = new_status
                session.add(db_task)
                await self._add_log_entry_db(
                    session,
                    f"El estado de la tarea '{db_task.description}' cambió de {old_status.capitalize()} a {new_status.capitalize()}.",
                    project_id=db_task.project_id,
                )
                session.commit()
                return rx.toast(
                    f"Estado de tarea '{db_task.description}' actualizado.",
                    duration=3000,
                )

    @rx.event
    def toggle_log_form_dialog(self):
        if self.selected_project_id is None:
            return rx.toast(
                "Por favor, selecciona primero un proyecto para añadir una entrada de bitácora.",
                duration=3000,
            )
        self.show_log_form_dialog = (
            not self.show_log_form_dialog
        )

    @rx.event
    async def add_manual_log_entry(self, form_data: dict):
        action = form_data.get("action", "").strip()
        if not self.selected_project_id:
            return rx.toast(
                "Ningún proyecto seleccionado.",
                duration=3000,
            )
        if not action:
            return rx.toast(
                "La acción de la bitácora no puede estar vacía.",
                duration=3000,
            )
        with rx.session() as session:
            await self._add_log_entry_db(
                session,
                f"(Entrada Manual) {action}",
                project_id=self.selected_project_id,
            )
            session.commit()
        self.show_log_form_dialog = False
        return rx.toast(
            "Entrada manual de bitácora añadida.",
            duration=3000,
        )

    def is_date_due_soon(
        self, due_date_str: str, days_threshold: int = 7
    ) -> bool:
        if not due_date_str:
            return False
        try:
            due_date = datetime.datetime.strptime(
                due_date_str, "%Y-%m-%d"
            ).date()
            today = datetime.date.today()
            return (
                today
                <= due_date
                <= today
                + datetime.timedelta(days=days_threshold)
            )
        except ValueError:
            return False

    def is_date_overdue(self, due_date_str: str) -> bool:
        if not due_date_str:
            return False
        try:
            due_date = datetime.datetime.strptime(
                due_date_str, "%Y-%m-%d"
            ).date()
            today = datetime.date.today()
            return due_date < today
        except ValueError:
            return False

    def format_timestamp(self, timestamp_str: str) -> str:
        try:
            dt_object = isoparse(timestamp_str)
            return dt_object.strftime(
                "%d-%m-%Y %H:%M:%S %Z"
            )
        except (ValueError, TypeError):
            return "Fecha Inválida"

    def set_search_term(self, term: str):
        self.search_term = term.strip()

    def set_filter_status(self, status: str):
        self.filter_status = status

    def set_filter_due_date(self, date: str):
        self.filter_due_date = date

    def set_filter_responsible(self, responsible: str):
        self.filter_responsible = responsible.strip()

    @rx.event
    def clear_filters(self):
        self.filter_status = "todos"
        self.filter_due_date = ""
        self.filter_responsible = ""
        self.search_term = ""

    def set_filter_log_project_status(self, status: str):
        self.filter_log_project_status = status

    def set_filter_log_action_text(self, text: str):
        self.filter_log_action_text = text.strip()

    @rx.event
    def clear_log_filters(self):
        self.filter_log_project_status = "todos"
        self.filter_log_action_text = ""

    @rx.event
    def filter_by_status_and_redirect(self, status: str):
        self.filter_status = status
        self.search_term = ""
        self.filter_due_date = ""
        self.filter_responsible = ""
        return rx.redirect("/proyectos")

    def _get_project_count_by_status(
        self, status: StatusType
    ) -> int:
        with rx.session() as session:
            return (
                session.exec(
                    sqlalchemy.select(
                        sqlalchemy.func.count(DBProject.id)
                    ).where(DBProject.status == status)
                ).scalar_one_or_none()
                or 0
            )

    def _get_task_count_by_status(self, status: str) -> int:
        with rx.session() as session:
            return (
                session.exec(
                    sqlalchemy.select(
                        sqlalchemy.func.count(DBTask.id)
                    ).where(DBTask.status == status)
                ).scalar_one_or_none()
                or 0
            )

    @rx.var
    def total_projects_count(self) -> int:
        with rx.session() as session:
            return (
                session.exec(
                    sqlalchemy.select(
                        sqlalchemy.func.count(DBProject.id)
                    )
                ).scalar_one_or_none()
                or 0
            )

    @rx.var
    def projects_idea_count(self) -> int:
        return self._get_project_count_by_status("idea")

    @rx.var
    def projects_diseno_count(self) -> int:
        return self._get_project_count_by_status("diseño")

    @rx.var
    def projects_ejecucion_count(self) -> int:
        return self._get_project_count_by_status(
            "ejecución"
        )

    @rx.var
    def projects_finalizado_count(self) -> int:
        return self._get_project_count_by_status(
            "finalizado"
        )

    @rx.var
    def projects_due_soon_count(self) -> int:
        with rx.session() as session:
            today = datetime.date.today()
            due_soon_threshold = today + datetime.timedelta(
                days=7
            )
            return (
                session.exec(
                    sqlalchemy.select(
                        sqlalchemy.func.count(DBProject.id)
                    )
                    .where(DBProject.due_date >= today)
                    .where(
                        DBProject.due_date
                        <= due_soon_threshold
                    )
                    .where(DBProject.status != "finalizado")
                ).scalar_one_or_none()
                or 0
            )

    @rx.var
    def projects_overdue_count(self) -> int:
        with rx.session() as session:
            today = datetime.date.today()
            return (
                session.exec(
                    sqlalchemy.select(
                        sqlalchemy.func.count(DBProject.id)
                    )
                    .where(DBProject.due_date < today)
                    .where(DBProject.status != "finalizado")
                ).scalar_one_or_none()
                or 0
            )

    @rx.var
    def project_status_distribution(
        self,
    ) -> list[dict[str, str | int]]:
        colors = {
            "idea": "#3B82F6",
            "diseño": "#8B5CF6",
            "ejecución": "#FBBF24",
            "finalizado": "#10B981",
        }
        counts = {
            "idea": self.projects_idea_count,
            "diseño": self.projects_diseno_count,
            "ejecución": self.projects_ejecucion_count,
            "finalizado": self.projects_finalizado_count,
        }
        return [
            {
                "name": status.capitalize(),
                "value": count_val,
                "fill": colors.get(status, "#A0AEC0"),
            }
            for status, count_val in counts.items()
            if count_val > 0
        ]

    @rx.var
    def projects_by_responsible_data(
        self,
    ) -> list[dict[str, Union[str, int]]]:
        with rx.session() as session:
            results = session.exec(
                sqlalchemy.select(
                    DBProject.responsible,
                    sqlalchemy.func.count(
                        DBProject.id
                    ).label("count"),
                )
                .group_by(DBProject.responsible)
                .order_by(
                    sqlalchemy.func.count(
                        DBProject.id
                    ).desc()
                )
            ).all()
            return [
                {"name": resp, "projects": count}
                for resp, count in results
            ]

    @rx.event
    def set_dashboard_filter_project_status(
        self, status: str
    ):
        self.dashboard_filter_project_status = status

    @rx.var
    def projects_by_status_dashboard_data(
        self,
    ) -> list[dict[str, Union[str, int]]]:
        query = sqlalchemy.select(
            DBProject.status,
            sqlalchemy.func.count(DBProject.id).label(
                "count"
            ),
        )
        if self.dashboard_filter_project_status != "todos":
            query = query.where(
                DBProject.status
                == self.dashboard_filter_project_status
            )
        query = query.group_by(DBProject.status).order_by(
            DBProject.status
        )
        with rx.session() as session:
            results = session.exec(query).all()
        data_to_return = []
        if self.dashboard_filter_project_status == "todos":
            status_counts = {
                status: 0
                for status in VALID_PROJECT_STATUSES
            }
            for status_db, count_db in results:
                if status_db in status_counts:
                    status_counts[status_db] = count_db
            for (
                status_val,
                count_val,
            ) in status_counts.items():
                data_to_return.append(
                    {
                        "name": status_val.capitalize(),
                        "count": count_val,
                    }
                )
        else:
            found = False
            for status_db, count_db in results:
                if (
                    status_db
                    == self.dashboard_filter_project_status
                ):
                    data_to_return.append(
                        {
                            "name": status_db.capitalize(),
                            "count": count_db,
                        }
                    )
                    found = True
                    break
            if (
                not found
                and self.dashboard_filter_project_status
                in VALID_PROJECT_STATUSES
            ):
                data_to_return.append(
                    {
                        "name": self.dashboard_filter_project_status.capitalize(),
                        "count": 0,
                    }
                )
        return data_to_return

    @rx.var
    def total_tasks_count(self) -> int:
        with rx.session() as session:
            return (
                session.exec(
                    sqlalchemy.select(
                        sqlalchemy.func.count(DBTask.id)
                    )
                ).scalar_one_or_none()
                or 0
            )

    @rx.var
    def tasks_por_hacer_count(self) -> int:
        return self._get_task_count_by_status("por hacer")

    @rx.var
    def tasks_en_progreso_count(self) -> int:
        return self._get_task_count_by_status("en progreso")

    @rx.var
    def tasks_hecho_count(self) -> int:
        return self._get_task_count_by_status("hecho")

    @rx.var
    def task_status_distribution(
        self,
    ) -> list[dict[str, str | int]]:
        colors = {
            "por hacer": "#A0AEC0",
            "en progreso": "#ECC94B",
            "hecho": "#48BB78",
        }
        counts = {
            "por hacer": self.tasks_por_hacer_count,
            "en progreso": self.tasks_en_progreso_count,
            "hecho": self.tasks_hecho_count,
        }
        return [
            {
                "name": status.capitalize(),
                "value": data_count,
                "fill": colors.get(status, "#A0AEC0"),
            }
            for status, data_count in counts.items()
            if data_count > 0
        ]