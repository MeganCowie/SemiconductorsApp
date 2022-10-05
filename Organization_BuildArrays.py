# All this script does is build arrays. There is zero physics in here.

from joblib import Parallel, delayed

import Physics_Semiconductors
import Physics_BandDiagram
import Physics_ncAFM
import Physics_Optics

# Should not need:
import numpy as np
kB = Physics_Semiconductors.kB
hbar = Physics_Semiconductors.hbar
me = Physics_Semiconductors.me
e = Physics_Semiconductors.e
epsilon_o = Physics_Semiconductors.epsilon_o


################################################################################
################################################################################
# Vs and F vs. Vg and zins

def VsF_arrays(Vg_array,zins_array,sampletype,   Vg,zins,Eg,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T):

    # Bias array
    Vs_biasarray = []
    F_biasarray = []
    Vs_soln = 1
    for Vg_index in range(len(Vg_array)):
        guess = Vs_soln

        Vg_variable = Vg_array[Vg_index]
        if guess >0:
            Vs_soln, F_soln = Physics_Semiconductors.Func_VsF(guess-0.1,sampletype,   Vg_variable,zins,Eg,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T)
        else:
            Vs_soln, F_soln = Physics_Semiconductors.Func_VsF(guess-0.1,sampletype,   Vg_variable,zins,Eg,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T)

        Vs_biasarray = np.append(Vs_biasarray, Vs_soln)
        F_biasarray = np.append(F_biasarray, F_soln)

    #zins array
    Vs_zinsarray = []
    F_zinsarray = []
    Vs_soln = -10
    for zins_index in range(len(zins_array)):
        guess = Vs_soln
        zins_variable = zins_array[zins_index]
        if guess >0:
            Vs_soln, F_soln = Physics_Semiconductors.Func_VsF(guess+0.1,sampletype,   Vg,zins_variable,Eg,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T)
        else:
            Vs_soln, F_soln = Physics_Semiconductors.Func_VsF(guess-0.1,sampletype,   Vg,zins_variable,Eg,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T)

        Vs_zinsarray = np.append(Vs_zinsarray, Vs_soln)
        F_zinsarray = np.append(F_zinsarray, F_soln)

    return Vs_biasarray, F_biasarray, Vs_zinsarray, F_zinsarray


################################################################################
################################################################################
# Find supplemental information related to Vs and F

