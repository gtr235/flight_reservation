from fastapi_utils.inferring_router import InferringRouter
from starlette.responses import RedirectResponse
from typing import List
from flight_reservation_api.enums.status import Status
from fastapi.responses import JSONResponse
from flight_reservation_api.models.response import Status as ResponseStatus
from flight_reservation_api.models.flight import Flight, Flights, Seats
import datetime


def read_flight_text() -> Flights:
    with open("flight_reservation_api/flights.txt") as reader:
        data = reader.readlines()
        flights: Flights = Flights()
        flight_id: int = 1
        for line in data:
            flights_string_list: List = line.replace(" ", "").split()
            flight = Flight(
                off=flights_string_list[0],
                to=flights_string_list[1],
                date=flights_string_list[2],
                departure=flights_string_list[3],
                arrival=flights_string_list[4],
                available=int(flights_string_list[5]),
                id=flight_id
            )
            flights.flights.append(flight)
            flight_id += 1
        return flights


"""
router with its .get and .post routes below.
include this router in a fastapi instance.
"""
router: InferringRouter = InferringRouter()
flight_data: Flights = read_flight_text()


@router.get(
    "/",
    summary="Home Page"
)
async def home():
    response: RedirectResponse = RedirectResponse(url="/docs")  # redirect to interface
    return response


@router.get(
    "/flights",
    summary="Returns all available flights"
)
async def available():
    flight_availability_data = Flights()
    for flight in flight_data.flights:
        if flight.available:
            flight_availability_data.flights.append(flight)
    return flight_availability_data


@router.get(
    "/flight/{f_id}",
    summary="Return one flight with this id"
)
async def get_flight(f_id: int):
    return flight_data.flights[f_id-1]


@router.put(
    "/search",
    summary="Return the available flights"
)
def search(searched_flight: Flight):
    flights: Flights = Flights()
    for flight in flight_data.flights:
        if flight.to == searched_flight.to.replace(" ", "") and flight.off == searched_flight.off.replace(" ", ""):
            if flight.date == searched_flight.date:
                flights.flights.append(flight)
    return flights


@router.put(
    "/reserve/{f_id}",
    summary="Return the status of reservation"
)
def reserve_flight(f_id: int, seats: Seats):
    response = ResponseStatus()
    try:
        current_flight = flight_data.flights[f_id-1]
        if seats.numberOfSeats > current_flight.available:
            raise Exception("number of seats is not available")
        else:
            current_flight.available -= seats.numberOfSeats
            response.status = Status.SUCCESSFUL
            return response
    except Exception as e:
        response.status = Status.UNSUCCESSFUL
        response.reason = str(e)
        return response







