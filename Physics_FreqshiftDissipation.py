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
from joblib import Parallel, delayed

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
# Integrals to calculate frequency shift and dissipation

def dfdg_biasarray(Vg_array,steps,amplitude,frequency,springconst,Qfactor,tipradius,sampletype,hop,lag,  Vg,zins,bandgap,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T):

    time_AFMarray = Physics_AFMoscillation.time_AFMarray(steps)
    zins_AFMarray = Physics_AFMoscillation.zins_AFMarray(time_AFMarray,amplitude,zins)
    zinslag_AFMarray = Physics_AFMoscillation.zinslag_AFMarray(time_AFMarray,amplitude,zins,lag)

    ######################################################

    df_prefactor = -1*(frequency**2)/(2*np.pi*springconst*amplitude*1e-9)
    dg_prefactor = -1*(frequency)/(np.pi)
    dg_addedterm = (springconst*amplitude*1e-9)/(Qfactor)
    tiparea = np.pi*tipradius**2

    def compute(Vg_variable):
        Vs_AFMarraysoln, F_AFMarraysoln = Physics_AFMoscillation.SurfacepotForce_AFMarray(1,zinslag_AFMarray,sampletype,False,hop,   Vg_variable,zins,bandgap,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T)

        # Integrals, RoyGobeil thesis eq. 2.33 & 2.34
        df_soln = df_prefactor*trapz(F_AFMarraysoln*tiparea*np.sin(time_AFMarray), time_AFMarray/frequency)
        dg_soln = dg_addedterm+dg_prefactor*trapz(F_AFMarraysoln*tiparea*np.cos(time_AFMarray), time_AFMarray/frequency)

        # Convert excitation model to energy units, Cockins thesis eq. 2.15
        E_o = np.pi*springconst*(amplitude*10**-9)**2/Qfactor*(1/Physics_Semiconductors.e)*1000 #meV
        A_exc = dg_soln
        A_exco = dg_addedterm
        E_ts = E_o*(A_exc-A_exco)/A_exc
        dg_soln = E_ts

        return [df_soln, dg_soln]

    result = Parallel(n_jobs=-1)(
        delayed(compute)(Vg) for Vg in Vg_array
    )
    return [
        [df_soln for df_soln, dg_soln in result],
        [dg_soln for df_soln, dg_soln in result]
    ]



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
