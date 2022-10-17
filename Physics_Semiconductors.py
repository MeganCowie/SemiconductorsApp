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
def Func_gcgv(E,Ec,Ev,mn,mp): # units?
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
def Func_NeNh(E, fc, fv, gc, gv, Ec, Ev): #dimensionless
    Ne=fc*gc
    Ne[E<Ec]=0
    Nh=fv*gv
    Nh[E>Ev]=0
    return Ne, Nh

# effective density of conduction and valence band states
    # Pierret Semiconductor Fundamentals, Vol 1, Ed 2 (pg 44)
    # Neamen Semiconductor Physics & Devices, Ed 2 (pg 89-91)
def Func_NCNV(T, mn, mp): # 1/cm**3
    NC = 2*((2*sp.pi*mn*kB*T/e)/((2*sp.pi*hbar)**2))**(3/2)*(100**3)#1/np.sqrt(2)*((mn*kB*T/e)/(sp.pi*(hbar**2)))**(3/2)*(100**3)
    NV = 2*((2*sp.pi*mp*kB*T/e)/((2*sp.pi*hbar)**2))**(3/2)*(100**3)#1/np.sqrt(2)*((mp*kB*T/e)/(sp.pi*(hbar**2)))**(3/2)*(100**3)
    return NC, NV

# electron and hole concentrations
    # Pierret Semiconductor Fundamentals, Vol 1, Ed 2 (pg 45)
    # Neamen Semiconductor Physics & Devices, Ed 2 (pg 89-91)
    # Jonscher Solid Semiconductors (pg 30-31)
def Func_nopo(NC, NV, Ec, Ev, Ef, T): #1/cm**3
    n_o = NC * np.exp((-Ec+Ef)/(kB*T))
    p_o = NV * np.exp((Ev-Ef)/(kB*T))
    return n_o, p_o

# intrinsic carrier density
    # Pierret Semiconductor Fundamentals, Vol 1, Ed 2 (pg 46)
    # Neamen Semiconductor Physics & Devices, Ed 2 (pg 92)
def Func_ni(NC, NV, Eg, T): #1/cm**3
    ni = np.sqrt(NC*NV)*np.exp(-Eg/(2*kB*T))
    return ni

# conduction and valence band absolute energies
# The conduction band level does not impact the Vs or F, so set arbitrarily as 1
    # Jonscher Solid Semiconductors (pg 30)
def Func_EcEv(T, Eg): # eV
    Ec = 1
    Ev = Ec-Eg
    return Ec, Ev

# intrinsic level
    # Pierret Semiconductor Fundamentals, Vol 1, Ed 2 (pg 52)
    # Neamen Semiconductor Physics & Devices, Ed 2 (pg 94)
    # Jonscher Solid Semiconductors (pg 31)
def Func_Ei(Ev, Ec, T, mn, mp): #eV
    Ei = (Ec+Ev)/2+(3/4)*kB*T*np.log(mp/mn) #Ev+(Ec-Ev)/2 + (kB*T)/2*np.log(mp/mn)**(3/2)
    return Ei

# Fermi level
    # Pierret Semiconductor Fundamentals, Vol 1, Ed 2 (pg 49)
    # Neamen Semiconductor Physics & Devices, Ed 2 (pg 115)
    # Jonscher Solid Semiconductors (pg 33)
def Func_Ef(NC, NV, Ec, Ev, T, Nd, Na): #eV
    def Ef_eqn(Ef_soln):
        no, po = Func_nopo(NC, NV, Ec, Ev, Ef_soln, T)
        expression = po-no+Nd-Na
        return expression
    Ef = fsolve(Ef_eqn, 1)[0]
    return Ef


################################################################################
################################################################################
# MIS capacitor

# Contact potential difference
    # Neamen Semiconductor Physics & Devices, Ed 2 (pg 431)
    # See pg. 225 in Sze
def Func_CPD(WFmet, EAsem, Ec, Ef):
    WFsem = EAsem + Ec - Ef
    CPD = WFmet - WFsem
    return CPD

# flatband voltage (assuming no trapped charges)
    # Neamen Semiconductor Physics & Devices, Ed 2 (pg 434)
def Func_Vfb(CPD_metsem): # eV
    Vfb = CPD_metsem
    return Vfb

# Debye length
    # Hudlet (1995) Electrostatic forces between metallic tip and semiconductor surfaces
    # Sze Physics of Semiconductor Devices (pg 202)
def Func_LD(epsilon_sem,N_D,N_A,T):
    LD = np.sqrt(epsilon_sem*epsilon_o*100*kB*T/(2*(N_D+N_A)*e)) #m (Note units: N_A and N_D are in m^-3)
    return LD

# Insulator capacitance
def Func_Cins(zins):
    Cins= epsilon_o*100/(zins/100) #C/Vm**2
    return Cins

