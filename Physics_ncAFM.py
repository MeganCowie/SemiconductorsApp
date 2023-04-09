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

# Add an effective force from the oxide overlayer
    #(Should be a polarization force, not a capacitive one... model as a linear force by putting in a very high dopant density)
def overlayer(Vg,zins,T,CPD): 

    Nd, Na = round(10**40)/(1e9), 0 #/m**3
    mn, mp = 1*Physics_Semiconductors.me, 1*Physics_Semiconductors.me #kg
    Eg = 1*Physics_Semiconductors.e #J
    epsilon_oxide = 3.9

    NC,NV = Physics_Semiconductors.Func_NCNV(T, mn, mp)
    Ec,Ev = Physics_Semiconductors.Func_EcEv(Eg)
    ni = Physics_Semiconductors.Func_ni(NC, NV, Eg, T)
    nb,pb = Physics_Semiconductors.Func_nbpb(Na, Nd, ni)
    
    Vs_over = Physics_Semiconductors.Func_Vs(Vg,zins,CPD,Na,Nd,epsilon_oxide,T,nb,pb,ni)
    f_over = Physics_Semiconductors.Func_f(T,Vs_over,nb,pb)
    Es_over = Physics_Semiconductors.Func_E(nb,pb,Vs_over,epsilon_oxide,T,f_over)
    Qs_over = Physics_Semiconductors.Func_Q(epsilon_oxide,Es_over)
    F_over = Physics_Semiconductors.Func_F(Qs_over,CPD,Vg,zins)
    return F_over


# Frequency shift and dissipation definitions
def dfdg(time_AFMarray,F_AFMarray,Fcant_AFMarray,Fover_AFMarray,frequency,springconst,amplitude,Qfactor,tipradius,cantarea,geometrybuttons):
    df_prefactor = -1*(frequency**2)/(2*np.pi*springconst*amplitude) #Hz**2/N
    dg_prefactor = -1*(frequency)/(np.pi) #Hz
    dg_addedterm = (springconst*amplitude)/(Qfactor) #N
    tiparea = np.pi*tipradius**2 #m**2

    F_tot = 0
    if 1 in geometrybuttons:
        F_tot+=F_AFMarray*tiparea
    if 2 in geometrybuttons:
        F_tot+=Fcant_AFMarray*cantarea
    if 3 in geometrybuttons:
        F_tot+=Fover_AFMarray*tiparea
    if 4 in geometrybuttons:
        F_tot+=F_AFMarray*tiparea+Fcant_AFMarray*cantarea+Fover_AFMarray*tiparea

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
