################################################################################
################################################################################
# This script calculates the frequency shift and dissipation by integrating the
# in-phase and out-of phase contributions to the time-dependent force (found in
# Physics_AFMoscillaiton). The second function is simply to visualize hopping.
################################################################################
################################################################################

import numpy as np
from numpy import random
from scipy.integrate import trapz
from scipy.optimize import fsolve
import Physics_Semiconductors
import Physics_SurfacepotForce
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

def dfdg_biasarray(Vg_array,steps,amplitude,frequency,springconst,Qfactor,tipradius,sampletype,hop,lag,  Vg,zins,bandgap,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T):

    time_AFMarray = Physics_AFMoscillation.time_AFMarray(steps)
    zins_AFMarray = Physics_AFMoscillation.zins_AFMarray(time_AFMarray,amplitude,zins)
    zinslag_AFMarray = Physics_AFMoscillation.zinslag_AFMarray(time_AFMarray,amplitude,zins,lag)

    ######################################################

    df_prefactor = -1*(frequency**2)/(2*np.pi*springconst*amplitude*1e-9)
    dg_prefactor = -frequency**2/(np.pi)
    dg_addedterm = (1*amplitude)/(2*Qfactor)
    scaling = 400
    tiparea = np.pi*tipradius**2

    df_biasarray = []
    dg_biasarray = []
    for Vg_index in range(len(Vg_array)):
        Vg_variable = Vg_array[Vg_index]

        Vs_AFMarraysoln, F_AFMarraysoln = Physics_AFMoscillation.SurfacepotForce_AFMarray(1,zinslag_AFMarray,sampletype,False,hop,   Vg_variable,zins,bandgap,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T)

        df_soln = df_prefactor*trapz(F_AFMarraysoln*tiparea*np.sin(time_AFMarray), time_AFMarray/frequency)
        dg_soln = scaling*(dg_addedterm+dg_prefactor*trapz(F_AFMarraysoln*tiparea*np.cos(time_AFMarray), time_AFMarray/frequency))

        df_biasarray = np.append(df_biasarray, df_soln)
        dg_biasarray = np.append(dg_biasarray, dg_soln)

    return df_biasarray, dg_biasarray



################################################################################
################################################################################
# Physics over time -- NOT FINISHED YET and not needed for MoSe2 data.

def dfdg_timearray(time_array,steps,amplitude,frequency,springconst,Qfactor,tipradius,sampletype,hop,lag,  Vg,zins,bandgap,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T):

    time_AFMarray = Physics_AFMoscillation.time_AFMarray(steps)
    zins_AFMarray = Physics_AFMoscillation.zins_AFMarray(time_AFMarray,amplitude,zins)
    zinslag_AFMarray = Physics_AFMoscillation.zinslag_AFMarray(time_AFMarray,amplitude,zins,lag)

    Vs_AFMtimearray = []
    F_AFMtimearray = []
    df_AFMtimearray = []
    dg_AFMtimearray = []

    df_prefactor = -1*(frequency**2)/(2*np.pi*springconst*amplitude*1e-9)
    dg_prefactor = -frequency/(np.pi)
    tiparea = np.pi*tipradius**2

    ######################################################
    #Find AFM oscillation solutions Vs, F, df, dg for two cases: Nd and Nd+1

    Vs_AFMarray_Nd0 = []
    F_AFMarray_Nd0 = []
    Vs_AFMarray_Nd0, F_AFMarray_Nd0 = Physics_AFMoscillation.SurfacepotForce_AFMarray(1,zinslag_AFMarray,sampletype,False,0,   Vg,zins,bandgap,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T)
    df_Nd0 = df_prefactor*trapz(F_AFMarray_Nd0*tiparea*np.sin(time_AFMarray), time_AFMarray/frequency)
    dg_Nd0 = dg_prefactor*trapz(F_AFMarray_Nd0*tiparea*np.cos(time_AFMarray), time_AFMarray/frequency)

    slider_donor = 19
    Nd = round((10**(slider_donor+hop)*10**8)/(1000**3))
    Vs_AFMarray_Nd1 = []
    F_AFMarray_Nd1 = []
    Vs_AFMarray_Nd1, F_AFMarray_Nd1 = Physics_AFMoscillation.SurfacepotForce_AFMarray(1,zinslag_AFMarray,sampletype,False,0,   Vg,zins,bandgap,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T)
    df_Nd1 = df_prefactor*trapz(F_AFMarray_Nd1*tiparea*np.sin(time_AFMarray), time_AFMarray/frequency)
    dg_Nd1 = dg_prefactor*trapz(F_AFMarray_Nd1*tiparea*np.cos(time_AFMarray), time_AFMarray/frequency)


    ######################################################
    #Set Nd to Nd+1 with a random probability at one moment in the time trace
    for time_arrayindex in range(len(time_array)):

        flip = np.random.randint(2)

        if flip == 0:
            df_Nd = df_Nd0
            dg_Nd = dg_Nd0
        else:
            df_Nd = df_Nd1
            dg_Nd = dg_Nd1

        df_AFMtimearray = np.append(df_AFMtimearray,df_Nd)
        dg_AFMtimearray = np.append(dg_AFMtimearray,dg_Nd)

    return df_AFMtimearray, dg_AFMtimearray
