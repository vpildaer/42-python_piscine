from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ValidationError


class SpaceStation(BaseModel):

    station_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=1, max_length=50)
    crew_size: int = Field(ge=1, le=20)
    power_level: float = Field(ge=0.0, le=100.0)
    oxygen_level: float = Field(ge=0.0, le=100.0)
    last_maintenance: datetime
    is_operational: bool = Field(default=True)
    notes: Optional[str] = Field(max_length=200, default=None)


def main() -> None:

    valid_space_station = SpaceStation(station_id="ISS001",
                                       name="International Space Station",
                                       crew_size=6,
                                       power_level=85.5,
                                       oxygen_level=92.3,
                                       last_maintenance=datetime.now(),
                                       is_operational=True)

    print("Space Station Data Validation")
    print("========================================")
    print("Valid station created:")
    print(f"ID: {valid_space_station.station_id}")
    print(f"Name: {valid_space_station.name}")
    print(f"Crew: {valid_space_station.crew_size} people")
    print(f"Power: {valid_space_station.power_level}%")
    print(f"Oxygen: {valid_space_station.oxygen_level}%")
    if valid_space_station.is_operational:
        print("Status: Operational")
    else:
        print("Status: Not Operational")

    print("\n========================================")

    try:
        SpaceStation(station_id="ISS999",
                     name="Invalid Station",
                     crew_size=65,
                     power_level=0.0,
                     oxygen_level=100,
                     last_maintenance=datetime.now(),
                     is_operational=False,
                     notes="invalid space station")

    except ValidationError as e:
        print("Expected validation error:")
        print(e.errors()[0]['msg'])


if __name__ == "__main__":
    try:
        main()
    except ValidationError as e:
        print(e.errors()[0]['msg'])
    except Exception as e:
        print(e)
