from typing import Dict, List, Tuple, Optional

from src.loading.container_selection_type import ContainerSelectionType
from src.loading.container_selector import ContainerSelector
from src.items.item_fabric import ItemFabric
from src.items.container import Container
from src.iterators.loadable_points_iterator import LoadablePointsIterator
from src.logger.logger import Logger
from src.parameters.container_parameters import ContainerParameters
from src.parameters.shipment_parameters import ShipmentParameters
from src.items.point import Point


class Loader:
    _container_counts: Dict[ContainerParameters, int]
    _auto_containers: List[ContainerParameters]
    _container_selection_type: ContainerSelectionType

    _shipments_counts: Dict[ShipmentParameters, int]

    _load_item_fabric: ItemFabric
    _container_selector: ContainerSelector

    _containers: List[Container]
    
    _logger: Logger

    def __init__(
            self,
            container_counts: Dict[ContainerParameters, int],
            auto_containers: List[ContainerParameters],
            container_selection_type: ContainerSelectionType,
            shipments_counts: Dict[ShipmentParameters, int],
            load_item_fabric: ItemFabric,
            container_selector: ContainerSelector,
            logger: Logger
    ) -> None:
        self._container_counts = container_counts
        self._auto_containers = auto_containers
        self._container_selection_type = container_selection_type
        self._shipments_counts = shipments_counts
        self._load_item_fabric = load_item_fabric
        self._container_selector = container_selector
        self._containers = []
        self._logger = logger

    @property
    def containers(self) -> List[Container]:
        return self._containers

    @property
    def shipments_counts(self) -> Dict[ShipmentParameters, int]:
        return self._shipments_counts

    def load(self) -> None:
        shipment_params_order = self._calculate_shipment_params_order()
        for shipment_params in shipment_params_order:
            while self._shipments_counts[shipment_params]:
                self._logger.info(f'Loading {shipment_params}, left: {self._shipments_counts[shipment_params]}')
                if not self._load_shipment_with_params(shipment_params):
                    break
                self._shipments_counts[shipment_params] -= 1
            self._logger.info(f'Loaded {shipment_params}')

    def _calculate_shipment_params_order(self) -> List[ShipmentParameters]:
        return list(sorted(
            self._shipments_counts.keys(),
            key=lambda s: [s.can_stack] + s.get_volume_params_sorted() + [s.weight],
            reverse=True))

    def _load_shipment_with_params(self, shipment_params: ShipmentParameters):
        shipment_params_variations = shipment_params.get_volume_params_variations()
        for v in shipment_params_variations:
            self._logger.info(f'Loading variation: {v}')
            if self._load_into_existing_container(v):
                return True
            if self._load_into_new_container(v):
                return True
        return False

    def _load_into_existing_container(self, shipment_params: ShipmentParameters) -> bool:
        for container in self._containers:
            if self._load_shipment_into_container(shipment_params, container):
                return True
        return False

    def _load_into_new_container(self, shipment_params: ShipmentParameters) -> bool:
        container_parameters = self._select_next_container_parameters()
        if not container_parameters:
            return False
        container = self._load_item_fabric.create_container(container_parameters)
        if self._load_shipment_into_container(shipment_params, container):
            self._containers.append(container)
            if self._container_selection_type == ContainerSelectionType.FIXED:
                self._container_counts[container_parameters] -= 1
            return True
        return False

    def _select_next_container_parameters(self) -> Optional[ContainerParameters]:
        possible_container_params = self._get_possible_container_params()
        if len(possible_container_params) <= 0:
            return None

        shipments_volume, shipments_weight = self._compute_shipments_weight_and_volume()
        return self._container_selector.select_params(possible_container_params, shipments_volume, shipments_weight)

    def _get_possible_container_params(self) -> List[ContainerParameters]:
        if self._container_selection_type == ContainerSelectionType.AUTO:
            return self._auto_containers
        return list(map(lambda x: x[0], filter(lambda x: x[1] > 0, self._container_counts.items())))

    def _compute_shipments_weight_and_volume(self) -> Tuple[float, float]:
        shipments_weight, shipments_volume = 0, 0
        for shipment_params, count in self._shipments_counts.items():
            shipments_weight += shipment_params.weight * count
            shipments_volume += shipment_params.compute_extended_volume() * count
        return shipments_volume, shipments_weight

    def _load_shipment_into_container(self, shipment_params: ShipmentParameters, container: Container) -> bool:
        self._logger.info("Selecting loading point")
        loading_point = self._select_loading_point(shipment_params, container)
        if loading_point:
            self._logger.info(f"Loading point found {loading_point}, loading")
            shipment = self._load_item_fabric.create_shipment(shipment_params)
            container.load(loading_point, shipment)
            return True
        return False

    def _select_loading_point(self, shipment_params: ShipmentParameters, container: Container) -> Optional[Point]:
        self._logger.info("Iterating container")
        for point in LoadablePointsIterator(container):
            # self._logger.info(f"Checking point {point}")
            can_load = container.can_load_into_point(point, shipment_params)
            if can_load:
                return point
        return None
