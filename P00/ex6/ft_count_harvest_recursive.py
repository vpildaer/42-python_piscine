def ft_days(day: int) -> None:
    if day > 1:
        ft_days(day - 1)
    print(f"Day {day}")


def ft_count_harvest_recursive() -> None:
    days: int = int(input("Days until harvest: "))
    ft_days(days)
    print("Harvest time!")
