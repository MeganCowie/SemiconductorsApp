################################################################################
################################################################################
# This script calculates cantilever and electronics and sample noise sources.

import numpy as np
import Physics_Semiconductors


################################################################################
################################################################################

def Array_timearray():
    timeperpoint = 0.020 #s
    totalpoints = 2000
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

def Func_AllanDev(array):

    timeperpoint = 0.02 # time per point (s)
    tau_array = np.linspace(0.1, 10, 100) # averaging time (s)

    tau_finalarray = []
    Allan_squared_array = []
    for index_tau in range(len(tau_array)):
        tau_soln = tau_array[index_tau]
        numpoints = tau_soln/timeperpoint # number of points in time interval tau
        n = len(array)/numpoints # number of intervals in my array

        if n%1==0:
            n = int(n)
            Allan_squared_bins = []
            for n_index in range(n-1):
                avg_bin1 = np.sum(array[n_index+1:n+n_index+1])/tau_soln
                avg_bin2 = np.sum(array[n_index:n+n_index])/tau_soln
                avg_diff = avg_bin1-avg_bin2
                Allan_squared_bin = (1/2)*(avg_diff)**2
                Allan_squared_bins = np.append(Allan_squared_bins,Allan_squared_bin)

            tau_finalarray = np.append(tau_finalarray,tau_soln)
            Allan_squared_array = np.append(Allan_squared_array,np.average(Allan_squared_bins))

    return tau_finalarray, Allan_squared_array


def Func_AC(x_array,y_array):

    AC_amp = np.correlate(y_array,y_array,'full')
    x_array = np.flip(x_array)

    return x_array,AC_amp

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

def Array_Signalarray(noise_timearray,mu,points):
    noise_signalarray = np.ones(len(noise_timearray))*mu
    return noise_signalarray

def Array_Gaussianarray(sigma,mu,x_array):
    noise_Gaussianarray = sigma*np.random.randn(x_array.size)+mu
    return noise_Gaussianarray

def Array_TwoLevelarray(hopmag,hopper,x_array):

    hopchance_sign = np.random.random_integers(low=0,high=1,size=1)*2-1
    hopchance_array = np.random.uniform(low=0,high=1,size=len(x_array))

    flip = 1
    noise_TwoLevelarray = []
    for flip_index in range(len(hopchance_array)):
       if hopchance_array[flip_index] > hopper:
           flip = flip*-1
       if flip == 1:
           hopmag_soln =0
       else:
           hopmag_soln = hopmag

       noise_TwoLevelarray = np.append(noise_TwoLevelarray,x_array[flip_index]+hopchance_sign*hopmag_soln)

    return noise_TwoLevelarray
