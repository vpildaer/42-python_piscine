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


def ft_plant_factory(name: str, height: float, age: int) -> Plant:
    return Plant(name, height, age)


if __name__ == "__main__":
    print("=== Plant Factory Output ===")
    plants: list[tuple[str, float, int]] = [("Rose", 25, 30),
                                            ("Oak", 200, 365),
                                            ("Cactus", 5, 90),
                                            ("Sunflower", 80, 45),
                                            ("Fern", 15, 120)]
    factory: list[Plant] = [ft_plant_factory(i[0], i[1], i[2]) for i in plants]
    for i in factory:
        print(f"Created: {i.name}: {i.height:.1f}cm, {i.days} days old")
