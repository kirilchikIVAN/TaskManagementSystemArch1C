from fastapi import FastAPI

from exceptions.base import ServiceExceptionBase
from exceptions.handlers import service_exception_handler
from routers import users
from utils.meta import ProjectMeta, project_info

app = FastAPI(
    title=project_info.name,
    description=project_info.description,
    version=project_info.version,
)
app.add_exception_handler(ServiceExceptionBase, service_exception_handler)
app.include_router(users.router)


@app.get("/")
def home() -> ProjectMeta:
    return project_info
