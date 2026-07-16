def ft_harvest_total() -> None:
    day_one: int = int(input("Day 1 harvest: "))
    day_two: int = int(input("Day 2 harvest: "))
    day_three: int = int(input("Day 3 harvest: "))
    tot_harvest: int = day_one + day_two + day_three
    print(f"Total harvest: {tot_harvest}")
