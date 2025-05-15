from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from database.connect import get_db
from schemas.report import ReportCreate, ReportUpdate, ReportOut
from database import crud as crud_report

router = APIRouter(prefix="/reports", tags=["Reports"])


@router.get("/", response_model=list[ReportOut])
async def list_reports(db: AsyncSession = Depends(get_db)):
    return await crud_report.get_reports(db)


@router.get("/{report_id}", response_model=ReportOut)
async def get_report(report_id: int, db: AsyncSession = Depends(get_db)):
    report = await crud_report.get_report(db, report_id)
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    return report


@router.post("/", response_model=ReportOut)
async def create_report(data: ReportCreate, db: AsyncSession = Depends(get_db)):
    return await crud_report.create_report(db, data)


@router.put("/{report_id}", response_model=ReportOut)
async def update_report(report_id: int, data: ReportUpdate, db: AsyncSession = Depends(get_db)):
    updated = await crud_report.update_report(db, report_id, data)
    if not updated:
        raise HTTPException(status_code=404, detail="Report not found")
    return updated


@router.delete("/{report_id}")
async def delete_report(report_id: int, db: AsyncSession = Depends(get_db)):
    success = await crud_report.delete_report(db, report_id)
    if not success:
        raise HTTPException(status_code=404, detail="Report not found")
    return {"ok": True}
