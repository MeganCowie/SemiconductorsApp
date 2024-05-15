import numpy as np
import scipy.constants as sp
from scipy.optimize import fsolve
from scipy.integrate import quad

from bokeh.io import show
from bokeh.plotting import figure
from bokeh.layouts import Column, Row, gridplot

##################
# VARIABLES 

Vg_value = 5
zins_value = 1
Nd_value = 17.5
Na_value = 0
Eg_value = 0.8
ep_value = 11.7
EA_value = 4.05
WF_value = 4.75
mn_value = 1
mp_value = 1
T_value = 300

def Var_Vg_Vgarray():
    Vgarray = np.arange(-10,10,0.4)
    return Vgarray

def Var_zins_zinsarray():
    zinsarray = np.arange(0.1,20,0.4)
    return zinsarray


##################
# PHYSICS

# Physical constants
kB = sp.value('Boltzmann constant') #J/K
hbar = sp.value('Planck constant')/(2*sp.pi) #J*s
me = sp.value('electron mass') #kg
e = sp.e #C
ep_o = sp.value('vacuum electric permittivity') #C/(V*m)

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
    if Na <=1e7: #n-type
        nb = (Nd-Na)/2+np.sqrt(((Nd-Na)/2)**2+ni**2)
        pb = ni**2/nb
    elif Nd <= 1e7: #p-type
        pb = (Na-Nd)/2+np.sqrt(((Na-Nd)/2)**2+ni**2)
        nb = ni**2/pb
    return nb,pb

# Fermi level
    # Pierret Semiconductor Fundamentals, Vol 1, Ed 2 (pg 49)
    # Neamen Semiconductor Physics & Devices, Ed 2 (pg 115)
    # Jonscher Solid Semiconductors (pg 33)
def Func_Ef(NC, NV, Ec, Ev, T, Nd, Na): # J
    guess = -1*e
    def Ef_eqn(Ef_soln):
        no, po = Func_nopo(NC, NV, Ec, Ev, Ef_soln, T)
        expression = po-no+Nd-Na
        return expression
    Ef = fsolve(Ef_eqn, guess)[0]
    return Ef

# Contact potential difference
    # Neamen Semiconductor Physics & Devices, Ed 2 (pg 431)
    # Sze Physics of Semiconductor Devices (pg 199, 225)
def Func_CPD(WFmet, EAsem, Ef, Eg, Ec, Ev, Ei, Na, Nd):
    
    WFsem = EAsem + (Ec-Ef) # J
    CPD = WFmet - WFsem # J

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
def Func_LD(ep,pb,T):
    LD = np.sqrt(kB*T*ep_o*ep/(pb*e**2)) # m
    return LD

# integration constants
    # Hudlet (1995) Electrostatic forces between metallic tip and semiconductor surfaces
def Func_f(T,V,nb,pb):
    u = V/(kB*T) #dimensionless
    f = np.sqrt(np.exp(-u)+u-1+nb/pb*(np.exp(u)-u-1)) #dimensionless
    return f

# Spatial electric field inside semiconductor
def Func_E(nb,pb,V,ep,T,f):
    LD = np.sqrt(kB*T*ep_o*ep/(pb*e**2)) # m
    E = np.sign(V)*np.sqrt(2)*kB*T/(LD*e)*f # V/m
    return E

# Spatial charge inside semiconductor
    # Sze Physics of Semiconductor Devices (pg. 201-202)
    # Hudlet (1995) Electrostatic forces between metallic tip and semiconductor surfaces
def Func_Q(ep,E):
    Q = -ep*ep_o*E #C/m**2 
    return Q

# Insulator capacitance
    # Hudlet (1995) Electrostatic forces between metallic tip and semiconductor surfaces
    # https://link.springer.com/content/pdf/10.1007/b117561.pdf pg 171
def Func_Cins(zins):
    Cins= ep_o/zins #C/Vm**2
    return Cins

# Surface potential
def Func_Vs(Vg,zins,CPD,Na,Nd,ep,T,nb,pb,ni):
    if Na <=1e7: #n-type
        guess = 1*e
    elif Nd <= 1e7: #p-type
        guess = -1*e
    def Vs_eqn(Vs,Vg_variable,zins_variable):
        fs = Func_f(T,Vs,nb,pb)
        Es = Func_E(nb,pb,Vs,ep,T,fs)
        Qs = Func_Q(ep,Es)
        Cins = Func_Cins(zins_variable)
        expression = Vg_variable-CPD-Vs+e*Qs/Cins #J
        return expression
    Vs = fsolve(Vs_eqn, guess, args=(Vg,zins))[0] #J
    return Vs

