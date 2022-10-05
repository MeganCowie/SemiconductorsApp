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
# zins arrays (watch what happens as the tip oscillates - varying zins)

def time_AFMarray(timesteps):
    time_AFMarray = np.linspace(0, 2*np.pi, timesteps)
    return time_AFMarray

def zins_AFMarray(time_AFMarray,amplitude,zins):
    position_AFMarray = amplitude*np.sin(time_AFMarray)+amplitude #nm
    zins_AFMarray = zins+position_AFMarray*1e-7 #cm
    return zins_AFMarray

def zinslag_AFMarray(time_AFMarray,amplitude,frequency,lag,sampletype,  Vg,zins,Eg,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T):

    zins_top = zins+amplitude*1e-7
    zins_bot = zins

    Vstop_soln, F_soln = Physics_Semiconductors.Func_VsF(1,sampletype,   Vg,zins_top,Eg,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T)
    Vsbot_soln, F_soln = Physics_Semiconductors.Func_VsF(1,sampletype,   Vg,zins_bot,Eg,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T)
    Vsdiff_soln = (Vsbot_soln-Vstop_soln)
    lag_soln = 3000*Vsdiff_soln**2/10**9*frequency #radians

    position_AFMarray = amplitude*np.sin(time_AFMarray-lag_soln)+amplitude #nm
    zinslag_AFMarray = zins+position_AFMarray*1e-7 #cm
    return zinslag_AFMarray, lag_soln


def SurfacepotForce_AFMarray(guess,zins_AFMarray,sampletype,RTN,hop,   Vg,zins,Eg,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T):
    Vs_AFMarray = []
    F_AFMarray = []

    for zins_AFMindex in range(len(zins_AFMarray)):
        zins_variable = zins_AFMarray[zins_AFMindex]
        Vs_soln, F_soln = Physics_Semiconductors.Func_VsF(guess+0.1,sampletype,   Vg,zins_variable,Eg,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T)
        Vs_AFMarray = np.append(Vs_AFMarray,Vs_soln)
        F_AFMarray = np.append(F_AFMarray,F_soln)

    return Vs_AFMarray, F_AFMarray


################################################################################
################################################################################
# Frequency shift and dissipation definitions

def dfdg(time_AFMarray,F_AFMarray,frequency,springconst,amplitude,Qfactor,tipradius):
    df_prefactor = -1*(frequency**2)/(2*np.pi*springconst*amplitude*1e-9)
    dg_prefactor = -1*(frequency)/(np.pi)
    dg_addedterm = (springconst*amplitude*1e-9)/(Qfactor)
    tiparea = np.pi*tipradius**2

    # Integrals
    df = df_prefactor*trapz(F_AFMarray*tiparea*np.sin(time_AFMarray), time_AFMarray/frequency)
    dg = dg_addedterm+dg_prefactor*trapz(F_AFMarray*tiparea*np.cos(time_AFMarray), time_AFMarray/frequency)

    # Convert excitation model to energy units, Cockins thesis eq. 2.15
    E_o = np.pi*springconst*(amplitude*10**-9)**2/Qfactor*(1/Physics_Semiconductors.e)*1000 #meV
    A_exc = dg
    A_exco = dg_addedterm
    E_ts = E_o*(A_exc-A_exco)/A_exc
    dg_soln = E_ts

    return df, dg
