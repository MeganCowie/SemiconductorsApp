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

def dfdg(time_AFMarray,F_AFMarray,frequency,springconst,amplitude,Qfactor,tipradius):
    df_prefactor = -1*(frequency**2)/(2*np.pi*springconst*amplitude) #Hz**2/N
    dg_prefactor = -1*(frequency)/(np.pi) #Hz
    dg_addedterm = (springconst*amplitude)/(Qfactor) #N
    tiparea = np.pi*tipradius**2 #m**2

    # Integrals
    df = df_prefactor*trapz(F_AFMarray*tiparea*np.sin(time_AFMarray-np.pi/2), time_AFMarray/frequency) #Hz
    dg = dg_addedterm+dg_prefactor*trapz(F_AFMarray*tiparea*np.cos(time_AFMarray-np.pi/2), time_AFMarray/frequency) #N

    # Convert excitation model to energy units, Cockins thesis eq. 2.15
    E_o = np.pi*springconst*tipradius**2/Qfactor/Physics_Semiconductors.e*1000 #meV
    A_exc = dg
    A_exco = dg_addedterm
    E_ts = E_o*(A_exc-A_exco)/A_exc #meV
    dg = E_ts #meV

    return df, dg
