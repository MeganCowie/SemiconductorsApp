################################################################################
################################################################################
# This script primarily calculates the surface potential and force by
# numerically solving a nonlinear equation. The second function uses the first
# to calculate Vs and F as a function of bias and tip-sample separation.
################################################################################
################################################################################

import numpy as np
from scipy.optimize import fsolve
from scipy.integrate import quad
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
# Surface potential and force expressions from Hudlet 1995

def VsF(guess,sampletype,   Vg,zins,bandgap,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T):

    NC,NV = Physics_Semiconductors.NCNV(T,mn,mp)
    Ec,Ev = Physics_Semiconductors.EcEv(T,bandgap)
    Eg = Physics_Semiconductors.Eg(Ec,Ev)
    ni = Physics_Semiconductors.ni(NC,NV,Eg,T)
    Ef = Physics_Semiconductors.Ef(NC, NV, Ec, Ev, T, Nd, Na)
    CPD_metsem = Physics_Semiconductors.CPD_metsem(WFmet, EAsem, Ec, Ef)

    n_i = ni*(100)**3 #m**-3
    N_D = Nd*(100)**3 #m**-3
    N_A = Na*(100)**3 #m**-3
    L_D = Physics_Semiconductors.LD(epsilon_sem, N_D, N_A, T)

    def Vs_eqn(Vs,Vg_variable,zins_variable):

        C_l= epsilon_o*100/(zins_variable/100) #C/Vm**2
        u = Vs/(kB*T) #dimensionless
        f = (np.exp(u)-u-1+(n_i**2/(N_D**2+N_A**2))*(np.exp(-1*u)+u-1))**(1/2) #dimensionless
        Qs = np.sign(u)*kB*T*epsilon_sem*epsilon_o*100/L_D*f #eV*C/Vm**2

        expression = Vg_variable+CPD_metsem-Vs-Qs/(C_l) #eV (I incorporated the CPD, not included in Hudlet)

        return expression

    def F_eqn(Vs_variable):
        u = Vs_variable/(kB*T) #dimensionless
        f = (np.exp(u)-u-1+(n_i**2/(N_D**2+N_A**2))*(np.exp(-1*u)+u-1))**(1/2) #dimensionless
        F_soln = 1/(2*epsilon_o*100)*(kB*T*epsilon_sem*epsilon_o*100/L_D*f)**2 #N/m**2
        return F_soln


    if sampletype==False: # semiconducting case
        Vs = fsolve(Vs_eqn, guess, args=(Vg,zins))[0]
        F = -1*F_eqn(Vs)*(1e-9)**2 #N/nm**2 (I multiplied by -1, not done in Hudlet, to represent attractive force)
    elif sampletype==True:# metallic case
        Vs = -CPD_metsem
        F = -0.5*(epsilon_o*100)*(Vg-Vs)**2/(zins/100)**2*(1e-9)**2 #U=0.5CV**2

    return Vs, F



################################################################################
################################################################################
# Organize arrays for Vs and F experimental sweeps

def VsF_arrays(Vg_array,zins_array,sampletype,   Vg,zins,bandgap,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T):

    Vs_biasarray = []
    F_biasarray = []
    Vs_soln = 1
    for Vg_index in range(len(Vg_array)):
        guess = Vs_soln

        Vg_variable = Vg_array[Vg_index]
        if guess >0:
            Vs_soln, F_soln = VsF(guess-0.1,sampletype,   Vg_variable,zins,bandgap,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T)
        else:
            Vs_soln, F_soln = VsF(guess-0.1,sampletype,   Vg_variable,zins,bandgap,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T)

        #try:
        #    Vs_soln, F_soln = VsF(-10,sampletype,   Vg_variable,zins,bandgap,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T)
        #    attempt=1
        #except:
        #    try:
        #        Vs_soln, F_soln = VsF(10,sampletype,   Vg_variable,zins,bandgap,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T)
        #        attempt=2
        #    except:
        #        try:
        #            Vs_soln, F_soln = VsF(0,sampletype,   Vg_variable,zins,bandgap,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T)
        #            attempt=3
        #        except:
        #            Vs_soln, F_soln = 0,0
        #            attempt = 4

        #if np.remainder(Vg_array[Vg_index]*10,2)==0:
        #    print([Vg_array[Vg_index], guess, attempt])

        Vs_biasarray = np.append(Vs_biasarray, Vs_soln)
        F_biasarray = np.append(F_biasarray, F_soln)

    Vs_zinsarray = []
    F_zinsarray = []
    Vs_soln = -10
    for zins_index in range(len(zins_array)):
        guess = Vs_soln
        zins_variable = zins_array[zins_index]
        if guess >0:
            Vs_soln, F_soln = VsF(guess+0.1,sampletype,   Vg,zins_variable,bandgap,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T)
        else:
            Vs_soln, F_soln = VsF(guess-0.1,sampletype,   Vg,zins_variable,bandgap,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T)
        Vs_zinsarray = np.append(Vs_zinsarray, Vs_soln)
        F_zinsarray = np.append(F_zinsarray, F_soln)

    return Vs_biasarray, F_biasarray, Vs_zinsarray, F_zinsarray
