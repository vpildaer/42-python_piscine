#!/usr/bin/env python3

class GardenError(Exception):

    def __str__(self) -> str:
        return "Unknown garden error"


class PlantError(GardenError):

    def __init__(self, plant: str, message: str = "Unknown plant error") \
                -> None:
        self.plant = plant
        self.message = message

    def __str__(self) -> str:
        return f"{self.message}"


class WaterError(GardenError):

    def __init__(self, message: str = "Unknown water error") -> None:
        self.message = message

    def __str__(self) -> str:
        return f"{self.message}"


def water_plant(plant_name: str) -> None:
    if plant_name != plant_name.capitalize():
        raise PlantError(plant_name,
                         f"Invalid plant name to water: '{plant_name}'")
    else:
        print(f"Watering {plant_name}: [OK]")


def test_watering_system(plants: list[str]) -> None:
    print("Opening watering system")
    try:
        for i in plants:
            water_plant(i)
    except PlantError as e:
        print(f"Caught PlantError: {e}")
        print(".. ending tests and returning to main")
        return
    finally:
        print("Closing watering system\n")


if __name__ == "__main__":
    plants_ok: list[str] = ["Tomato", "Lettuce", "Carrots"]
    plants_fail: list[str] = ["Tomato", "lettuce", "Carrots"]
    print("=== Garden Watering System ===\n")
    print("Testing valid plants...")
    test_watering_system(plants_ok)
    print("Testing invalid plants...")
    test_watering_system(plants_fail)
    print("Cleanup always happens, even with errors!")
