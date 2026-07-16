#!/usr/bin/env python3

import math


def get_player_pos() -> tuple[float, ...]:
    while True:
        pos: str = input("Enter new coordinates as floats in format 'x,y,z': ")
        try:
            x_str, y_str, z_str = pos.split(',')
        except ValueError:
            print("Invalid syntax")
            continue
        draft: list[str] = [x_str.strip(), y_str.strip(), z_str.strip()]
        res: list[float] = []
        valid: bool = True
        for elem in draft:
            try:
                res = res + [float(elem)]
            except ValueError as e:
                print(f"Error on parameter '{elem}': {e}")
                valid = False
        if valid:
            return (res[0], res[1], res[2])


if __name__ == "__main__":
    print("=== Game Coordinate System ===\n")
    print("Get a first set of coordinates")
    pos1: tuple[float, ...] = get_player_pos()
    print(f"Got a first tuple: {pos1}")
    x1, y1, z1 = pos1
    print(f"It includes: X={x1}, Y={y1}, Z={z1}")
    dis_to_cent: float = math.sqrt((x1**2) + (y1**2) + (z1**2))
    print(f"Distance to center: {dis_to_cent}")
    print("\nGet a second set of coordinates")
    pos2: tuple[float, ...] = get_player_pos()
    x2, y2, z2 = pos2
    dis_between: float = math.sqrt((x2-x1)**2 + (y2-y1)**2 + (z2-z1)**2)
    print(f"Distance between the 2 sets of coordinates: {dis_between}")
