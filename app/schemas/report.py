# app/schemas/report.py
from typing import Dict, Optional

from pydantic import BaseModel


class ReportSummary(BaseModel):
    total_calculations: int
    counts_by_type: Dict[str, int]
    average_a: Optional[float] = None
    average_b: Optional[float] = None
    most_used_type: Optional[str] = None
    last_calculation_id: Optional[int] = None
