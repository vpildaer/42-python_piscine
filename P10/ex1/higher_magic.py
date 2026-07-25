from collections.abc import Callable


def spell_combiner(spell1: Callable, spell2: Callable) -> Callable:

    def res_spell(target: str, power: int) -> tuple[str, str]:
        return (spell1(target, power), spell2(target, power))

    return res_spell


def power_amplifier(base_spell: Callable, multiplier: int) -> Callable:

    def res_power(target: str, power: int) -> str:
        return (base_spell(target, power * multiplier))

    return res_power


def conditional_caster(condition: Callable, spell: Callable) -> Callable:

    def res_conditional(target: str, power: int) -> str:
        if condition(target, power):
            return spell(target, power)
        else:
            return "Spell fizzled"

    return res_conditional


def spell_sequence(spells: list[Callable]) -> Callable:

    def res_sequence(target: str, power: int) -> list[str]:
        return [spell(target, power) for spell in spells]

    return res_sequence


def fireball(target: str, power: int) -> str:
    return f"Fireball hits {target} who loses {power} HP"


def heal(target: str, power: int) -> str:
    return f"Heal restores {target} for {power} HP"


def protego(target: str, power: int) -> str:
    return f"Protego protects {target} from {power} HP dammage"


if __name__ == "__main__":

    print("Testing spell_combiner...")
    target1: str = "Dragon"
    power1: int = 80
    print(f"Spell1: {fireball(target1, power1)}")
    print(f"Spell2: {heal(target1, power1)}")
    combined = spell_combiner(fireball, heal)
    out: tuple[str, str] = combined(target1, power1)
    print("Combined spell result: " + out[0] + ", " + out[1])

    print("\nTesting power_amplifier...")
    mega_fireball = power_amplifier(fireball, 4)
    print(f"Original: {fireball(target1, power1)}")
    print(f"Amplified (by 4): {mega_fireball(target1, power1)}")

    print("\nTesting conditional_caster for 'if power > 50'...")
    power2: int = 30

    def condition(target: str, power: int) -> bool:
        return power > 50

    conditional_fireball = conditional_caster(condition, fireball)
    print(f"Condition verified (HP = {power1}): "
          f"{conditional_fireball(target1, power1)}")
    print(f"Condition not verified (HP = {power2}): "
          f"{conditional_fireball(target1, power2)}")

    print("\nTesting spell_sequence...")
    spells: list[Callable] = [fireball, heal, protego]
    spells_seq = spell_sequence(spells)
    for spell in spells_seq(target1, power2):
        print(spell)
