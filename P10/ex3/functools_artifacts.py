from collections.abc import Callable
from typing import Any
from functools import reduce, partial, lru_cache, singledispatch
from operator import add, mul


def spell_reducer(spells: list[int], operation: str) -> int:

    functs: dict[str, Callable] = {}

    def ft_add(spells: list[int]) -> int:
        return reduce(add, spells)

    def ft_multiply(spells: list[int]) -> int:
        return reduce(mul, spells)

    def ft_min(spells: list[int]) -> int:
        return reduce(lambda a, b: a if a < b else b, spells)

    def ft_max(spells: list[int]) -> int:
        return reduce(lambda a, b: a if a > b else b, spells)

    functs['add'] = ft_add
    functs['multiply'] = ft_multiply
    functs['min'] = ft_min
    functs['max'] = ft_max

    if not spells:
        return 0
    else:
        try:
            return functs[operation](spells)
        except KeyError:
            print("Operation unknown")
            return 0


def partial_enchanter(base_enchantment: Callable) -> dict[str, Callable]:

    fire_enchantment = partial(base_enchantment, 50, 'fire')
    ice_enchantment = partial(base_enchantment, 50, 'ice')
    fairy_enchantment = partial(base_enchantment, 50, 'fairy')

    return {'fire': fire_enchantment,
            'ice': ice_enchantment,
            'fairy': fairy_enchantment}


@lru_cache
def memoized_fibonacci(n: int) -> int:
    if n <= 1:
        return n
    else:
        return memoized_fibonacci(n - 1) + memoized_fibonacci(n - 2)


def spell_dispatcher() -> Callable[[Any], str]:

    @singledispatch
    def dispatcher(spell: Any) -> str:
        return "Unknown spell type"

    @dispatcher.register
    def damage_spell(spell: int) -> str:
        return f"{spell} damage"

    @dispatcher.register
    def enchantment(spell: str) -> str:
        return f"{spell}"

    @dispatcher.register
    def multi_cast(spell: list) -> str:
        return f"{len(spell)} spells"

    return dispatcher


if __name__ == "__main__":

    print("\nTesting spell_reducer...")
    spells: list[int] = [9, 1, 0, -42, 42, 100]
    print(f"Spells: {spells}")
    print(f"Add: {spell_reducer(spells, 'add')}")
    print(f"Multiply: {spell_reducer(spells, 'multiply')}")
    print(f"Max: {spell_reducer(spells, 'max')}")
    print(f"Min: {spell_reducer(spells, 'min')}")
    print("Unknown: ", end="")
    print(f"Res = {spell_reducer(spells, 'unknown')}")
    print(f"Empty list/spells with 'add': {spell_reducer([], 'add')}")

    print("\nTesting partial_enchanter...")

    def base_enchantment(power: int, element: str, target: str) -> str:
        return f"{target} gets hit by a {element} type attack " \
               f"and looses {power} HP"

    enchantments = partial_enchanter(base_enchantment)

    print("Sending target = 'dragon'")
    print(f"{enchantments['fire']('dragon')}")
    print(f"{enchantments['ice']('dragon')}")
    print(f"{enchantments['fairy']('dragon')}")

    print("\nTesting memoized_fibonacci...")
    print(f"N = 0 : {memoized_fibonacci(0)}")
    print(f"N = 1 : {memoized_fibonacci(1)}")
    print(f"N = 2 : {memoized_fibonacci(2)}")
    print(f"N = 3 : {memoized_fibonacci(3)}")
    print(f"N = 4 : {memoized_fibonacci(4)}")
    print(f"N = 5 : {memoized_fibonacci(5)}")
    print(f"Checking cache : {memoized_fibonacci.cache_info()}")
    print(f"N = 6 : {memoized_fibonacci(6)}")
    print(f"N = 7 : {memoized_fibonacci(7)}")
    print(f"N = 8 : {memoized_fibonacci(8)}")
    print(f"Checking cache : {memoized_fibonacci.cache_info()}")

    print("\nTesting spell_dispatcher....")
    dispatcher = spell_dispatcher()
    print(f"Damage spell: {dispatcher(42)}")
    print(f"Enchantment: {dispatcher('fireball')}")
    print(f"Multi-cast: {dispatcher(['fireball', 'fireball', 'fireball'])}")
    print(f"Unknown (sending float): {dispatcher(1.0)}")
