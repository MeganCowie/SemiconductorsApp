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

# intrinsic carrier density
def ni(NC, NV, Eg, T): #1/cm**3
    ni = np.sqrt(NC * NV) * np.exp(-Eg / (2 * kB * T))
    return ni

# intrinsic level
def Ei(T, ni, NC, NV, Ec, Eg): #eV
    Ei = kB * T * np.log(ni / NC) + Ec
    return Ei

# flatband voltage
def Vfb(CPD_metsem): # eV
    Vfb = CPD_metsem
    return Vfb

# oxide capacitance per unit area
def Coxp(eox,epsilon_o,tox): # C / (V*cm**2)
    Coxp = eox * epsilon_o / tox
    return Coxp

# electron and hole concentrations
def nopo(NC, NV, Ec, Ev, Ef, T): #1/cm**3
    n_o = NC * np.exp((-Ec + Ef) / (kB * T))
    p_o = NV * np.exp((Ev - Ef) / (kB * T))
    return n_o, p_o

def Ef(NC, NV, Ec, Ev, T, Nd, Na):
    def Ef_eqn(Ef):
        no, po = nopo(NC, NV, Ec, Ev, Ef, T)
        eqn = po-no+Nd-Na
        return eqn
    Ef = fsolve(Ef_eqn, 1)[0]
    return Ef

# Contact potential difference
def CPD_metsem(WFmet, EAsem, Ec, Ef):
    WFsem = EAsem + Ec - Ef
    CPD_metsem = WFmet - WFsem
    return CPD_metsem


################################################################################

# Debye length
def LD(epsilon_sem, Nd, T):
    LD = np.sqrt(epsilon_sem*epsilon_o*100*kB*T/(2*Nd*e)) #m
    return LD


################################################################################
################################################################################
# Solve for Vg given Vs

def Vgbuttons(Vs,   zins,bandgap,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T):

    NC,NV = NCNV(T,mn,mp)
    Ec,Ev = EcEv(T,bandgap)
    Eg_value = Eg(Ec,Ev)
    ni_value = ni(NC,NV,Eg_value,T)
    Ef_value = Ef(NC, NV, Ec, Ev, T, Nd, Na)
    CPD_metsem_value = CPD_metsem(WFmet, EAsem, Ec, Ef_value)

    n_i = ni_value*(100)**3 #m**-3
    N_D = Nd*(100)**3 #m**-3
    L_D = LD(epsilon_sem, N_D, T)

    def Vg_eqn(Vg,Vs_variable,zins_variable):

        C_l= epsilon_o*100/(zins_variable/100) #C/Vm**2

        u = Vs_variable/(kB*T) #dimensionless
        f = (np.exp(u)-u-1+(n_i**2/N_D**2)*(np.exp(-1*u)+u-1))**(1/2) #dimensionless
        Qs = -np.sign(u)*kB*T*epsilon_sem*epsilon_o*100/L_D*f #eV*C/Vm**2
        eqn = Vg+CPD_metsem_value-Vs-Qs/(C_l) #eV (I incorporated the CPD, not included in Hudlet)
        return eqn

    Vg = fsolve(Vg_eqn, 0, args=(Vs,zins))[0]

    return [Vg]
