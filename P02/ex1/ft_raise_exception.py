#!/usr/bin/env python3

def input_temperature(temp_str: str) -> int:
    try:
        res: int = int(temp_str)
    except Exception as e:
        raise e
    if res < 0:
        raise Exception(f"{res}°C is too cold for plants (min 0°C)")
    elif res > 40:
        raise Exception(f"{res}°C is too hot for plants (max 40°C)")
    return res


def test_temperature() -> None:
    temp_str: list[str] = ["25", "abc", "100", "-50"]
    for i in temp_str:
        print(f"Input data is '{i}'")
        try:
            res: int = input_temperature(i)
        except Exception as e:
            print(f"Caught input_temperature error: {e}")
        else:
            print(f"Temperature is now {res}°C")
        print("")


if __name__ == "__main__":
    print("=== Garden Temperature Checker ===\n")
    test_temperature()
    print("All tests completed - program didn't crash!")
