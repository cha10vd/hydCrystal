from cspy.alpha.crystal import CrystalStructure
import logging

LOG = logging.getLogger(__name__)

class HydCrystalStructure(CrystalStructure):
    """ A simple extension of Crystal class for providing extra functionality
    particular to hydrate crystals"""

    def __init__(self, filename=None):
        CrystalStructure.__init__(self, filename=None)
        self.press_str = '0.0 KPa'

        #   must insert 'multipole_file': hyd.mult entry into neighcrys_args dict
        #   before running minimization

        self.neighcrys_args = {
             'foreshorten_hydrogens': 'n', 'max_search': 7,
             'force_field_type': 'F', 'pressure': self.press_str,
             'potential_file':'/home/vdn1m17/cspy/potentials/fit_water_X.pots',
             'dont_check_anisotropy': True}
        self.gdma_args = {'ms': 4.0}
        self.gaussian_args = {'opt': 'EmpiricalDispersion=GD3BJ'}
        self.dmacrys_args = {}

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
                    LOG.info("we have a water")
                    self.unique_molecule_list.remove(molecule)

    def update_press_str(self, press=0.0):
        """Pressure string update function"""
        self.press_str = '{} KPa'.format(press)
        self.neighcrys_args['pressure'] = self.press_str

    def stdMin(self):
        """Helper function for structural energy minimization"""

        arg1 = self.neighcrys_args
        arg2 = self.gaussian_args
        arg3 = self.gdma_args
        arg4 = self.dmacrys_args

        LOG.debug("%s %s %s %s", arg1, arg2, arg3, arg4)

        self.energy_minimize("default", ".", arg1, arg2, arg3, arg4)
        LOG.debug("NAME: %s\n\n", self.name)
        LOG.info(self.energy)
        LOG.info(self.data_summary.final_density)


if __name__ == '__main__':

    import unittest
    import os

    test_res =  "TITL 100301457938 -151.882 1.4276\n"\
                "CELL 0.7 6.5051 14.7219 7.1155 90.0 79.77 90.0\n"\
                "ZERR 4\n"\
                "LATT 1\n"\
                "SYMM -X,+Y+1/2,-Z+1/2\n"\
                "SFAC O H C N\n"\
                "O1 1 0.789510090 0.475219440 0.027433810\n"\
                "H1 2 0.905352890 0.435213220 0.034738090\n"\
                "H2 2 0.750976960 0.460251740 -0.093723850\n"\
                "O2 1 0.348755270 0.599943160 0.296877980\n"\
                "O3 1 0.998958340 0.697173510 0.010943310\n"\
                "H3 2 0.486901160 0.891151260 0.257722110\n"\
                "H4 2 1.040164030 0.880241310 0.136506980\n"\
                "H5 2 0.956330670 0.884614700 -0.084403800\n"\
                "H6 2 0.830313930 0.953269850 0.107561470\n"\
                "H7 2 0.268751580 0.764018020 0.346112060\n"\
                "H8 2 0.720375230 0.585628380 0.127875240\n"\
                "C1 3 0.469657930 0.662100780 0.247227910\n"\
                "C2 3 0.823704760 0.718077060 0.091773590\n"\
                "C3 3 0.750259950 0.811438670 0.132400670\n"\
                "C4 3 0.551609360 0.824078490 0.223139740\n"\
                "C5 3 0.901485650 0.886960400 0.070120470\n"\
                "N1 4 0.673846860 0.650735660 0.154088930\n"\
                "N2 4 0.416510410 0.752899570 0.278482160\n"\
                "END"

    class MyTest(unittest.TestCase):
        def setUp(self):
            self.structure = HydCrystalStructure()
            self.structure.name = "test_structure"
            self.structure.filename = "test_structure.res"
            self.structure.init_from_res_string(test_res)
            self.structure.neighcrys_args['multipole_file'] = '../hyd.mult'
            self.structure.stdMin()

            os.remove(self.structure.name + ".zip")
            self.hyd_energy = self.structure.data_summary.final_energy

            self.structure.dehydrate()
            self.structure.neighcrys_args['multipole_file'] = '../dehyd.mult'
            self.structure.stdMin()

            self.dehyd_energy = self.structure.data_summary.initial_energy
            self.reopt_energy = self.structure.data_summary.final_energy

        def tearDown(self):
            os.remove(self.structure.name + ".zip")

        def test_orig(self):
            self.assertEqual(self.hyd_energy, -151.8821)
        def test_dehyd(self):
            self.assertEqual(self.dehyd_energy, -68.4916)
        def test_reopt(self):
            self.assertEqual(self.reopt_energy, -147.8891)

    unittest.main()
