from fastapi import APIRouter, Depends
from db.dal.dals import ReportDAL, ReportPartDAL
from dependencies.db import get_db_dal_by_type
from schemas.schemas import ReportScheme, ReportCreateScheme, ReportUpdateScheme, ReportPartScheme, \
    ReportPartCreateScheme

router = APIRouter(prefix="/reports", tags=["reports"])


@router.get("/{id}")
async def get_report_by_id(
    id: int, report_dal: ReportDAL = Depends(get_db_dal_by_type(ReportDAL))
) -> ReportScheme | None:
    return ReportScheme.from_orm(await report_dal.get_by_id_with_exception(id))


@router.get("/{id}/parts")
async def get_report_parts(
        id: int, report_dal: ReportDAL = Depends(get_db_dal_by_type(ReportDAL))
) -> list[ReportPartScheme] | None:
    report = await report_dal.get_full_by_id_with_exception(id)
    if report is None:
        return None

    return [ReportPartScheme.from_orm(report_part) for report_part in report.parts]


@router.get("")
async def get_reports(
    report_dal: ReportDAL = Depends(get_db_dal_by_type(ReportDAL))
) -> list[ReportScheme]:
    return [ReportScheme.from_orm(report) for report in await report_dal.get_all()]


@router.post("")
async def create_report(
    report: ReportCreateScheme,
    report_dal: ReportDAL = Depends(get_db_dal_by_type(ReportDAL))
) -> ReportScheme:
    return ReportScheme.from_orm(await report_dal.create_from_api(report))


@router.post("/{report_id}/add_report_part")
async def create_report_part(
    report_id: int,
    report_part: ReportPartCreateScheme,
    report_dal: ReportPartDAL = Depends(get_db_dal_by_type(ReportPartDAL))
) -> ReportPartScheme:
    report = await report_dal.get_by_id_with_exception(report_id)
    return ReportPartScheme.from_orm(await report_dal.create_from_api(report_part))


@router.put("/{id}")
async def update_report(
    id: int,
    report: ReportUpdateScheme,
    report_dal: ReportDAL = Depends(get_db_dal_by_type(ReportDAL))
) -> ReportScheme | None:
    return ReportScheme.from_orm(await report_dal.update_by_id_with_exception(id, report))


@router.delete("/{id}")
async def delete_report(
    id: int,
    report_dal: ReportDAL = Depends(get_db_dal_by_type(ReportDAL))
) -> None:
    await report_dal.remove_by_id_from_api(id)
