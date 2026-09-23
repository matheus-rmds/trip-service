from datetime import date, timedelta
from typing import Optional
from sqlmodel import SQLModel, Field

_example_start = (date.today() + timedelta(days=3)).isoformat()
_example_end = (date.today() + timedelta(days=5)).isoformat()

class TripBase(SQLModel):
    city: str
    start_date: date
    end_date: date

class Trip(TripBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    best_day: Optional[date] = None
    rain_chance: Optional[float] = None
    packing_suggestion: Optional[str] = None

class TripCreate(TripBase):
    model_config = {
        "json_schema_extra": {
            "example": {
                "city": "Rio de Janeiro",
                "start_date": _example_start,
                "end_date": _example_end,
            }
        }
    }

class TripUpdate(SQLModel):
    city: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None

    model_config = {
        "json_schema_extra": {
            "example": {
                "city": "São Paulo",
                "start_date": _example_start,
                "end_date": _example_end,
            }
        }
    }
