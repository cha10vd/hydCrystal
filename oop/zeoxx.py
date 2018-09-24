from cspy.alpha.cspy_links import ZEOXX_EXEC

def calc_void_dims(crystal=None, ha=False):
    '''Routine developed to elucidate dimensionality of voids in crystal using
    Zeo++.

    Zeo++ Syntax:   ./network -chan probe_radius input_structure.cssr
              eg:   ./network -ha -chan 1.5 EDI.cssr

    '''
    import os
    from subprocess import call

    print("Performing void calculation with Zeo++...")
    if crystal is None:
        structure = self.parent
    else:
        structure = crystal
    

calc_void_dims()
