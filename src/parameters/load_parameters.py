from abc import ABC, abstractmethod


class LoadParameters(ABC):
    _length: int
    _width: int
    _height: int

    def __init__(self, length: int, width: int, height: int):
        self._length = length
        self._width = width
        self._height = height

    @property
    def length(self):
        return self._length

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    def __eq__(self, other):
        if isinstance(other, type(self)):
            return self._key() == other._key()
        return NotImplemented

    def __hash__(self):
        return hash(self._key())

    @abstractmethod
    def _key(self):
        ...
