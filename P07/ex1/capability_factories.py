import ex0.creatures as creatures
import ex0.creature_factories as factories
from abc import ABC, abstractmethod


class HealCapability(ABC):

    @abstractmethod
    def heal(self) -> str:
        pass


class TransformCapability(ABC):

    @abstractmethod
    def transform(self) -> str:
        pass

    @abstractmethod
    def revert(self) -> str:
        pass


class HealingCreatureFactory(factories.CreatureFactory):

    class Sproutling(creatures.Creature, HealCapability):

        def __init__(self) -> None:
            super().__init__("Sproutling", "Grass")

        def attack(self) -> str:
            return f"{self.name} uses Vine Whip!"

        def heal(self) -> str:
            return f"{self.name} heals itself for a small amount"

    class Bloomelle(creatures.Creature, HealCapability):

        def __init__(self) -> None:
            super().__init__("Bloomelle", "Grass/Fairy")

        def attack(self) -> str:
            return f"{self.name} uses Petal Dance!"

        def heal(self) -> str:
            return f"{self.name} heals itself and others for a large amount"

    def create_base(self) -> Sproutling:
        return HealingCreatureFactory.Sproutling()

    def create_evolved(self) -> Bloomelle:
        return HealingCreatureFactory.Bloomelle()


class TransformCreatureFactory(factories.CreatureFactory):

    class Shiftling(creatures.Creature, TransformCapability):

        def __init__(self) -> None:
            super().__init__("Shiftling", "Normal")
            self.is_transformed = False

        def attack(self) -> str:
            if self.is_transformed:
                return f"{self.name} performs a boosted strike!"
            else:
                return f"{self.name} attacks normally."

        def transform(self) -> str:
            self.is_transformed = True
            return f"{self.name} shifts into a sharper form!"

        def revert(self) -> str:
            self.is_transformed = False
            return f"{self.name} returns to normal."

    class Morphagon(creatures.Creature, TransformCapability):

        def __init__(self) -> None:
            super().__init__("Morphagon", "Normal/Dragon")
            self.is_transformed = False

        def attack(self) -> str:
            if self.is_transformed:
                return f"{self.name} unleashes a devasting morph strike!"
            else:
                return f"{self.name} attacks normally."

        def transform(self) -> str:
            self.is_transformed = True
            return f"{self.name} morphs into a dragonic battle form!"

        def revert(self) -> str:
            self.is_transformed = False
            return f"{self.name} stabilizes its form."

    def create_base(self) -> Shiftling:
        return TransformCreatureFactory.Shiftling()

    def create_evolved(self) -> Morphagon:
        return TransformCreatureFactory.Morphagon()