def VsF_supp(Vs,Vg_array,zins_array,Vs_biasarray,Vs_zinsarray,Vg,zins,Eg,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T):

    NC,NV = Physics_Semiconductors.Func_NCNV(T,mn,mp)
    Ec,Ev = Physics_Semiconductors.Func_EcEv(T,Eg)
    ni = Physics_Semiconductors.Func_ni(NC,NV,Eg,T)
    Ei = Physics_Semiconductors.Func_Ei(Ev, Ec, T, mn, mp)
    Ef = Physics_Semiconductors.Func_Ef(NC, NV, Ec, Ev, T, Nd, Na)
    CPD = Physics_Semiconductors.Func_CPD(WFmet, EAsem, Ec, Ef)

    n_i = ni*(100)**3 #m**-3
    N_D = Nd*(100)**3 #m**-3
    N_A = Na*(100)**3 #m**-3
    L_D = Physics_Semiconductors.Func_LD(epsilon_sem, N_D, N_A, T)
    C_l= epsilon_o*100/(zins/100) #C/Vm**2

    # Values
    regime = Physics_Semiconductors.Func_regime(Na,Nd,Vs,Ei,Ef)
    LD = Physics_Semiconductors.Func_LD(epsilon_sem,N_D,N_A,T)
    u,f=Physics_Semiconductors.Func_uf(N_A,N_D,n_i,T,Vs)
    zA = Physics_Semiconductors.Func_zA(Nd,Na,LD,Vs,T)
    zD = Physics_Semiconductors.Func_zD(epsilon_sem,Nd,Na,Vs,T)
    Qs = Physics_Semiconductors.Func_Qs(N_A,N_D,u,f,epsilon_sem,T,L_D)
    Cs = Physics_Semiconductors.Func_Qs(N_A,N_D,u,f,epsilon_sem,T,L_D)


    # Bias array
    zD_biasarray = []
    Cs_biasarray = []
    Qs_biasarray = []
    for Vg_index in range(len(Vg_array)):
        Vs_soln = Vs_biasarray[Vg_index]
        zD_soln = Physics_Semiconductors.Func_zD(epsilon_sem, Nd, Na, Vs_soln, T)
        u_soln,f_soln=Physics_Semiconductors.Func_uf(N_A,N_D,n_i,T,Vs_soln)
        f =       (np.exp(u_soln)-u_soln-1+(n_i**2/N_D**2)*(np.exp(-1*u_soln)+u_soln-1))**(1/2) #dimensionless
        Qs_soln = Physics_Semiconductors.Func_Qs(N_A,N_D,u_soln,f_soln,epsilon_sem,T,L_D)

        zD_biasarray = np.append(zD_biasarray, zD_soln)
        Qs_biasarray = np.append(Qs_biasarray, Qs_soln)

    # zins array
    zD_zinsarray = []
    Cs_zinsarray = []
    Qs_zinsarray = []
    for zins_index in range(len(zins_array)):
        Vs_soln = Vs_zinsarray[zins_index]
        zD_soln = Physics_Semiconductors.Func_zD(epsilon_sem, Nd, Na, Vs_soln, T)
        u_soln,f_soln=Physics_Semiconductors.Func_uf(N_A,N_D,n_i,T,Vs_soln)
        Qs_soln = Physics_Semiconductors.Func_Qs(N_A,N_D,u_soln,f_soln,epsilon_sem,T,L_D)

        zD_zinsarray = np.append(zD_zinsarray, zD_soln)
        Qs_zinsarray = np.append(Qs_zinsarray, Qs_soln)


    zQ_biasarray = zD_biasarray
    zQ_zinsarray = zD_zinsarray
    zQ = zD

    return regime, LD, zQ,Qs, zQ_biasarray, Qs_biasarray, zQ_zinsarray, Qs_zinsarray


################################################################################
################################################################################
# Vs, F, df, and dg vs. Vg


# This function returns df and dg for the given Vg, as well as Vs and F at
# that Vg
def VsFdfdg_biasarray(Vg_array,timesteps,amplitude,frequency,springconst,Qfactor,tipradius,sampletype,hop,lag,  Vg,zins,Eg,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T):

    # First list any functions that are constant as a function of Vg
    time_AFMarray = Physics_ncAFM.time_AFMarray(timesteps)
    zins_AFMarray = Physics_ncAFM.zins_AFMarray(time_AFMarray,amplitude,zins)

    # Then list any functions that are not constant as a function of Vg
    def compute(Vg_variable):
        zinslag_AFMarraysoln,lag_soln = Physics_ncAFM.zinslag_AFMarray(time_AFMarray,amplitude,frequency,lag,sampletype,  Vg_variable,zins,Eg,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T)
        Vs_AFMarraysoln, F_AFMarraysoln = Physics_ncAFM.SurfacepotForce_AFMarray(1,zinslag_AFMarraysoln,sampletype,False,hop,   Vg_variable,zins,Eg,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T)
        df_soln, dg_soln = Physics_ncAFM.dfdg(time_AFMarray,F_AFMarraysoln,frequency,springconst,amplitude,Qfactor,tipradius)
        Vs_soln, F_soln = Vs_AFMarraysoln[0],F_AFMarraysoln[0]
        return [Vs_soln,F_soln,df_soln, dg_soln, lag_soln]

    # Then parallelize the calculation of y for every Vg
    result = Parallel(n_jobs=-1)(
        delayed(compute)(Vg) for Vg in Vg_array
    )
    return [
        [Vs_soln for Vs_soln,F_soln,df_soln,dg_soln,lag_soln in result],
        [F_soln for Vs_soln,F_soln,df_soln,dg_soln,lag_soln in result],
        [df_soln for Vs_soln,F_soln,df_soln,dg_soln,lag_soln in result],
        [dg_soln for Vs_soln,F_soln,df_soln,dg_soln,lag_soln in result],
        [lag_soln for Vs_soln,F_soln,df_soln,dg_soln,lag_soln in result]
    ]

