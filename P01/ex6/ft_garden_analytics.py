#!/usr/bin/env python3

class Plant:

    class Stats:

        def __init__(self) -> None:
            self.grow_count = 0
            self.age_count = 0
            self.show_count = 0

        def display(self) -> None:
            print(f"Stats: {self.grow_count} grow, {self.age_count} age, "
                  f"{self.show_count} show")

    def __init__(self, name: str, height: float, days: int) -> None:
        self.name = name
        self._height = 0.0
        self._days = 0
        if self._days > 0:
            self.growth_rate = round(height / days, 1)
        else:
            self.growth_rate = 1
        self.set_height(height)
        self.set_age(days)
        self.stats = Plant.Stats()

    def show(self) -> None:
        print(f"{self.name.capitalize()}: "
              f"{self._height:.1f}cm, {self._days} days old")
        self.stats.show_count += 1

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

    @staticmethod
    def check_age(days: int) -> bool:
        return days > 365

    @classmethod
    def anon_plant(cls) -> "Plant":
        return Plant("unknown plant", 0, 0)


class Flower(Plant):

    def __init__(self, name: str, height: float, days: int,
                 color: str) -> None:
        super().__init__(name, height, days)
        self.color = color
        self.bloomed = False

    def bloom(self) -> None:
        print(f"[asking the {self.name} to grow and bloom]")
        self.grow()
        self.bloomed = True
        self.stats.grow_count += 1

    def show(self) -> None:
        super().show()
        print(f" Color: {self.color}")
        if self.bloomed:
            print(f" {self.name.capitalize()} is blooming beautifully!")
        else:
            print(f" {self.name.capitalize()} has not bloomed yet")


class Seed(Flower):

    def __init__(self, name: str, height: float, days: int,
                 color: str) -> None:
        super().__init__(name, height, days, color)
        self.seeds = 0

    def grow_age_and_bloom(self, time: int) -> None:
        print(f"[make {self.name} grow, age and bloom]")
        self.bloomed = True
        self.stats.grow_count += 1
        self.stats.age_count += 1
        for _ in range(time):
            super().age()
            super().grow()
            self.seeds += 2

    def show(self) -> None:
        super().show()
        print(f" Seeds: {self.seeds}")


class Tree(Plant):

    class TreeStats(Plant.Stats):

        def __init__(self) -> None:
            super().__init__()
            self._shades = 0

        def display(self) -> None:
            super().display()
            print(f" {self._shades} shade")

    def __init__(self, name: str, height: float, days: int,
                 trunk_diameter: float) -> None:
        super().__init__(name, height, days)
        self.trunk_diameter = trunk_diameter
        self.stats: Tree.TreeStats = Tree.TreeStats()

    def produce_shade(self) -> None:
        print(f"[asking the {self.name} to produce shade]")
        self.stats._shades += 1
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


def ft_garden_analytics() -> None:
    print("=== Check year-old")
    print(f"Is 30 days more than a year? -> {Plant.check_age(30)}")
    print(f"Is 400 days more than a year? -> {Plant.check_age(400)}")
    print("")
    flower = Flower("rose", 15, 10, "red")
    print("=== Flower")
    flower.show()
    print(f"[statistics for {flower.name.capitalize()}]")
    flower.stats.display()
    flower.bloom()
    flower.show()
    flower.stats.display()
    print("")
    tree = Tree("oak", 200, 365, 5)
    print("=== Tree")
    tree.show()
    print(f"[statistics for {tree.name.capitalize()}]")
    tree.stats.display()
    tree.produce_shade()
    print(f"[statistics for {tree.name.capitalize()}]")
    tree.stats.display()
    print("")
    seed = Seed("sunflower", 80, 45, "yellow")
    print("=== Seed")
    seed.show()
    seed.grow_age_and_bloom(20)
    seed.show()
    print(f"[statistics for {seed.name.capitalize()}]")
    seed.stats.display()
    print("")
    anonymous = Plant.anon_plant()
    print("=== Anonymous")
    anonymous.show()
    print(f"[statistics for {anonymous.name.capitalize()}]")
    anonymous.stats.display()


if __name__ == "__main__":
    print("=== Garden Statistics ===")
    ft_garden_analytics()
