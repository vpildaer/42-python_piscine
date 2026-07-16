#!/usr/bin/env python3

def ft_garden_intro() -> None:
    name: str = "Rose"
    height: int = 25
    age: int = 30
    print("Plant: " + name)
    print(f"Height: {height}cm")
    print(f"Age: {age} days\n")


if __name__ == "__main__":
    print("=== Welcome to My Garden ===")
    ft_garden_intro()
    print("=== End of Program ===")
