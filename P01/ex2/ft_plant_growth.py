#!/usr/bin/env python3

class Plant:

    def __init__(self, name: str, height: float, days: int) -> None:
        self.name = name
        self.height = height
        self.days = days
        self.growth_rate = round(height / days, 1)

    def show(self) -> None:
        print(f"{self.name}: {round(self.height, 1)}cm, {self.days} days old")

    def grow(self) -> None:
        self.height += self.growth_rate

    def age(self) -> None:
        self.days += 1


def ft_plant_growth() -> None:
    plant1 = Plant("Rose", 25, 30)
    # plant2 = Plant("Sunflower", 80, 45)
    # plant3 = Plant("Cactus", 15, 120)
    initial_height: float = plant1.height
    plant1.show()
    for i in range(1, 8):
        print(f"=== Day {i} ===")
        plant1.grow()
        plant1.age()
        plant1.show()
    print(f"Growth this week: {round(plant1.height - initial_height, 1)}cm")


if __name__ == "__main__":
    print("=== Garden Plant Growth ===")
    ft_plant_growth()
