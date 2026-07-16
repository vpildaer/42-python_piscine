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


class Plant:

    def __init__(self, name: str, days: int,
                 water_needs: int, last_water: int) -> None:
        self.name = name
        self.days = days
        self.water_needs = water_needs
        self.last_water = last_water

    def age(self) -> None:
        self.days += 1
        self.last_water += 1
        if self.last_water > 5:
            raise PlantError(self.name, f"The {self.name} plant is wilting!")


class WaterTank:

    def __init__(self, current_level: int, max_capacity: int) -> None:
        self.current_level = current_level
        self.max_capacity = max_capacity


def ft_water_plant(plant: Plant, tank: WaterTank) -> None:
    tank.current_level -= plant.water_needs
    if tank.current_level < 0:
        raise WaterError("Not enough water in the tank!")
    plant.last_water = 0


def ft_custom_errors() -> None:
    plant = Plant("tomato", 20, 4, 5)
    tank = WaterTank(3, 1000)
    print("Testing PlantError...")
    try:
        plant.age()
    except PlantError as e:
        print(f"Caught PlantError: {e}")
    print("\nTesting WaterError...")
    try:
        ft_water_plant(plant, tank)
    except WaterError as e:
        print(f"Caught WaterError: {e}")
    print("\nTesting catching all garden errors...")
    try:
        plant.age()
    except GardenError as e:
        print(f"Caught GardenError: {e}")
    try:
        ft_water_plant(plant, tank)
    except GardenError as e:
        print(f"Caught GardenError: {e}")


if __name__ == "__main__":
    print("=== Custom Garden Errors Demo ===\n")
    ft_custom_errors()
    print("\nAll custom error types work correctly")
