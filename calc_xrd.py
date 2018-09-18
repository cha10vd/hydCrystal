from cspy.alpha.cspy_links import PLATON_EXEC
from cspy.alpha.popen_timeout import PopenTimeout
import numpy as np

def calc_xrd(final_res_string):

    timeout = 5

    """
    Calculates the XRD pattern using platon
    final_res_string: a res file as a string taken from a .db file

    used by:
    dump_clustered_data
    get_clustered_data
    """

    tmp_res_file = open("tmp.res","w")
    tmp_res_file.write(final_res_string)
    tmp_res_file.close()

    xrd=[]
    #os.system("/home/dm1m15/cspy-1.0/progs/platon/platon -o -Q tmp.res")
    #os.system(PLATON_EXEC + " -o -Q tmp.res > /dev/null")
    o = open('/dev/null','w')
    status = PopenTimeout([PLATON_EXEC,  "-o", "-Q", "tmp.res"], output_file=o).run(timeout)
    try:
        XRD_result=open("tmp.cpi","r")
    except IOError as e:
        print("I/O error({0}): {1}".format(e.errno, e.strerror))
        return None
    read=False
    for lines in XRD_result:
        if read == True:
            xrd.append(float(lines.strip()))
        if "SCANDATA" in lines:
            read=True
    xrd=np.array(xrd,dtype='float64')
    XRD_result.close()

    try:
        os.system("rm tmp.res tmp.cpi tmp.lis tmp.ps tmp_pl.spf")
    except:
        pass
    return xrd
