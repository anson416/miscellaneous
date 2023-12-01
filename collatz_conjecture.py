# -*- coding: utf-8 -*-
# File: collatz_conjecture.py

"""
Given a positive integer n, return a list of positive integers generated from 
the Collatz conjecture: 
Repeat the following until 1 is obtained: For even numbers, divide by 2; for 
odd numbers, multiply by 3 and add 1.

### Usage 1:

```bash
python collatz_conjecture.py 7
```

### Usage 2:

```python
import collatz_conjecture
n: int = 7
generated: list[int] = collatz_conjecture.generate(n)
```
"""

import argparse


def generate(n: int) -> list[int]:
    assert n > 0, f"{n} <= 0. n must be a positive integer."

    lst = []
    while n != 1:
        n = n // 2 if n % 2 == 0 else 3 * n + 1
        lst.append(n)

    return lst


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "n", type=int,
        help="Positive integer",
    )
    args = parser.parse_args()

    print(*generate(args.n), sep=", ")
