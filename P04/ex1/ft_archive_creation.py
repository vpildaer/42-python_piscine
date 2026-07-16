#!/usr/bin/env python3

import sys
import typing


def ft_archive_creation() -> None:
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
    print("\nTransform data:\n---\n")
    f = open(file, "r")
    for line in f:
        print(line.strip("\n") + "#")
    f.close()
    f = open(file, "r")
    print("---")
    new_file: str = input("Enter new file name (or empty): ")
    if new_file == "":
        print("Not saving data.")
        return
    print(f"Saving data to '{new_file}'")
    try:
        new_f: typing.IO[str] = open(new_file, "w")
    except Exception as e:
        print(f"Error opening file '{new_file}': {e}")
        print("Data not saved.")
        return
    for line in f:
        new_f.write(line.strip("\n") + "#\n")
    f.close()
    new_f.close()
    print(f"Data saved in {new_file}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: ft_archive_creation.py <file>")
    else:
        print("=== Cyber Archive Recovery & Preservation ===")
        ft_archive_creation()
