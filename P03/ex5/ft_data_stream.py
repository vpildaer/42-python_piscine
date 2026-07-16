#!/usr/bin/env python3

import random
import typing


def gen_event() -> typing.Generator[tuple[str, ...], None, None]:
    players: list[str] = ["alice", "bob", "charlie", "dylan", "ethan"]
    actions: list[str] = ["jump", "run", "eat", "attack", "parry", "heal",
                          "sleep", "swim", "move", "climb", "walk", "fly",
                          "release", "grab", "turn", "shoot", "focus",
                          "drink", "throw", "scrouch", "mount", "freeze"]
    while True:
        yield (random.choice(players), random.choice(actions))


def consume_event(lst: list[tuple[str, ...]]) \
                   -> typing.Generator[tuple[str, ...], None, None]:
    while len(lst) > 0:
        index: int = random.randint(0, len(lst) - 1)
        res: tuple[str, ...] = lst[index]
        lst.pop(index)
        yield res


def ft_data_stream() -> None:
    gen = gen_event()
    player: str
    action: str
    for i in range(1000):
        player, action = next(gen)
        print(f"Event {i}: Player {player} did action {action}")
    lst: list[tuple[str, ...]] = []
    for _ in range(10):
        lst = lst + [next(gen)]
    print(f"Built list of 10 events: {lst}")
    for event in consume_event(lst):
        print(f"Got event from list: {event}")
        print(f"Remains in list: {lst}")


if __name__ == "__main__":
    print("=== Game Data Strem Processor ===")
    ft_data_stream()
