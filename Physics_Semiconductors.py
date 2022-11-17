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
def Func_NCNV(T, mn, mp): # /(m**3)
    NC = 2*((2*sp.pi*mn*kB*T)/(2*sp.pi*hbar**2))**(3/2)
    NV = 2*((2*sp.pi*mp*kB*T)/(2*sp.pi*hbar**2))**(3/2)
    return NC, NV

# conduction and valence band absolute energies
# The conduction band level does not impact the Vs or F, so set arbitrarily as 1
    # Jonscher Solid Semiconductors (pg 30)
def Func_EcEv(Eg): # J
    Ev = 1*e
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

# intrinsic level
    # Pierret Semiconductor Fundamentals, Vol 1, Ed 2 (pg 52)
    # Neamen Semiconductor Physics & Devices, Ed 2 (pg 94)
    # Jonscher Solid Semiconductors (pg 31)
def Func_Ei(Ev, Ec, T, mn, mp): # J
    Ei = (Ec+Ev)/2+(1/2)*kB*T*np.log(mp/mn)
    return Ei

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
def Func_CPD(WFmet, EAsem, Ef, Eg, Ec, Ev, Na, Nd):
    if Na <=1e-9: #n-type
        WFsem = EAsem + (Ec-Ef) # J
    elif Nd <=1e-9: #p-type
        WFsem = EAsem + Eg/2 + (Ef-Ev) # J
    CPD = WFmet - WFsem # J
    return CPD

# flatband voltage (assuming no trapped charges)
    # Neamen Semiconductor Physics & Devices, Ed 2 (pg 434)
def Func_Vfb(CPD):
    Vfb = CPD # J
    return Vfb

# Insulator capacitance
    # Hudlet (1995) Electrostatic forces between metallic tip and semiconductor surfaces
    # https://link.springer.com/content/pdf/10.1007/b117561.pdf pg 171
def Func_Cins(zins):
    Cins= epsilon_o/zins #C/Vm**2
    return Cins

# Debye length
    # Hudlet (1995) Electrostatic forces between metallic tip and semiconductor surfaces
    # Sze Physics of Semiconductor Devices (pg 202)
def Func_LD(epsilon_sem,pb,T):
    LD = np.sqrt(kB*T*epsilon_o*epsilon_sem/(pb*e**2)) # m
    return LD

# intgration constants
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

# Spatial electron and hole concentrations inside semiconductor
    # Sze Physics of Semiconductor Devices (pg 201)
def Func_ndpd(nb,pb,Na,Nd,V,T):
    nd = nb*np.exp(V/(kB*T)) # /m**3
    pd = pb*np.exp(-V/(kB*T)) # /m**3
    return nd,pd

# Surface potential
def Func_Vs(Vg,zins,CPD,Na,Nd,epsilon_sem,T,nb,pb,ni,):
    if Na <=1e-9: #n-type
        guess = 1*e
    elif Nd <= 1e-9: #p-type
        guess = -1*e
    def Vs_eqn(Vs,Vg_variable,zins_variable):
        f = Func_f(T,Vs,nb,pb)
        Es = Func_E(nb,pb,Vs,epsilon_sem,T,f)
        Qs = Func_Q(epsilon_sem,Es)
        Cins = Func_Cins(zins_variable)
        expression = Vg_variable-CPD-Vs+e*Qs/Cins #J
        return expression
    Vs = fsolve(Vs_eqn, guess, args=(Vg,zins))[0] #J
    return Vs

# Force between MIS plates
    # Hudlet (1995) Electrostatic forces between metallic tip and semiconductor surfaces
def Func_F(f,epsilon_sem,T,LD):
    F = -1/(2*epsilon_o)*(kB*T*epsilon_sem*epsilon_o*f/(LD*e))**2 # N/m**2
    return F

