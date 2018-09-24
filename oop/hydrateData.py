from hydCrystal import HydCrystalStructure
import logging
import unittest

LOG = logging.getLogger(__name__)

class HydrateData:

    def __init__(self, res_string):
        title = ((res_string).split('\n')[0]).split()[1]

        self.orig = HydCrystalStructure()
        self.orig.name = title + '_orig'
        self.orig.filename = self.orig.name + '.res'
        self.orig.init_from_res_string(res_string)
        self.orig.calculate_symm_ops_per_cell()
        self.orig.neighcrys_args['multipole_file'] = '../hyd.mult'
        self.orig.stdMin()
        self.orig.voids.calc_void(None, 0.99,0.09)
        LOG.debug(self.orig.voids.__dict__)

        os.remove(self.orig.name + ".zip")

        self.dehyd = HydCrystalStructure()
        self.dehyd.name = title + '_dehyd'
        self.dehyd.filename = self.dehyd.name + '.res'
        self.dehyd.init_from_res_string(self.orig.data_summary.final_res_string)
        self.dehyd.dehydrate()
        self.dehyd.neighcrys_args['multipole_file'] = '../dehyd.mult'
        self.dehyd.neighcrys_args['max_iterations'] = 0
        self.dehyd.stdMin()
        self.dehyd.voids.calc_void(None, 0.99, 0.09)

        os.remove(self.dehyd.name + ".zip")

        self.reopt = HydCrystalStructure()
        self.reopt.name = title +'_reopt'
        self.reopt.filename = self.reopt.name + '.res'
        self.reopt.init_from_res_string(self.dehyd.data_summary.final_res_string)
        self.reopt.neighcrys_args['multipole_file'] = '../dehyd.mult'
        self.reopt.stdMin()
        self.reopt.voids.calc_void(None, 0.99, 0.09)

        os.remove(self.reopt.name + ".zip")


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
            self.structure    = HydrateData(test_res)
            self.hyd_en   = self.structure.orig.energy
            self.dehyd_en = self.structure.dehyd.energy
            self.reopt_en = self.structure.reopt.energy

        def tearDown(self):
            pass

        def test_orig(self):
            self.assertAlmostEqual(self.hyd_en['lattice'], -151.8821, places=3)
            self.assertAlmostEqual(self.dehyd_en['lattice'], -68.4916, places=3)
            self.assertAlmostEqual(self.reopt_en['lattice'], -147.8891, places=3)

    unittest.main()
