#!/usr/bin/env python3

import sys


def ft_score_analytics() -> None:
    if len(sys.argv) == 1:
        print("No scores provided. Usage: python3 "
              "ft_score_analytics.py <score1> <score2> ...")
        return
    if len(sys.argv) > 1:
        i: int = 1
        draft: list[str] = sys.argv[1:]
        scores: list[int] = []
        for elem in draft:
            try:
                int(elem)
            except Exception:
                print(f"Invalid parameter: '{elem}'")
            else:
                scores = scores + [int(elem)]
            i += 1
    if len(scores) == 0:
        print("No scores provided. Usage: python3 "
              "ft_score_analytics.py <score1> <score2> ...")
        return
    print(f"Scores processed: {scores}")
    print(f"Total players: {len(scores)}")
    print(f"Total score: {sum(scores)}")
    print(f"Average score: {sum(scores) / len(scores)}")
    print(f"High score: {max(scores)}")
    print(f"Low score: {min(scores)}")
    print(f"Score range: {max(scores) - min(scores)}")


if __name__ == "__main__":
    print("=== Player Score Analytics ===")
    ft_score_analytics()
