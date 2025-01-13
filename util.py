from collections import namedtuple
from dataclasses import dataclass
from typing import Tuple, List
import json

TensileOutput = namedtuple('tensile_output', 'force ext r100')

Point = namedtuple('point', 'X Y')

@dataclass
class MattProperties:
    elasticity_modulu:Tuple=()
    curve:Tuple[List,List] = None
    uts:float = 0
    strain_at_uts:float = 0
    yield_strenght_offset:float = 0
    yield_strain_offset:float = 0
    strain_at_break:float = 0
    stress_at_break:float = 0
     
    






range_lookup_table = {
        "5": 5,
        "17": 10,
        "18": 20,
        "19": 25,
        "20": 30,
        "21": 50,
        "33": 100,
        "34": 200,
        "35": 250,
        "36": 300,
        "37": 500,
        "49": 1000,
        "50": 2000,
        "51": 2500,
        "52": 3000,
        "53": 5000,
        "65": 10000,
        "66": 20000,
        "67": 25000,
        "68": 30000,
        "69": 50000,
        "81": 100000,
        "82": 200000,
        "83": 250000
    }

def write_data(file_obj,*, width,thickness,extl0,r100l0,data ):
    dimension = f'width={width}  ,thickness={thickness}  ,extl0={extl0}  ,r100l0={r100l0}\n'
    file_obj.write(dimension)
    data_header = f'   Force   |   ext   |   r100   \n'
    file_obj.write(data_header)

    for item in data :
        measurement = f'{item.force:^11}|{item.ext:^9}|{item.r100:^9}\n'
        file_obj.write(measurement)

def read_header(file_obj):
    header = file_obj.readline()

    header = header.split(',')
    width = float(header[0].split('=')[1])
    thickness = float(header[1].split('=')[1])
    extl0 = float(header[2].split('=')[1])
    r100l0 = float(header[3].split('=')[1])

    return (width, thickness, extl0, r100l0)

def read_fer(file_obj):

    for line in file_obj.readlines():
        force = float(line.split('|')[0])
        ext = float(line.split('|')[1])
        r100 = float(line.split('|')[2])
        tensil_out_put = TensileOutput (force=force, ext = ext, r100=r100)
        yield tensil_out_put
