from datetime import date
from typing import Optional
from sqlmodel import SQLModel, Field

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
    pass

class TripUpdate(SQLModel):
    city: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
