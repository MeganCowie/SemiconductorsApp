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

kB = sp.value('Boltzmann constant') #J/K
hbar = sp.value('Planck constant')/(2*sp.pi) #J*s
me = sp.value('electron mass') #kg
e = sp.e #C
epsilon_o = sp.value('vacuum electric permittivity') #C/(V*m)


################################################################################
################################################################################
# solid state and extrinsic semiconductor definitions

# Electron and hole Fermi-dirac distributions
    # Pierret Semiconductor Fundamentals, Vol 1, Ed 2 (pg 38)
    # Neamen Semiconductor Physics & Devices, Ed 2 (pg 71)
    # Jonscher Solid Semiconductors (pg 12-13)
def Func_fcfv(E,Ef,T): # dimensionless
    fc = np.reciprocal(np.exp((E-Ef)/(kB*T))+1)
    fv = 1-np.reciprocal(np.exp((E-Ef)/(kB*T))+1)
    return fc, fv

# Maxwell Boltzmann probability distribution
    # Neamen Semiconductor Physics & Devices, Ed 2 (pg 75)
def Func_MaxwellBoltzmann(E,Ef,T): #dimensionless
    fb = np.reciprocal(np.exp((E-Ef)/(kB*T)))
    return fb

# Density of states in the conduction and valence bands
    # Pierret Semiconductor Fundamentals, Vol 1, Ed 2 (pg 36)
    # Neamen Semiconductor Physics & Devices, Ed 2 (pg 69-70)
def Func_gcgv(E,Ec,Ev,mn,mp): # /(J*m**3)
    Earg=E-Ec
    Earg[Earg<0]=0
    gc = 1/(2*sp.pi**2)*((2*mn)/(hbar**2))**(3/2)*np.sqrt(Earg)
    Earg=Ev-E
    Earg[Earg<0]=0
    gv = 1/(2*sp.pi**2)*((2*mp)/(hbar**2))**(3/2)*np.sqrt(Earg)
    return gc, gv


# Number of electrons/holes in the conduction/valence band
    # Pierret Semiconductor Fundamentals, Vol 1, Ed 2 (pg 43)
    # Neamen Semiconductor Physics & Devices, Ed 2 (pg 86)
    # Jonscher Solid Semiconductors (pg 29)
def Func_NeNh(E, fc, fv, gc, gv, Ec, Ev): # /(J*m**3)
    Ne=fc*gc
    Ne[E<Ec]=0
    Nh=fv*gv
    Nh[E>Ev]=0
    return Ne, Nh

# effective density of conduction and valence band states
    # Pierret Semiconductor Fundamentals, Vol 1, Ed 2 (pg 44)
    # Neamen Semiconductor Physics & Devices, Ed 2 (pg 89-91)
    # Sze Physics of Semiconductor Devices (pg 19)
def Func_NCNV(T, mn, mp): # /(m**3)
    NC = 1/np.sqrt(2)*((mn*kB*T)/(sp.pi*hbar**2))**(3/2)
    NV = 1/np.sqrt(2)*((mp*kB*T)/(sp.pi*hbar**2))**(3/2)
    return NC, NV

# conduction and valence arbitrary energies
# The conduction band level does not impact the Vs or F, so set arbitrarily as 1 for now
# We only need absolute eneries for drawing the band diagram. See CPD definition below. 
    # Jonscher Solid Semiconductors (pg 30)
def Func_EcEv(Eg): # J
    Ev = 0*e
    Ec = Ev+Eg
    return Ec, Ev

# intrinsic carrier density
    # Pierret Semiconductor Fundamentals, Vol 1, Ed 2 (pg 46)
    # Neamen Semiconductor Physics & Devices, Ed 2 (pg 92)
def Func_ni(NC, NV, Eg, T): # 1/m**3
    ni = np.sqrt(NC*NV)*np.exp(-Eg/(2*kB*T))
    return ni

# electron and hole thermal concentrations
    # Pierret Semiconductor Fundamentals, Vol 1, Ed 2 (pg 45)
    # Neamen Semiconductor Physics & Devices, Ed 2 (pg 89-91)
    # Jonscher Solid Semiconductors (pg 30-31)
def Func_nopo(NC, NV, Ec, Ev, Ef, T): # 1/m**3
    no = NC * np.exp((-Ec+Ef)/(kB*T))
    po = NV * np.exp((Ev-Ef)/(kB*T))
    return no, po

# Intrinsic level
    # Pierret Semiconductor Fundamentals, Vol 1, Ed 2 (pg 52)
    # Neamen Semiconductor Physics & Devices, Ed 2 (pg 94)
    # Jonscher Solid Semiconductors (pg 31)
def Func_Ei(Ev, Ec, T, mn, mp): # J
    Ei = (Ec+Ev)/2+(1/2)*kB*T*np.log(mp/mn)
    return Ei

# Total carrier concentrations in the bulk
    # Neamen Semiconductor Physics & Devices, Ed 2 (pg 115)
    # Sze Physics of Semiconductor Devices (pg 32)
def Func_nbpb(Na, Nd, ni): # /m**3
    if Na <=1e-9: #n-type
        nb = (Nd-Na)/2+np.sqrt(((Nd-Na)/2)**2+ni**2)
        pb = ni**2/nb
    elif Nd <= 1e-9: #p-type
        pb = (Na-Nd)/2+np.sqrt(((Na-Nd)/2)**2+ni**2)
        nb = ni**2/pb
    return nb,pb

# Fermi level
    # Pierret Semiconductor Fundamentals, Vol 1, Ed 2 (pg 49)
    # Neamen Semiconductor Physics & Devices, Ed 2 (pg 115)
    # Jonscher Solid Semiconductors (pg 33)
