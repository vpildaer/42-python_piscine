#!/usr/bin/env python3

def input_temperature(temp_str: str) -> int:
    return int(temp_str)


def test_temperature(temp_str: str) -> None:
    try:
        res: int = input_temperature(temp_str)
    except Exception as e:
        print(f"Caught input_temperature error: {e}")
    else:
        print(f"Temperature is now {res}°C")


if __name__ == "__main__":
    print("=== Garden Temperature ===\n")
    print("Input data is '25'")
    test_temperature("25")
    print("")
    print("Input data is 'abc'")
    test_temperature("abc")
    print("")
    print("All tests completed - program didn't crash!")
