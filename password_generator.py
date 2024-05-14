# -*- coding: utf-8 -*-
# File: password_generator.py

import argparse
import random
import string
import warnings
from typing import Optional


def generate_password(
    n: int,
    include_uppercase: bool = True,
    include_lowercase: bool = True,
    include_digits: bool = True,
    include_symbols: bool = True,
    exclusion: Optional[set[str]] = None,
) -> str:
    # Check arguments
    if n < 0:
        raise ValueError(f"`n` must be greater than or equal to 0, got {n}.")
    elif n == 0:
        return ""
    if exclusion is not None and not isinstance(exclusion, set):
        warnings.warn(f"`exclusion` is expected to be of type set, got {type(exclusion).__name__}.")
    elif exclusion is None:
        exclusion = set()

    # Construct a list of included groups of character
    uppercase = list(string.ascii_uppercase)
    lowercase = list(string.ascii_lowercase)
    digits = list(string.digits)
    symbols = list(r"~`!@#$%^&*()_-+={[}]|\\:;\"'<,>.?/")
    included = []
    if include_uppercase:
        included.append(uppercase)
    if include_lowercase:
        included.append(lowercase)
    if include_digits:
        included.append(digits)
    if include_symbols:
        included.append(symbols)
    if len(included) == 0:
        raise ValueError("At least 1 group of character must be included, got 0.")

    # Flatten the above list of lists into a single list
    combined = [c for group in included for c in group]
    if len(set(combined).difference(exclusion)) == 0:
        raise ValueError("No usable character left after exclusion.")

    # Generate password
    pwd = []
    minimum = min(len(included), n)
    for group in random.sample(included, minimum):  # At least 1 character from each included group
        while (c := random.choice(group)) in exclusion:
            continue
        pwd.append(c)
    for _ in range(n - minimum):  # The remaining portion
        while (c := random.choice(combined)) in exclusion:
            continue
        pwd.append(c)

    return "".join(random.sample(pwd, len(pwd)))  # Shuffle again


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("n", type=int)
    parser.add_argument("-nu", "--no_uppercase", action="store_true")
    parser.add_argument("-nl", "--no_lowercase", action="store_true")
    parser.add_argument("-nd", "--no_digits", action="store_true")
    parser.add_argument("-ns", "--no_symbols", action="store_true")
    parser.add_argument("-e", "--exclusion", type=str, default=None)
    args = parser.parse_args()
    pwd = generate_password(
        args.n,
        include_uppercase=not args.no_uppercase,
        include_lowercase=not args.no_lowercase,
        include_digits=not args.no_digits,
        include_symbols=not args.no_symbols,
        exclusion=set(args.exclusion) if args.exclusion is not None else None,
    )
    print(pwd)
