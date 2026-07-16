#!/usr/bin/env python3

import random


def ft_data_alchemist() -> None:
    lst: list[str] = ["Alice", "bob", "Charlie", "dylan", "Emma", "Gregory",
                      "john", "kevin", "Liam"]
    print(f"Initial list of players: {lst}")
    lst_all_cap: list[str] = [i.capitalize() for i in lst]
    print(f"New list with all names capitalized: {lst_all_cap}")
    lst_cap_only: list[str] = [i for i in lst if i == i.capitalize()]
    print(f"New list with capitalized names only: {lst_cap_only}\n")
    dic: dict[str, int] = {i: random.randint(0, 1000) for i in lst_all_cap}
    print(f"Score dict: {dic}")
    average: float = sum(dic.values()) / len(dic)
    print(f"Score average is {round(average, 2)}")
    dic_high: dict[str, int] = {i: dic[i] for i in dic if dic[i] > average}
    print(f"High scores: {dic_high}")


if __name__ == "__main__":
    print("=== Game Data Alchemist ===\n")
    ft_data_alchemist()
