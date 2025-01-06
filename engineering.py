import math
def convert_to_force_displacement(*,data,
                               width ,
                               thickness ,
                               extl0,
                               r100l0,
                               displacement_choice):
    points_x = []
    points_y = []
    if displacement_choice == 1:    
        for item in data:
            (x,y) = (item.ext, item.force)
            points_x.append(x)
            points_y.append(y)
    if displacement_choice == 2:
        for item in data:
            (x,y) = (item.r100, item.force)
            points_x.append(x)
            points_y.append(y)

    return (points_x, points_y)


def convert_to_eng_stress_strain(*,data,
                               width ,
                               thickness ,
                               extl0,
                               r100l0,
                               displacement_choice):
    points_x = []
    points_y = []
    try:    
        if displacement_choice == 1:    
            for item in data:
                (x,y) = (item.ext, item.force)
                strain = x/extl0
                stress = y/(width * thickness)
                points_x.append(strain)
                points_y.append(stress)
        if displacement_choice == 2:
            
            for item in data:
                (x,y) = (item.r100, item.force)
                strain = x/r100l0
                stress = y/(width * thickness)
                points_x.append(strain)
                points_y.append(stress)
    except :
        pass

    return (points_x, points_y)

def conver_to_real_stress_strain(*,data,
                               width ,
                               thickness ,
                               extl0,
                               r100l0,
                               displacement_choice):
    points_x = []
    points_y = []
    try:    
        if displacement_choice == 1:    
            for item in data:
                (x,y) = (item.ext, item.force)
                strain = x/extl0
                stress = y/(width * thickness)
                real_strain = math.log(1+strain, math.e)
                real_stress = stress * ( 1 + strain)
                points_x.append(real_strain)
                points_y.append(real_stress)
        if displacement_choice == 2:
            for item in data:
                (x,y) = (item.r100, item.force)
                strain = x/r100l0
                stress = y/(width * thickness)
                real_strain = math.log(1+strain, math.e)
                real_stress = stress * ( 1 + strain)
                points_x.append(real_strain)
                points_y.append(real_stress)
        
    except:
        pass
  
    return (points_x, points_y)
