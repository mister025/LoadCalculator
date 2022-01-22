from src.parameters.container_parameters import ContainerParameters
from src.parameters.pallet_parameters import PalletParameters
from src.parameters.shipment_parameters import ShipmentParameters


SMALL_CONTAINER_PARAMETERS = ContainerParameters(40, 20, 20, 100)
SMALL_SHIPMENT_COUNTS = {ShipmentParameters(2, 2, 2, 1, 'b'): 4, ShipmentParameters(5, 5, 5, 1, 'r'): 1}
SMALL_PALLET_PARAMETERS = PalletParameters(8, 10, 1, 2, 20, 'g')

CONTAINER_PARAMETERS = ContainerParameters(400, 200, 200, 100)
SHIPMENT_COUNTS = {ShipmentParameters(10, 10, 10, 2, 'b'): 10, ShipmentParameters(50, 50, 50, 10, 'r'): 1}
PALLET_PARAMETERS = PalletParameters(80, 100, 15, 1, 20, 'g')
