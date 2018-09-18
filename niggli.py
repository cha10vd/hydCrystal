from cspy.alpha.crystal import CrystalStructure
from hydCrystal import HydCrystalStructure

XRD_threshold = 200

def squashed(crystal):
    """ Calculate squashing parameter of crystal to test necessity for
    nigglying."""
    ang_comp = crystal.lattice.lattice_parameters_volume()
    print(ang_comp)
    len_comp = crystal.lattice.length_component_of_volume()
    print(len_comp)
    squash = (ang_comp/len_comp)

    print("\n-----------------------------------")
    print("The squashing parameter is: {:05.2f}".format(squash))
    print("-----------------------------------\n")

    return (True if (squash < 0.5) else False)


def delete_temp_files():
    """ Following compleption of niggli coparison, remove temporary files
    created for routine"""
    from os import remove
    remove("original.res")
    remove("niggli.res")


def identical(crystal1_res, crystal2_res, XRD_thresh=XRD_threshold):
    """test for idenity of crystals 1 and 2. tries dynamic timewarping, if this
    fails we try COMPACK comparison. return boolean for success"""
    from numpy import min
    from cspy.alpha.lib import cdtw
    import calc_xrd as xrd

    xrd_c1 = xrd.calc_xrd(crystal1_res)
    xrd_c2 = xrd.calc_xrd(crystal2_res)

    XRD_diff = [cdtw.cdtw_sakoe_chiba(xrd_c1, xrd_c2, XRD_diff) for \
                XRD_diff in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]]
    if min(XRD_diff) < XRD_thresh:
        print("Niggli accepted.")
        delete_temp_files()
        return True
    else:
        from cspy.alpha import process_data_tools as pdt
        import os

        print("XRD failed, trying COMPACK.")
        with open('original.res', 'w') as o:
            o.write(crystal1_res)
        with open('niggli.res', 'w') as n:
            n.write(crystal2_res)

        success, rms, exit_status = pdt.compack_2_match(
                'original.res',
                'niggli.res')

        os.remove(compack_results.txt)

        if(success == True):
            print("Niggli accepted.")
            delete_temp_files()
            return True
        else:
            print("No change made to structure.")
            delete_temp_files()
            return False


def niggli(input):
    """Routine defined to optimize unit cell representation prior to
    calculations such as solid-state DFT, void analysis, et cetera, where
    programs struggle to deal with highly flat cells."""

    if type(input) == str:
        print("STRING")
        crystal1 = CrystalStructure()
        crystal1.init_from_res_string(input)# Main copy of crystal. Takes in
                                            # original representation of
                                            # crystal and is replaced by
                                            # nigglied copy if squashed and
                                            # niggli successful.

    elif isinstance(input, CrystalStructure):
        print("OBJECT")
        crystal1 = input

    else:
        print("ERROR")
        return(IOError)

    if squashed(crystal1) is True:
        crystal1_res = str(crystal1.res_string_form())

        crystal2 = input                   # serves as temporary copy of
                                           # structure as its tested for
                                           # success of niggli process.
        crystal2.krivy_gruber()

        crystal2_res = str(crystal2.res_string_form())

        if identical(crystal1_res, crystal2_res) is True:
            return crystal2
        else:
            return input    # Nigglied structure NOT same as original, do not
                            # replace.

    else:
        return input        # Fed in structure is not squished, keep as is.


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", type=str)
    args = parser.parse_args()

    with open(args.input_file, 'r') as f:
        data = f.read()

    crystal_object = CrystalStructure()
    crystal_object.init_from_res_string(data)

    new_res = niggli(crystal_object).res_string_form()
    print(new_res)