# Force between MIS plates
    # Hudlet (1995) Electrostatic forces between metallic tip and semiconductor surfaces
def Func_F(Qs,CPD,Vg,zins):
    F = (-Qs**2/(2*ep_o))
    return F

# Identify MIS capacitor regime
def Func_regime(Na,Nd,Vs,Ei,Ef,Ec,Ev):
    if Na <=1e7: #n-type
        if Vs > 0:
            regime = "accumulation"
        elif Vs == 0:
            regime = "flatband"
        elif Ef > (Ei-Vs):
            regime = "depletion"
        elif Ef == (Ei-Vs):
            regime = "threshold"
        elif Ef < (Ev-Vs):
            regime = "strong inversion"
        else:
            regime = "weak inversion"
    elif Nd <=1e7: #p-type
        if Vs < 0:
            regime = "accumulation"
        elif Vs == 0:
            regime = "flatband"
        elif Ef < (Ei-Vs):
            regime = "depletion"
        elif Ef == (Ei-Vs):
            regime = "threshold"
        elif Ef > (Ec-Vs):
            regime = "strong inversion"
        else:
            regime = "weak inversion"
    return regime


##################
# BAND DIAGRAM

# Calculate band bending
def BandBending(T,ep,nb,pb,Vs):

    numdatapoints = 21

    def z_sem_eqn(V_variable):
        f_soln= Func_f(T,V_variable,nb,pb) #dimensionless
        E_soln=Func_E(nb,pb,V_variable,ep,T,f_soln) #V/m
        eqn = 1 / (e*E_soln) #m/J
        return eqn

    def compute(V_variable):
        zsem_soln, error = quad(z_sem_eqn, V_variable, Vs) #m
        fsem_soln = Func_f(T,V_variable,nb,pb) #dimensionless
        Esem_soln = Func_E(nb,pb,V_variable,ep,T,fsem_soln) #V/m
        Qsem_soln = Func_Q(ep,Esem_soln) #C/m**2
        Vsem_soln = V_variable #J
        return [zsem_soln, Vsem_soln, Esem_soln, Qsem_soln]

    if Vs == 0: # flatband case
        Vsem_soln = 0
        fsem_soln = Func_f(T,0,nb,pb)
        Esem_soln = Func_E(nb,pb,0,ep,T,fsem_soln)
        Qsem_soln = Func_Q(ep,Esem_soln)
        z_sem = np.linspace(0, 150, numdatapoints)
        V_sem = np.repeat(Vsem_soln, numdatapoints)
        E_sem = np.repeat(Esem_soln, numdatapoints)
        Q_sem = np.repeat(Qsem_soln, numdatapoints)

    else:
        V_sem = np.linspace(Vs, Vs * 0.0001, numdatapoints)
        z_sem = []
        E_sem = []
        Q_sem = []
        for V_variable in V_sem:
            result = compute(V_variable)
            z_sem.append(result[0])
            E_sem.append(result[2])
            Q_sem.append(result[3])
    return [z_sem, V_sem, E_sem, Q_sem]

# Create arrays needed to draw the band diagram
def BandDiagram(Vg,zins,T,Nd,Na,WFmet,EAsem,ep, ni,nb,pb,Vs,Ec,Ev,Ef,Ei,Eg,CPD, zsem,Vsem,Esem,Qsem):

    # Insulator (gap)
    zgap = np.array([0, 0, -zins, -zins, 0])
    Eins = -Qsem[1]/(ep_o)
    if Vs<0:
        offbot = Ef-EAsem #J #Arbitrary, just to draw as a generic wide-gap insulator
    else:
        offbot = -Vg-WFmet

    Vgap = np.array([offbot, Ec-Vs+EAsem, -Vg+WFmet, offbot, offbot]) #J #Definitions of WFmet and EAsem

    # Metal (gate)
    offgate = 20e-9 #m #Arbitrary spatial drawing of the gate (z)
    zmet = np.array([-zins-offgate, -zins])
    Vmet = np.array([-Vg, -Vg])
    Qmet = -1*Qsem[1]
    # Vacuum
    zvac = np.hstack((zmet,zsem))
    Vvac = np.hstack((Vmet+WFmet, Ec-Vsem+EAsem))

    ##

    # Combined z
    zsemarray = zsem
    zinsarray = np.array([-zins, 0])
    zmetarray = np.array([-zins-offgate, -zins,-zins])
    zarray = np.hstack((zmetarray,zinsarray,zsemarray))

    # Combined E
    Esemarray = Esem
    Einsarray = np.array([Eins, Eins])
    Emetarray = np.array([0, 0, 0])
    Earray = np.hstack((Emetarray,Einsarray,Esemarray))

    # Combined Q
    Qsemarray = Qsem
    Qinsarray = np.array([0, 0])
    Qmetarray = np.array([0, 0, Qmet])
    Qarray = np.hstack((Qmetarray,Qinsarray,Qsemarray))

    return zgap,Vgap, zvac,Vvac, zmet,Vmet, zarray,Earray,Qarray


