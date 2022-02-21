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
# Surface potential and force expressions
    # Sze Physics of Semiconductor Devices (pg. 201-202)
    # Hudlet (1995) Electrostatic forces between metallic tip and semiconductor surfaces


def VsF(guess,sampletype,   Vg,zins,Eg,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T):

    NC,NV = Physics_Semiconductors.NCNV(T,mn,mp)
    Ec,Ev = Physics_Semiconductors.EcEv(T,Eg)
    ni = Physics_Semiconductors.ni(NC,NV,Eg,T)
    Ef = Physics_Semiconductors.Ef(NC, NV, Ec, Ev, T, Nd, Na)
    CPD_metsem = Physics_Semiconductors.CPD_metsem(WFmet, EAsem, Ec, Ef)

    n_i = ni*(100)**3 #m**-3
    N_D = Nd*(100)**3 #m**-3
    N_A = Na*(100)**3 #m**-3
    L_D = Physics_Semiconductors.LD(epsilon_sem, N_D, N_A, T)

    def Vs_eqn(Vs,Vg_variable,zins_variable):
        C_l= epsilon_o*100/(zins_variable/100) #C/Vm**2
        u,f=Physics_Semiconductors.uf(N_A,N_D,n_i,T,Vs)
        Qs = Physics_Semiconductors.Qs(u,f,epsilon_sem,T,L_D)
        if Na ==0: #n-type
            expression = Vg_variable+CPD_metsem+Vs-Qs/(C_l) #eV (I incorporated the CPD, not included in Hudlet)
        elif Nd ==0: #p-type
            expression = Vg_variable+CPD_metsem+Vs+Qs/(C_l) #eV
        return expression

    def F_eqn(Vs_variable):
        u,f=Physics_Semiconductors.uf(N_A,N_D,n_i,T,Vs)
        F_soln=Physics_Semiconductors.F(f,epsilon_sem,T,L_D)
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

def VsF_arrays(Vg_array,zins_array,sampletype,   Vg,zins,Eg,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T):

    # Bias array
    Vs_biasarray = []
    F_biasarray = []
    Vs_soln = 1
    for Vg_index in range(len(Vg_array)):
        guess = Vs_soln

        Vg_variable = Vg_array[Vg_index]
        if guess >0:
            Vs_soln, F_soln = VsF(guess-0.1,sampletype,   Vg_variable,zins,Eg,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T)
        else:
            Vs_soln, F_soln = VsF(guess-0.1,sampletype,   Vg_variable,zins,Eg,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T)

        Vs_biasarray = np.append(Vs_biasarray, Vs_soln)
        F_biasarray = np.append(F_biasarray, F_soln)

    #zins array
    Vs_zinsarray = []
    F_zinsarray = []
    Vs_soln = -10
    for zins_index in range(len(zins_array)):
        guess = Vs_soln
        zins_variable = zins_array[zins_index]
        if guess >0:
            Vs_soln, F_soln = VsF(guess+0.1,sampletype,   Vg,zins_variable,Eg,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T)
        else:
            Vs_soln, F_soln = VsF(guess-0.1,sampletype,   Vg,zins_variable,Eg,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T)

        Vs_zinsarray = np.append(Vs_zinsarray, Vs_soln)
        F_zinsarray = np.append(F_zinsarray, F_soln)

    return Vs_biasarray, F_biasarray, Vs_zinsarray, F_zinsarray


################################################################################
################################################################################
# Find supplemental information related to Vs and F

