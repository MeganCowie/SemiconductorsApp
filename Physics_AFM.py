import numpy as np
import scipy.constants as sp

import Physics_SemiconductorSurface
import Physics_SurfacepotForce
import Physics_BandDiagram

################################################################################
################################################################################
# Cantilever motion arrays

def time_AFMarray(steps):
    time_AFMarray = np.linspace(0, 4*np.pi, steps)
    return time_AFMarray

def zins_AFMarray(time_AFMarray, amplitude, zins):
    frequency = 1
    position_AFMarray = amplitude*np.sin(frequency*time_AFMarray)+amplitude #nm
    zins_AFMarray = zins+position_AFMarray*1e-7 #cm
    return zins_AFMarray


################################################################################
################################################################################
# Physics as the cantilever position varies


def SurfacepotForce_AFMarray(guess,zins_AFMarray,   Vg,zins,bandgap,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T):
    Vs_AFMarray = []
    F_AFMarray = []
    for zins_AFMindex in range(len(zins_AFMarray)):
        zins_variable = zins_AFMarray[zins_AFMindex]
        Vs_soln, F_soln = Physics_SurfacepotForce.VsF(guess+0.1,   Vg,zins_variable,bandgap,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T)
        Vs_AFMarray = np.append(Vs_AFMarray,Vs_soln)
        F_AFMarray = np.append(F_AFMarray,F_soln)
    return Vs_AFMarray, F_AFMarray


def BandDiagram_AFMarray(Vs_AFMarray,zins_AFMarray,   Vg,zins,bandgap,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T):

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

        Ec, Ev, Ei, Ef, zsem, psi, z_array, E_array, Q_array, Insulatorx, Insulatory, Vacuumx, Vacuumy, Gatex, Gatey, ni = Physics_BandDiagram.BandDiagram(Vs_variable,   Vg,zins_variable,bandgap,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T)

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



################################################################################
################################################################################
# Separate the in-phase and out-of-phase force contributions
