from typing import Any


def artifact_sorter(artifacts: list[dict]) -> list[dict]:
    return sorted(artifacts, key=lambda x: x['power'], reverse=True)


def power_filter(mages: list[dict], min_power: int) -> list[dict]:
    return list(filter(lambda x: (x['power'] > min_power), mages))


def spell_transformer(spells: list[str]) -> list[str]:
    return list(map(lambda x: "* " + x + " *", spells))


def mage_stats(mages: list[dict]) -> dict:
    res: dict = {}
    res['max_power'] = max(mages, key=lambda
                           mage: mage['power'])['power']
    res['min_power'] = min(mages, key=lambda
                           mage: mage['power'])['power']
    res['avg_power'] = round(sum(m['power'] for m in mages) / len(mages), 2)
    return res


def artifact_sorter_tester(artifacts: list[dict]) -> None:
    print(f"{artifacts[0]['type']} {artifacts[0]['name']} "
          f"({artifacts[0]['power']} power)")

    for elem in artifacts[1:]:
        print("comes before")
        print(f"{elem['type']} {elem['name']} ({elem['power']} power)")

    print("")


if __name__ == "__main__":
    artifacts: list[dict] = [{'name': 'Staff',
                              'power': 92,
                              'type': 'Fire'},
                             {'name': 'Orb',
                              'power': 85,
                              'type': 'Crystal'},
                             {'name': 'Chess',
                              'power': 35,
                              'type': 'Fairy'},
                             {'name': 'Sword',
                              'power': 100,
                              'type': 'Legendary'}]

    print("Initial artifacts list:")
    artifact_sorter_tester(artifacts)

    print("Testing artifact_sorter...")
    print("Sorted artifacts list:")
    sorted_artifacts: list[dict] = artifact_sorter(artifacts)
    artifact_sorter_tester(sorted_artifacts)

    mages: list[dict] = [{'name': 'Felie',
                          'power': 92,
                          'element': 'Fire'},
                         {'name': 'Camis',
                          'power': 85,
                          'element': 'Water'},
                         {'name': 'Ganagathar',
                          'power': 35,
                          'element': 'Light'},
                         {'name': 'Naius',
                          'power': 100,
                          'element': 'Blood'}]

    print("List of mages:")
    for elem in mages:
        print(f"{elem['name']} is a {elem['element']} type mage "
              f"with a power of {elem['power']}")

    print("")
    print("Testing power_filter...")
    min_power: int = 60
    print(f"List of mages with a power greater than {min_power}:")
    filtered_mages: list[dict] = power_filter(mages, min_power)
    for elem in filtered_mages:
        print(f"{elem['name']} is a {elem['element']} type mage "
              f"with a power of {elem['power']}")

    spells: list[str] = ["fireball", "heal", "shield", "lightbeam"]

    print("\nList of spells:")
    for spell in spells:
        print(spell)

    transformed_spells: list[str] = spell_transformer(spells)

    print("\nTesting spell_transformer...")
    print("Transformed spells:")
    for spell in transformed_spells:
        print(spell)

    print("\nTesting mage_stats...")
    stats: dict[str, Any] = mage_stats(mages)
    print(f"Most powerful mage's power level: {stats['max_power']}")
    print(f"Least powerful mage's power level: {stats['min_power']}")
    print(f"Average power level: {stats['avg_power']}")
