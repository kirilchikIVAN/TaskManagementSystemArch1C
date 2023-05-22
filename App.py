from fastapi import FastAPI

from exceptions.base import ServiceExceptionBase
from exceptions.handlers import service_exception_handler
from routers import employee_router, report_router, task_router
from utils.meta import ProjectMeta, project_info

app = FastAPI(
    title=project_info.name,
    description=project_info.description,
    version=project_info.version,
)
app.add_exception_handler(ServiceExceptionBase, service_exception_handler)
app.include_router(employee_router.router)
app.include_router(task_router.router)
app.include_router(report_router.router)


@app.get("/")
def home() -> ProjectMeta:
    return project_info