# intgration constants
def Func_uf(N_A,N_D,n_i,T,V):
    if N_A ==0: #n-type
        u = V/(kB*T) #dimensionless
        f = (np.exp(u)-u-1+(n_i**2/(N_D**2))*(np.exp(-1*u)+u-1))**(1/2) #dimensionless
    elif N_D ==0: #p-type
        u = -1*V/(kB*T) #dimensionless
        f = (np.exp(u)-u-1+(n_i**2/(N_A**2))*(np.exp(-1*u)+u-1))**(1/2) #dimensionless
    return u,f

# Charge at the surface of the semiconductor
    # Sze Physics of Semiconductor Devices (pg. 201-202)
    # Hudlet (1995) Electrostatic forces between metallic tip and semiconductor surfaces
def Func_Qs(N_A,N_D,u,f,epsilon_sem,T,LD):
    if N_A ==0: #n-type
        Qs = 1*np.sign(u)*kB*T*epsilon_sem*epsilon_o*100/LD*f #eV*C/Vm**2
    elif N_D ==0: #p-type
        Qs = -1*np.sign(u)*kB*T*epsilon_sem*epsilon_o*100/LD*f #eV*C/Vm**2
    return Qs

# Force between MIS plates
    # Hudlet (1995) Electrostatic forces between metallic tip and semiconductor surfaces
def Func_F(f,epsilon_sem,T,LD):
    F = 1/(2*epsilon_o*100)*(kB*T*epsilon_sem*epsilon_o*100/LD*f)**2 #N/m**2
    return F



# Surface potential and force
# Surface potential and force expressions
    # Sze Physics of Semiconductor Devices (pg. 201-202)
    # Hudlet (1995) Electrostatic forces between metallic tip and semiconductor surfaces
def Func_VsF(guess,sampletype,   Vg,zins,Eg,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T):
    NC,NV = Func_NCNV(T,mn,mp)
    Ec,Ev = Func_EcEv(T,Eg)
    ni = Func_ni(NC,NV,Eg,T)
    Ef = Func_Ef(NC, NV, Ec, Ev, T, Nd, Na)
    CPD_metsem = Func_CPD(WFmet, EAsem, Ec, Ef)

    n_i = ni*(100)**3 #m**-3
    N_D = Nd*(100)**3 #m**-3
    N_A = Na*(100)**3 #m**-3
    LD = Func_LD(epsilon_sem, N_D, N_A, T)

    def Vs_eqn(Vs,Vg_variable,zins_variable):
        Cins= Func_Cins(zins_variable)
        u,f= Func_uf(N_A,N_D,n_i,T,Vs)
        Qs = Func_Qs(N_A,N_D,u,f,epsilon_sem,T,LD)

        # Continuity equations (needs citation)
        #if Na ==0: #n-type
            #expression = Vg_variable+CPD_metsem-Vs+Qs/(Cins) # INCORRECT #eV (I incorporated the CPD, not included in Hudlet)
            #expression = Vg_variable+CPD_metsem+Vs-Qs/(Cins) #eV (I incorporated the CPD, not included in Hudlet)
        #elif Nd ==0: #p-type
        expression = Vg_variable+CPD_metsem+Vs+Qs/(Cins) #eV
        return expression

    def F_eqn(Vs_variable):
        u,f= Func_uf(N_A,N_D,n_i,T,Vs)
        F_soln= Func_F(f,epsilon_sem,T,LD)
        return F_soln

    if sampletype==False: # semiconducting case
        Vs = fsolve(Vs_eqn, guess, args=(Vg,zins))[0]
        F = -1*F_eqn(Vs)*(1e-9)**2 #N/nm**2 (I multiplied by -1, not done in Hudlet, to represent attractive force)
    elif sampletype==True:# metallic case
        Vs = -CPD_metsem
        F = -0.5*(epsilon_o*100)*(Vg-Vs)**2/(zins/100)**2*(1e-9)**2 #U=0.5CV**2

    return Vs, F


# Identify MIS capacitor regime (accumulation, depletion, inversion)
def Func_regime(Na,Nd,Vs,Ei,Ef):
    Vb = Ef-Ei
    if Na ==0: #n-type
        if Vs < 0:
            regime = 1 #accumulation
        elif Vs == 0:
            regime = 2 #flatband
        elif Vs < Vb:
            regime = 3 #depletion
        elif Vs == Vb:
            regime = 4 #threshold
        elif Vs > Vb:
            regime = 5 #inversion
    elif Nd ==0: #p-type
        if Vs > 0:
            regime = 1 #accumulation
        elif Vs == 0:
            regime = 2 #flatband
        elif Vs > Vb:
            regime = 3 #depletion
        elif Vs == Vb:
            regime = 4 #threshold
        elif Vs < Vb:
            regime = 5 #inversion
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
    CPD = Func_CPD(WFmet, EAsem, Ec, Ef)
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
