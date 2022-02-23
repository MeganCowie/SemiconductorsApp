################################################################################
################################################################################
# This script calculates characteristics of input laser beams as well as
# formulas for the sample response to light.
################################################################################
################################################################################

import numpy as np
from numpy import random
from scipy.integrate import trapz
from scipy.optimize import fsolve

import Physics_Semiconductors

################################################################################
################################################################################

# Ultrafast optical pulse
def Epulse(pulsetime):
    omega_pulse = 20 # Hz
    Epulse=np.exp(-pulsetime**2)*np.cos(omega_pulse*pulsetime) # non-chirped
    #Epulse=np.exp(-pulsetime**2)*np.cos(50*pulsetime - np.exp(-2*pulsetime**2)*8*np.pi) # Chirped
    return Epulse

# Ultrafast optical pulse
def Epulse_array(pulsetime_array,delay):
    Epulse_array = []
    for pulsetime_index in range(len(pulsetime_array)):
        pulsetime_soln = pulsetime_array[pulsetime_index]+delay
        Epulse_soln=Epulse(pulsetime_soln)
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
def NaNd_intensity(Na,Nd,intensity):
    Na = Na*intensity
    Nd = Nd
    return Na,Nd
