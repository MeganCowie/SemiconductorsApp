import numpy as np
import pandas as pd
from scipy.optimize import fsolve
import Physics_SemiconductorSurface

################################################################################
################################################################################
# physical constants

kB = Physics_SemiconductorSurface.kB
hbar = Physics_SemiconductorSurface.hbar
me = Physics_SemiconductorSurface.me
e = Physics_SemiconductorSurface.e
epsilon_o = Physics_SemiconductorSurface.epsilon_o


################################################################################
################################################################################
# Surface potential and force expressions from Hudlet 1995

def VsF(guess,   Vg,zins,bandgap,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T):

    NC,NV = Physics_SemiconductorSurface.NCNV(T,mn,mp)
    Ec,Ev = Physics_SemiconductorSurface.EcEv(T,bandgap)
    Eg = Physics_SemiconductorSurface.Eg(Ec,Ev)
    ni = Physics_SemiconductorSurface.ni(NC,NV,Eg,T)
    Ef = Physics_SemiconductorSurface.Ef(NC, NV, Ec, Ev, T, Nd, Na)
    CPD_metsem = Physics_SemiconductorSurface.CPD_metsem(WFmet, EAsem, Ec, Ef)

    n_i = ni*(100)**3 #m**-3
    N_D = Nd*(100)**3 #m**-3
    L_D = Physics_SemiconductorSurface.LD(epsilon_sem, N_D, T)

    def Vs_eqn(Vs,Vg_variable,zins_variable):

        C_l= epsilon_o*100/(zins_variable/100) #C/Vm**2

        u = Vs/(kB*T) #dimensionless
        f = (np.exp(u)-u-1+(n_i**2/N_D**2)*(np.exp(-1*u)+u-1))**(1/2) #dimensionless
        Qs = -np.sign(u)*kB*T*epsilon_sem*epsilon_o*100/L_D*f #eV*C/Vm**2
        eqn = Vg_variable+CPD_metsem-Vs-Qs/(C_l) #eV (I incorporated the CPD, not included in Hudlet)
        return eqn

    def F_eqn(Vs_variable):
        u = Vs_variable/(kB*T) #dimensionless
        f = (np.exp(u)-u-1+(n_i**2/N_D**2)*(np.exp(-1*u)+u-1))**(1/2) #dimensionless
        F_soln = 1/(2*epsilon_o*100)*(kB*T*epsilon_sem*epsilon_o*100/L_D*f)**2 #N/m**2
        return F_soln

    Vs = fsolve(Vs_eqn, guess, args=(Vg,zins))[0]
    F = F_eqn(Vs)

    return Vs, F



################################################################################
################################################################################
# Organize arrays for Vs and F experimental sweeps

def VsF_arrays(Vg_array,zins_array,   Vg,zins,bandgap,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T):

    Vs_biasarray = []
    F_biasarray = []
    Vs_soln = 1
    for Vg_index in range(len(Vg_array)):
        guess = Vs_soln
        Vg_variable = Vg_array[Vg_index]
        if guess >0:
            Vs_soln, F_soln = VsF(guess+0.1,   Vg_variable,zins,bandgap,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T)
        else:
            Vs_soln, F_soln = VsF(guess-0.1,   Vg_variable,zins,bandgap,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T)
        Vs_biasarray = np.append(Vs_biasarray, Vs_soln)
        F_biasarray = np.append(F_biasarray, F_soln)

    Vs_zinsarray = []
    F_zinsarray = []
    Vs_soln = -10
    for zins_index in range(len(zins_array)):
        guess = Vs_soln
        zins_variable = zins_array[zins_index]
        if guess >0:
            Vs_soln, F_soln = VsF(guess+0.1,   Vg,zins_variable,bandgap,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T)
        else:
            Vs_soln, F_soln = VsF(guess-0.1,   Vg,zins_variable,bandgap,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T)
        Vs_zinsarray = np.append(Vs_zinsarray, Vs_soln)
        F_zinsarray = np.append(F_zinsarray, F_soln)

    return Vs_biasarray, F_biasarray, Vs_zinsarray, F_zinsarray



#    Vs_array = [[] for _ in range(len(Vg_array))]
#    guessarray = [[] for _ in range(len(Vg_array))]
#    Vs_soln = 1
#    for Vg_index in range(len(Vg_array)):
#        guess = Vs_soln
#        for zins_index in range(len(zins_array)):
#            guess = Vs_soln
#            if guess >0:
#                Vs_soln = fsolve(Vs_eqn, guess+0.1, args=(Vg_array[Vg_index],zins_array[zins_index]))[0]
#                guessarray[Vg_index] = np.append(guessarray[Vg_index], guess+0.1)
#            else:
#                Vs_soln = fsolve(Vs_eqn, guess-0.1, args=(Vg_array[Vg_index],zins_array[zins_index]))[0]
#                guessarray[Vg_index] = np.append(guessarray[Vg_index], guess-0.1)
#
#            Vs_array[Vg_index] = np.append(Vs_array[Vg_index], Vs_soln)
