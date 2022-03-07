################################################################################
################################################################################
# This script calculates cantilever and electronics and sample noise sources.

import numpy as np
import Physics_Semiconductors


################################################################################
################################################################################

def Array_timearray():
    timeperpoint = 0.020 #s
    totalpoints = 25000
    noise_timearray = np.linspace(0, timeperpoint*totalpoints, totalpoints)
    return noise_timearray

def Func_Histogram(array,bins):
    Histogram = np.histogram(array,bins)
    return Histogram

def Func_PSD(array):
    PSD_freqs = np.fft.fftfreq(array.size,0.020)
    PSD_ps = np.abs(np.fft.fft(array))**2
    PSD_freqs = np.abs(PSD_freqs[1:])
    PSD_ps = PSD_ps[1:]

    # Get rid of numerical error
    if sum(PSD_ps)<0.0001:
        PSD_ps = np.round(PSD_ps)

    return PSD_freqs,PSD_ps

################################################################################
################################################################################
# Noise sources

def Func_Gaussian(sigma,mu,x):
    y = 1/(sigma*np.sqrt(2*np.pi))*np.exp((-(x-mu)**2/(2*sigma**2)))
    return y


################################################################################
################################################################################
# Transfer functions

def TransferFunction_Electrical(f,T):
    R = 500
    TF_Electrical = 4*Physics_Semiconductors.kB*T*R*(f/f)
    return TF_Electrical

def TransferFunction_Cantilever():
    return TransferFunction_Cantilever

################################################################################
################################################################################
# Build arrays

def Array_Signalarray(noise_timearray,mu):
    noise_signalarray = np.ones(len(noise_timearray))*mu
    return noise_signalarray

def Array_Randomarray(noise_timearray):
    noise_randomarray = np.random.rand(noise_timearray.size)*10-5
    return noise_randomarray

def Array_Gaussianarray(sigma,mu,x_array):
    noise_Gaussianarray = sigma*np.random.randn(x_array.size)+mu
    #noise_Gaussianarray = Func_Gaussian(sigma,mu,x_array)
    return noise_Gaussianarray

def Array_TwoLevelarray(hopmag,hopfreq,x_array):
    # every hopfreq, give it a chance to flip
    hopchance_array = np.zeros(len(x_array))
    hopchance_array[::hopfreq] = 1
    flip_array = hopchance_array*np.random.randint(2,size=len(x_array))

    # if we flip, it hops up from x_array by hopmag
    flip = 1
    noise_TwoLevelarray = []
    for flip_index in range(len(flip_array)):
       if flip_array[flip_index] == 1:
           flip = flip*-1
       if flip == 1:
           noise_TwoLevelarray = np.append(noise_TwoLevelarray,x_array[flip_index])
       else:
           noise_TwoLevelarray = np.append(noise_TwoLevelarray,x_array[flip_index]+hopmag)

    return noise_TwoLevelarray
