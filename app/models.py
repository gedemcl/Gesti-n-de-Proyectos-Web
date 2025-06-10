from typing import Literal, TypedDict

StatusType = Literal[
    "por hacer",
    "en progreso",
    "hecho",
    "idea",
    "diseño",
    "ejecución",
    "finalizado",
]
PriorityType = Literal["crítica", "alta", "media", "baja"]
VALID_PRIORITIES: list[PriorityType] = [
    "crítica",
    "alta",
    "media",
    "baja",
]
VALID_STATUSES: list[StatusType] = [
    "por hacer",
    "en progreso",
    "hecho",
]
VALID_PROJECT_STATUSES: list[StatusType] = [
    "idea",
    "diseño",
    "ejecución",
    "finalizado",
]


class Task(TypedDict):
    id: int
    project_id: int
    description: str
    due_date: str
    status: StatusType
    priority: PriorityType
    is_overdue: bool
    is_due_soon: bool


class LogEntry(TypedDict):
    id: int
    project_id: int | None
    timestamp: str
    formatted_timestamp: str
    action: str
    user: str


class Project(TypedDict):
    id: int
    name: str
    responsible: str
    start_date: str
    due_date: str
    status: StatusType
    description: str
    is_overdue: bool
    is_due_soon: bool


class User(TypedDict):
    id: int
    username: str
    password: str
    roles: list[str]
    email: str | None
    phone: str | None
    contact_info: str | None
    temp_password: bool