# Identify MIS capacitor regime
def Func_regime(Na,Nd,Vs,Ei,Ef,Ec,Ev):
    if Na <=1e-9: #n-type
        if Vs > 0:
            regime = 1 #accumulation
        elif Vs == 0:
            regime = 2 #flatband
        elif Ef < (Ec+Vs):
            regime = 3 #depletion
        elif Ef == (Ec+Vs):
            regime = 4 #threshold
        elif Vs <= 2*(Ei-Ef):
            regime = 6 #strong inversion
        elif Ef > (Ec+Vs):
            regime = 5 #weak inversion
    elif Nd <=1e-9: #p-type
        if Vs < 0:
            regime = 1 #accumulation
        elif Vs == 0:
            regime = 2 #flatband
        elif Ef > (Ev+Vs):
            regime = 3 #depletion
        elif Ef == (Ev+Vs):
            regime = 4 #threshold
        elif Vs >= 2*(Ei-Ef):
            regime = 6 #strong inversion
        elif Ef < (Ev+Vs):
            regime = 5 #weak inversion
    return regime


################################################################################
# WHAT A MESS. FIX THIS -- NOT DONE YET

# Accumulation layer width
    # ? Chapter  pg 173
def Func_zA(Nd,Na,LD,Vs,T):
    zA = 1
    #if Na ==0: #n-type
    #    zA = np.sqrt(2)*LD*np.arccos(np.exp(-Vs/(2*kB*T))) #m
    #elif Nd ==0: #p-type
    #    zA = np.sqrt(2)*LD*np.arccos(np.exp(Vs/(2*kB*T))) #m
    return zA

# Depletion layer width (pg. 435 eq. 10.5)
    # ? Chapter  pg 173
def Func_zD(zins,epsilon_sem,Nd,Na,Vg,T,WFmet,EAsem,Ec,Ef,Vs):
    Cins= Func_Cins(zins)
    CPD = Func_CPD(WFmet, EAsem, Ef)
    #zD = 1
    if Na ==0: #n-type
        zD = np.sqrt((epsilon_sem*epsilon_o*100)**2/Cins**2+2*(epsilon_sem*epsilon_o*100)*np.abs(Vg-CPD)/(Nd*e)) -(epsilon_sem*epsilon_o*100)/Cins #m (Note units: Na and Nd are in cm^-3)
        zD = np.sqrt(2*(epsilon_sem*epsilon_o*100)*np.abs(Vs)/(Nd*e)) #m (Note units: Na and Nd are in cm^-3)
    elif Nd ==0: #p-type
        zD = np.sqrt((epsilon_sem*epsilon_o*100)**2/Cins**2+2*(epsilon_sem*epsilon_o*100)*np.abs(Vg-CPD)/(Na*e)) -(epsilon_sem*epsilon_o*100)/Cins #m (Note units: Na and Nd are in cm^-3)
        zD = np.sqrt(2*(epsilon_sem*epsilon_o*100)*Vs/(Na*e)) #m (Note units: Na and Nd are in cm^-3)

    return zD

# Inversion layer width
    # ? Chapter  pg 180
def Func_zI():
    zI = 1
    #if Na ==0: #n-type
    #    zI = np.sqrt(4*epsilon_sem*epsilon_o*Vs/(Nd*e))/100 #m (Note units: Na and Nd are in cm^-3)
    #elif Nd ==0: #p-type
    #    zI = np.sqrt(4*epsilon_sem*epsilon_o*Vs/(Na*e))/100 #m (Note units: Na and Nd are in cm^-3)
    return zI


# Return zA, zD, or zI depending on what regime we are in
def Func_zQ(Na,Nd,Vs,Ei,Ef,zins,epsilon_sem,Vg,T,WFmet,EAsem,Ec):
    regime = Func_regime(Na,Nd,Vs,Ei,Ef)
    zD = Func_zD(zins,epsilon_sem,Nd,Na,Vg,T,WFmet,EAsem,Ec,Ef,Vs)

    if regime == 1: #accumulation
        zQ=zD
    elif regime == 2: #flatband
        zQ=zD
    elif regime == 3: #depletion
        zQ = zD
    elif regime == 4: #threshold
        zQ=zD
    elif regime == 5: #inversion
        zQ=zD

    return zQ


################################################################################
def Func_P(Qs,zQ):
    P = 1*Qs*zQ #polarization given dipole moment, treating with N=1
    return polarization
