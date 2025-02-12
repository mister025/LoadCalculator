from typing import Tuple, Dict

from src.parameters.util_parameters.item_parameters import NameParameters
from src.parameters.util_parameters.volume_parameters import VolumeParameters


class ContainerParameters(VolumeParameters, NameParameters):
    _lifting_capacity: int

    def __init__(self, name: str, length: int, width: int, height: int, lifting_capacity: int) -> None:
        NameParameters.__init__(self, name)
        VolumeParameters.__init__(self, length, width, height, 0)
        self._lifting_capacity = lifting_capacity

    @property
    def lifting_capacity(self) -> int:
        return self._lifting_capacity

    def _key(self) -> Tuple:
        return self.name, self.length, self.width, self.height, self.lifting_capacity

    def __str__(self) -> str:
        return f'Container parameters: ({self._key()})'

    def build_response(self) -> Dict:
        return {
            'length': self.length,
            'width': self.width,
            'height': self.height,
            'weight': self.lifting_capacity,
            'type': self.name
        }


