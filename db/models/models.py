from datetime import datetime

from sqlalchemy import CHAR, TEXT, Column, DateTime, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from db.models.base import BaseModel

TaskStatus = Enum("open", "active", "resolved", name="task_status")
EmployeeChangeType = Enum("add", "remove", name="employee_change_type")
OriginReportPartType = Enum("report", "task", name="origin_report_part_type")


class Employee(BaseModel):
    __tablename__ = "Employee"
    id = Column(Integer, primary_key=True)

    name = Column(String)
    boss_id = Column(Integer, ForeignKey("Employee.id"))

    boss = relationship("Employee", remote_side=[id], backref="subordinates")


class Task(BaseModel):
    __tablename__ = "Task"
    id = Column(Integer, primary_key=True)

    title = Column(CHAR(20), nullable=False)
    description = Column(TEXT)
    status = Column(TaskStatus, nullable=False)
    creation = Column(DateTime, nullable=False, default=datetime.utcnow)


class EmployeeTask(BaseModel):
    __tablename__ = "EmployeeTask"
    id = Column(Integer, primary_key=True)

    employee = Column(Integer, ForeignKey("Employee.id"), nullable=False)
    task = Column(Integer, ForeignKey("Task.id"), nullable=False)

    employee_rel = relationship("Employee", backref="employee_task_rel")
    task_rel = relationship("Task", backref="employee_task_rel")


class Event(BaseModel):
    __tablename__ = "Event"
    id = Column(Integer, primary_key=True)

    employee = Column(Integer, ForeignKey("Employee.id"))
    task = Column(Integer, ForeignKey("Task.id"), nullable=False)
    creation = Column(DateTime, nullable=False, default=datetime.utcnow)

    employee_rel = relationship("Employee", backref="event_rel")
    task_rel = relationship("Task", backref="event_rel")


class Comment(BaseModel):
    __tablename__ = "Comment"
    id = Column(Integer, primary_key=True)

    event = Column(Integer, ForeignKey("Event.id"), nullable=False)
    content = Column(TEXT)
    creation = Column(DateTime, nullable=False, default=datetime.utcnow)

    event_rel = relationship("Event", backref="comment_rel")


class EmployeeChange(BaseModel):
    __tablename__ = "EmployeeChange"
    id = Column(Integer, primary_key=True)

    event = Column(Integer, ForeignKey("Event.id"), nullable=False)
    employee = Column(Integer, ForeignKey("Employee.id"), nullable=False)
    action = Column(EmployeeChangeType, nullable=False)

    event_rel = relationship("Event", backref="employee_change_rel")
    employee_rel = relationship("Employee", backref="employee_change_rel")


class StatusChange(BaseModel):
    __tablename__ = "StatusChange"
    id = Column(Integer, primary_key=True)

    event = Column(Integer, ForeignKey("Event.id"), nullable=False)
    old = Column(TaskStatus, nullable=False)
    new = Column(TaskStatus, nullable=False)

    event_rel = relationship("Event", backref="status_change_rel")


class Report(BaseModel):
    __tablename__ = "Report"
    id = Column(Integer, primary_key=True)

    employee = Column(Integer, ForeignKey("Employee.id"), nullable=False)
    start = Column(DateTime, nullable=False)
    end = Column(DateTime, nullable=False)

    employee_rel = relationship("Employee", backref="report_rel")


class ReportPart(BaseModel):
    __tablename__ = "ReportPart"
    id = Column(Integer, primary_key=True)

    report = Column(Integer, ForeignKey("Report.id"), nullable=False)
    origin_report = Column(Integer, ForeignKey("Report.id"))
    origin_task = Column(Integer, ForeignKey("Task.id"))
    origin_type = Column(OriginReportPartType, nullable=False)
    comment = Column(TEXT)

    report_rel = relationship(
        "Report", backref="report_part_rel", foreign_keys=[report]
    )
    origin_report_rel = relationship(
        "Report", backref="origin_report_part_rel", foreign_keys=[origin_report]
    )
    origin_task_rel = relationship(
        "Task", backref="task_part_rel", foreign_keys=[origin_task]
    )
