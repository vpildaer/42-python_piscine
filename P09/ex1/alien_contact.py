from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ValidationError, model_validator
from enum import Enum


class ContactType(Enum):

    radio = "radio"
    visual = "visual"
    physical = "physical"
    telepathic = "telepathic"


class AlienContact(BaseModel):

    contact_id: str = Field(min_length=5, max_length=15)
    timestamp: datetime
    location: str = Field(min_length=3, max_length=100)
    contact_type: ContactType
    signal_strength: float = Field(ge=0.0, le=10.0)
    duration_minutes: int = Field(ge=1, le=1440)
    witness_count: int = Field(ge=1, le=100)
    message_received: Optional[str] = Field(max_length=500, default=None)
    is_verified: bool = Field(default=False)

    @model_validator(mode='after')
    def alien_validator(self) -> 'AlienContact':

        if not (self.contact_id.startswith("AC")):
            raise ValueError('Contact ID must start with "AC"')

        if self.contact_type.value == "physical" and \
                not self.is_verified:
            raise ValueError("Physical contact reports must be verified")

        if self.contact_type.value == "telepathic" and self.witness_count < 3:
            raise ValueError("Telepathic contact requires "
                             "at least 3 witnesses")

        if self.signal_strength > 7.0 and self.message_received is None:
            raise ValueError("Strong signals (> 7.0) should "
                             "include received messages")

        return self


def main() -> None:

    valid_ac = AlienContact(contact_id="AC_2024_001",
                            timestamp=datetime.now(),
                            location="Area 51, Nevada",
                            contact_type=ContactType.radio,
                            signal_strength=8.5,
                            duration_minutes=45,
                            witness_count=5,
                            message_received="Greetings from Zeta Reticuli",
                            is_verified=True)

    print("Alien Contact Log Validation")
    print("======================================")
    print("Valid contact report:")
    print(f"ID: {valid_ac.contact_id}")
    print(f"Type: {valid_ac.contact_type.value}")
    print(f"Location: {valid_ac.location}")
    print(f"Signal: {valid_ac.signal_strength}/10")
    print(f"Duration: {valid_ac.duration_minutes} minutes")
    print(f"Witnesses: {valid_ac.witness_count}")
    print(f"Message: {valid_ac.message_received}")
    print("\n=====================================")

    try:
        AlienContact(contact_id="AC_2024_001",
                     timestamp=datetime.now(),
                     location="Area 51, Nevada",
                     contact_type=ContactType.telepathic,
                     signal_strength=8.5,
                     duration_minutes=45,
                     witness_count=2,
                     message_received="hello world!",
                     is_verified=False)
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
