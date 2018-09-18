from hydCrystal import HydCrystalStructure
from niggli import niggli
import argparse
import expander
import os

from opt_dicts import (af, mf, press_str, neighcrys_args,
   gdma_args, gaussian_args, dmacrys_args)

parser = argparse.ArgumentParser()
parser.add_argument("filename", type=str, help="Input res string file for\
                    study.", default="")
args = parser.parse_args()

crystal = expander.openFile(args.filename)
crystal.filename = args.filename

def gen_axis(crystal):
	if ( not os.path.isfile('dehyd.mult')):
		expander.set_hyd_stat(crystal, False)
		expander.stdMin(crystal)

gen_axis(crystal)