##################
# CALCULATORS

def calculator_banddiagram(Vg,zins,Nd,Na,Eg,ep,EA,WF,mn,mp,T):
    
    # Unit conversions to SI
    Vg = Vg*e #J
    zins = zins*1e-9 #m
    Nd = round(10**Nd)*(1e6) #m-3
    Na = round(10**Na)*(1e6) #m-3
    Eg = Eg*e #J
    ep = ep
    EA = EA*e #J
    WF = WF*e #J
    mn = mn*me #kg
    mp = mp*me #kg
    T = T #K

    # Calculations
    NC,NV = Func_NCNV(T,mn,mp)
    Ec,Ev = Func_EcEv(Eg)
    Ei = Func_Ei(Ev,Ec,T,mn,mp)
    Ef = Func_Ef(NC,NV,Ec,Ev,T,Nd,Na)
    no,po = Func_nopo(NC,NV,Ec,Ev,Ef,T)
    ni = Func_ni(NC,NV,Eg,T)
    nb,pb = Func_nbpb(Na,Nd,ni)
    CPD,Ef,Ec,Ev,Ei = Func_CPD(WF,EA,Ef,Eg,Ec,Ev,Ei,Na,Nd)   
    LD = Func_LD(ep,po,T)
    Vs = Func_Vs(Vg,zins,CPD,Na,Nd,ep,T,nb,pb,ni)
    f = Func_f(T,Vs,nb,pb)
    Es = Func_E(nb,pb,Vs,ep,T,f)
    Qs = Func_Q(ep,Es)
    F = Func_F(Qs,CPD,Vg,zins)
    regime = Func_regime(Na,Nd,Vs,Ei,Ef,Ec,Ev)
    zsem, Vsem, Esem, Qsem = BandBending(T,ep,nb,pb,Vs)
    zgap,Vgap, zvac,Vvac, zmet,Vmet, zarray,Earray,Qarray = BandDiagram(Vg,zins,T,Nd,Na,WF,EA,ep,ni,nb,pb,Vs,Ec,Ev,Ef,Ei,Eg,CPD,zsem,Vsem,Esem,Qsem)

    # Unit conversions from SI
    Vg = Vg/e #eV
    zins = zins/1e-9 #nm
    Vs = Vs/e #eV
    F = F*(1e-9)**2*1e12 #pN/nm^2
    Ef = Ef/e #eV
    Ec = Ec/e #eV
    Ev = Ev/e #eV
    zgap = zgap/1e-9 #nm
    Vgap = Vgap/e #eV
    zvac = zvac/1e-9 #nm
    Vvac = Vvac/e #eV
    zmet = zmet/1e-9 #nm
    Vmet = Vmet/e #eV
    zsem = [z/1e-9 for z in zsem] #nm
    Vsem = Vsem/e #eV
    zarray = zarray/1e-9 #nm
    Earray = Earray*1e-9 #V/nm
    Qarray = Qarray/e*(1e-9)**2

    return Vg,zins,Vs,F,Ef,Ec,Ev,zgap,Vgap,zvac,Vvac,zmet,Vmet,zsem,Vsem,zarray,Earray,Qarray,regime


