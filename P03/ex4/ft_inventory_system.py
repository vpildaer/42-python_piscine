#!/usr/bin/env python3

import sys


def parser() -> dict[str, int]:
    draft: list[str] = sys.argv[1:]
    if len(draft) == 0:
        return ({})
    res: dict[str, int] = {}
    for elem in draft:
        if elem.count(":") != 1 or elem.find(":") == 0:
            try:
                raise Exception(f"Error - invalid parameter '{elem}'")
            except Exception as e:
                print(e)
            finally:
                continue
        item: list[str] = elem.split(':')
        if item[0] in res:
            try:
                raise Exception(f"Redundant item '{item[0]}' - discarding")
            except Exception as e:
                print(e)
            finally:
                continue
        try:
            res[item[0]] = int(item[1])
        except ValueError as e:
            print(f"Quantity error for '{item[0]}': {e}")
        finally:
            continue
    return (res)


def ft_inventory_system() -> None:
    inventory: dict[str, int] = parser()
    if inventory == {}:
        print("Empty inventory")
        return
    print(f"Got inventory: {inventory}")
    print(f"Item list: {list(inventory.keys())}")
    tot: int = sum(inventory.values())
    print(f"Total quantity of the {len(inventory)} items: {tot}")
    mini: str = list(inventory.keys())[0]
    maxi: str = list(inventory.keys())[0]
    for key in inventory.keys():
        print(f"Item {key} represents "
              f"{round((inventory[key] / tot) * 100, 1)}%")
        if inventory[key] < inventory[mini]:
            mini = key
        if inventory[key] > inventory[maxi]:
            maxi = key
    print(f"Item most abundant: {maxi} with quantity {inventory[maxi]}")
    print(f"Item least abundant: {mini} with quantity {inventory[mini]}")
    inventory["magic item"] = 42
    print(f"Updated inventory: {inventory}")


if __name__ == "__main__":
    print("=== Inventory System Analysis ===")
    ft_inventory_system()
