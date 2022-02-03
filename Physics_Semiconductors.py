################################################################################
################################################################################
# This script simply includes basic semiconductor equations.
################################################################################
################################################################################

import numpy as np
import scipy.constants as sp
from scipy.optimize import fsolve

################################################################################
################################################################################
# physical constants

kB = sp.value('Boltzmann constant in eV/K') #eV/K
hbar = sp.value('Planck constant in eV/Hz')*(2*sp.pi) #eV*s
me = sp.value('electron mass') #kg
e = sp.e #C
epsilon_o = sp.value('vacuum electric permittivity')/100 #C/(V*cm)

################################################################################
################################################################################
# probability distributions

# Electron and hole Fermi-dirac distributions
def fcfv(E, Ef, T): # dimensionless
    fc = np.reciprocal(np.exp((E-Ef)/(kB*T))+1)
    fv = 1-np.reciprocal(np.exp((E-Ef)/(kB*T))+1)
    return fc, fv

# Maxwell Boltzmann probability distribution
def MaxwellBoltzmann(E, Ef, T): #dimensionless
    g = np.reciprocal(np.exp((E-Ef)/(kB*T)))
    return g

# Density of states in the conduction and valence bands
def gcgv(E, Ec, Ev, mn, mp): # units?
    Earg=E-Ec
    Earg[Earg<0]=0
    gc = 1/(2*sp.pi**2)*((2*mn/e)/(hbar**2))**(3/2)*np.sqrt(Earg)
    Earg=Ev-E
    Earg[Earg<0]=0
    gv = 1/(2*sp.pi**2)*((2*mp/e)/(hbar**2))**(3/2)*np.sqrt(Earg)
    return gc, gv

# Number of electrons/holes in the conduction/valence band
def NeNh(E, fc, fv, gc, gv, Ec, Ev): #dimensionless
    Ne=fc*gc
    Ne[E<Ec]=0
    Nh=fv*gv
    Nh[E>Ev]=0
    return Ne, Nh

################################################################################
################################################################################
# carrier & energy definitions

# effective density of conduction and valence band states
def NCNV(T, mn, mp): # 1/cm**3
    NC = 1/np.sqrt(2)*((mn*kB*T/e)/(sp.pi*(hbar**2)))**(3/2)*(100**3)
    NV = 1/np.sqrt(2)*((mp*kB*T/e)/(sp.pi*(hbar**2)))**(3/2)*(100**3)
    return NC, NV

# conduction and valence band absolute energies
def EcEv(T, bandgap): # eV
    Ec = 1.17 - 4.73e-4 * T ** 2 / (T + 636.0)
    Ev = Ec-bandgap
    return Ec, Ev

# band gap energy
def Eg(Ec, Ev): #eV
    Eg = Ec-Ev
    return Eg

# intrinsic level
def Ei(Ev, Ec, T, mn, mp): #eV
    Ei = Ev+(Ec-Ev)/2 + (kB*T)/2*np.log(mp/mn)**(3/2)
    #Ei = kB * T * np.log(ni / NC) + Ec
    return Ei

# intrinsic carrier density
def ni(NC, NV, Eg, T): #1/cm**3
    ni = np.sqrt(NC*NV)*np.exp(-Eg/(2*kB*T))
    return ni

# electron and hole concentrations
def nopo(NC, NV, Ec, Ev, Ef, T): #1/cm**3
    n_o = NC * np.exp((-Ec+Ef)/(kB*T))
    p_o = NV * np.exp((Ev-Ef)/(kB*T))
    return n_o, p_o

# Fermi level
def Ef(NC, NV, Ec, Ev, T, Nd, Na): #eV
    def Ef_eqn(Ef):
        no, po = nopo(NC, NV, Ec, Ev, Ef, T)
        expression = po-no+Nd-Na
        return expression
    Ef = fsolve(Ef_eqn, 1)[0]
    #Efn = Ei+kB*T*np.log((ND_ion+p)/ni)
    #Efp = Ei-kB*T*np.log((NA_ion+n)/ni)
    return Ef


################################################################################

# Contact potential difference
def CPD_metsem(WFmet, EAsem, Ec, Ef):
    WFsem = EAsem + Ec - Ef
    CPD_metsem = WFmet - WFsem
    return CPD_metsem

# flatband voltage
def Vfb(CPD_metsem): # eV
    Vfb = CPD_metsem
    return Vfb

# oxide capacitance per unit area
def Coxp(eox,epsilon_o,tox): # C / (V*cm**2)
    Coxp = eox * epsilon_o / tox
    return Coxp

# Debye length
def LD(epsilon_sem, N_D, N_A, T):
    LD = np.sqrt(epsilon_sem*epsilon_o*100*kB*T/(2*(N_D+N_A)*e)) #m (Note units: N_A and N_D are in m^-3)
    return LD

# Depletion Width (pg. 435 eq. 10.5)
def zD(epsilon_sem, Nd, Na, Vs, T):
    zD = np.sqrt(2*epsilon_sem*epsilon_o*abs(Vs)/((Na+Nd)*e))/100 #m (Note units: Na and Nd are in cm^-3)
    return zD
