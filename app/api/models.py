from pydantic import BaseModel
from typing import Optional, List, Dict, Any

class Query(BaseModel):
    text: str

class Response(BaseModel):
    answer: str
    sources: Optional[List[Dict[str, Any]]] = None
    additional_info: Optional[Dict[str, Any]] = None

class SummaryStats(BaseModel):
    total_orders: int
    total_suppliers: int
    total_departments: int
    total_spend: str