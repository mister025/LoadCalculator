from typing import Tuple

from src.iterators.points_iterator import PointsIterator
from src.loading.point.point import Point


class HorizontalPointsIterator(PointsIterator):
    def _get_point_order_key(self, point: Point) -> Tuple:
        return point.z, point.x, point.y