################################################################################
################################################################################
# Vs, F, df, and dg vs. zins

# This function returns df and dg for the given zins as the closest tip-sample
# separation, as well as Vs and F at the closest tip-sample separation
def VsFdfdg_zinsarray(zins_array,timesteps,amplitude,frequency,springconst,Qfactor,tipradius,sampletype,hop,lag,  Vg,zins,Eg,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T):

    # First list any functions that are constant as a function of zins
    time_AFMarray = Physics_ncAFM.time_AFMarray(timesteps)

    # Then list any functions that are not constant as a function of zins
    def compute(zins_variable):
        zins_AFMarray = Physics_ncAFM.zins_AFMarray(time_AFMarray,amplitude,zins_variable)
        zinslag_AFMarray,lag_soln = Physics_ncAFM.zinslag_AFMarray(time_AFMarray,amplitude,frequency,lag,sampletype,  Vg,zins,Eg,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T)
        Vs_AFMarraysoln, F_AFMarraysoln = Physics_ncAFM.SurfacepotForce_AFMarray(1,zinslag_AFMarray,sampletype,False,hop,   Vg,zins_variable,Eg,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T)
        df_soln, dg_soln = Physics_ncAFM.dfdg(time_AFMarray,F_AFMarraysoln,frequency,springconst,amplitude,Qfactor,tipradius)
        Vs_soln, F_soln = Vs_AFMarraysoln[0],F_AFMarraysoln[0]
        return [Vs_soln,F_soln,df_soln, dg_soln]

    # Then parallelize the calculation of y for every zins
    result = Parallel(n_jobs=-1)(
        delayed(compute)(zins) for zins in zins_array
    )
    return [
        [Vs_soln for Vs_soln,F_soln,df_soln,dg_soln in result],
        [F_soln for Vs_soln,F_soln,df_soln,dg_soln in result],
        [df_soln for Vs_soln,F_soln,df_soln,dg_soln in result],
        [dg_soln for Vs_soln,F_soln,df_soln,dg_soln in result]
    ]

