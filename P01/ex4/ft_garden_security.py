#!/usr/bin/env python3

class Plant:

    def __init__(self, name: str, height: float, days: int) -> None:
        self.name = name
        self._height = 0.0
        self._days = 0
        self.growth_rate = round(height / days, 1)
        self.set_height(height)
        self.set_age(days)

    def show(self) -> str:
        return f"{self.name}: {self._height:.1f}cm, {self._days} days old"

    def grow(self) -> None:
        self._height += self.growth_rate

    def age(self) -> None:
        self._days += 1

    def set_height(self, new_height: float) -> None:
        if new_height < 0:
            print(f"{self.name}: Error, height can't be negative")
        else:
            self._height = new_height

    def set_age(self, new_age: int) -> None:
        if new_age < 0:
            print(f"{self.name}: Error, age can't be negative")
        elif new_age > 1800000:
            print(f"{self.name}: Error, age is too big")
        else:
            self._days = new_age

    def get_height(self) -> float:
        return self._height

    def get_age(self) -> int:
        return self._days


def ft_garden_security(name: str, height: float, days: int) -> Plant:
    return Plant(name, height, days)


if __name__ == "__main__":

    def test_new_height(plant: Plant, new_height: float) -> None:
        plant.set_height(new_height)
        test_height: float = plant.get_height()
        if test_height == new_height:
            print(f"Height updated: {new_height}cm")
        else:
            print("Height update rejected")

    def test_new_age(plant: Plant, new_age: int) -> None:
        plant.set_age(new_age)
        test_age: int = plant.get_age()
        if test_age == new_age:
            print(f"Age updated: {new_age} days")
        else:
            print("Age update rejected")

    print("=== Garden Security System ===")
    plant1 = ft_garden_security("Rose", 15, 10)
    print(f"Plant created: {plant1.show()}\n")
    test_new_height(plant1, 25)
    test_new_age(plant1, 30)
    print("")
    test_new_height(plant1, -1)
    test_new_age(plant1, -1)
    print("")
    print(f"Current state: {plant1.show()}")
