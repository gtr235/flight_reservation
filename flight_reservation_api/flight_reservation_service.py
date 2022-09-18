from fastapi import FastAPI
from flight_reservation_api.router import router as flight_router
import uvicorn
from fastapi.middleware.cors import CORSMiddleware


class FlightReservationService:
    def __init__(self):
        self.api: FastAPI = FastAPI(
            title="Flight reservation system",
            description="Helps people with flight reservations"
        )
        self.api.include_router(flight_router)
        self.api.add_middleware(
            CORSMiddleware,
            allow_origins=["http://localhost:3000"], #allow frontend to connect
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"], )

        self._run_uvicorn()

    def _run_uvicorn(self) -> None:
        uvicorn.run(self.api, host="0.0.0.0", port=8888)

    def get_api(self) -> FastAPI:
        return self.api
