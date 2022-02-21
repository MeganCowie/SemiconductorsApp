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
# solid state and extrinsic semiconductor definitions

# Electron and hole Fermi-dirac distributions
    # Pierret Semiconductor Fundamentals, Vol 1, Ed 2 (pg 38)
    # Neamen Semiconductor Physics & Devices, Ed 2 (pg 71)
    # Jonscher Solid Semiconductors (pg 12-13)
def fcfv(E, Ef, T): # dimensionless
    fc = np.reciprocal(np.exp((E-Ef)/(kB*T))+1)
    fv = 1-np.reciprocal(np.exp((E-Ef)/(kB*T))+1)
    return fc, fv

# Maxwell Boltzmann probability distribution
    # Neamen Semiconductor Physics & Devices, Ed 2 (pg 75)
def MaxwellBoltzmann(E, Ef, T): #dimensionless
    fb = np.reciprocal(np.exp((E-Ef)/(kB*T)))
    return fb

# Density of states in the conduction and valence bands
    # Pierret Semiconductor Fundamentals, Vol 1, Ed 2 (pg 36)
    # Neamen Semiconductor Physics & Devices, Ed 2 (pg 69-70)
def gcgv(E, Ec, Ev, mn, mp): # units?
    Earg=E-Ec
    Earg[Earg<0]=0
    gc = 1/(2*sp.pi**2)*((2*mn/e)/(hbar**2))**(3/2)*np.sqrt(Earg)
    Earg=Ev-E
    Earg[Earg<0]=0
    gv = 1/(2*sp.pi**2)*((2*mp/e)/(hbar**2))**(3/2)*np.sqrt(Earg)
    return gc, gv


# Number of electrons/holes in the conduction/valence band
    # Pierret Semiconductor Fundamentals, Vol 1, Ed 2 (pg 43)
    # Neamen Semiconductor Physics & Devices, Ed 2 (pg 86)
    # Jonscher Solid Semiconductors (pg 29)
def NeNh(E, fc, fv, gc, gv, Ec, Ev): #dimensionless
    Ne=fc*gc
    Ne[E<Ec]=0
    Nh=fv*gv
    Nh[E>Ev]=0
    return Ne, Nh

# effective density of conduction and valence band states
    # Pierret Semiconductor Fundamentals, Vol 1, Ed 2 (pg 44)
    # Neamen Semiconductor Physics & Devices, Ed 2 (pg 89-91)
def NCNV(T, mn, mp): # 1/cm**3
    NC = 2*((2*sp.pi*mn*kB*T/e)/((2*sp.pi*hbar)**2))**(3/2)*(100**3)#1/np.sqrt(2)*((mn*kB*T/e)/(sp.pi*(hbar**2)))**(3/2)*(100**3)
    NV = 2*((2*sp.pi*mp*kB*T/e)/((2*sp.pi*hbar)**2))**(3/2)*(100**3)#1/np.sqrt(2)*((mp*kB*T/e)/(sp.pi*(hbar**2)))**(3/2)*(100**3)
    return NC, NV

# electron and hole concentrations
    # Pierret Semiconductor Fundamentals, Vol 1, Ed 2 (pg 45)
    # Neamen Semiconductor Physics & Devices, Ed 2 (pg 89-91)
    # Jonscher Solid Semiconductors (pg 30-31)
def nopo(NC, NV, Ec, Ev, Ef, T): #1/cm**3
    n_o = NC * np.exp((-Ec+Ef)/(kB*T))
    p_o = NV * np.exp((Ev-Ef)/(kB*T))
    return n_o, p_o

# intrinsic carrier density
    # Pierret Semiconductor Fundamentals, Vol 1, Ed 2 (pg 46)
    # Neamen Semiconductor Physics & Devices, Ed 2 (pg 92)
def ni(NC, NV, Eg, T): #1/cm**3
    ni = np.sqrt(NC*NV)*np.exp(-Eg/(2*kB*T))
    return ni

# conduction and valence band absolute energies
# The conduction band level does not impact the Vs or F, so set arbitrarily as 1
    # Jonscher Solid Semiconductors (pg 30)
def EcEv(T, Eg): # eV
    Ec = 1 #silicon 1.17 - 4.73e-4 * T ** 2 / (T + 636.0)
    Ev = Ec-Eg
    return Ec, Ev

# intrinsic level
    # Pierret Semiconductor Fundamentals, Vol 1, Ed 2 (pg 52)
    # Neamen Semiconductor Physics & Devices, Ed 2 (pg 94)
    # Jonscher Solid Semiconductors (pg 31)
def Ei(Ev, Ec, T, mn, mp): #eV
    Ei = (Ec+Ev)/2+(3/4)*kB*T*np.log(mp/mn) #Ev+(Ec-Ev)/2 + (kB*T)/2*np.log(mp/mn)**(3/2)
    return Ei

