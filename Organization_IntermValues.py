import numpy as np

import Physics_Semiconductors
import Physics_BandDiagram
import Physics_ncAFM


################################################################################
################################################################################
# Surface

def Surface_inputvalues(slider_Vg,slider_zins,slider_alpha,slider_Eg,slider_epsilonsem,slider_WFmet,slider_EAsem,slider_donor,slider_acceptor,slider_emass,slider_hmass,slider_T,slider_biassteps,slider_zinssteps):

    # values
    Vg = slider_Vg*(1-slider_alpha)*Physics_Semiconductors.e #J
    zins = slider_zins*1e-9 #m
    Eg = slider_Eg*Physics_Semiconductors.e #J
    epsilon_sem = slider_epsilonsem #dimensionless
    WFmet = slider_WFmet*Physics_Semiconductors.e #J
    EAsem = slider_EAsem*Physics_Semiconductors.e #J
    Nd = round(10**slider_donor)/(1e9) #/m**3
    Na = round(10**slider_acceptor)/(1e9) #/m**3
    mn = slider_emass*Physics_Semiconductors.me #kg
    mp = slider_hmass*Physics_Semiconductors.me #kg
    T = slider_T #K
    biassteps = slider_biassteps
    zinssteps = slider_zinssteps
    sampletype = False #semiconducting

    # arrays
    Vg_array = np.linspace(-10,10,biassteps)*(1-slider_alpha)*Physics_Semiconductors.e #J
    zins_array = np.linspace(0.5,20,zinssteps)*1e-9 #m

    return Vg,zins,Eg,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T,sampletype,biassteps,zinssteps,Vg_array,zins_array



def Surface_calculations(Vg,zins,Eg,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T):

    NC,NV = Physics_Semiconductors.Func_NCNV(T, mn, mp)
    Ec,Ev = Physics_Semiconductors.Func_EcEv(Eg)
    Ei = Physics_Semiconductors.Func_Ei(Ev, Ec, T, mn, mp)
    Ef = Physics_Semiconductors.Func_Ef(NC, NV, Ec, Ev, T, Nd, Na)
    no,po = Physics_Semiconductors.Func_nopo(NC, NV, Ec, Ev, Ef, T)
    ni = Physics_Semiconductors.Func_ni(NC, NV, Eg, T)
    nb,pb = Physics_Semiconductors.Func_nbpb(Na, Nd, ni)
    CPD,Ef,Ec,Ev,Ei = Physics_Semiconductors.Func_CPD(WFmet, EAsem, Ef, Eg, Ec, Ev, Ei, Na, Nd)   
    LD = Physics_Semiconductors.Func_LD(epsilon_sem,po,T)
    Vs = Physics_Semiconductors.Func_Vs(Vg,zins,CPD,Na,Nd,epsilon_sem,T,nb,pb,ni)
    f = Physics_Semiconductors.Func_f(T,Vs,nb,pb)
    Es = Physics_Semiconductors.Func_E(nb,pb,Vs,epsilon_sem,T,f)
    Qs = Physics_Semiconductors.Func_Q(epsilon_sem,Es)
    F = Physics_Semiconductors.Func_F(Qs,CPD,Vg,zins)
    regime = Physics_Semiconductors.Func_regime(Na,Nd,Vs,Ei,Ef,Ec,Ev)
    zsem, Vsem, Esem, Qsem = Physics_BandDiagram.BandBending(T,epsilon_sem,nb,pb,Vs)
    P = Physics_Semiconductors.Func_P(zsem, Qsem)

    return NC,NV,Ec,Ev,Ei,Ef,no,po,ni,nb,pb,CPD,LD,Vs,Es,Qs,F,regime, zsem,Vsem,Esem,Qsem, P


################################################################################
################################################################################
# AFM

def AFM1_inputvalues(slider_amplitude,slider_resfreq,slider_lag,slider_timesteps, zins):

    # values
    amplitude = slider_amplitude/2*1e-9 #m
    frequency = 2*np.pi*slider_resfreq #rad/s
    lag = slider_lag*10**-9*frequency #rad
    timesteps = slider_timesteps

    # arrays
    time_AFMarray = np.linspace(0, 2, timesteps+1)*np.pi/frequency #s/rad
    zins_AFMarray = zins+amplitude+amplitude*np.cos(frequency*time_AFMarray) #m
    zinslag_AFMarray = zins+amplitude+amplitude*np.cos(frequency*time_AFMarray+lag) #m

    return amplitude,frequency,lag,timesteps,time_AFMarray,zins_AFMarray,zinslag_AFMarray


def AFM2_inputvalues(slider_springconst,slider_Qfactor,slider_tipradius,slider_cantheight,slider_cantarea):

    # values
    springconst = slider_springconst #N/m
    Qfactor = slider_Qfactor
    tipradius = slider_tipradius*1e-9 #m
    cantheight = slider_cantheight*1e-6 #m
    cantarea = slider_cantarea*(1e-6)**2 #m^2

    return springconst,Qfactor,tipradius,cantheight,cantarea
