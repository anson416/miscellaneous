# -*- coding: utf-8 -*-
# File: rref.py

from copy import deepcopy
from fractions import Fraction
from numbers import Real


class RowVector(object):
    def __init__(self, value: Real, *values: Real) -> None:
        self._vector = [Fraction(str(v)) for v in (value, *values)]

    def __str__(self) -> str:
        return f"[{', '.join(self._get_str_fraction())}]"

    def __repr__(self) -> str:
        return f"RowVector({', '.join(self._get_str_fraction())})"

    def __len__(self) -> int:
        return len(self.vector)

    def __add__(self, other: "RowVector") -> "RowVector":
        assert len(self) == len(other)
        return RowVector(*(self[i] + other[i] for i in range(len(self))))

    def __sub__(self, other: "RowVector") -> "RowVector":
        assert len(self) == len(other)
        return RowVector(*(self[i] - other[i] for i in range(len(self))))

    def __mul__(self, multiplier: Real) -> "RowVector":
        return RowVector(*(v * multiplier for v in self))

    def __truediv__(self, divisor: Real) -> "RowVector":
        assert divisor != 0
        return RowVector(*(v / divisor for v in self))

    def __getitem__(self, index: int) -> Fraction:
        return self.vector[index]

    def __setitem__(self, index: int, value: Real) -> None:
        self._vector[index] = Fraction(str(value))

    def _get_str_fraction(self) -> tuple[str, ...]:
        return tuple(str(v) for v in self)

    def get_first_nonzero_index(self) -> int:
        for i in range(len(self)):
            if self[i] != 0:
                return i
        return len(self)

    def get_max_len(self) -> int:
        return max((len(str(v)) for v in self))

    def is_nonzero(self) -> bool:
        return self.get_first_nonzero_index() != len(self)

    @property
    def vector(self) -> list[Fraction]:
        return self._vector


class Matrix(object):
    def __init__(self, row: tuple[Real, ...], *rows: tuple[Real, ...]) -> None:
        assert len({len(row), *(len(r) for r in rows)}) == 1
        self._matrix = [RowVector(*r) for r in (row, *rows)]

    def __str__(self) -> str:
        max_len = max((v.get_max_len() for v in self))
        return "\n".join(
            (
                "  ".join((f"{str(v[i]):>{max_len}s}" for i in range(len(v))))
                for v in self
            )
        )

    def __repr__(self) -> str:
        return f"Matrix({', '.join((str(v) for v in self))})"

    def __len__(self) -> int:
        return len(self.matrix)

    def __getitem__(self, index: int) -> RowVector:
        return self.matrix[index]

    def __setitem__(self, index: int, vector: RowVector) -> None:
        self._matrix[index] = vector

    def get_rref(self):
        matrix = deepcopy(self)
        for i in range(len(matrix)):
            matrix = Matrix(
                *sorted(matrix.matrix, key=lambda x: x.get_first_nonzero_index())
            )
            if not matrix[i].is_nonzero():
                break
            matrix[i] /= matrix[i][matrix[i].get_first_nonzero_index()]
            for j in range(len(matrix)):
                if j != i:
                    matrix[j] -= (
                        matrix[i] * matrix[j][matrix[i].get_first_nonzero_index()]
                    )
        return matrix

    @property
    def matrix(self) -> list[RowVector]:
        return self._matrix


if __name__ == "__main__":
    # Source: CUHK ENGG1120 Spring 2022 Assignments
    test_cases = (
        (
            [[6, -2, 1, -3], [5, -1, 2, -4], [1, -2, 1, 2]],
            "Matrix([1, 0, 0, -1], [0, 1, 0, -5/3], [0, 0, 1, -1/3])",
        ),
        (
            [[1, -1, 2, 2], [2, -6, 9, 14], [3, 1, 1, -4]],
            "Matrix([1, 0, 3/4, -1/2], [0, 1, -5/4, -5/2], [0, 0, 0, 0])",
        ),
        (
            [[3, -2, 1, -3], [5, -3, 1, -6], [0, -1, 1, 5]],
            "Matrix([1, 0, 0, -5], [0, 1, 0, -7], [0, 0, 1, -2])",
        ),
        (
            [[1, 1, 1, 1, 5], [2, 3, -4, 5, -2], [4, 2, 0, -3, 3]],
            "Matrix([1, 0, 0, -39/16, -15/16], [0, 1, 0, 27/8, 27/8], [0, 0, 1, 1/16, 41/16])",
        ),
        (
            [[2, 3, -1, 3, 6], [1, 1, -4, -2, -1], [5, 7, -6, 4, 11]],
            "Matrix([1, 0, -11, -9, -9], [0, 1, 7, 7, 8], [0, 0, 0, 0, 0])",
        ),
        (
            [[1, -1, 3, 5], [3, 2, 6, -3], [4, 1, -8, 0], [-1, 3, 0, 4]],
            "Matrix([1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1])",
        ),
        (
            [[2, -4, 3, 2], [-1, 1, 10, -3], [3, 4, -8, 4], [2, 5, 4, 1]],
            "Matrix([1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1])",
        ),
        (
            [[-1, -1, 3, 0], [3, 0, -2, 0]],
            "Matrix([1, 0, -2/3, 0], [0, 1, -7/3, 0])",
        ),
        (
            [[1, -1, 3, 1, 1], [2, 4, 0, 2, -1], [0, 3, -5, 0, 0]],
            "Matrix([1, 0, 0, 1, 2], [0, 1, 0, 0, -5/4], [0, 0, 1, 0, -3/4])",
        ),
        (
            [
                [1, -2, 0, 3, -2, 4],
                [0, 8, -4, 5, 6, 1],
                [-1, 10, -4, 2, 8, -3],
                [2, 4, -4, 11, 2, 9],
            ],
            "Matrix([1, 0, -1, 17/4, -1/2, 17/4], [0, 1, -1/2, 5/8, 3/4, 1/8], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0])",
        ),
        (
            [
                [1, -3, 4, 0, 1, 0, 0, 0],
                [0, 8, 0, -5, 0, 1, 0, 0],
                [0, 0, 2, 0, 0, 0, 1, 0],
                [0, 0, 0, 4, 0, 0, 0, 1],
            ],
            "Matrix([1, 0, 0, 0, 1, 3/8, -2, 15/32], [0, 1, 0, 0, 0, 1/8, 0, 5/32], [0, 0, 1, 0, 0, 0, 1/2, 0], [0, 0, 0, 1, 0, 0, 0, 1/4])",
        ),
    )

    for test_matrix, test_rref in test_cases:
        assert repr(Matrix(*test_matrix).get_rref()) == test_rref
