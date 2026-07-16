def ft_seed_inventory(seed_type: str, quantity: int, unit: str) -> None:
    if unit == "packets":
        print(f"{seed_type.capitalize()} seeds: {quantity} "
              f"packets available")
    elif unit == "grams":
        print(f"{seed_type.capitalize()} seeds: {quantity} "
              f"grams total")
    elif unit == "area":
        print(f"{seed_type.capitalize()} seeds: covers {quantity} "
              f"square meters")
    else:
        print("Unknown unit type")
