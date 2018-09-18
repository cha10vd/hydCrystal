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
