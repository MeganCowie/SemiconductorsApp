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
# Add an effective force from the cantilever
    #(Uses the same physics as the tip apex, just at a different tip-sample separation and effective area)
def cantilever(Vg,zins,CPD,Na,Nd,epsilon_sem,T,nb,pb,ni,cantheight): 
    Vs_cant = Physics_Semiconductors.Func_Vs(Vg,zins+cantheight,CPD,Na,Nd,epsilon_sem,T,nb,pb,ni)
    f_cant = Physics_Semiconductors.Func_f(T,Vs_cant,nb,pb)
    Es_cant = Physics_Semiconductors.Func_E(nb,pb,Vs_cant,epsilon_sem,T,f_cant)
    Qs_cant = Physics_Semiconductors.Func_Q(epsilon_sem,Es_cant)
    F_cant = Physics_Semiconductors.Func_F(Qs_cant,CPD,Vg,zins+cantheight)
    return F_cant


# Frequency shift and dissipation definitions
def dfdg(time_AFMarray,F_AFMarray,Fcant_AFMarray,frequency,springconst,amplitude,Qfactor,tipradius,cantarea):
    df_prefactor = -1*(frequency**2)/(2*np.pi*springconst*amplitude) #Hz**2/N
    dg_prefactor = -1*(frequency)/(np.pi) #Hz
    dg_addedterm = (springconst*amplitude)/(Qfactor) #N
    tiparea = np.pi*tipradius**2 #m**2

    F_tot = F_AFMarray*tiparea+Fcant_AFMarray*cantarea

    # Integrals
    df = df_prefactor*trapz(F_tot*np.sin(time_AFMarray-np.pi/2), time_AFMarray/frequency) #Hz
    dg = dg_addedterm+dg_prefactor*trapz(F_tot*np.cos(time_AFMarray-np.pi/2), time_AFMarray/frequency) #N

    # Convert excitation model to energy units
        # Cockins thesis eq. 2.15
    E_o = np.pi*springconst*tipradius**2/Qfactor/Physics_Semiconductors.e*1000 #meV
    A_exc = dg
    A_exco = dg_addedterm
    E_ts = E_o*(A_exc-A_exco)/A_exc #meV
    dg = E_ts #meV

    return df, dg
