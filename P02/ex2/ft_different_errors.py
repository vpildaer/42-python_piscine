#!/usr/bin/env python3

def garden_operations(operation_number: int) -> None:
    if operation_number == 0:
        try:
            int("abc")
        except Exception as e:
            raise e
    elif operation_number == 1:
        try:
            2 / 0
        except Exception as e:
            raise e
    elif operation_number == 2:
        try:
            open("file.txt", "r")
        except Exception as e:
            raise e
    elif operation_number == 3:
        try:
            ("abc" + 42)
        except Exception as e:
            raise e
    else:
        return


def test_error_types() -> None:
    tests: list[int] = [0, 1, 2, 3, 4]
    for i in tests:
        print(f"Testing operation {i}...")
        try:
            garden_operations(i)
        except ValueError as e:
            print(f"Caught ValueError: {e}")
        except ZeroDivisionError as e:
            print(f"Caught ZeroDivisionError: {e}")
        except FileNotFoundError as e:
            print(f"Caught FileNotFoundError: {e}")
        except TypeError as e:
            print(f"Caught TypeError: {e}")
        else:
            print("Operation completed successfull")


if __name__ == "__main__":
    print("=== Garden Error Types Demo ===")
    test_error_types()
    print("")
    print("All error types tested successfully!")
