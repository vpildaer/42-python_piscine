#!/usr/bin/env python3

import sys


def ft_command_quest() -> None:
    print(f"Program name: {sys.argv[0]}")
    if len(sys.argv) > 1:
        print(f"Arguments received: {len(sys.argv) - 1}")
        i: int = 1
        for elem in sys.argv[1:]:
            print(f"Argument {i}: {elem}")
            i += 1
    else:
        print("No arguments provided!")
    print(f"Total arguments: {len(sys.argv)}")


if __name__ == "__main__":
    print("=== Command Quest ===")
    ft_command_quest()
