from cspy.alpha.crystal import CrystalStructure

class HydCrystalStructure(CrystalStructure):
    """ A simple extension of Crystal class for providing extra functionality
    particular to hydrate crystals"""
    def dehydrate(self):
        """Function to remove water molecules from crystal"""
        for molecule in self.unique_molecule_list:
            if len(molecule.atoms) == 3:
                n_O = 0
                n_H = 0
                for atom in molecule.atoms:
                    if atom.atomic_number == 8:
                        n_O += 1
                    elif atom.atomic_number == 1:
                        n_H += 1
                if (n_O == 1 and n_H == 2):
                    print("we have a water")
                    self.unique_molecule_list.remove(molecule)

    def avg_void_vol(self):
        import os, glob

        tot_void_vol = 0
        for void in self.void_volumes():
            tot_void_vol += void
        return(tot_void_vol/self.symm_ops_per_cell)

        try:
            os.remove(self.name + "_void.res")
#            lis_files = glob.glob("*.lis")
#            for file in lis_files:
#                os.remove(file)
            os.remove(self.name + "_void.lis")
        except IOError:
            print("FAILED TO DELETE REQUESTED FILES!!!")
        else:
            print("SUCCESSFULLY DELETED VOID STUFF")
