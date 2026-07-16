#!/usr/bin/env python3

import sys
import typing


def ft_ancient_text() -> None:
    file: str = sys.argv[1]
    print(f"Accessing file '{file}'")
    try:
        f: typing.IO[str] = open(file, "r")
    except FileNotFoundError as e:
        print(f"Error opening file '{file}': {e}")
        return
    except PermissionError as e:
        print(f"Error opening file '{file}': {e}")
        return
    except Exception as e:
        print(f"Error opening file '{file}': {e}")
        return
    print("---")
    print(f.read())
    print("---")
    f.close()
    print(f"File '{file}' closed.")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: ft_ancient_text.py <file>")
    else:
        print("=== Cyber Archive Recovery ===")
        ft_ancient_text()
