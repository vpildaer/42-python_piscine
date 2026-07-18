import ex0
import ex1
import ex2


def battle(opponents: list[tuple[ex0.CreatureFactory, ex2.BattleStrategy]]) \
           -> None:
    if len(opponents) < 2:
        raise Exception("Not enough opponents to battle")
    labels: list[str] = [f"({fact.create_base().name}"
                         f"+{type(strat).__name__.removesuffix('Strategy')})"
                         for fact, strat in opponents]
    print("[ " + ", ".join(labels) + " ]")
    print("*** Tournament ***")
    print(f"{len(opponents)} opponents involved")
    for i in range(len(opponents)):
        fact1, strat1 = opponents[i]
        opp1 = fact1.create_base()
        for tup in opponents[i + 1:]:
            fact2, strat2 = tup
            opp2 = fact2.create_base()
            print("")
            print("* Battle *")
            print(f"{opp1.describe()}")
            print(" vs.")
            print(f"{opp2.describe()}")
            print(" now fight!")
            try:
                strat1.act(opp1)
            except ex2.InvalidStrategyError as e:
                print(f"Battle error, aborting tournament: {e}")
                return
            try:
                strat2.act(opp2)
            except ex2.InvalidStrategyError as e:
                print(f"Battle error, aborting tournament: {e}")
                return


if __name__ == "__main__":
    flame_fact = ex0.FlameFactory()
    aqua_fact = ex0.AquaFactory()
    heal_fact = ex1.HealingCreatureFactory()
    trans_fact = ex1.TransformCreatureFactory()
    norm_strat = ex2.NormalStrategy()
    agg_strat = ex2.AggressiveStrategy()
    def_strat = ex2.DefensiveStrategy()

    print("Tournament 0 (basic)")
    battle([(flame_fact, norm_strat), (heal_fact, def_strat)])
    print("")
    print("Tournament 1 (error)")
    battle([(flame_fact, agg_strat), (heal_fact, def_strat)])
    print("")
    print("Tournament 2 (multiple)")
    battle([(aqua_fact, norm_strat),
            (heal_fact, def_strat), (trans_fact, agg_strat)])
