from collections.abc import Callable


def mage_counter() -> Callable:

    count: int = 0

    def res() -> int:
        nonlocal count
        count += 1
        return count

    return res


def spell_accumulator(initial_power: int) -> Callable:

    base: int = initial_power

    def res(amount: int) -> int:
        nonlocal base
        base += amount
        return base

    return res


def enchantment_factory(enchantment_type: str) -> Callable:

    def res(item_name: str) -> str:
        return f"{enchantment_type} {item_name}"

    return res


def memory_vault() -> dict[str, Callable]:

    storage: dict[str, int] = {}

    def store(key: str, value: int) -> None:
        storage[key] = value

    def recall(key: str) -> int | str:
        return storage.get(key, "Memory not found")

    return {'store': store, 'recall': recall}


if __name__ == "__main__":

    print("\nTesting mage_counter...")
    counter_a = mage_counter()
    counter_b = mage_counter()
    print(f"1st call for counter_a: {counter_a()}")
    print(f"2nd call for counter_a: {counter_a()}")
    print(f"3rd call for counter_a: {counter_a()}")
    print(f"1st call for counter_b: {counter_b()}")
    print(f"2nd call for counter_b: {counter_b()}")

    print("\nTesting spell_accumulator...")
    accumulator_a = spell_accumulator(100)
    accumulator_b = spell_accumulator(1)
    print(f"1st call for accumulator_a (base: 100) "
          f"with 20: {accumulator_a(20)}")
    print(f"2nd call for accumulator_a with 30: {accumulator_a(30)}")
    print(f"3rd call for accumulator_a with 40: {accumulator_a(40)}")
    print(f"1st call for accumulator_b (base 1) with 1: {accumulator_b(1)}")
    print(f"2nd call for accumulator_b with 2: {accumulator_b(2)}")

    print("\nTesting enchantment_factory...")
    factory_a = enchantment_factory("fairy")
    factory_b = enchantment_factory("light")
    print("Testing factory_a : fairy")
    print(f"Creating a sword: {factory_a('sword')}")
    print(f"Creating a shield: {factory_a('shield')}")
    print("Testing factory_b : light")
    print(f"Creating a sword: {factory_b('sword')}")
    print(f"Creating a shield: {factory_b('shield')}")

    print("\nTesting memory_vault...")
    vault = memory_vault()
    print("Store 'secret' = 42")
    vault['store']('secret', 42)
    print(f"Recall 'secret': {vault['recall']('secret')}")
    print(f"Recall 'unknown' : {vault['recall']('unknown')}")
