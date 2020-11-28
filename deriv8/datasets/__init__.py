import gzip
import struct

from pathlib import Path

from deriv8.matrix2d import Matrix2D, shape


MAX_ITEMS = 10


def load_mnist() -> tuple[Matrix2D, Matrix2D, Matrix2D, Matrix2D]:
    path = Path(__file__).parent.parent.parent / 'datasets' / 'mnist'
    train_images = _load_images(path / 't10k-images-idx3-ubyte.gz')
    train_labels = _load_labels(path / 't10k-labels-idx1-ubyte.gz')
    test_images = _load_images(path / 'train-images-idx3-ubyte.gz')
    test_labels = _load_labels(path / 'train-labels-idx1-ubyte.gz')
    return train_images, train_labels, test_images, test_labels


def _load_labels(path: Path) -> Matrix2D:
    with gzip.open(path, 'rb') as f:
        magic, num_labels = struct.unpack('>II', f.read(8))

        # should get values specified here http://yann.lecun.com/exdb/mnist/
        assert magic == 2049
        assert num_labels == 10000 or num_labels == 60000

        num_labels = min(num_labels, MAX_ITEMS)
        labels = [[float(b)] for (b,) in struct.iter_unpack('>b', f.read(num_labels))]

    print(shape(labels))
    return labels


def _load_images(path: Path) -> Matrix2D:
    with gzip.open(path, 'rb') as f:
        magic, num_images, rows, cols = struct.unpack('>IIII', f.read(16))

        # should get values specified here http://yann.lecun.com/exdb/mnist/
        assert magic == 2051
        assert num_images == 10000 or num_images == 60000
        assert rows == 28
        assert cols == 28

        num_pixels = rows * cols
        num_images = min(num_images, MAX_ITEMS)
        images = [
            list(map(float, struct.unpack('>{}b'.format(num_pixels), f.read(num_pixels))))
            for _ in range(num_images)
        ]

    print(shape(images))
    return images