#!/usr/bin/env python3

from typing import Any
from abc import ABC, abstractmethod


class DataProcessor(ABC):

    def __init__(self) -> None:
        self.res: list[str] = []
        self.popped: int = 0

    @abstractmethod
    def validate(self, data: Any) -> bool:
        pass

    @abstractmethod
    def ingest(self, data: Any) -> None:
        pass

    def output(self) -> tuple[int, str]:
        out: tuple[int, str] = (self.popped, self.res[0])
        self.res.pop(0)
        self.popped += 1
        return out


class NumericProcessor(DataProcessor):

    def validate(self, data: Any) -> bool:
        if isinstance(data, list):
            if data == []:
                return False
            else:
                return all(isinstance(elem, int | float)
                           and not isinstance(elem, bool) for elem in data)
        else:
            return isinstance(data, int | float) and not isinstance(data,
                                                                    bool)

    def ingest(self, data: int | float | list[int | float]) -> None:
        if not self.validate(data):
            raise TypeError("Got exception: Improper numeric data")
        if isinstance(data, list):
            for elem in data:
                self.res.append(str(elem))
        else:
            self.res.append(str(data))


class TextProcessor(DataProcessor):

    def validate(self, data: Any) -> bool:
        if isinstance(data, list):
            if data == []:
                return False
            else:
                return all(isinstance(elem, str) for elem in data)
        else:
            return isinstance(data, str)

    def ingest(self, data: str | list[str]) -> None:
        if not self.validate(data):
            raise TypeError("Got exception: Not a (list of) string(s)")
        if isinstance(data, list):
            for elem in data:
                self.res.append(elem)
        else:
            self.res.append(data)


class LogProcessor(DataProcessor):

    def validate(self, data: Any) -> bool:
        if isinstance(data, list):
            if data == []:
                return False
            else:
                if all(isinstance(elem, dict) for elem in data):
                    return all(all(isinstance(k, str) and isinstance(v, str)
                                   for k, v in elem.items()) for elem in data)
                else:
                    return False
        else:
            if isinstance(data, dict):
                return all(isinstance(k, str) and isinstance(v, str)
                           for k, v in data.items())
            else:
                return False

    def ingest(self, data: dict[str, str] | list[dict[str, str]]) -> None:
        if not self.validate(data):
            raise TypeError("Got exception: Not a (list of) dict")
        entry: str
        if isinstance(data, list):
            for elem in data:
                entry = ": ".join(elem.values())
                self.res.append(entry)
        else:
            entry = ": ".join(data.values())
            self.res.append(entry)


if __name__ == "__main__":
    print("=== Code Nexus - Data Processor ===\n")

    print("Testing Numeric Processor...")
    processor1 = NumericProcessor()
    test1: int = 42
    print(f" Trying to validate input '{test1}': {processor1.validate(test1)}")
    test2: str = "Hello"
    print(f" Trying to validate input '{test2}': {processor1.validate(test2)}")
    test3: str = "foo"
    print(f" Test invalid ingestion of string '{test3}' "
          f"without prior validation:")
    try:
        processor1.ingest(test3)
    except TypeError as e:
        print(f" {e}")
    data1: list[int | float] = [1, 2, 3, 4, 5]
    print(f" Processing data: {data1}")
    processor1.ingest(data1)
    print(" Extracting 3 values...")
    for i in range(3):
        rank, val = processor1.output()
        print(f" Numeric value {rank}: {val}")

    print("\nTesting Text Processor...")
    processor2 = TextProcessor()
    print(f" Trying to validate input '{test1}': {processor2.validate(test1)}")
    data2: list[str] = ["Hello", "Nexus", "World"]
    print(f" Processing data: {data2}")
    processor2.ingest(data2)
    print(" Extracting 1 value...")
    rank, val = processor2.output()
    print(f" Text value {rank}: {val}")

    print("\nTesting Log Processor...")
    processor3 = LogProcessor()
    print(f" Trying to validate input '{test2}': {processor3.validate(test2)}")
    data3: list[dict[str, str]] = [{'log_level': 'NOTICE',
                                    'log_message': 'Connection to server'},
                                   {'log_level': 'ERROR',
                                    'log_message': 'Unauthorized access!!'}]
    print(f" Processing data: {data3}")
    processor3.ingest(data3)
    print(" Extracting 2 values...")
    for i in range(2):
        rank, val = processor3.output()
        print(f" Log entry {rank}: {val}")
