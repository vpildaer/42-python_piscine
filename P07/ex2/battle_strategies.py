from abc import ABC, abstractmethod
from typing import Any
import ex1.capability_factories as capabilities


class InvalidStrategyError(Exception):
    pass


class BattleStrategy(ABC):

    @abstractmethod
    def act(self, creature: Any) -> None:
        pass

    @abstractmethod
    def is_valid(self, creature: Any) -> bool:
        pass


class NormalStrategy(BattleStrategy):

    def act(self, creature: Any) -> None:
        print(f"{creature.attack()}")

    def is_valid(self, creature: Any) -> bool:
        return True


class AggressiveStrategy(BattleStrategy):

    def act(self, creature: Any) -> None:
        if not self.is_valid(creature):
            raise InvalidStrategyError(f"Invalid Creature '{creature.name}' "
                                       "for this aggressive strategy")
        else:
            print(f"{creature.transform()}")
            print(f"{creature.attack()}")
            print(f"{creature.revert()}")

    def is_valid(self, creature: Any) -> bool:
        if isinstance(creature, capabilities.TransformCapability):
            return True
        else:
            return False


class DefensiveStrategy(BattleStrategy):

    def act(self, creature: Any) -> None:
        if not self.is_valid(creature):
            raise InvalidStrategyError(f"Invalid Creature '{creature.name}' "
                                       "for this defensive strategy")
        else:
            print(f"{creature.attack()}")
            print(f"{creature.heal()}")

    def is_valid(self, creature: Any) -> bool:
        if isinstance(creature, capabilities.HealCapability):
            return True
        else:
            return False