def Func_Ef(NC, NV, Ec, Ev, T, Nd, Na): # J
    guess = 1*e
    def Ef_eqn(Ef_soln):
        no, po = Func_nopo(NC, NV, Ec, Ev, Ef_soln, T)
        expression = po-no+Nd-Na
        return expression
    Ef = fsolve(Ef_eqn, guess)[0]
    return Ef

################################################################################
################################################################################
# MIS capacitor

# Contact potential difference
    # Neamen Semiconductor Physics & Devices, Ed 2 (pg 431)
    # Sze Physics of Semiconductor Devices (pg 199, 225)
def Func_CPD(WFmet, EAsem, Ef, Eg, Ec, Ev, Ei, Na, Nd):
    
    WFsem = EAsem + (Ec-Ef) # J
    CPD = WFmet - WFsem # J

    # Now we can state the energy levels explicitly. 
    # They aren't needed for anything except drawing the band diagram. 
    # (That is, all equations account just for energy differences rather than absolute energies, except drawing the band diagram.)

    Delta_EcEf = Ec-Ef
    Delta_EvEf = Ev-Ef
    Delta_EiEf = Ei-Ef

    Ef = -CPD
    Ec = Ef+Delta_EcEf
    Ev = Ef+Delta_EvEf
    Ei = Ef+Delta_EiEf

    return CPD, Ef,Ec,Ev,Ei

# flatband voltage (assuming no trapped charges)
    # Neamen Semiconductor Physics & Devices, Ed 2 (pg 434)
def Func_Vfb(CPD):
    Vfb = CPD # J
    return Vfb

# Debye length
    # Hudlet (1995) Electrostatic forces between metallic tip and semiconductor surfaces
    # Sze Physics of Semiconductor Devices (pg 202)
def Func_LD(epsilon_sem,pb,T):
    LD = np.sqrt(kB*T*epsilon_o*epsilon_sem/(pb*e**2)) # m
    return LD

# integration constants
    # Hudlet (1995) Electrostatic forces between metallic tip and semiconductor surfaces
def Func_f(T,V,nb,pb):
    u = V/(kB*T) #dimensionless
    f = np.sqrt(np.exp(-u)+u-1+nb/pb*(np.exp(u)-u-1)) #dimensionless
    return f

# Spatial electric field inside semiconductor
def Func_E(nb,pb,V,epsilon_sem,T,f):
    LD = np.sqrt(kB*T*epsilon_o*epsilon_sem/(pb*e**2)) # m
    E = np.sign(V)*np.sqrt(2)*kB*T/(LD*e)*f # V/m
    return E

# Spatial charge inside semiconductor
    # Sze Physics of Semiconductor Devices (pg. 201-202)
    # Hudlet (1995) Electrostatic forces between metallic tip and semiconductor surfaces
def Func_Q(epsilon_sem,E):
    Q = -epsilon_sem*epsilon_o*E #C/m**2 
    return Q

# Insulator capacitance
    # Hudlet (1995) Electrostatic forces between metallic tip and semiconductor surfaces
    # https://link.springer.com/content/pdf/10.1007/b117561.pdf pg 171
def Func_Cins(zins):
    Cins= epsilon_o/zins #C/Vm**2
    return Cins

# Surface potential
def Func_Vs(Vg,zins,CPD,Na,Nd,epsilon_sem,T,nb,pb,ni):
    if Na <=1e-9: #n-type
        guess = 1*e
    elif Nd <= 1e-9: #p-type
        guess = -1*e
    def Vs_eqn(Vs,Vg_variable,zins_variable):
        fs = Func_f(T,Vs,nb,pb)
        Es = Func_E(nb,pb,Vs,epsilon_sem,T,fs)
        Qs = Func_Q(epsilon_sem,Es)
        Cins = Func_Cins(zins_variable)
        expression = Vg_variable-CPD-Vs+e*Qs/Cins #J
        return expression
    Vs = fsolve(Vs_eqn, guess, args=(Vg,zins))[0] #J
    return Vs

# Force between MIS plates
    # Hudlet (1995) Electrostatic forces between metallic tip and semiconductor surfaces
def Func_F(Qs,CPD,Vg,zins):
    F = (-Qs**2/(2*epsilon_o))#-10**(37.35)*(epsilon_o*(Vg-CPD)**2/(2*zins**2)) # N/m**2
    return F

# Polarization
    # One-dimensional sum of electric dipoles
def Func_P(zsem, Qsem):
    p = zsem*Qsem #electric dipole  #Cm 
    P = np.sum(p) #electric polarization #Cm
    return P

# Identify MIS capacitor regime
def Func_regime(Na,Nd,Vs,Ei,Ef,Ec,Ev):
    if Na <=1e-9: #n-type
        if Vs > 0:
            regime = 1 #accumulation
        elif Vs == 0:
            regime = 2 #flatband
        elif Ef > (Ei-Vs):
            regime = 3 #depletion
        elif Ef == (Ei-Vs):
            regime = 4 #threshold
        elif Ef < (Ev-Vs):
            regime = 6 #strong inversion
        else:
            regime = 5 #weak inversion
    elif Nd <=1e-9: #p-type
        if Vs < 0:
            regime = 1 #accumulation
        elif Vs == 0:
            regime = 2 #flatband
        elif Ef < (Ei-Vs):
            regime = 3 #depletion
        elif Ef == (Ei-Vs):
            regime = 4 #threshold
        elif Ef > (Ec-Vs):
            regime = 6 #strong inversion
        else:
            regime = 5 #weak inversion
    return regime



