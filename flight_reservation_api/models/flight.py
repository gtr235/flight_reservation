from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List


class Flight(BaseModel):
    off: Optional[str]
    to: Optional[str]
    date: Optional[str]
    departure: Optional[str]
    arrival: Optional[str]
    available: Optional[int]
    id: int


class Flights(BaseModel):
    flights: List[Flight] = []


class Seats(BaseModel):
    numberOfSeats: int



