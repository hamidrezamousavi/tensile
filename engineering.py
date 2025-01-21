
from typing import Tuple
import math
from util import MattProperties

def force_displacement_calculatoin(*,data,
                               width ,
                               thickness ,
                               extl0,
                               r100l0,
                               displacement_choice):
    displacements = []
    forces = []
    if displacement_choice == 1:    
        for item in data:
            (x,y) = (item.ext, item.force)
            displacements.append(x)
            forces.append(y)
    if displacement_choice == 2:
        for item in data:
            (x,y) = (item.r100, item.force)
            displacements.append(x)
            forces.append(y)
    properties = MattProperties()
    properties.curve = (displacements, forces)
   
    return properties


def eng_stress_strain_calculatoin(*,data,
                               width ,
                               thickness ,
                               extl0,
                               r100l0,
                               displacement_choice):
    strains = []
    stresses = []
    properties = None

    try:    
        if displacement_choice == 1:    
            for item in data:
                (x,y) = (item.ext, item.force)
                strain = x/extl0
                stress = y/(width * thickness)
                strains.append(strain)
                stresses.append(stress)
        if displacement_choice == 2:
            
            for item in data:
                (x,y) = (item.r100, item.force)
                strain = x/r100l0
                stress = y/(width * thickness)
                strains.append(strain)
                stresses.append(stress)

        properties = MattProperties()
        properties.curve = (strains, stresses)
        properties.uts , properties.strain_at_uts = find_uts(
                                            stresses, strains)

        properties.strain_at_break, properties.stress_at_break = \
            find_strain_at_break(strains, stresses)
        properties.elasticity_modulu = find_elasticity_modulu(strains, stresses)
    except :
        pass
    return properties

def real_stress_strain_calculatoin(*,data,
                               width ,
                               thickness ,
                               extl0,
                               r100l0,
                               displacement_choice):
    strains = []
    stresses = []
    try:    
        if displacement_choice == 1:    
            for item in data:
                (x,y) = (item.ext, item.force)
                strain = x/extl0
                stress = y/(width * thickness)
                real_strain = math.log(1+strain, math.e)
                real_stress = stress * ( 1 + strain)
                strains.append(real_strain)
                stresses.append(real_stress)
        if displacement_choice == 2:
            for item in data:
                (x,y) = (item.r100, item.force)
                strain = x/r100l0
                stress = y/(width * thickness)
                real_strain = math.log(1+strain, math.e)
                real_stress = stress * ( 1 + strain)
                strains.append(real_strain)
                stresses.append(real_stress)
        
    except:
        pass
  
    properties = MattProperties()
    properties.curve = (strains, stresses)

    properties.elasticity_modulu = find_elasticity_modulu(strains, stresses)
    return properties

def find_uts(stresses, strains):
    uts = max(stresses)
    index = stresses.index(uts)
    uts_strain = strains[index]
    return (uts, uts_strain)

def find_strain_at_break(strains, stresses):
    uts = max(stresses)
    break_def = uts * 0.2
    uts_index = stresses.index(uts)
    for i in range(uts_index,len(strains)):
        if stresses[i] < break_def:
            strain_at_break = strains[i]
            stress_at_break = stresses[i]
            break
    else:
        strain_at_break = strains[-1]
        stress_at_break = stresses[-1]

    return (strain_at_break, stress_at_break) 

def find_elasticity_modulu(strains, stresses):
    
    modulu1 ,_ = linear_regression(strains[0:3],stresses[0:3])
    modulu2, _ = linear_regression(strains[0:10],stresses[0:10])
    modulu3, _ = linear_regression(strains[0:50],stresses[0:50])

    return (modulu1,modulu2, modulu3)


def linear_regression(xs:list, ys:list)->Tuple[float, float]:
    """
    assum line is y = ax + b
    return a, b
    """
    try:
        product_sum = sum([x * y for x,y in zip(xs, ys)])
        xsquar_sum = sum(x * x for x in xs)
        xsum_squar = sum(xs)* sum(xs)
        a = ((len(xs)* product_sum) - (sum(xs) * sum(ys)))/ (len(xs)*xsquar_sum - xsum_squar)
        b = (xsquar_sum * sum(ys) - sum(xs) * product_sum)/ (len(xs)*xsquar_sum - xsum_squar)
    except :
        a = 0
        b = 0
    return (a, b)