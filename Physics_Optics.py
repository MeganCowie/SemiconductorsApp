################################################################################
################################################################################
# This script calculates .
################################################################################
################################################################################

import numpy as np
from numpy import random
from scipy.integrate import trapz
from scipy.optimize import fsolve
import Physics_Semiconductors
import Physics_SurfacepotForce
import Physics_AFMoscillation
import Physics_FreqshiftDissipation
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

# Ultrafast optical pulse
def Epulse(t):
    omega_pulse = 20 # Hz
    Epulse=np.exp(-t**2)*np.cos(omega_pulse*t) # non-chirped
    #Epulse=np.exp(-t**2)*np.cos(50*t - np.exp(-2*t**2)*8*np.pi) # Chirped
    return Epulse

# Ultrafast optical pulse
def Epulse_array(t_array,delay):
    Epulse_array = []
    for t_index in range(len(t_array)):
        t_soln = t_array[t_index]+delay
        Epulse_soln=Epulse(t_soln)
        Epulse_array = np.append(Epulse_array, Epulse_soln)
    return Epulse_array


# Field autocorrelation
def intensity(t_array,delay):
    intensity=np.trapz(np.abs(Epulse_array(t_array,0)+Epulse_array(t_array,delay))**2, x=t_array)
    #FieldAC=np.trapz(Epulse_array(t_array,0)*Epulse_array(t_array,delay), x=t_array) #This is the field autocorrelation
    return intensity

# Field autocorrelation function
def intensity_delayarray(t_array,delay_array):
    intensity_delayarray = []
    for delay_index in range(len(delay_array)):
        delay_soln = delay_array[delay_index]
        intensity_soln = intensity(t_array,delay_soln)
        intensity_delayarray = np.append(intensity_delayarray, intensity_soln)
    return intensity_delayarray


# TEMPORARILY assume that the number of carriers is proportional to the illumination intensity
################################################################################
################################################################################
# Organize arrays for experimental delay sweeps

def VsF_delayarrays(delay_array,intensity_delayarray,sampletype,   Vg,zins,Eg,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T):

    Vs_delayarray = []
    F_delayarray = []
    Vs_soln = 1
    for delay_index in range(len(delay_array)):

        guess = Vs_soln
        delay_variable = delay_array[delay_index]

        Na_variable = Na*intensity_delayarray[delay_index]
        Nd_variable = Nd

        if guess >0:
            Vs_soln, F_soln = Physics_SurfacepotForce.VsF(guess-0.1,sampletype,   Vg,zins,Eg,epsilon_sem,WFmet,EAsem,Nd_variable,Na_variable,mn,mp,T)
        else:
            Vs_soln, F_soln = Physics_SurfacepotForce.VsF(guess-0.1,sampletype,   Vg,zins,Eg,epsilon_sem,WFmet,EAsem,Nd_variable,Na_variable,mn,mp,T)

        Vs_delayarray = np.append(Vs_delayarray, Vs_soln)
        F_delayarray = np.append(F_delayarray, F_soln)

    return Vs_delayarray, F_delayarray


def VsFdfdg_delayarrays(delay_array,intensity_delayarray,steps,amplitude,frequency,springconst,Qfactor,tipradius,sampletype,hop,lag,  Vg,zins,bandgap,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T):

    time_AFMarray = Physics_AFMoscillation.time_AFMarray(steps)
    zins_AFMarray = Physics_AFMoscillation.zins_AFMarray(time_AFMarray,amplitude,zins)
    zinslag_AFMarray = Physics_AFMoscillation.zinslag_AFMarray(time_AFMarray,amplitude,zins,lag)

    ######################################################

    df_prefactor = -1*(frequency**2)/(2*np.pi*springconst*amplitude*1e-9)
    dg_prefactor = -1*(frequency)/(np.pi)
    dg_addedterm = (springconst*amplitude*1e-9)/(Qfactor)
    tiparea = np.pi*tipradius**2

    def compute(intensity_variable):

        Na_variable = Na*intensity_variable
        Nd_variable = Nd

        Vs_AFMarraysoln, F_AFMarraysoln = Physics_AFMoscillation.SurfacepotForce_AFMarray(1,zinslag_AFMarray,sampletype,False,hop,   Vg,zins,bandgap,epsilon_sem,WFmet,EAsem,Nd_variable,Na_variable,mn,mp,T)

        Vs_soln = Vs_AFMarraysoln[0]
        F_soln = F_AFMarraysoln[0]*np.pi*tipradius**2

        # Integrals, RoyGobeil thesis eq. 2.33 & 2.34
        df_soln = df_prefactor*trapz(F_AFMarraysoln*tiparea*np.sin(time_AFMarray), time_AFMarray/frequency)
        dg_soln = dg_addedterm+dg_prefactor*trapz(F_AFMarraysoln*tiparea*np.cos(time_AFMarray), time_AFMarray/frequency)


        # Convert excitation model to energy units, Cockins thesis eq. 2.15
        E_o = np.pi*springconst*(amplitude*10**-9)**2/Qfactor*(1/Physics_Semiconductors.e)*1000 #meV
        A_exc = dg_soln
        A_exco = dg_addedterm
        E_ts = E_o*(A_exc-A_exco)/A_exc
        dg_soln = E_ts

        return [Vs_soln, F_soln, df_soln, dg_soln]

    result = Parallel(n_jobs=-1)(
        delayed(compute)(intensity_variable) for intensity_variable in intensity_delayarray
    )
    return [
        [Vs_soln for Vs_soln, F_soln, df_soln, dg_soln in result],
        [F_soln for Vs_soln, F_soln, df_soln, dg_soln in result],
        [df_soln for Vs_soln, F_soln, df_soln, dg_soln in result],
        [dg_soln for Vs_soln, F_soln, df_soln, dg_soln in result]
    ]
