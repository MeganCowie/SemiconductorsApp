import numpy as np
from numpy import random
import scipy.constants as sp

import Physics_Semiconductors
import Physics_SurfacepotForce
import Physics_BandDiagram

################################################################################
################################################################################
# Cantilever motion arrays

def time_AFMarray(steps):
    time_AFMarray = np.linspace(0, 2*np.pi, steps)
    return time_AFMarray

def zins_AFMarray(time_AFMarray, amplitude, zins):
    position_AFMarray = amplitude*np.sin(time_AFMarray)+amplitude #nm
    zins_AFMarray = zins+position_AFMarray*1e-7 #cm
    return zins_AFMarray

def zinslag_AFMarray(time_AFMarray, amplitude, zins, lag):
    position_AFMarray = amplitude*np.sin(time_AFMarray-lag)+amplitude #nm
    zinslag_AFMarray = zins+position_AFMarray*1e-7 #cm
    return zinslag_AFMarray


################################################################################
################################################################################
# Physics as the cantilever position varies

# Finds how the surface position varies over a cantilever oscillation
def SurfacepotForce_AFMarray(guess,zins_AFMarray,sampletype,RTN,hop,   Vg,zins,bandgap,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T):
    Vs_AFMarray = []
    F_AFMarray = []

    for zins_AFMindex in range(len(zins_AFMarray)):

        if RTN==True:
            #Set Nd to Nd+1 with a random probability at one moment in the cycle
            if np.remainder(zins_AFMindex,2)==0:
                slider_donor = 19+ np.random.randint(2)*hop
                Nd = round((10**slider_donor*10**8)/(1000**3))

        zins_variable = zins_AFMarray[zins_AFMindex]
        Vs_soln, F_soln = Physics_SurfacepotForce.VsF(guess+0.1,sampletype,   Vg,zins_variable,bandgap,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T)
        Vs_AFMarray = np.append(Vs_AFMarray,Vs_soln)
        F_AFMarray = np.append(F_AFMarray,F_soln)
    return Vs_AFMarray, F_AFMarray


# Plots the band diagream as the cantilever position varies.
def BandDiagram_AFMarray(Vs_AFMarray,zins_AFMarray,sampletype,   Vg,zins,bandgap,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T):

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
            Ec, Ev, Ei, Ef, zsem, psi, z_array, E_array, Q_array, Insulatorx, Insulatory, Vacuumx, Vacuumy, Gatex, Gatey, ni = Physics_BandDiagram.BandDiagram(Vs_variable,sampletype,   Vg,zins_variable,bandgap,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T)
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
