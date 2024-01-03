# -*- coding: utf-8 -*-
# File: guess_the_number.py

"""
### Requirements:

```text
getch
```

### Usage:

```bash
python guess_the_number.py [-min MIN_VALUE] [-max MAX_VALUE] [-s SEED]
```
"""

import argparse
import random
import sys

import getch


def get_number(prompt: str = "") -> int:
    print(prompt, end="", flush=True)
    num = []
    while True:
        char = getch.getch()
        if char.isdigit():  # Get digits only
            num.append(char)
            print(char, end="", flush=True)
        elif char == "-" and len(num) == 0:  # Minus sign
            num.append(char)
            print(char, end="", flush=True)
        elif char in {"\b", "\x7F"} and len(num) > 0:  # Delete previous character
            num.pop()
            print("\b \b", end="", flush=True)
        elif char == "\x1B":  # Exit
            print(flush=True)
            sys.exit()
        elif char in {"\r", "\n", "\r\n"}:  # Return
            print(flush=True)
            return int("".join(num))


def main(min_value: int = 1, max_value: int = 100) -> None:
    answer = random.randint(min_value, max_value)
    attempts = 1
    bound_len = max(len(str(min_value)), len(str(max_value)))
    while (guess := get_number(f"{min_value:{bound_len}d} <= x <= {max_value:{bound_len}d}: ")) != answer:
        if not min_value <= guess <= max_value:
            continue
        attempts += 1
        if guess < answer:
            min_value = guess
        elif guess > answer:
            max_value = guess
    print(f"BINGO! The answer is {answer}. You took {attempts} attempts.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-min", "--min_value", type=int, default=1,
        help="Initial lower bound. Defaults to 1.",
    )
    parser.add_argument(
        "-max", "--max_value", type=int, default=100,
        help="Initial upper bound. Defaults to 100.",
    )
    parser.add_argument(
        "-s", "--seed", type=int, default=None,
        help="Seed for random number generator. Defaults to None.",
    )
    args = parser.parse_args()

    random.seed(args.seed)
    main(args.min_value, args.max_value)
