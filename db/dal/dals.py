from db.dal.base import BaseDAL
from db.models.models import *
from schemas.schemas import *


class EmployeeDAL(BaseDAL[Employee, EmployeeCreateScheme, EmployeeUpdateScheme]):
    model = Employee
    readable_object_name = "EmployeeDAL"


class TaskDAL(BaseDAL[Task, TaskCreateScheme, TaskUpdateScheme]):
    model = Task
    readable_object_name = "TaskDAL"


class EmployeeTaskDAL(BaseDAL[EmployeeTask, EmployeeTaskCreateScheme, EmployeeTaskUpdateScheme]):
    model = EmployeeTask
    readable_object_name = "EmployeeTaskDAL"


class EventDAL(BaseDAL[Event, EventCreateScheme, EventUpdateScheme]):
    model = Event
    readable_object_name = "EventDAL"


class CommentDAL(BaseDAL[Comment, CommentCreateScheme, CommentUpdateScheme]):
    model = Comment
    readable_object_name = "CommentDAL"


class EmployeeChangeDAL(BaseDAL[EmployeeChange, EmployeeChangeCreateScheme, EmployeeChangeUpdateScheme]):
    model = EmployeeChange
    readable_object_name = "EmployeeChangeDAL"


class StatusChangeDAL(BaseDAL[StatusChange, StatusChangeCreateScheme, StatusChangeUpdateScheme]):
    model = StatusChange
    readable_object_name = "StatusChangeDAL"


class ReportDAL(BaseDAL[Report, ReportCreateScheme, ReportUpdateScheme]):
    model = Report
    readable_object_name = "ReportDAL"


class ReportPartDAL(BaseDAL[ReportPart, ReportPartCreateScheme, ReportPartUpdateScheme]):
    model = ReportPart
    readable_object_name = "ReportPartDAL"
