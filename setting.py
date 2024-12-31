from dataclasses import dataclass
from enum import Enum



class ForceDirection(Enum):
    Tension = 1
    Compression = 2

class DisplacementControl(Enum):
    Displacement = 1
    Strain = 2

class LengthDevice(Enum):
    Instrument = 1
    Extensometer = 2

class GraphType(Enum):
    ForceDislacement = 1
    EngineeringStressStrain = 2
    RealStressStrain = 3

@dataclass
class Setting:
    force_direction:ForceDirection
    displacement_control:DisplacementControl
    length_measurement_device:LengthDevice
    graph_type:GraphType
    strain_rate:float
    speed_rate:float
    l0_length:float
    widht:float
    thickness:float
    
