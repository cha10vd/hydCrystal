import argparse
import expander
import pickle
from hydCrystal import HydCrystalStructure

parser = argparse.ArgumentParser()
parser.add_argument("filename", type=str, help="Input res string file for\
                    study.", default="")
args = parser.parse_args()
struct_data = {}

def get_key(res_string):
    """Get the structure's key from the title line of .res file"""
    key =(('').join(res_string).split('\n'))[0].split()[1]
    print(key)
    return(key)


def initStruct(entry):
    """Instantiate object from string"""
    title = get_key(entry)
    crystal = HydCrystalStructure()
    crystal.name = title
    crystal.filename = title + '.res'

#    with open(title+'.res', 'w') as f:
#        f.write(entry)

    crystal.init_from_res_string(entry)
    crystal.calculate_symm_ops_per_cell()
    return(crystal)

def pickleData(results, failiures):
    """function to pickle results from void analysis as dictionary of energies,
    densities and average void volumes per molecule"""
    pickle.dump(results, open("results.p", "wb"))
    pickle.dump(failiures, open("failiures.p", "wb"))

with open(args.filename, 'r') as f:
    structures = f.read().split('\n\n')

results = []
failiures = []

# MAIN LOOP:

for structure in structures:
    crystal = initStruct(structure)
    print(crystal)
    try:
        results.append(expander.void_analysis(crystal))
        print("Another is done")
    except:
        failiures.append(crystal.name)
        print("It failed")

print(results)
print(failiures)

pickleData(results, failiures)
