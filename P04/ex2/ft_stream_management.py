#!/usr/bin/env python3

import sys
import typing


def print_to_stderr(a: str) -> None:
    print(a, file=sys.stderr)


def ft_stream_management() -> None:
    file: str = sys.argv[1]
    print(f"Accessing file '{file}'")
    try:
        f: typing.IO[str] = open(file, "r")
    except FileNotFoundError as e:
        print_to_stderr(f"[STDERR] Error opening file '{file}': {e}")
        return
    except PermissionError as e:
        print_to_stderr(f"[STDERR] Error opening file '{file}': {e}")
        return
    except Exception as e:
        print_to_stderr(f"[STDERR] Error opening file '{file}': {e}")
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
    print("Enter new file name (or empty):", end=" ")
    sys.stdout.flush()
    new_file: str = sys.stdin.readline().strip()
    if new_file == "":
        print("Not saving data.")
        return
    try:
        new_f: typing.IO[str] = open(new_file, "w")
    except Exception as e:
        print_to_stderr(f"[STDERR] Error opening file '{file}': {e}")
        print("Data not saved.")
        return
    for line in f:
        new_f.write(line.strip("\n") + "#\n")
    f.close()
    new_f.close()
    print(f"Data saved in {new_file}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: ft_stream_management.py <file>")
    else:
        print("=== Cyber Archive Recovery & Preservation ===")
        ft_stream_management()