def calculator_arrayvalues(Vg,zins,Nd,Na,Eg,ep,EA,WF,mn,mp,T):

     # Unit conversions to SI
    Vg = Vg*e #J
    zins = zins*1e-9 #m
    Nd = round(10**Nd)*(1e6) #m-3
    Na = round(10**Na)*(1e6) #m-3
    Eg = Eg*e #J
    ep = ep
    EA = EA*e #J
    WF = WF*e #J
    mn = mn*me #kg
    mp = mp*me #kg
    T = T #K

    # Calculations
    NC,NV = Func_NCNV(T,mn,mp)
    Ec,Ev = Func_EcEv(Eg)
    Ei = Func_Ei(Ev,Ec,T,mn,mp)
    Ef = Func_Ef(NC,NV,Ec,Ev,T,Nd,Na)
    no,po = Func_nopo(NC,NV,Ec,Ev,Ef,T)
    ni = Func_ni(NC,NV,Eg,T)
    nb,pb = Func_nbpb(Na,Nd,ni)
    CPD,Ef,Ec,Ev,Ei = Func_CPD(WF,EA,Ef,Eg,Ec,Ev,Ei,Na,Nd)   
    LD = Func_LD(ep,po,T)
    Vs = Func_Vs(Vg,zins,CPD,Na,Nd,ep,T,nb,pb,ni)
    f = Func_f(T,Vs,nb,pb)
    Es = Func_E(nb,pb,Vs,ep,T,f)
    Qs = Func_Q(ep,Es)
    F = Func_F(Qs,CPD,Vg,zins)

    # Unit conversions from SI
    Vs = Vs/e #eV
    F = F*(1e-9)**2*1e12 #pN/nm^2

    return Vs,F

def calculator_Vgarrays(Vg_Vgarray,Vg,zins,Nd,Na,Eg,ep,EA,WF,mn,mp,T):
    Vs_Vgarray = []
    F_Vgarray = []
    for Vg in Vg_Vgarray:
        Vs,F = calculator_arrayvalues(Vg,zins,Nd,Na,Eg,ep,EA,WF,mn,mp,T)
        Vs_Vgarray.append(Vs)
        F_Vgarray.append(F)
    return Vg_Vgarray,Vs_Vgarray,F_Vgarray

def calculator_zinsarrays(zins_zinsarray,Vg,zins,Nd,Na,Eg,ep,EA,WF,mn,mp,T):
    Vs_zinsarray = []
    F_zinsarray = []
    for zins in zins_zinsarray:
        Vs,F = calculator_arrayvalues(Vg,zins,Nd,Na,Eg,ep,EA,WF,mn,mp,T)
        Vs_zinsarray.append(Vs)
        F_zinsarray.append(F)
    return zins_zinsarray,Vs_zinsarray,F_zinsarray


##################
# RESULTS

Vg_value,zins_value,Vs_value,F_value,Ef_value,Ec_value,Ev_value,zgap_value,Vgap_value,zvac_value,Vvac_value,zmet_value,Vmet_value,zsem_value,Vsem_value,zarray_value,Earray_value,Qarray_value,regime_value = calculator_banddiagram(Vg_value,zins_value,Nd_value,Na_value,Eg_value,ep_value,EA_value,WF_value,mn_value,mp_value,T_value)

Vg_Vgarray_value,Vs_Vgarray_value,F_Vgarray_value = calculator_Vgarrays(Var_Vg_Vgarray(),Vg_value,zins_value,Nd_value,Na_value,Eg_value,ep_value,EA_value,WF_value,mn_value,mp_value,T_value)

zins_zinsarray_value,Vs_zinsarray_value,F_zinsarray_value = calculator_zinsarrays(Var_zins_zinsarray(),Vg_value,zins_value,Nd_value,Na_value,Eg_value,ep_value,EA_value,WF_value,mn_value,mp_value,T_value)


##################
# PLOTTING

# Axes limits & ticks
xlim_1 = [0,0.5,1]
xlim_2 = [0,10**19]
xlim_3 = [0,10]
ylim = [0,3]

# Colours
color_fc='#2ca02c'
color_fv='#bcbd22'
color_Ef='#1f77b4'
color_Ei='#17becf'
color_Ev='#9467bd'
color_Ec='#e377c2'
color_n='#ff7f0e'
color_p='#8c564b'
color_gap='#e6e6e6'
color_met='#2f4f4f'
color_vac='#efefef'
color_indicator='#2ca02c'
color_line = '#000000'

