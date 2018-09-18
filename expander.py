from hydCrystal import HydCrystalStructure
from niggli import niggli
import os

"""Dictionaries necessary for reoptimization"""

press_str = '0.0 KPa'

af = {'hyd': '../hyd.axis', 'dehyd': '../dehyd.axis'}
mf = {'hyd': '../hyd.mult', 'dehyd': '../dehyd.mult'}


neighcrys_args = {
     'pressure': press_str, 'foreshorten_hydrogens': 'n', 'max_search': 7,
     'force_field_type': 'F', 'multipole_file': mf['hyd'],
     'potential_file':'/home/vdn1m17/cspy/potentials/fit_water_X.pots',
     'dont_check_anisotropy': True}
gdma_args = {'ms': 4.0}
gaussian_args = {'opt': 'EmpiricalDispersion=GD3BJ'}
dmacrys_args = {}

def remove_files(crystal):
    if os.path.isfile(crystal.name + "_void.res"): os.remove(crystal.name + "_void.res")
    if os.path.isfile(crystal.name + "_void.lis"): os.remove(crystal.name + "_void.lis")
    if os.path.isfile("check.def"): os.remove("check.def")
    if os.path.isfile(crystal.name+".zip"): os.remove(crystal.name+".zip")
    if os.path.isfile(crystal.name+".zip"): os.remove(crystal.name+".res")

def update_press_str(press):
    """Pressure string update function"""
    global press_str
    press_str = '{} KPa'.format(press)

def set_hyd_stat(crystal, hyd=True):
    """Helper function to alter the hydration state parameters for a given
    crystal in the course of an optimization"""
    if hyd == True:
        neighcrys_args['multipole_file'] = mf['hyd']
#        neighcrys_args['axis_file'] = af['hyd']
    elif hyd == False:
        crystal.dehydrate()
        neighcrys_args['multipole_file'] = mf['dehyd']
 #       neighcrys_args['axis_file'] = af['dehyd']


def stdMin(item, pressure=0.0, arg1=neighcrys_args ,arg2=gaussian_args,
           arg3=gdma_args, arg4=dmacrys_args):
    """Helper function for structural energy minimization"""
    update_press_str(pressure)
    item.energy_minimize(
        "default", ".", arg1, arg2, arg3, arg4)
    print("NAME: ", item.name, "\n\n")
    print(item.energy)
    print(item.data_summary.final_density)


def openFile(filename):
    """Extracts res string from file"""
    with open(filename, 'r') as f:
        entry = f.read()
        crystal = initStruct(entry)
        return(crystal)

def initStruct(res_string):
    """Instantiates object from res string"""
    title = ((res_string).split('\n')[0]).split()[1]
    crystal = HydCrystalStructure()
    crystal.name = title
    crystal.init_from_res_string(res_string)
    crystal.calculate_symm_ops_per_cell()
    return(crystal)


def calc_void_vols(crystal):
    """Request cspy void volume calculation, and delete calculation files at the
    end."""
    from numpy import sum
    void_vols = crystal.void_volumes()
    remove_files(crystal)
    return(void_vols)

def extract_data(crystal, final=True):
    """Function designed to extract useful data from a crystal energy
    miminization procedure.

    :param final: True for post-minimization data, False for pre-minmiization."""
    stats = [None, None]
    if final == True:
        stats[0] = crystal.data_summary.final_energy
        stats[1] = crystal.data_summary.final_density
        return(stats)
    if final == False:
        stats[0] = crystal.data_summary.initial_energy
        stats[1] = crystal.data_summary.initial_density
        return(stats)

def void_analysis(crystal):
    global neighcrys_args

    en = {'orig': None, 'dehyd': None, 'reopt': None}
    den = {'orig': None, 'dehyd': None, 'reopt': None}
    voids = {'orig': None, 'dehyd': None, 'reopt': None}

    crystal = niggli(crystal)
    print("\n\nMonohydrate void analysis:")
    print("--------------------------\n")
    set_hyd_stat(crystal, True)
    stdMin(crystal)
    en['orig'], den['orig'] = extract_data(crystal)
    voids['orig'] = crystal.avg_void_vol()

    remove_files(crystal)

    set_hyd_stat(crystal, False)
    print(neighcrys_args)
    print("\n\nDehydrated void analysis:")
    print("-------------------------\n")
    voids['dehyd'] = crystal.avg_void_vol()
    print("\n\nReoptimized void analysis:")
    print("--------------------------\n")
    stdMin(crystal)
    reopt_crystal = initStruct(crystal.data_summary.final_res_string)
    reopt_crystal.name = crystal.name
    voids['reopt'] = reopt_crystal.avg_void_vol()
    en['dehyd'], den['dehyd'] = extract_data(crystal, False)
    en['reopt'], den['reopt'] = extract_data(crystal, True)

    remove_files(crystal)

    stats = {'key': crystal.name, 'energy': en, 'density': den, 'voids': voids}

    print(stats)

    return(stats)



if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("filename", type=str, help="Input res string file for\
                        study.", default="")
    args = parser.parse_args()
    crystal = openFile(args.filename)
    crystal.filename = args.filename

    data = void_analysis(crystal)

    print(data)
