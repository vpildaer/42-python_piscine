#!/usr/bin/env python3

import random


def gen_player_achievements() -> set[str]:
    achievements: list[str] = ["Epic Cycle", "This is Sparta!",
                               "An Odyssey in the Making", "Past Mistakes",
                               "Evil Unearthed", "The Bright Minds",
                               "From the Ashes", "Democracy Falls",
                               "Legend in the Making",
                               "Taking Back Athens", "Odyssey's End",
                               "Child of Poseidon", "Make It Your Own",
                               "You Work For Me Now", "Shiny!", "I am Legend",
                               "Are You Not Entertained?", "Demigod",
                               "Godly Power", "Legacy Restored",
                               "Top of the Food Chain", "The Cult Unmasked",
                               "Stink Eye", "Hermes's Homie",
                               "In Perseus's Image", "A-maze-ing Victory!",
                               "Eye on the Prize", "Riddle Me This",
                               "Lord of the Seas", "The Argonauts",
                               "Master of the Hunt", "Everybody Benefits",
                               "Trust Me, I'm a Doctor",
                               "A Pirate's Life for Me", "Going For Gold",
                               "Scourge of the Aegean", "Blood Sport",
                               "Harder, Better, Faster, Stronger",
                               "Fashion's Creed", "Aphrodite's Embrace",
                               "One Head Down…", "Birthright", "Ramming Speed",
                               "I Have the Power", "War Master",
                               "Misthios in Training", "Island Hopper",
                               "Infamous", "Hero for Hire",
                               "Wrath of the Amazons", "The Midas Touch"]
    return (set(random.sample(achievements, random.randint(0, 51))))


if __name__ == "__main__":
    print("=== Achievement Tracker System ===\n")
    a: set[str] = gen_player_achievements()
    b: set[str] = gen_player_achievements()
    c: set[str] = gen_player_achievements()
    d: set[str] = gen_player_achievements()
    print(f"Player Alice: {a}")
    print(f"Player Bob: {b}")
    print(f"Player Charlie: {c}")
    print(f"Player Dylan: {d}")
    print("")
    all_ach = a.union(b).union(c).union(d)
    print(f"All distinct achievements: {all_ach}\n")
    common = a.intersection(b).intersection(c).intersection(d)
    print(f"Common achievements: {common}\n")
    print(f"Only Alice has: {a.difference(common)}")
    print(f"Only Bob has: {b.difference(common)}")
    print(f"Only Charlie has: {c.difference(common)}")
    print(f"Only Dylan has: {d.difference(common)}")
    print("")
    print(f"Alice is missing: {all_ach.difference(a)}")
    print(f"Bob is missing: {all_ach.difference(b)}")
    print(f"Charlie is missing: {all_ach.difference(c)}")
    print(f"Dylan is missing: {all_ach.difference(d)}")
