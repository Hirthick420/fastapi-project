# app/routers/reports.py
from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.models.calculation import Calculation
from app.schemas.calculation import CalculationRead
from app.schemas.report import ReportSummary

router = APIRouter(prefix="/reports", tags=["reports"])


@router.get("/summary", response_model=ReportSummary)
def get_summary(db: Session = Depends(get_db)) -> ReportSummary:
    # Total calculations
    total = db.query(func.count(Calculation.id)).scalar() or 0

    # Counts per type
    rows = (
        db.query(Calculation.type, func.count(Calculation.id))
        .group_by(Calculation.type)
        .all()
    )
    counts_by_type = {row[0]: row[1] for row in rows}

    # Averages
    avg_a, avg_b = db.query(
        func.avg(Calculation.a), func.avg(Calculation.b)
    ).one()
    average_a = float(avg_a) if avg_a is not None else None
    average_b = float(avg_b) if avg_b is not None else None

    # Most used type
    most_used_type = None
    if counts_by_type:
        most_used_type = max(counts_by_type.items(), key=lambda kv: kv[1])[0]

    # Last calculation (by id)
    last_calc = (
        db.query(Calculation)
        .order_by(Calculation.id.desc())
        .first()
    )
    last_id = last_calc.id if last_calc else None

    return ReportSummary(
        total_calculations=int(total),
        counts_by_type=counts_by_type,
        average_a=average_a,
        average_b=average_b,
        most_used_type=most_used_type,
        last_calculation_id=last_id,
    )


@router.get("/recent", response_model=List[CalculationRead])
def get_recent_calculations(
    limit: int = 10,
    db: Session = Depends(get_db),
) -> list[Calculation]:
    limit = max(1, min(limit, 100))  # clamp 1–100
    items = (
        db.query(Calculation)
        .order_by(Calculation.id.desc())
        .limit(limit)
        .all()
    )
    # return newest first is fine; or reversed(items) if you want oldest→newest
    return items
