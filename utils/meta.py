import tomllib
from pydantic import BaseModel


class ProjectMeta(BaseModel):
    name: str
    description: str
    version: str


def parse_from_toml(filename: str = "pyproject.toml") -> ProjectMeta:
    with open(filename, "rb") as fd:
        data = tomllib.load(fd)
    return ProjectMeta(
        name=data["tool"]["poetry"]["name"],
        description=data["tool"]["poetry"]["description"],
        version=data["tool"]["poetry"]["version"],
    )


project_info = parse_from_toml()