'''
################################################################################
################################################################################
# Find the difference in surface potential as a function of bias

def Vsdiff_biasarray(Vg_array,zins_array,sampletype,   Vg,zins,Eg,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T,  amplitude):

    zins_top = zins+amplitude
    zins_bot = zins

    time_AFMarray = Physics_ncAFM.time_AFMarray(30)
    zins_AFMarray = Physics_ncAFM.zins_AFMarray(time_AFMarray,amplitude,zins)
    lag = 30

    # Then list any functions that are not constant as a function of Vg
    def compute(Vg_variable):
        Vstop_soln, F_soln = Physics_Semiconductors.Func_VsF(1,sampletype,   Vg_variable,zins_top,Eg,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T)
        Vsbot_soln, F_soln = Physics_Semiconductors.Func_VsF(1,sampletype,   Vg_variable,zins_bot,Eg,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T)
        Vsdiff_soln = (Vsbot_soln-Vstop_soln)
        lag_soln = 300*np.abs(Vsdiff_soln**2)/10**9*300000 #radians

        zinslag_AFMarray, lag_soln=Physics_ncAFM.zinslag_AFMarray(time_AFMarray,amplitude,lag,sampletype,  Vg_variable,zins,Eg,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T)

        return [Vstop_soln, Vsbot_soln, Vsdiff_soln, lag_soln]

    # Then parallelize the calculation of y for every Vg
    result = Parallel(n_jobs=-1)(
        delayed(compute)(Vg) for Vg in Vg_array
    )
    return [
        lag_soln for Vstop_soln,Vsbot_soln,Vsdiff_soln, lag_soln in result
    ]
'''
################################################################################
################################################################################
# DELAY ARRAYS
'''
def VsFdfdg_delayarrays(delay_array,intensity_delayarray,steps,amplitude,frequency,springconst,Qfactor,tipradius,sampletype,hop,lag,  Vg,zins,Eg,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T):

    # First list any functions that are constant as a function of x
    time_AFMarray = Physics_ncAFM.time_AFMarray(steps)
    zins_AFMarray = Physics_ncAFM.zins_AFMarray(time_AFMarray,amplitude,zins)
    zinslag_AFMarray = Physics_ncAFM.zinslag_AFMarray(time_AFMarray,amplitude,zins,lag)

    # Then list any functions that are not constant as a function of x
    def compute(intensity_variable):
        Na_soln,Nd_soln = Physics_Optics.NaNd_intensity(Na,Nd,intensity_variable)
        Vs_AFMarraysoln, F_AFMarraysoln = Physics_ncAFM.SurfacepotForce_AFMarray(1,zinslag_AFMarray,sampletype,False,hop,   Vg,zins,Eg,epsilon_sem,WFmet,EAsem,Nd_soln,Na_soln,mn,mp,T)
        Vs_soln, F_soln = Vs_AFMarraysoln[0],F_AFMarraysoln[0]
        df_soln, dg_soln = Physics_ncAFM.dfdg(time_AFMarray,F_AFMarraysoln,frequency,springconst,amplitude,Qfactor,tipradius)
        return [Vs_soln, F_soln, df_soln, dg_soln]

    # Then parallelize the calcylation of y for every x
    result = Parallel(n_jobs=-1)(
        delayed(compute)(intensity_variable) for intensity_variable in intensity_delayarray
    )
    return [
        [Vs_soln for Vs_soln, F_soln, df_soln, dg_soln in result],
        [F_soln for Vs_soln, F_soln, df_soln, dg_soln in result],
        [df_soln for Vs_soln, F_soln, df_soln, dg_soln in result],
        [dg_soln for Vs_soln, F_soln, df_soln, dg_soln in result]
    ]
'''























'''
################################################################################
################################################################################
# Physics over time -- NOT FINISHED YET and not needed for MoSe2 data.

def dfdg_timearray(time_array,steps,amplitude,frequency,springconst,Qfactor,tipradius,sampletype,hop,lag,  Vg,zins,Eg,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T):

    time_AFMarray = Physics_ncAFM.time_AFMarray(steps)
    zins_AFMarray = Physics_ncAFM.zins_AFMarray(time_AFMarray,amplitude,zins)
    zinslag_AFMarray = Physics_ncAFM.zinslag_AFMarray(time_AFMarray,amplitude,zins,lag)

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
    Vs_AFMarray_Nd0, F_AFMarray_Nd0 = Physics_AFMoscillation.SurfacepotForce_AFMarray(1,zinslag_AFMarray,sampletype,False,0,   Vg,zins,Eg,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T)
    df_Nd0 = df_prefactor*trapz(F_AFMarray_Nd0*tiparea*np.sin(time_AFMarray), time_AFMarray/frequency)
    dg_Nd0 = dg_prefactor*trapz(F_AFMarray_Nd0*tiparea*np.cos(time_AFMarray), time_AFMarray/frequency)

    slider_donor = 19
    Nd = round((10**(slider_donor+hop)*10**8)/(1000**3))
    Vs_AFMarray_Nd1 = []
    F_AFMarray_Nd1 = []
    Vs_AFMarray_Nd1, F_AFMarray_Nd1 = Physics_AFMoscillation.SurfacepotForce_AFMarray(1,zinslag_AFMarray,sampletype,False,0,   Vg,zins,Eg,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T)
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

'''



