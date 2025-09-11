# core/models.py
from pydantic import BaseModel, validator, Field
from typing import Optional, Dict, Any
from datetime import datetime
import json


class ProjectHisModel(BaseModel):
    name: str
    client_name: str
    project_type: Optional[str] = None
    area_sqm: Optional[float] = None
    location_city: Optional[str] = None
    total_heating_load_kw: Optional[float] = None
    total_cooling_load_kw: Optional[float] = None
    system_type: Optional[str] = None
    selected_products: Optional[Dict[str, Any]] = None
    total_cost_cny: Optional[float] = None
    annual_energy_consumption_kwh: Optional[float] = None
    solution_summary: Optional[str] = None
    file_attachments: Optional[Dict[str, Any]] = None
    success_rating: Optional[int] = Field(None, ge=1, le=5)  # 1~5 分
    create_at: datetime = Field(default_factory=datetime.now)

    @validator("selected_products", "file_attachments", pre=True)
    def validate_json_fields(cls, v):
        if isinstance(v, str):
            if not v.strip():
                return None
            try:
                return json.loads(v)
            except json.JSONDecodeError:
                raise ValueError("JSON 格式错误")
        return v

    class Config:
        arbitrary_types_allowed = True
