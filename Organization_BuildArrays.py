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

def Surface_biasarrays(Vg_array,zins,Na,Nd,epsilon_sem,T,CPD,LD,nb,pb,ni):

    # Calculate list any functions that are not constant as a function of Vg
    def compute(Vg_variable):
        Vs_soln = Physics_Semiconductors.Func_Vs(Vg_variable,zins,CPD,Na,Nd,epsilon_sem,T,nb,pb,ni)
        f_soln = Physics_Semiconductors.Func_f(T,Vs_soln,nb,pb)
        F_soln = Physics_Semiconductors.Func_F(f_soln,epsilon_sem,T,LD)
        Es_soln = Physics_Semiconductors.Func_E(nb,pb,Vs_soln,epsilon_sem,T,f_soln)
        Qs_soln = Physics_Semiconductors.Func_Q(epsilon_sem,Es_soln)
        return [Vs_soln,F_soln,Es_soln,Qs_soln]

    # Then parallelize the calculations for every Vg
    result = Parallel(n_jobs=-1)(
        delayed(compute)(Vg) for Vg in Vg_array
    )
    return [
        np.asarray([Vs_soln for Vs_soln,F_soln,Es_soln,Qs_soln in result]),
        np.asarray([F_soln  for Vs_soln,F_soln,Es_soln,Qs_soln in result]),
        np.asarray([Es_soln for Vs_soln,F_soln,Es_soln,Qs_soln in result]),
        np.asarray([Qs_soln for Vs_soln,F_soln,Es_soln,Qs_soln in result]),
    ]

################################################################################

def Surface_zinsarrays(zins_array,Vg,Na,Nd,epsilon_sem,T,CPD,LD,nb,pb,ni):

    # Calculate list any functions that are not constant as a function of zins
    def compute(zins_variable):
        Vs_soln = Physics_Semiconductors.Func_Vs(Vg,zins_variable,CPD,Na,Nd,epsilon_sem,T,nb,pb,ni)
        f_soln = Physics_Semiconductors.Func_f(T,Vs_soln,nb,pb)
        F_soln = Physics_Semiconductors.Func_F(f_soln,epsilon_sem,T,LD)
        Es_soln = Physics_Semiconductors.Func_E(nb,pb,Vs_soln,epsilon_sem,T,f_soln)
        Qs_soln = Physics_Semiconductors.Func_Q(epsilon_sem,Es_soln)
        return [Vs_soln,F_soln,Es_soln,Qs_soln]

    # Then parallelize the calculations for every zins
    result = Parallel(n_jobs=-1)(
        delayed(compute)(zins) for zins in zins_array
    )
    return [
        np.asarray([Vs_soln for Vs_soln,F_soln,Es_soln,Qs_soln in result]),
        np.asarray([F_soln  for Vs_soln,F_soln,Es_soln,Qs_soln in result]),
        np.asarray([Es_soln for Vs_soln,F_soln,Es_soln,Qs_soln in result]),
        np.asarray([Qs_soln for Vs_soln,F_soln,Es_soln,Qs_soln in result]),
    ]


################################################################################
################################################################################

def AFM_timearrays(zinslag_AFMarray,Vg,zins,Na,Nd,epsilon_sem,T,CPD,LD,nb,pb,ni):

    # Calculate list any functions that are not constant as a function of time
    def compute(zins_variable):
        Vs_soln = Physics_Semiconductors.Func_Vs(Vg,zins_variable,CPD,Na,Nd,epsilon_sem,T,nb,pb,ni)
        f_soln = Physics_Semiconductors.Func_f(T,Vs_soln,nb,pb)
        F_soln = Physics_Semiconductors.Func_F(f_soln,epsilon_sem,T,LD)
        return [Vs_soln,F_soln]

    # Then parallelize the calculations for every time
    result = Parallel(n_jobs=-1)(
        delayed(compute)(zins) for zins in zinslag_AFMarray
    )
    return [
        np.asarray([Vs_soln for Vs_soln,F_soln in result]),
        np.asarray([F_soln  for Vs_soln,F_soln in result]),
    ]

################################################################################

