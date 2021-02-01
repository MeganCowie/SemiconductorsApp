import numpy as np
import scipy.constants as sp

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

def E():
    E = np.arange(5000)/1000
    return E

def Constant(min, max):
    mat = np.array([min, max])
    return mat

def fcfv(E, Ef, T):
    fc = np.reciprocal(np.exp((E-Ef)/(kB*T))+1)
    fv = 1-np.reciprocal(np.exp((E-Ef)/(kB*T))+1)
    return fc, fv

def MaxwellBoltzmann(E, Ef, T):
    g = np.reciprocal(np.exp((E-Ef)/(kB*T)))
    return g


################################################################################
################################################################################
# carrier & energy definitions

def EcEv():
    Ec = 2
    Ev = 1
    return Ec,Ev

def NCNV(T, mn, mp):
    NC = 1/np.sqrt(2)*((mn*kB*T)/(sp.pi*(hbar**2)))**(3/2)
    NV = 1/np.sqrt(2)*((mp*kB*T)/(sp.pi*(hbar**2)))**(3/2)
    return NC,NV

def ni(NC, NV, Ec, Ev, T):
    ni = np.sqrt(NC*NV)*np.exp(((Ev-Ec)/2)/(kB*T))
    return ni

def n(ni, NA_ion):
    n = (1/2)*(-NA_ion+np.sqrt(NA_ion**2+4*ni**2))
    # n=(ND_ion-NA_ion)/2+np.sqrt(((ND_ion-NA_ion)/2)**2+ni**2)
    return n

def p(ni, ND_ion):
    p = (1/2)*(-ND_ion+np.sqrt(ND_ion**2+4*ni**2))
    #p=(NA_ion-ND_ion)/2+np.sqrt(((NA_ion-ND_ion)/2)**2+ni**2)
    return p

def nc(E, Ei, Ef, fc, gc, Ec, Ev, T, ND_ion, n, ni):
    nc=fc*gc
    nc[E<Ec]=0
    return nc

def pv(E, Ei, Ef, fv, gv, Ec, Ev, T, ND_ion, n, ni):
    pv=fv*gv
    pv[E>Ev]=0
    return pv

def gc(E, Ec, mn):
    Earg=E-Ec
    Earg[Earg<0]=0
    gc = 1/(2*sp.pi**2)*((2*mn)/(hbar**2))**(3/2)*np.sqrt(Earg)
    return gc

def gv(E, Ev, mp):
    Earg=Ev-E
    Earg[Earg<0]=0
    gv = 1/(2*sp.pi**2)*((2*mp)/(hbar**2))**(3/2)*np.sqrt(Earg)
    return gv

def Ei(Ev, Ec, T, mn, mp):
    Ei = Ev+(Ec-Ev)/2 + (kB*T)/2*np.log(mp/mn)**(3/2)
    return Ei

def Efn(T, p, ND_ion, NA_ion, ni, Ei):
    Efn = Ei+kB*T*np.log((ND_ion+p)/ni)
    return Efn

def Efp(T, n, ND_ion, NA_ion, ni, Ei):
    Efp = Ei-kB*T*np.log((NA_ion+n)/ni)
    return Efp