def BandDiagram_AFMarray(Vs_AFMarray,zins_AFMarray,sampletype,   Vg,zins,Eg,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T):

    Ec_AFMarray = []
    Ev_AFMarray = []
    Ei_AFMarray = []
    Ef_AFMarray = []
    zsem_AFMarray = []
    psi_AFMarray = []
    Insulatorx_AFMarray = []
    Insulatory_AFMarray = []
    Vacuumx_AFMarray = []
    Vacuumy_AFMarray = []
    Gatex_AFMarray = []
    Gatey_AFMarray = []

    for zins_AFMindex in range(len(zins_AFMarray)):
        zins_variable = zins_AFMarray[zins_AFMindex]
        Vs_variable = Vs_AFMarray[zins_AFMindex]

        if sampletype == False: # semiconductor band diagram
            Ec, Ev, Ei, Ef, zsem, psi, z_array, E_array, Q_array, Insulatorx, Insulatory, Vacuumx, Vacuumy, Gatex, Gatey, ni = Physics_BandDiagram.BandDiagram(Vs_variable,sampletype,   Vg,zins_variable,Eg,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T)
            Ec_AFMarray.append(Ec)
            Ev_AFMarray.append(Ev)
            Ei_AFMarray.append(Ei)
            Ef_AFMarray.append(Ef)
            zsem_AFMarray.append(zsem)
            psi_AFMarray.append(psi)
            Insulatorx_AFMarray.append(Insulatorx)
            Insulatory_AFMarray.append(Insulatory)
            Vacuumx_AFMarray.append(Vacuumx)
            Vacuumy_AFMarray.append(Vacuumy)
            Gatex_AFMarray.append(Gatex)
            Gatey_AFMarray.append(Gatey)


        elif sampletype == True: # metal band diagram
            CPD_metsem = Physics_Semiconductors.CPD_metsem(WFmet, EAsem, 0, 0)
            Ef = [0-CPD_metsem]
            Ec = [Ef[0], Ef[0]]
            Ev = [Ef[0], Ef[0]]
            Ei = [Ef[0], Ef[0]]
            zsem = [0, 20]
            psi = [0, 0]
            offtop = 1
            offbot = 10
            Insulatorx = [0, 0, -zins_variable*1e7, -zins_variable*1e7, 0]
            Insulatory = [EAsem-offbot, EAsem-offtop, Vg+WFmet-offtop, Vg+WFmet-offbot,  EAsem-offbot]
            Vacuumx = np.hstack((np.array([-zins_variable*1e7-20, -zins_variable*1e7]), zsem))
            Vacuumy = np.hstack((np.array([Vg+WFmet, Vg+WFmet]), np.array([Ef[0]+WFmet, Ef[0]+WFmet])))
            Gatex = np.array([-zins_variable*1e7-20, -zins_variable*1e7])
            Gatey = np.array([Vg, Vg])

            Ec_AFMarray.append(Ec)
            Ev_AFMarray.append(Ev)
            Ei_AFMarray.append(Ei)
            Ef_AFMarray.append(Ef)
            zsem_AFMarray.append(zsem)
            psi_AFMarray.append(psi)
            Insulatorx_AFMarray.append(Insulatorx)
            Insulatory_AFMarray.append(Insulatory)
            Vacuumx_AFMarray.append(Vacuumx)
            Vacuumy_AFMarray.append(Vacuumy)
            Gatex_AFMarray.append(Gatex)
            Gatey_AFMarray.append(Gatey)

    return Ec_AFMarray,Ev_AFMarray,Ei_AFMarray,Ef_AFMarray,zsem_AFMarray,psi_AFMarray,Insulatorx_AFMarray,Insulatory_AFMarray,Vacuumx_AFMarray,Vacuumy_AFMarray,Gatex_AFMarray,Gatey_AFMarray
