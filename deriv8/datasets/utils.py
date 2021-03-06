from math import floor
from random import shuffle
from typing import List, Tuple

from deriv8.matrix2d import Tensor2D, shape


def shuffle_truncate_dataset(X: Tensor2D, Y: Tensor2D, truncate: int = None) -> Tuple[Tensor2D, Tensor2D]:
    assert shape(X)[1] == shape(Y)[1], "X and Y should have the same number of columns (training examples)"

    index = list(range(shape(X)[1]))
    shuffle(index)
    if truncate and truncate < len(index):
        index = index[:truncate]

    X_ = [[Xi[j] for j in index] for Xi in X]
    Y_ = [[Yi[j] for j in index] for Yi in Y]
    return X_, Y_


# split A in batch_size batches, split by cols
def split_into_batches(A: Tensor2D, batch_size: int) -> List[Tensor2D]:
    A_shape = shape(A)
    num_batches = floor(A_shape[1] / batch_size)
    overflow = A_shape[1] - (num_batches * batch_size)
    batches = []

    def _one_batch(start, end):
        return [Ai[start:end] for Ai in A]

    for b in range(num_batches):
        batches.append(_one_batch(b * batch_size, (b + 1) * batch_size))

    if overflow != 0:
        batches.append(_one_batch(num_batches * batch_size, A_shape[1]))

    total_cols_size = 0
    for batch in batches:
        batch_shape = shape(batch)
        assert batch_shape[0] == A_shape[0]
        assert batch_shape[1] == batch_size or batch_shape[1] == overflow
        total_cols_size += batch_shape[1]
    assert total_cols_size == A_shape[1]

    return batches
