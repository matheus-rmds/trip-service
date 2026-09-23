import httpx
from typing import List
from fastapi import Depends, FastAPI, HTTPException, Path
from sqlmodel import Session, select
from .database import get_session, init_db
from .models import Trip, TripCreate, TripUpdate
from .weather import geocode_city, get_forecast, choose_best_day, generate_packing_suggestion

app = FastAPI(title="TravelPlan - Trip Service")

@app.on_event("startup")
def on_startup() -> None:
    init_db()

@app.get("/health")
def health():
    return {"status": "ok"}

async def _build_trip_plan(city: str, start_date, end_date) -> dict:
    try:
        lat, lon = await geocode_city(city)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

    try:
        daily = await get_forecast(lat, lon, start_date, end_date)
    except httpx.HTTPStatusError:
        raise HTTPException(
            status_code=400,
            detail="Não foi possível obter a previsão para essas datas. "
                   "A Open-Meteo cobre apenas os próximos 16 dias a partir do dia atual.",
        )

    info = choose_best_day(daily)
    info["packing_suggestion"] = generate_packing_suggestion(info)
    return info

@app.post("/trips", response_model=Trip)
async def create_trip(trip_in: TripCreate, session: Session = Depends(get_session)):
    info = await _build_trip_plan(trip_in.city, trip_in.start_date, trip_in.end_date)

    trip = Trip(
        city=trip_in.city,
        start_date=trip_in.start_date,
        end_date=trip_in.end_date,
        best_day=info["best_day"],
        rain_chance=info["rain_chance"],
        packing_suggestion=info["packing_suggestion"],
    )
    session.add(trip)
    session.commit()
    session.refresh(trip)
    return trip

@app.get("/trips", response_model=List[Trip])
def list_trips(session: Session = Depends(get_session)):
    return session.exec(select(Trip)).all()

@app.get("/trips/{trip_id}", response_model=Trip)
def get_trip(
    trip_id: int = Path(..., examples=[1]),
    session: Session = Depends(get_session),
):
    trip = session.get(Trip, trip_id)
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    return trip

@app.put("/trips/{trip_id}", response_model=Trip)
async def update_trip(
    trip_in: TripUpdate,
    trip_id: int = Path(..., examples=[1]),
    session: Session = Depends(get_session),
):
    trip = session.get(Trip, trip_id)
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")

    data = trip_in.dict(exclude_unset=True)
    for field, value in data.items():
        setattr(trip, field, value)

    info = await _build_trip_plan(trip.city, trip.start_date, trip.end_date)
    trip.best_day = info["best_day"]
    trip.rain_chance = info["rain_chance"]
    trip.packing_suggestion = info["packing_suggestion"]

    session.add(trip)
    session.commit()
    session.refresh(trip)
    return trip

@app.delete("/trips/{trip_id}")
def delete_trip(
    trip_id: int = Path(..., examples=[1]),
    session: Session = Depends(get_session),
):
    trip = session.get(Trip, trip_id)
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    session.delete(trip)
    session.commit()
    return {"ok": True}
