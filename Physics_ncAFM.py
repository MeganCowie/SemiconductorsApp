################################################################################
################################################################################
# This script

################################################################################
################################################################################

import numpy as np
from scipy.integrate import trapz

import Physics_Semiconductors

################################################################################
################################################################################

# Frequency shift and dissipation definitions
def dfdg(time_AFMarray,F_AFMarray,Fcant_AFMarray,frequency,springconst,amplitude,Qfactor,tipradius,cantarea,geometrybuttons):
    df_prefactor = -1*(frequency**2)/(2*np.pi*springconst*amplitude) #Hz**2/N
    dg_prefactor = -1*(frequency)/(np.pi) #Hz
    dg_addedterm = (springconst*amplitude)/(Qfactor) #N
    tiparea = np.pi*tipradius**2 #m**2

    F_tot = 0
    if 1 in geometrybuttons:
        F_tot+=F_AFMarray*tiparea
    if 2 in geometrybuttons:
        F_tot+=Fcant_AFMarray*cantarea

    # Integrals
    df = df_prefactor*trapz(F_tot*np.cos(frequency*time_AFMarray), time_AFMarray) #Hz
    dg = dg_prefactor*trapz(F_tot*np.sin(frequency*time_AFMarray), time_AFMarray)+dg_addedterm #N

    # Convert excitation model to energy units
        # Cockins thesis eq. 2.15
    E_o = np.pi*springconst*amplitude**2/Qfactor/Physics_Semiconductors.e*1000 #meV
    A_exc = dg
    A_exco = dg_addedterm
    E_ts = E_o*(A_exc-A_exco)/A_exco #meV
    dg = E_ts #meV

    return df, dg