def AFM_banddiagrams(zins_AFMarray,Vg,T,Nd,Na,WFmet,EAsem,epsilon_sem, ni,nb,pb,Vs,Ec,Ev,Ef,CPD):

    # Calculate list any functions that are not constant as a function of zins
    def compute(zins_variable):
        Vs_soln = Physics_Semiconductors.Func_Vs(Vg,zins_variable,CPD,Na,Nd,epsilon_sem,T,nb,pb,ni)
        zsem_soln,Vsem_soln,zgap_soln,Vgap_soln,zvac_soln,Vvac_soln,zmet_soln,Vmet_soln,zarray_soln,Earray_soln,Qarray_soln  = Physics_BandDiagram.BandDiagram(Vg,zins_variable,T,Nd,Na,WFmet,EAsem,epsilon_sem, ni,nb,pb,Vs_soln,Ec,Ev,Ef,CPD)
        return [zsem_soln,Vsem_soln,zgap_soln,Vgap_soln,zvac_soln,Vvac_soln,zmet_soln,Vmet_soln]

    # Then parallelize the calculations for every zins
    result = Parallel(n_jobs=-1)(
        delayed(compute)(zins) for zins in zins_AFMarray
    )
    return [
        np.asarray([zsem_soln for zsem_soln,Vsem_soln,zgap_soln,Vgap_soln,zvac_soln,Vvac_soln,zmet_soln,Vmet_soln in result]),
        np.asarray([Vsem_soln for zsem_soln,Vsem_soln,zgap_soln,Vgap_soln,zvac_soln,Vvac_soln,zmet_soln,Vmet_soln in result]),
        np.asarray([zgap_soln for zsem_soln,Vsem_soln,zgap_soln,Vgap_soln,zvac_soln,Vvac_soln,zmet_soln,Vmet_soln in result]),
        np.asarray([Vgap_soln for zsem_soln,Vsem_soln,zgap_soln,Vgap_soln,zvac_soln,Vvac_soln,zmet_soln,Vmet_soln in result]),
        np.asarray([zvac_soln for zsem_soln,Vsem_soln,zgap_soln,Vgap_soln,zvac_soln,Vvac_soln,zmet_soln,Vmet_soln in result]),
        np.asarray([Vvac_soln for zsem_soln,Vsem_soln,zgap_soln,Vgap_soln,zvac_soln,Vvac_soln,zmet_soln,Vmet_soln in result]),
        np.asarray([zmet_soln for zsem_soln,Vsem_soln,zgap_soln,Vgap_soln,zvac_soln,Vvac_soln,zmet_soln,Vmet_soln in result]),
        np.asarray([Vmet_soln for zsem_soln,Vsem_soln,zgap_soln,Vgap_soln,zvac_soln,Vvac_soln,zmet_soln,Vmet_soln in result]),
    ]

################################################################################

def AFM_biasarrays(Vg_array,zins,Na,Nd,epsilon_sem,T,CPD,LD,nb,pb,ni,frequency,springconst,amplitude,Qfactor,tipradius,time_AFMarray,zinslag_AFMarray):

    # Calculate list any functions that are not constant as a function of Vg
    def compute(Vg_variable):
        Vs_AFMarray_soln,F_AFMarray_soln = AFM_timearrays(zinslag_AFMarray,Vg_variable,zins,Na,Nd,epsilon_sem,T,CPD,LD,nb,pb,ni)
        Vs_soln = Vs_AFMarray_soln[0]
        F_soln = F_AFMarray_soln[0]
        df_soln,dg_soln = Physics_ncAFM.dfdg(time_AFMarray,F_AFMarray_soln,frequency,springconst,amplitude,Qfactor,tipradius)
        return [Vs_soln,F_soln,df_soln,dg_soln]

    # Then parallelize the calculations for every Vg
    result = Parallel(n_jobs=-1)(
        delayed(compute)(Vg) for Vg in Vg_array
    )
    return [
        np.asarray([Vs_soln for Vs_soln,F_soln,Es_soln,Qs_soln in result]),
        np.asarray([F_soln  for Vs_soln,F_soln,Es_soln,Qs_soln in result]),
        np.asarray([Es_soln for Vs_soln,F_soln,Es_soln,Qs_soln in result]),
        np.asarray([Qs_soln for Vs_soln,F_soln,Es_soln,Qs_soln in result]),
    ]


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