def VsF_supp(Vs,Vg_array,zins_array,Vs_biasarray,Vs_zinsarray,   Vg,zins,Eg,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T):

    NC,NV = Physics_Semiconductors.NCNV(T,mn,mp)
    Ec,Ev = Physics_Semiconductors.EcEv(T,Eg)
    ni = Physics_Semiconductors.ni(NC,NV,Eg,T)
    Ei = Physics_Semiconductors.Ei(Ev, Ec, T, mn, mp)
    Ef = Physics_Semiconductors.Ef(NC, NV, Ec, Ev, T, Nd, Na)
    CPD_metsem = Physics_Semiconductors.CPD_metsem(WFmet, EAsem, Ec, Ef)

    n_i = ni*(100)**3 #m**-3
    N_D = Nd*(100)**3 #m**-3
    N_A = Na*(100)**3 #m**-3
    L_D = Physics_Semiconductors.LD(epsilon_sem, N_D, N_A, T)
    C_l= epsilon_o*100/(zins/100) #C/Vm**2

    # Values
    regime = Physics_Semiconductors.MOS_regime(Na,Nd,Vs,Ei,Ef)
    LD = Physics_Semiconductors.LD(epsilon_sem,N_D,N_A,T)
    u,f=Physics_Semiconductors.uf(N_A,N_D,n_i,T,Vs)
    zA = Physics_Semiconductors.zA(Nd,Na,LD,Vs,T)
    zD = Physics_Semiconductors.zD(epsilon_sem,Nd,Na,Vs,T)
    Qs = Physics_Semiconductors.Qs(u,f,epsilon_sem,T,L_D)
    Cs = Physics_Semiconductors.Qs(u,f,epsilon_sem,T,L_D)


    # Bias array
    zD_biasarray = []
    Cs_biasarray = []
    Qs_biasarray = []
    for Vg_index in range(len(Vg_array)):
        Vs_soln = Vs_biasarray[Vg_index]
        zD_soln = Physics_Semiconductors.zD(epsilon_sem, Nd, Na, Vs_soln, T)
        u_soln,f_soln=Physics_Semiconductors.uf(N_A,N_D,n_i,T,Vs_soln)
        Qs_soln = Physics_Semiconductors.Qs(u_soln,f_soln,epsilon_sem,T,L_D)


        if N_A ==0: #n-type
            Cd_soln = (epsilon_sem*epsilon_o*100)/(np.sqrt(2)*LD)*(1-np.exp(-u_soln)+(n_i**2/(N_D**2)*(np.exp(u_soln)-1)))/f_soln
        elif N_D ==0: #p-type
            Cd_soln = (epsilon_sem*epsilon_o*100)/(np.sqrt(2)*LD)*(1-np.exp(-u_soln)+(n_i**2/(N_A**2)*(np.exp(u_soln)-1)))/f_soln/C_l
        Cs_soln = Cd_soln/(C_l+Cd_soln)

        # This is only true in depletion.
        #Cs_soln = (np.sqrt(1/C_l**2+2*(Vg_array[Vg_index]-CPD_metsem)/(e*N_A*epsilon_o*epsilon_sem)))**-1

        zD_biasarray = np.append(zD_biasarray, zD_soln)
        Cs_biasarray = np.append(Cs_biasarray, Cs_soln)
        Qs_biasarray = np.append(Qs_biasarray, Qs_soln)

    # zins array
    zD_zinsarray = []
    Cs_zinsarray = []
    Qs_zinsarray = []
    for zins_index in range(len(zins_array)):
        Vs_soln = Vs_zinsarray[zins_index]
        zD_soln = Physics_Semiconductors.zD(epsilon_sem, Nd, Na, Vs_soln, T)
        u_soln,f_soln=Physics_Semiconductors.uf(N_A,N_D,n_i,T,Vs_soln)
        Qs_soln = Physics_Semiconductors.Qs(u_soln,f_soln,epsilon_sem,T,L_D)
        Cs_soln = Qs_soln/Vs_soln/C_l

        zD_zinsarray = np.append(zD_zinsarray, zD_soln)
        Cs_zinsarray = np.append(Cs_zinsarray, Cs_soln)
        Qs_zinsarray = np.append(Qs_zinsarray, Qs_soln)


    zQ_biasarray = zD_biasarray
    zQ_zinsarray = zD_zinsarray
    zQ = zD
    Cs = zD

    return regime, LD, zQ, Cs, Qs, zQ_biasarray, Cs_biasarray, Qs_biasarray, zQ_zinsarray, Cs_zinsarray, Qs_zinsarray
