from datetime import datetime

from pydantic import BaseModel


class EmployeeCreateScheme(BaseModel):
    name: str
    boss_id: int | None = None

    class Config:
        orm_mode = True


class EmployeeUpdateScheme(BaseModel):
    name: str | None = None
    boss_id: int | None = None

    class Config:
        orm_mode = True


class EmployeeScheme(EmployeeCreateScheme):
    id: int


class TaskCreateScheme(BaseModel):
    title: str
    description: str
    status: str

    class Config:
        orm_mode = True


class TaskUpdateScheme(BaseModel):
    title: str | None = None
    description: str | None = None
    status: str | None = None

    class Config:
        orm_mode = True


class TaskScheme(TaskCreateScheme):
    id: int
    creation: datetime
    
    class Config:
        orm_mode = True


class EmployeeTaskCreateScheme(BaseModel):
    employee: int
    task: int

    class Config:
        orm_mode = True


class EmployeeTaskUpdateScheme(BaseModel):
    employee: int | None = None
    task: int | None = None

    class Config:
        orm_mode = True


class EmployeeTaskScheme(EmployeeTaskCreateScheme):
    id: int


class EventCreateScheme(BaseModel):
    employee: int
    task: int
    creation: datetime

    class Config:
        orm_mode = True


class EventUpdateScheme(BaseModel):
    employee: int | None = None
    task: int | None = None
    creation: str | None = None

    class Config:
        orm_mode = True


class EventScheme(EventCreateScheme):
    id: int


class CommentCreateScheme(BaseModel):
    event: int
    content: str

    class Config:
        orm_mode = True


class CommentUpdateScheme(BaseModel):
    event: int | None = None
    content: str | None = None

    class Config:
        orm_mode = True


class CommentScheme(CommentCreateScheme):
    id: int


class EmployeeChangeCreateScheme(BaseModel):
    event: int
    employee: int
    action: str

    class Config:
        orm_mode = True


class EmployeeChangeUpdateScheme(BaseModel):
    event: int | None = None
    employee: int | None = None
    action: str | None = None

    class Config:
        orm_mode = True


class EmployeeChangeScheme(EmployeeChangeCreateScheme):
    id: int


class StatusChangeCreateScheme(BaseModel):
    event: int
    old: str
    new: str

    class Config:
        orm_mode = True


class StatusChangeUpdateScheme(BaseModel):
    event: int | None = None
    old: str | None = None
    new: str | None = None

    class Config:
        orm_mode = True


class StatusChangeScheme(StatusChangeCreateScheme):
    id: int


class ReportCreateScheme(BaseModel):
    employee: int
    start: datetime
    end: datetime

    class Config:
        orm_mode = True


class ReportUpdateScheme(BaseModel):
    employee: int | None = None
    start: datetime | None = None
    end: datetime | None = None

    class Config:
        orm_mode = True


class ReportScheme(ReportCreateScheme):
    id: int


class ReportPartCreateScheme(BaseModel):
    origin_report: int | None = None
    origin_task: int | None = None
    origin_type: str
    comment: str

    class Config:
        orm_mode = True


class ReportPartUpdateScheme(BaseModel):
    report: int | None = None
    origin_report: int | None = None
    origin_task: int | None = None
    origin_type: str | None = None
    comment: str | None = None

    class Config:
        orm_mode = True


class ReportPartScheme(ReportPartCreateScheme):
    id: int
