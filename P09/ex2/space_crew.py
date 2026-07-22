from datetime import datetime
from pydantic import BaseModel, Field, ValidationError, model_validator
from enum import Enum


class Rank(Enum):

    cadet = "cadet"
    officer = "officer"
    lieutenant = "lieutenant"
    captain = "captain"
    commander = "commander"


class CrewMember(BaseModel):

    member_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=2, max_length=50)
    rank: Rank
    age: int = Field(ge=18, le=80)
    specialization: str = Field(min_length=3, max_length=30)
    years_experience: int = Field(ge=0, le=50)
    is_active: bool = Field(default=True)


class SpaceMission(BaseModel):

    mission_id: str = Field(min_length=5, max_length=15)
    mission_name: str = Field(min_length=3, max_length=100)
    destination: str = Field(min_length=3, max_length=50)
    launch_date: datetime
    duration_days: int = Field(ge=1, le=3650)
    crew: list[CrewMember] = Field(min_length=1, max_length=12)
    mission_status: str = Field(default="planned")
    budget_millions: float = Field(ge=1.0, le=10000.0)

    @model_validator(mode='after')
    def mission_validator(self) -> 'SpaceMission':

        if not self.mission_id.startswith("M"):
            raise ValueError('Mission ID must start with "M"')

        if not any(member.rank == Rank.commander or
                   member.rank == Rank.captain for member in self.crew):
            raise ValueError("Must have at least one Commander or Captain")

        if self.duration_days > 365:
            if (sum(member.years_experience >= 5 for member in self.crew) <
                    (len(self.crew) / 2)):
                raise ValueError("Long missions (> 365 days) need 50% "
                                 "experienced crew (5+ years)")

        if any(not member.is_active for member in self.crew):
            raise ValueError("All crew members must be active")

        return self


def get_valid_crew() -> list[CrewMember]:

    return [CrewMember(member_id="sconnor",
                       name="Sarah Connor",
                       rank=Rank.commander,
                       age=55,
                       specialization="Mission Command",
                       years_experience=20,
                       is_active=True),
            CrewMember(member_id="jsmith",
                       name="John Smith",
                       rank=Rank.lieutenant,
                       age=45,
                       specialization="Navigation",
                       years_experience=15,
                       is_active=True),
            CrewMember(member_id="ajohnson",
                       name="Alice Johnson",
                       rank=Rank.officer,
                       age=35,
                       specialization="Engineering",
                       years_experience=10,
                       is_active=True)]


def get_invalid_crew() -> list[CrewMember]:

    return [CrewMember(member_id="sconnor",
                       name="Sarah Connor",
                       rank=Rank.officer,
                       age=55,
                       specialization="Mission Command",
                       years_experience=20,
                       is_active=True),
            CrewMember(member_id="jsmith",
                       name="John Smith",
                       rank=Rank.lieutenant,
                       age=45,
                       specialization="Navigation",
                       years_experience=15,
                       is_active=True),
            CrewMember(member_id="ajohnson",
                       name="Alice Johnson",
                       rank=Rank.cadet,
                       age=35,
                       specialization="Engineering",
                       years_experience=10,
                       is_active=True)]


def main() -> None:

    space_mission = SpaceMission(mission_id="M2024_MARS",
                                 mission_name="Mars Colony Establishment",
                                 destination="Mars",
                                 launch_date=datetime.now(),
                                 duration_days=900,
                                 crew=get_valid_crew(),
                                 mission_status="active",
                                 budget_millions=2500.0)

    print("Space Mission Crew Validation")
    print("=========================================")
    print("Valid mission created:")
    print(f"Mission: {space_mission.mission_name}")
    print(f"ID: {space_mission.mission_id}")
    print(f"Destination: {space_mission.destination}")
    print(f"Duration: {space_mission.duration_days} days")
    print(f"Budget: ${space_mission.budget_millions}M")
    print(f"Crew size: {len(space_mission.crew)}")

    print("Crew members:")

    for member in space_mission.crew:
        print(f"- {member.name} ({member.rank.value}) - "
              f"{member.specialization}")

    print("\n=========================================")

    try:
        SpaceMission(mission_id="M2024_MARS",
                     mission_name="Mars Colony",
                     destination="Mars",
                     launch_date=datetime.now(),
                     duration_days=900,
                     crew=get_invalid_crew(),
                     mission_status="active",
                     budget_millions=2500.0)
    except ValidationError as e:
        print("Expected validation error:")
        print(e.errors()[0]['msg'].removeprefix("Value error, "))


if __name__ == "__main__":
    try:
        main()
    except ValidationError as e:
        print(e.errors()[0]['msg'])
    except Exception as e:
        print(e)
