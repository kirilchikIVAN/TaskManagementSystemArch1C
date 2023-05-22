import typing
from datetime import datetime

from fastapi import APIRouter, Depends

from db.dal.dals import TaskDAL
from dependencies.db import get_db_dal_by_type
from schemas.schemas import (
    CommentCreateScheme,
    CommentScheme,
    EmployeeChangeCreateScheme,
    EmployeeChangeScheme,
    EventScheme,
    StatusChangeCreateScheme,
    StatusChangeScheme,
    TaskCreateScheme,
    TaskScheme,
    TaskUpdateScheme,
)

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("/{id}")
async def get_task_by_id(
    id: int, task_dal: TaskDAL = Depends(get_db_dal_by_type(TaskDAL))
) -> TaskScheme | None:
    return TaskScheme.from_orm(await task_dal.get_by_id_with_exception(id))


@router.get("")
async def get_tasks(
    task_dal: TaskDAL = Depends(get_db_dal_by_type(TaskDAL)),
) -> list[TaskScheme]:
    return [TaskScheme.from_orm(task) for task in await task_dal.get_all()]


@router.post("")
async def create_task(
    task: TaskCreateScheme, task_dal: TaskDAL = Depends(get_db_dal_by_type(TaskDAL))
) -> TaskScheme:
    return TaskScheme.from_orm(await task_dal.create_from_api(task))


@router.put("/{id}")
async def update_task(
    id: int,
    task: TaskUpdateScheme,
    task_dal: TaskDAL = Depends(get_db_dal_by_type(TaskDAL)),
) -> TaskScheme | None:
    return TaskScheme.from_orm(await task_dal.update_by_id_with_exception(id, task))


@router.delete("/{id}")
async def delete_task(
    id: int, task_dal: TaskDAL = Depends(get_db_dal_by_type(TaskDAL))
) -> None:
    await task_dal.remove_by_id_from_api(id)


@router.get("/filter/")
async def filter_tasks(
    start_time: datetime | None = None,
    end_time: datetime | None = None,
    employee_id: int | None = None,
    status: str | None = None,
    task_dal: TaskDAL = Depends(get_db_dal_by_type(TaskDAL)),
) -> list[TaskScheme]:
    tasks = await task_dal.filter_tasks(
        start_time=start_time, end_time=end_time, employee_id=employee_id, status=status
    )
    return [TaskScheme.from_orm(task) for task in tasks]


@router.get("/{task_id}/detailed_events")
async def get_all_related_objects_for_task(
    task_id: int, task_dal: TaskDAL = Depends(get_db_dal_by_type(TaskDAL))
) -> typing.Sequence[
    typing.Union[CommentScheme, EmployeeChangeScheme, StatusChangeScheme]
]:
    await task_dal.get_by_id_with_exception(task_id)

    comments = await task_dal.get_comments_for_task(task_id)
    comment_schemes = [CommentScheme.from_orm(comment) for comment in comments]

    employee_changes = await task_dal.get_employee_changes_for_task(task_id)
    employee_change_schemes = [
        EmployeeChangeScheme.from_orm(ec) for ec in employee_changes
    ]

    status_changes = await task_dal.get_status_changes_for_task(task_id)
    status_change_schemes = [StatusChangeScheme.from_orm(sc) for sc in status_changes]

    related_object_schemes = (
        comment_schemes + employee_change_schemes + status_change_schemes
    )
    related_object_schemes.sort(key=lambda obj: obj.creation)

    return related_object_schemes


@router.get("/{task_id}/events", response_model=typing.Sequence[EventScheme])
async def get_all_events_for_task(
    task_id: int, task_dal: TaskDAL = Depends(get_db_dal_by_type(TaskDAL))
) -> typing.Sequence[EventScheme]:
    events = await task_dal.get_all_events_for_task(task_id)
    return [EventScheme.from_orm(event) for event in events]


@router.post("/{task_id}/{employee_id}/events/comments", response_model=CommentScheme)
async def create_event_comment(
    task_id: int,
    employee_id: int,
    comment_data: CommentCreateScheme,
    task_dal: TaskDAL = Depends(get_db_dal_by_type(TaskDAL)),
) -> CommentScheme:
    comment = await task_dal.create_event_comment_with_event(
        task_id, employee_id, comment_data
    )
    return CommentScheme.from_orm(comment)


@router.post(
    "/{task_id}/{employee_id}/events/employee-changes",
    response_model=EmployeeChangeScheme,
)
async def create_event_employee_change(
    task_id: int,
    employee_id: int,
    employee_change_data: EmployeeChangeCreateScheme,
    task_dal: TaskDAL = Depends(get_db_dal_by_type(TaskDAL)),
) -> EmployeeChangeScheme:
    employee_change = await task_dal.create_event_employee_change_with_event(
        task_id, employee_id, employee_change_data
    )
    return EmployeeChangeScheme.from_orm(employee_change)


@router.post(
    "/{task_id}/{employee_id}/events/status-changes", response_model=StatusChangeScheme
)
async def create_event_status_change(
    task_id: int,
    employee_id: int,
    status_change_data: StatusChangeCreateScheme,
    task_dal: TaskDAL = Depends(get_db_dal_by_type(TaskDAL)),
) -> StatusChangeScheme:
    status_change = await task_dal.create_event_status_change_with_event(
        task_id, employee_id, status_change_data
    )
    return StatusChangeScheme.from_orm(status_change)
