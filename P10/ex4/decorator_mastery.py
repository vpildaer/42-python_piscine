from collections.abc import Callable
from functools import wraps
from time import time, sleep


def spell_timer(func: Callable) -> Callable:

    @wraps(func)
    def timer(*args, **kwargs):
        start = time()
        res = func(*args, **kwargs)
        sleep(1)
        end = time()
        print(f"Spell completed in {round(end - start, 3)}")
        return res

    return timer


def power_validator(min_power: int) -> Callable:

    def power_validator_decorator(func: Callable) -> Callable:

        @wraps(func)
        def validator(*args, **kwargs):
            power = kwargs.get('power')
            if power is not None and power >= min_power:
                return func(*args, **kwargs)
            return "Insufficient power for this spell"

        return validator

    return power_validator_decorator


def retry_spell(max_attempts: int) -> Callable:

    def retry_spell_decorator(func: Callable) -> Callable:

        @wraps(func)
        def retry(*args, **kwargs):
            for i in range(max_attempts):
                try:
                    res = func(*args, **kwargs)
                except Exception:
                    print(f"Spell failed, retrying... "
                          f"(attempt {i + 1}/{max_attempts})")
                else:
                    return res
            return f"Spell casting failed after {max_attempts} attempts"

        return retry

    return retry_spell_decorator


class MageGuild:

    @staticmethod
    def validate_mage_name(name: str) -> bool:
        if len(name) >= 3 and all(c.isalpha()
                                  or c.isspace() for c in name):
            return True
        else:
            return False

    @power_validator(10)
    def cast_spell(self, spell_name: str, power: int) -> str:
        return f"Successfully cast {spell_name} with {power} power"


if __name__ == "__main__":

    print("Testing spell_timer...")

    @spell_timer
    def timed_fireball() -> str:
        return "Fireball cast!"

    print("Casting fireball...")
    print(f"{timed_fireball()}")

    print("\nTesting power_validator...")

    def heal(power: int) -> str:
        return f"Heal restores {power} HP"

    min_power: int = 30
    validated_heal = power_validator(min_power)(heal)

    print(f"Trying to validate heal with min_power = {min_power} and "
          f"power = 20:")

    print(f"{validated_heal(power=20)}")

    print(f"Trying to validate heal with min_power = {min_power} and "
          f"power = 50:")

    print(f"{validated_heal(power=50)}")

    print("\nTesting retry_spell...")

    def cursed_spell(target: str) -> str:
        raise ValueError(f"The spell backfires on {target}")

    max_attempts: int = 3
    retry_heal = retry_spell(max_attempts)(heal)
    retry_cursed = retry_spell(max_attempts)(cursed_spell)

    print("Trying heal:")
    print(retry_heal(60))
    print("Trying cursed spell (designed to always raise error):")
    print(retry_cursed('Dragon'))

    print("\nTesting MageGuild class...")

    m_g = MageGuild()
    print("\nTesting validate_mage_name...")
    print(f"Validating 'Felina': {m_g.validate_mage_name('Felina')}")
    print(f"Validating 'F3l1n4': {m_g.validate_mage_name('F3l1n4')}")

    print("\nTesting cast_spell...")
    print(f"{m_g.cast_spell('heal', power=50)}")
    print(f"{m_g.cast_spell('heal', power=5)}")
