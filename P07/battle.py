import ex0


def gen_factory(factory: ex0.CreatureFactory) -> None:
    base = factory.create_base()
    print(f"{base.describe()}")
    print(f"{base.attack()}")
    evol = factory.create_evolved()
    print(f"{evol.describe()}")
    print(f"{evol.attack()}")


def battle(fact1: ex0.CreatureFactory, fact2: ex0.CreatureFactory) -> None:
    base1 = fact1.create_base()
    base2 = fact2.create_base()
    print(f"{base1.describe()}")
    print(" vs")
    print(f"{base2.describe()}")
    print(" fight!")
    print(f"{base1.attack()}")
    print(f"{base2.attack()}")


if __name__ == "__main__":
    flame_fact: ex0.CreatureFactory = ex0.FlameFactory()
    aqua_fact: ex0.CreatureFactory = ex0.AquaFactory()
    print("Testing factory")
    gen_factory(flame_fact)
    print("")
    print("Testing factory")
    gen_factory(aqua_fact)
    print("")
    print("Testing battle")
    battle(flame_fact, aqua_fact)
