#!/usr/bin/env python3

from typing import Any, Protocol
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


class ExportPlugin(Protocol):

    def process_output(self, data: list[tuple[int, str]]) -> None:
        pass


class CsvPlugin:

    def process_output(self, data: list[tuple[int, str]]) -> None:
        print("CSV Output:")
        out: list[str] = []
        for i in range(len(data)):
            out.append(data[i][1])
        res: str = ",".join(out)
        print(res)


class JsonPlugin:

    def process_output(self, data: list[tuple[int, str]]) -> None:
        print("JSON Output:")
        res: list[str] = []
        for rank, value in data:
            res.append(f'"item_{rank}": "{value}"')
        print("{" + ", ".join(res) + "}")


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

    def output_pipeline(self, nb: int, plugin: ExportPlugin) -> None:
        for proc in self.processors:
            out: list[tuple[int, str]] = []
            for i in range(nb):
                if len(proc.res) > 0:
                    out.append(proc.output())
            plugin.process_output(out)


if __name__ == "__main__":
    print("=== Code Nexus - Data Pipeline ===\n")
    print("Initialize Data Stream...\n")
    data_s = DataStream()
    data_s.print_processors_stats()
    num_p = NumericProcessor()
    text_p = TextProcessor()
    log_p = LogProcessor()
    print("Registering Processors\n")
    data_s.register_processor(num_p)
    data_s.register_processor(text_p)
    data_s.register_processor(log_p)
    data1 = ['Hello world', [3.14, -1, 2.71], [{'log_level': 'WARNING',
             'log_message': 'Telnet access! Use ssh instead'},
                                               {'log_level': 'INFO',
                                                'log_message':
                                                'User wil is connected'}],
             42, ['Hi', 'five']]
    print(f"Send first batch of data on stream: {data1}\n")
    data_s.process_stream(data1)
    data_s.print_processors_stats()
    csv_plugin = CsvPlugin()
    print("\nSend 3 processed data from each processor to a CSV plugin:")
    data_s.output_pipeline(3, csv_plugin)
    print("")
    data_s.print_processors_stats()
    data2 = [21, ['I love AI', 'LLMs are wonderful', 'Stay healthy'],
                 [{'log_level': 'ERROR', 'log_message': '500 server crash'},
                  {'log_level': 'NOTICE',
                   'log_message': 'Certificate expires in 10 days'}],
                 [32, 42, 64, 84, 128, 168], 'World hello']
    print(f"\nSend another batch of data: {data2}\n")
    data_s.process_stream(data2)
    data_s.print_processors_stats()
    print("")
    json_plugin = JsonPlugin()
    print("\nSend 5 processed data from each processor to a JSON plugin:")
    data_s.output_pipeline(5, json_plugin)
    print("")
    data_s.print_processors_stats()
