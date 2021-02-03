import numpy as np
from scipy.integrate import trapz
from scipy.optimize import fsolve
import Physics_Semiconductors
import Physics_AFMoscillation

################################################################################
################################################################################
# physical constants

kB = Physics_Semiconductors.kB
hbar = Physics_Semiconductors.hbar
me = Physics_Semiconductors.me
e = Physics_Semiconductors.e
epsilon_o = Physics_Semiconductors.epsilon_o


################################################################################
################################################################################
# Integrals from Holscher 2001 and RoyGobeil thesis

def dfdg(Vg_array,steps,amplitude,frequency,springconst,Qfactor,tipradius,  Vg,zins,bandgap,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T):


    time_AFMarray = Physics_AFMoscillation.time_AFMarray(steps)
    zins_AFMarray = Physics_AFMoscillation.zins_AFMarray(time_AFMarray,amplitude,zins)


    ######################################################



    df_prefactor = frequency**2/(springconst*amplitude*1e-9)
    dg_prefactor = 2*frequency/(springconst*amplitude*1e-9)
    tiparea = np.pi*tipradius**2

    df_biasarray = []
    dg_biasarray = []
    for Vg_index in range(len(Vg_array)):
        Vg_variable = Vg_array[Vg_index]
        Vs_AFMarraysoln, F_AFMarraysoln = Physics_AFMoscillation.SurfacepotForce_AFMarray(1,zins_AFMarray,   Vg_variable,zins,bandgap,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T)

        df_soln = df_prefactor*trapz(F_AFMarraysoln*tiparea*np.sin(time_AFMarray), time_AFMarray/frequency)
        dg_soln = dg_prefactor*trapz(F_AFMarraysoln*tiparea*np.cos(time_AFMarray), time_AFMarray/frequency)+1/Qfactor

        df_biasarray = np.append(df_biasarray, df_soln)
        dg_biasarray = np.append(dg_biasarray, dg_soln)

    return df_biasarray, dg_biasarray