# Fermi level
    # Pierret Semiconductor Fundamentals, Vol 1, Ed 2 (pg 49)
    # Neamen Semiconductor Physics & Devices, Ed 2 (pg 115)
    # Jonscher Solid Semiconductors (pg 33)
def Ef(NC, NV, Ec, Ev, T, Nd, Na): #eV
    def Ef_eqn(Ef_soln):
        no, po = nopo(NC, NV, Ec, Ev, Ef_soln, T)
        expression = po-no+Nd-Na
        return expression
    Ef = fsolve(Ef_eqn, 1)[0]
    return Ef


################################################################################
################################################################################
# MOS capacitor (not illuminated)

# Identify MOS capacitor regime (accumulation, depletion, inversion)
def MOS_regime(Na,Nd,Vs,Ei,Ef):
    Vb = Ei-Ef
    if Na ==0: #n-type
        if Vs > 0:
            regime = 1 #accumulation
        elif Vs == 0:
            regime = 2 #flatband
        elif Vs > Vb:# & Vs > 0:
            regime = 3 #depletion
        elif Vs == Vb:
            regime = 4 #threshold
        elif Vs < Vb:
            regime = 5 #inversion
    elif Nd ==0: #p-type
        if Vs < 0:
            regime = 1 #accumulation
        elif Vs == 0:
            regime = 2 #flatband
        elif Vs < Vb:# & Vs > 0:
            regime = 3 #depletion
        elif Vs == Vb:
            regime = 4 #threshold
        elif Vs > Vb:
            regime = 5 #inversion
    return regime


# Contact potential difference
    # Neamen Semiconductor Physics & Devices, Ed 2 (pg 431)
    # See pg. 225 in Sze
def CPD_metsem(WFmet, EAsem, Ec, Ef):
    WFsem = EAsem + Ec - Ef
    CPD_metsem = WFmet - WFsem
    return CPD_metsem

# flatband voltage (assuming no trapped charges)
    # Neamen Semiconductor Physics & Devices, Ed 2 (pg 434)
def Vfb(CPD_metsem): # eV
    Vfb = CPD_metsem
    return Vfb

# intgration constants
def uf(N_A,N_D,n_i,T,Vs):
    if N_A ==0: #n-type
        u = Vs/(kB*T) #dimensionless
        f = (np.exp(u)-u-1+(n_i**2/(N_D**2))*(np.exp(-1*u)+u-1))**(1/2) #dimensionless
    elif N_D ==0: #p-type
        u = -1*Vs/(kB*T) #dimensionless
        f = (np.exp(u)-u-1+(n_i**2/(N_A**2))*(np.exp(-1*u)+u-1))**(1/2) #dimensionless
    return u,f

# Charge in the semiconductor
def Qs(u,f,epsilon_sem,T,L_D):
    Qs = -1*np.sign(u)*kB*T*epsilon_sem*epsilon_o*100/L_D*f #eV*C/Vm**2
    return Qs

# Force between MOS plates
def F(f,epsilon_sem,T,L_D):
    F = 1/(2*epsilon_o*100)*(kB*T*epsilon_sem*epsilon_o*100/L_D*f)**2 #N/m**2
    return F

# Debye length
def LD(epsilon_sem, N_D, N_A, T):
    LD = np.sqrt(epsilon_sem*epsilon_o*100*kB*T/(2*(N_D+N_A)*e)) #m (Note units: N_A and N_D are in m^-3)
    return LD

# Accumulation layer width
    # ? Chapter  pg 173
def zA(Nd,Na,LD,Vs,T):
    if Na ==0: #n-type
        zA = np.sqrt(2)*LD*np.arccos(np.exp(-Vs/(2*kB*T))) #m
    elif Nd ==0: #p-type
        zA = np.sqrt(2)*LD*np.arccos(np.exp(Vs/(2*kB*T))) #m
    return zA

# Depletion layer width (pg. 435 eq. 10.5)
    # ? Chapter  pg 173
def zD(epsilon_sem, Nd, Na, Vs, T):
    if Na ==0: #n-type
        zD = np.sqrt(2*epsilon_sem*epsilon_o*Vs/(Nd*e))/100 #m (Note units: Na and Nd are in cm^-3)
    elif Nd ==0: #p-type
        zD = np.sqrt(2*epsilon_sem*epsilon_o*Vs/(Na*e))/100 #m (Note units: Na and Nd are in cm^-3)
    return zD

# Inversion layer width
    # ? Chapter  pg 180
def zI():
    if Na ==0: #n-type
        zI = np.sqrt(4*epsilon_sem*epsilon_o*Vs/(Nd*e))/100 #m (Note units: Na and Nd are in cm^-3)
    elif Nd ==0: #p-type
        zI = np.sqrt(4*epsilon_sem*epsilon_o*Vs/(Na*e))/100 #m (Note units: Na and Nd are in cm^-3)
    return zI

################################################################################
################################################################################
# MOS capacitor (illuminated)
