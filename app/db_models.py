import reflex as rx
import datetime
from typing import Optional
from sqlmodel import Field, Relationship


def get_utc_now():
    return datetime.datetime.now(datetime.timezone.utc)


class DBProjectCategory(rx.Model, table=True):
    __tablename__ = "dbprojectcategory"
    id: int | None = Field(
        default=None, primary_key=True, index=True
    )
    name: str = Field(
        unique=True, index=True, nullable=False
    )
    projects: list["DBProject"] = Relationship(
        back_populates="category"
    )


class DBUser(rx.Model, table=True):
    __tablename__ = "dbuser"
    id: int | None = Field(
        default=None, primary_key=True, index=True
    )
    username: str = Field(
        unique=True, index=True, nullable=False
    )
    password: str = Field(nullable=False)
    email: str | None = Field(default=None)
    phone: str | None = Field(default=None)
    contact_info: str | None = Field(default=None)
    temp_password: bool = Field(
        default=False, nullable=False
    )
    roles_internal: str = Field(
        default="[]", nullable=False
    )

    @property
    def roles(self) -> list[str]:
        import json

        return json.loads(self.roles_internal)

    @roles.setter
    def roles(self, value: list[str]):
        import json

        self.roles_internal = json.dumps(value)


class DBProject(rx.Model, table=True):
    __tablename__ = "dbproject"
    id: int | None = Field(
        default=None, primary_key=True, index=True
    )
    name: str = Field(index=True, nullable=False)
    responsible: str = Field(nullable=False)
    start_date: datetime.date = Field(nullable=False)
    due_date: datetime.date | None = Field(default=None)
    status: str = Field(nullable=False)
    description: str | None = Field(default=None)
    category_id: int | None = Field(
        default=None, foreign_key="dbprojectcategory.id"
    )
    category: Optional["DBProjectCategory"] = Relationship(
        back_populates="projects"
    )
    tasks: list["DBTask"] = Relationship(
        back_populates="project"
    )
    log_entries: list["DBLogEntry"] = Relationship(
        back_populates="project"
    )


class DBTask(rx.Model, table=True):
    __tablename__ = "dbtask"
    id: int | None = Field(
        default=None, primary_key=True, index=True
    )
    description: str = Field(nullable=False)
    due_date: datetime.date | None = Field(default=None)
    status: str = Field(nullable=False)
    priority: str = Field(nullable=False)
    created_at: datetime.datetime = Field(
        default_factory=get_utc_now, nullable=False
    )
    project_id: int = Field(
        foreign_key="dbproject.id", nullable=False
    )
    project: "DBProject" = Relationship(
        back_populates="tasks"
    )


class DBLogEntry(rx.Model, table=True):
    __tablename__ = "dblogentry"
    id: int | None = Field(
        default=None, primary_key=True, index=True
    )
    timestamp: datetime.datetime = Field(
        default_factory=get_utc_now, nullable=False
    )
    action: str = Field(nullable=False)
    user: str = Field(nullable=False)
    project_id: int | None = Field(
        default=None, foreign_key="dbproject.id"
    )
    project: Optional["DBProject"] = Relationship(
        back_populates="log_entries"
    )