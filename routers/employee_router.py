from fastapi import APIRouter, Depends
from db.dal.dals import EmployeeDAL
from dependencies.db import get_db_dal_by_type
from schemas.schemas import EmployeeScheme, EmployeeCreateScheme, EmployeeUpdateScheme

router = APIRouter(prefix="/employees", tags=["employees"])


@router.get("/{id}")
async def get_employee_by_id(
    id: int, employee_dal: EmployeeDAL = Depends(get_db_dal_by_type(EmployeeDAL))
) -> EmployeeScheme | None:
    return EmployeeScheme.from_orm(await employee_dal.get_by_id_with_exception(id))


@router.get("")
async def get_employees(
    employee_dal: EmployeeDAL = Depends(get_db_dal_by_type(EmployeeDAL))
) -> list[EmployeeScheme]:
    return [EmployeeScheme.from_orm(employee) for employee in await employee_dal.get_all()]


@router.post("")
async def create_employee(
    employee: EmployeeCreateScheme,
    employee_dal: EmployeeDAL = Depends(get_db_dal_by_type(EmployeeDAL))
) -> EmployeeScheme:
    return EmployeeScheme.from_orm(await employee_dal.create_from_api(employee))


@router.put("/{id}")
async def update_employee(
    id: int,
    employee: EmployeeUpdateScheme,
    employee_dal: EmployeeDAL = Depends(get_db_dal_by_type(EmployeeDAL))
) -> EmployeeScheme | None:
    return EmployeeScheme.from_orm(await employee_dal.update_by_id_with_exception(id, employee))


@router.delete("/{id}")
async def delete_employee(
    id: int,
    employee_dal: EmployeeDAL = Depends(get_db_dal_by_type(EmployeeDAL))
) -> None:
    await employee_dal.remove_by_id_from_api(id)
