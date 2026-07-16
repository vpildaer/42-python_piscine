#!/usr/bin/env python3

from typing import Any
from abc import abstractmethod, ABC


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


class DataStream:

    def __init__(self) -> None:
        self.processors: list[DataProcessor] = []

    def register_processor(self, proc: DataProcessor) -> None:
        to_add: bool = True
        for elem in self.processors:
            if isinstance(elem, type(proc)):
                to_add = False
        if to_add:
            self.processors.append(proc)

    def process_stream(self, stream: list[Any]) -> None:
        for elem in stream:
            try:
                is_ingested: bool = False
                for proc in self.processors:
                    if proc.validate(elem):
                        proc.ingest(elem)
                        is_ingested = True
                        break
                if not is_ingested:
                    raise Exception(f"Can't process element in stream: {elem}")
            except Exception as e:
                print(f"DataStream error - {e}")

    def print_processors_stats(self) -> None:
        print("== DataStream statistics ==")
        if self.processors == []:
            print("No processor found, no data")
            return
        for proc in self.processors:
            print(f"{type(proc).__name__} : "
                  f"total {len(proc.res) + proc.popped} items processed, "
                  f"remaining {len(proc.res)} on processor")


if __name__ == "__main__":
    print("=== Code Nexus - Data Stream ===\n")
    print("Initialize Data Stream...")
    data_s = DataStream()
    data_s.print_processors_stats()
    print("")
    print("Registering Numeric Processor")
    num_p = NumericProcessor()
    data_s.register_processor(num_p)
    print("")
    data1 = ['Hello world', [3.14, -1, 2.71], [{'log_level': 'WARNING',
             'log_message': 'Telnet access! Use ssh instead'},
                                               {'log_level': 'INFO',
                                                'log_message':
                                                'User wil is connected'}],
             42, ['Hi', 'five']]
    print(f"Send first batch of data on stream: {data1}")
    data_s.process_stream(data1)
    data_s.print_processors_stats()
    text_p = TextProcessor()
    log_p = LogProcessor()
    print("\nRegistering other data processors")
    data_s.register_processor(text_p)
    data_s.register_processor(log_p)
    print("Send the same batch again")
    data_s.process_stream(data1)
    data_s.print_processors_stats()
    print("")
    print("Consume some elements from the data processors:"
          "Numeric 3, Text 2, Log 1")
    for i in range(3):
        num_p.output()
    for i in range(2):
        text_p.output()
    log_p.output()
    data_s.print_processors_stats()