# Plot
plot1a = figure(height=240, sizing_mode="stretch_width", toolbar_location=None)
plot1a.line(zmet_value, Vmet_value, color=color_met, line_width=2)
plot1a.line(zgap_value, Vgap_value, color=color_gap, line_width=2)
plot1a.line(zvac_value, Vvac_value, color=color_vac, line_width=2)
plot1a.line(zsem_value, Ec_value-Vsem_value, color=color_Ec, line_width=2)
plot1a.line(zsem_value, Ev_value-Vsem_value, color=color_Ev, line_width=2)
plot1a.line(zsem_value, np.full_like(zsem_value, Ef_value), color=color_Ef, line_width=2)
plot1a.xaxis.axis_label = "z (nm)"
plot1a.yaxis.axis_label = "Energy (eV)"
plot1a.xaxis.axis_label_text_font_style = "normal" 
plot1a.yaxis.axis_label_text_font_style = "normal"

plot1b = figure(height=120, sizing_mode="stretch_width", toolbar_location=None)
plot1b.line(zvac_value, Vvac_value, color=color_line, line_width=2)
plot1b.xaxis.axis_label = "z (nm)"
plot1b.yaxis.axis_label = "V (eV)"
plot1b.xaxis.axis_label_text_font_style = "normal" 
plot1b.yaxis.axis_label_text_font_style = "normal"

plot1c = figure(height=120, sizing_mode="stretch_width", toolbar_location=None)
plot1c.line(zarray_value, Earray_value, color=color_line, line_width=2)
plot1c.xaxis.axis_label = "z (nm)"
plot1c.yaxis.axis_label = "Efield (V/nm)"
plot1c.xaxis.axis_label_text_font_style = "normal" 
plot1c.yaxis.axis_label_text_font_style = "normal"

plot1d = figure(height=120, sizing_mode="stretch_width", toolbar_location=None)
plot1d.line(zarray_value, Qarray_value, color=color_line, line_width=2)
plot1d.xaxis.axis_label = "z (nm)"
plot1d.yaxis.axis_label = "Q (e/nm^2)"
plot1d.xaxis.axis_label_text_font_style = "normal" 
plot1d.yaxis.axis_label_text_font_style = "normal"

plot2a = figure(height=300, sizing_mode="stretch_width", toolbar_location=None)
plot2a.line(Vg_Vgarray_value, Vs_Vgarray_value, line_width=2, color=color_line)
plot2a.scatter(Vg_value, Vs_value, color=color_line, size=8)
plot2a.xaxis.axis_label = "Vg (eV)"
plot2a.yaxis.axis_label = "Vs (eV)"
plot2a.xaxis.axis_label_text_font_style = "normal" 
plot2a.yaxis.axis_label_text_font_style = "normal" 

plot2b = figure(height=300, sizing_mode="stretch_width", toolbar_location=None)
plot2b.line(Vg_Vgarray_value, F_Vgarray_value, line_width=2, 
color=color_line)
plot2b.scatter(Vg_value, F_value, color=color_line, size=8)
plot2b.xaxis.axis_label = "Vg (eV)"
plot2b.yaxis.axis_label = "F (pN/nm^2)"
plot2b.xaxis.axis_label_text_font_style = "normal" 
plot2b.yaxis.axis_label_text_font_style = "normal" 

plot3a = figure(height=300, sizing_mode="stretch_width", toolbar_location=None)
plot3a.line(zins_zinsarray_value, Vs_zinsarray_value, line_width=2, color=color_line)
plot3a.scatter(zins_value, Vs_value, color=color_line, size=8)
plot3a.xaxis.axis_label = "zins (nm)"
plot3a.yaxis.axis_label = "Vs (eV)"
plot3a.xaxis.axis_label_text_font_style = "normal" 
plot3a.yaxis.axis_label_text_font_style = "normal" 

plot3b = figure(height=300, sizing_mode="stretch_width", toolbar_location=None)
plot3b.line(zins_zinsarray_value, F_zinsarray_value, line_width=2, color=color_line)
plot3b.scatter(zins_value, F_value, color=color_line, size=8)
plot3b.xaxis.axis_label = "zins (nm)"
plot3b.yaxis.axis_label = "F (pN/nm^2)"
plot3b.xaxis.axis_label_text_font_style = "normal" 
plot3b.yaxis.axis_label_text_font_style = "normal" 


# Layout
plots = Row(Column(plot1a,plot1b,plot1c,plot1d, sizing_mode="scale_width"), Column(plot2a,plot2b, sizing_mode="scale_width"), Column(plot3a,plot3b, sizing_mode="scale_width"), sizing_mode="scale_width")


##################

show(plots)
print(f"regime = {regime_value}")
