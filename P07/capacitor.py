import ex1


def heal_fact(fact: ex1.HealingCreatureFactory) -> None:
    base = fact.create_base()
    evol = fact.create_evolved()
    print(" base:")
    print(f"{base.describe()}")
    print(f"{base.attack()}")
    print(f"{base.heal()}")
    print(" evolved:")
    print(f"{evol.describe()}")
    print(f"{evol.attack()}")
    print(f"{evol.heal()}")


def trans_fact(fact: ex1.TransformCreatureFactory) -> None:
    base = fact.create_base()
    evol = fact.create_evolved()
    print(" base:")
    print(f"{base.describe()}")
    print(f"{base.attack()}")
    print(f"{base.transform()}")
    print(f"{base.attack()}")
    print(f"{base.revert()}")
    print(" evolved:")
    print(f"{evol.describe()}")
    print(f"{evol.attack()}")
    print(f"{evol.transform()}")
    print(f"{evol.attack()}")
    print(f"{evol.revert()}")


if __name__ == "__main__":
    print("Testing Creature with healing capability")
    fact1 = ex1.HealingCreatureFactory()
    heal_fact(fact1)
    print("")
    print("Testing Creature with transform capability")
    fact2 = ex1.TransformCreatureFactory()
    trans_fact(fact2)
