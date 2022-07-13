import numpy as np

import Physics_Semiconductors
import Physics_ncAFM


def Surface_inputvalues(slider_Vg,slider_zins,slider_alpha,slider_Eg,slider_epsilonsem,slider_WFmet,slider_EAsem,slider_donor,slider_acceptor,slider_emass,slider_hmass,slider_T,slider_biassteps,slider_zinssteps):

    # values
    Vg = slider_Vg*(1-slider_alpha) #eV
    zins = slider_zins*1e-7 #cm
    Eg = slider_Eg #eV
    epsilon_sem = slider_epsilonsem #dimensionless
    WFmet = slider_WFmet #eV
    EAsem = slider_EAsem #eV
    Nd = round((10**slider_donor*10**8)/(1000**3)) #/cm^3
    Na = round((10**slider_acceptor*10**8)/(1000**3)) #/cm^3
    mn = slider_emass*Physics_Semiconductors.me #kg
    mp = slider_hmass*Physics_Semiconductors.me #kg
    T = slider_T #K
    biassteps = slider_biassteps
    zinssteps = slider_zinssteps
    sampletype = False #semiconducting

    # arrays
    Vg_array = np.linspace(-10,10,biassteps)*(1-slider_alpha) #eV
    zins_array = np.linspace(0.05,20,zinssteps)*1e-7 #nm

    return Vg,zins,Eg,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T,sampletype,biassteps,zinssteps,Vg_array,zins_array


def AFM1_inputvalues(toggle_sampletype,toggle_RTN,slider_amplitude,slider_resfreq,slider_hop,slider_lag,slider_timesteps,zins):

    # values
    sampletype = toggle_sampletype #false = semiconducting, true = metallic
    RTN = toggle_RTN #false = off, true = on
    amplitude = slider_amplitude #nm
    frequency = slider_resfreq #Hz
    hop = slider_hop
    lag = slider_lag/10**9*frequency #radians
    timesteps = slider_timesteps

    # arrays
    time_AFMarray = Physics_ncAFM.time_AFMarray(timesteps)
    zins_AFMarray = Physics_ncAFM.zins_AFMarray(time_AFMarray,amplitude,zins)
    zinslag_AFMarray = Physics_ncAFM.zinslag_AFMarray(time_AFMarray,amplitude,zins, lag)

    return sampletype,RTN,amplitude,frequency,hop,lag,timesteps,time_AFMarray,zins_AFMarray,zinslag_AFMarray

def AFM2_inputvalues(slider_springconst,slider_Qfactor,slider_tipradius):

    # values
    springconst = slider_springconst #N/m
    Qfactor = slider_Qfactor
    tipradius = slider_tipradius #nm

    return springconst,Qfactor,tipradius
