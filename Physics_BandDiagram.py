################################################################################
################################################################################
# This script has one primary purpose: draw a band diagram. With the first
# function we simply calculate band bending. The second function uses the first
# to create the arrays needed to draw the band diagram.
################################################################################
################################################################################

import numpy as np
import scipy.constants as sp
from scipy.integrate import quad
from scipy.integrate import trapz

import Physics_Semiconductors


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
# Calculate band bending

def BandBending(Vs,sampletype,   Vg,zins,bandgap,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T):

    Ec, Ev = Physics_Semiconductors.EcEv(T, bandgap)
    NC,NV = Physics_Semiconductors.NCNV(T,mn,mp)
    Ef = Physics_Semiconductors.Ef(NC, NV, Ec, Ev, T, Nd, Na)
    no,po = Physics_Semiconductors.nopo(NC, NV, Ec, Ev, Ef, T)


    def zsem_eqn(psi_variable):
          f = psi_variable*(Na-Nd) + (kB*T)*po*(np.exp(-psi_variable/(kB*T))-1) + (kB*T)*no*(np.exp(psi_variable/(kB*T))-1)
          E = np.sign(psi_variable) * np.sqrt(2*e/(epsilon_sem*epsilon_o)*f)
          eqn = 1 / E
          return eqn

    if Vs == 0:     # flatband case
        zsem = np.linspace(0, 150, 101)
        psi = 0 * zsem
    else:
        psi = np.linspace(Vs, Vs * 0.01, 1001)
        zsem = np.array([])
        for value in psi:
            zsem_current, error = quad(zsem_eqn, value, Vs)
            zsem = np.hstack((zsem, zsem_current))

    return zsem, psi


################################################################################
################################################################################
# Create arrays needed to draw the band diagram

def BandDiagram(Vs,sampletype,   Vg,zins,bandgap,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T):

    NC,NV = Physics_Semiconductors.NCNV(T,mn,mp)
    Ec,Ev = Physics_Semiconductors.EcEv(T,bandgap)
    Eg = Physics_Semiconductors.Eg(Ec,Ev)
    ni = Physics_Semiconductors.ni(NC,NV,Eg,T)
    Ei = Physics_Semiconductors.Ei(Ev, Ec, T, mn, mp)
    Ef = Physics_Semiconductors.Ef(NC, NV, Ec, Ev, T, Nd, Na)
    zsem, psi = BandBending(Vs,sampletype,   Vg,zins,bandgap,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T)
    CPD_metsem = Physics_Semiconductors.CPD_metsem(WFmet, EAsem, Ec, Ef)


    Vins = Vg - Vs - CPD_metsem # potential drop across insulator
    offtop = 1 # arbitraty offsets to draw vacuum gap as "wide gap" semiconductor
    offbot = 10
    Insulatorx = [0, 0, -zins*1e7, -zins*1e7, 0]
    Insulatory = [Ec-Vs+EAsem-offbot, Ec-Vs+EAsem-offtop, Vg+WFmet-offtop, Vg+WFmet-offbot,  Ec-Vs+EAsem-offbot]

    Vacuumx = np.hstack((np.array([-zins*1e7-20, -zins*1e7]),zsem*1e7))
    Vacuumy = np.hstack((np.array([Vg+WFmet, Vg+WFmet]),np.array(Ec-psi+EAsem)))

    Gatex = np.array([-zins*1e7-20, -zins*1e7])
    Gatey = np.array([Vg, Vg])


    zmetarray = np.array([-zins*1e7-20, -zins*1e7,-zins*1e7])
    zinsarray = np.array([-zins*1e7, 0])
    z_array = np.hstack((zmetarray,zinsarray,zsem*1e7))

    CBO = 3.5
    psiox = Vg - Vs - CPD_metsem
    func_ins = psiox/(zins*1e7)*zinsarray+Ec-Vs+CBO
    Esem=-np.gradient(psi,zsem*1e7)
    Eins=-np.gradient(func_ins,-zinsarray)
    Emet = [0,0,0] # the electric field inside a metal is zero
    E_array = np.hstack((Emet,Eins,Esem))

    Qsem=-np.gradient(Esem,zsem*1e7)
    Qins=-np.array([0, 0])
    Qmet = [0,0,-trapz(Qsem,zsem*1e7)] # the metal has equal and opposite charge as the net semiconductor
    Q_array = np.hstack((Qmet,Qins,Qsem))


    return Ec, Ev, Ei, Ef, zsem, psi, z_array, E_array, Q_array, Insulatorx, Insulatory, Vacuumx, Vacuumy, Gatex, Gatey, ni
