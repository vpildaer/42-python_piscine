#!/usr/bin/env python3

class Plant:

    def __init__(self, name: str, height: float, days: int) -> None:
        self.name = name
        self._height = 0.0
        self._days = 0
        self.growth_rate = round(height / days, 1)
        self.set_height(height)
        self.set_age(days)

    def show(self) -> None:
        print(f"{self.name.capitalize()}: "
              f"{self._height:.1f}cm, {self._days} days old")

    def grow(self) -> None:
        self._height += self.growth_rate

    def age(self) -> None:
        self._days += 1

    def set_height(self, new_height: float) -> None:
        if new_height < 0:
            print(f"{self.name.capitalize()}: Error, height can't be negative")
        else:
            self._height = new_height

    def set_age(self, new_age: int) -> None:
        if new_age < 0:
            print(f"{self.name.capitalize()}: Error, age can't be negative")
        elif new_age > 1800000:
            print(f"{self.name.capitalize()}: Error, age is too big")
        else:
            self._days = new_age

    def get_height(self) -> float:
        return self._height

    def get_age(self) -> int:
        return self._days


class Flower(Plant):

    def __init__(self, name: str, height: float, days: int,
                 color: str) -> None:
        super().__init__(name, height, days)
        self.color = color
        self.bloomed = False

    def bloom(self) -> None:
        print(f"[asking the {self.name} to bloom]")
        self.bloomed = True

    def show(self) -> None:
        super().show()
        print(f" Color: {self.color}")
        if self.bloomed:
            print(f" {self.name.capitalize()} is blooming beautifully!")
        else:
            print(f" {self.name.capitalize()} has not bloomed yet")


class Tree(Plant):

    def __init__(self, name: str, height: float, days: int,
                 trunk_diameter: float) -> None:
        super().__init__(name, height, days)
        self.trunk_diameter = trunk_diameter

    def produce_shade(self) -> None:
        print(f"[asking the {self.name} to produce shade]")
        print(f"Tree {self.name.capitalize()} now produces a shade of "
              f"{self._height:.1f}cm"
              f" long and {self.trunk_diameter:.1f}cm wide.")

    def show(self) -> None:
        super().show()
        print(f" Trunk diameter: {self.trunk_diameter:.1f}cm")


class Vegetable(Plant):

    def __init__(self, name: str, height: float, days: int,
                 harvest_season: str, nutritional_value: float) -> None:
        super().__init__(name, height, days)
        self.harvest_season = harvest_season
        self.nutritional_value = nutritional_value

    def grow(self) -> None:
        super().grow()
        self.nutritional_value += 0.5

    def age(self) -> None:
        super().age()
        self.nutritional_value += 0.5

    def show(self) -> None:
        super().show()
        print(f" Harvest season: {self.harvest_season}")
        print(f" Nutritional value: {self.nutritional_value}")


def ft_plant_types() -> None:
    flower = Flower("rose", 15, 10, "red")
    print("=== Flower")
    flower.show()
    flower.bloom()
    flower.show()
    print("")
    tree = Tree("oak", 200, 365, 5)
    print("=== Tree")
    tree.show()
    tree.produce_shade()
    print("")
    vegetable = Vegetable("tomato", 5, 10, "April", 0)
    print("=== Vegetable")
    vegetable.show()
    print(f"[make {vegetable.name} grow and age for 20 days]")
    for _ in range(20):
        vegetable.age()
        vegetable.grow()
    vegetable.show()


if __name__ == "__main__":
    print("=== Garden Plant Types ===")
    ft_plant_types()
