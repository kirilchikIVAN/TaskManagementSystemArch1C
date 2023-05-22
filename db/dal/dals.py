import typing
from datetime import datetime

from pydantic import typing
from sqlalchemy import and_, select

from db.dal.base import BaseDAL
from db.models.models import *
from schemas.schemas import *


class EmployeeDAL(BaseDAL[Employee, EmployeeCreateScheme, EmployeeUpdateScheme]):
    model = Employee
    readable_object_name = "EmployeeDAL"


class TaskDAL(BaseDAL[Task, TaskCreateScheme, TaskUpdateScheme]):
    model = Task
    readable_object_name = "TaskDAL"

    async def filter_by_time(
        self, start_time: datetime, end_time: datetime
    ) -> typing.Sequence[Task]:
        query = self.get_query().where(
            and_(Task.creation >= start_time, Task.creation <= end_time)
        )
        return await self.get_all(query=query)

    async def filter_by_employee(self, employee_id: int) -> typing.Sequence[Task]:
        query = (
            self.get_query()
            .join(EmployeeTask)
            .filter(EmployeeTask.employee == employee_id)
        )
        return await self.get_all(query=query)

    async def filter_by_boss(self, boss_id: int) -> typing.Sequence[Task]:
        query = self.get_query().join(Employee).filter(Employee.boss_id == boss_id)
        return await self.get_all(query=query)

    async def filter_by_status(self, status: TaskStatus) -> typing.Sequence[Task]:
        query = self.get_query().filter(Task.status == status)
        return await self.get_all(query=query)

    async def filter_tasks(
        self,
        start_time: datetime | None = None,
        end_time: datetime | None = None,
        employee_id: int | None = None,
        status: str | None = None,
    ) -> typing.Sequence[Task]:
        query = self.get_query()

        if start_time is not None:
            query = query.where(Task.creation >= start_time)
        if end_time is not None:
            query = query.where(Task.creation <= end_time)
        if employee_id is not None:
            query = query.join(EmployeeTask).where(EmployeeTask.employee == employee_id)
        if status is not None:
            query = query.where(Task.status == status)

        return await self.get_all(query)

    async def get_all_events_for_task(self, task_id: int) -> typing.Sequence[Event]:
        query = select(Event).filter(Event.task == task_id).order_by(Event.creation)
        events = await self.db_session.execute(query)
        return events.scalars().all()

    async def get_comments_for_task(self, task_id: int) -> typing.Sequence[Comment]:
        query = (
            select(Comment)
            .join(Event)
            .filter(Event.task == task_id)
            .order_by(Comment.creation)
        )
        comments = await self.db_session.execute(query)
        return comments.scalars().all()

    async def get_employee_changes_for_task(
        self, task_id: int
    ) -> typing.Sequence[EmployeeChange]:
        query = (
            select(EmployeeChange)
            .join(Event)
            .filter(Event.task == task_id)
            .order_by(EmployeeChange.creation)
        )
        employee_changes = await self.db_session.execute(query)
        return employee_changes.scalars().all()

    async def get_status_changes_for_task(
        self, task_id: int
    ) -> typing.Sequence[StatusChange]:
        query = (
            select(StatusChange)
            .join(Event)
            .filter(Event.task == task_id)
            .order_by(StatusChange.creation)
        )
        status_changes = await self.db_session.execute(query)
        return status_changes.scalars().all()

    async def create_event_comment_with_event(
        self, task_id: int, employee_id: int, comment_data: CommentCreateScheme
    ) -> Comment:
        event = Event(employee=employee_id, task=task_id)
        comment = Comment(**comment_data.dict())
        event.comment_rel.append(comment)
        self.db_session.add(event)
        await self.db_session.commit()
        return comment

    async def create_event_employee_change_with_event(
        self,
        task_id: int,
        employee_id: int,
        employee_change_data: EmployeeChangeCreateScheme,
    ) -> EmployeeChange:
        event = Event(employee=employee_id, task=task_id)
        employee_change = EmployeeChange(**employee_change_data.dict())
        event.employee_change_rel.append(employee_change)
        self.db_session.add(event)
        await self.db_session.commit()
        return employee_change

    async def create_event_status_change_with_event(
        self,
        task_id: int,
        employee_id: int,
        status_change_data: StatusChangeCreateScheme,
    ) -> StatusChange:
        event = Event(employee=employee_id, task=task_id)
        status_change = StatusChange(**status_change_data.dict())
        event.status_change_rel.append(status_change)
        self.db_session.add(event)
        await self.db_session.commit()
        return status_change


class EmployeeTaskDAL(
    BaseDAL[EmployeeTask, EmployeeTaskCreateScheme, EmployeeTaskUpdateScheme]
):
    model = EmployeeTask
    readable_object_name = "EmployeeTaskDAL"


class EventDAL(BaseDAL[Event, EventCreateScheme, EventUpdateScheme]):
    model = Event
    readable_object_name = "EventDAL"


class CommentDAL(BaseDAL[Comment, CommentCreateScheme, CommentUpdateScheme]):
    model = Comment
    readable_object_name = "CommentDAL"


class EmployeeChangeDAL(
    BaseDAL[EmployeeChange, EmployeeChangeCreateScheme, EmployeeChangeUpdateScheme]
):
    model = EmployeeChange
    readable_object_name = "EmployeeChangeDAL"


class StatusChangeDAL(
    BaseDAL[StatusChange, StatusChangeCreateScheme, StatusChangeUpdateScheme]
):
    model = StatusChange
    readable_object_name = "StatusChangeDAL"


class ReportDAL(BaseDAL[Report, ReportCreateScheme, ReportUpdateScheme]):
    model = Report
    readable_object_name = "ReportDAL"

    async def get_full_by_id_with_exception(
        self, report_id: int
    ) -> typing.Sequence[ReportPart]:
        await self.get_by_id_with_exception(report_id)
        report_parts = await self.db_session.execute(
            select(ReportPart).where(ReportPart.report == report_id)
        )
        return report_parts.scalars().all()


class ReportPartDAL(
    BaseDAL[ReportPart, ReportPartCreateScheme, ReportPartUpdateScheme]
):
    model = ReportPart
    readable_object_name = "ReportPartDAL"
