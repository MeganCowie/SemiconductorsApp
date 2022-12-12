################################################################################
################################################################################
# This script has one primary purpose: draw a band diagram. With the first
# function we simply calculate band bending. The second function uses the first
# to create the arrays needed to draw the band diagram.
################################################################################
################################################################################

import numpy as np
import pandas as pd
from scipy.integrate import quad
from scipy.integrate import trapz
from joblib import Parallel, delayed

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
# Calculate band bending
def BandBending(T,epsilon_sem,Na,Nd,ni,nb,pb,Vs):

    numdatapoints = 101

    # Source?
    def z_sem_eqn(V_variable):
        f_soln= Physics_Semiconductors.Func_f(T,V_variable,nb,pb) #dimensionless
        E_soln=Physics_Semiconductors.Func_E(nb,pb,V_variable,epsilon_sem,T,f_soln) #V/m
        eqn = 1 / (Physics_Semiconductors.e*E_soln) #m/J
        return eqn

    def compute(V_variable):
        zsem_soln, error = quad(z_sem_eqn, V_variable, Vs) #m
        fsem_soln = Physics_Semiconductors.Func_f(T,V_variable,nb,pb) #dimensionless
        Esem_soln = Physics_Semiconductors.Func_E(nb,pb,V_variable,epsilon_sem,T,fsem_soln) #V/m
        Qsem_soln = Physics_Semiconductors.Func_Q(epsilon_sem,Esem_soln) #C/m**2
        Vsem_soln = V_variable #J
        return [zsem_soln, Vsem_soln, Esem_soln, Qsem_soln]

    if Vs == 0: # flatband case
        Vsem_soln = 0
        fsem_soln = Physics_Semiconductors.Func_f(T,0,nb,pb)
        Esem_soln = Physics_Semiconductors.Func_E(nb,pb,0,epsilon_sem,T,fsem_soln)
        Qsem_soln = Physics_Semiconductors.Func_Q(epsilon_sem,Esem_soln)
        z_sem = np.linspace(0, 150, numdatapoints)
        V_sem = np.repeat(Vsem_soln, numdatapoints)
        E_sem = np.repeat(Esem_soln, numdatapoints)
        Q_sem = np.repeat(Qsem_soln, numdatapoints)
        return [z_sem, V_sem, E_sem, Q_sem]

    else:
        V_sem = np.linspace(Vs, Vs * 0.01, numdatapoints)
        result = Parallel(n_jobs=-1)(
            delayed(compute)(V_variable) for V_variable in V_sem
        )
        return [
            np.asarray([zsem_soln for zsem_soln,Vsem_soln,Esem_soln,Qsem_soln in result]),
            np.asarray([Vsem_soln for zsem_soln,Vsem_soln,Esem_soln,Qsem_soln in result]),
            np.asarray([Esem_soln for zsem_soln,Vsem_soln,Esem_soln,Qsem_soln in result]),
            np.asarray([Qsem_soln for zsem_soln,Vsem_soln,Esem_soln,Qsem_soln in result]),
        ]



# Create arrays needed to draw the band diagram
def BandDiagram(Vg,zins,T,Nd,Na,WFmet,EAsem,epsilon_sem, ni,nb,pb,Vs,Ec,Ev,Ef,CPD, zsem,Vsem,E_sem,Q_sem):

    # Insulator
    if EAsem>WFmet:
        offbot =  2*EAsem #J #Arbitrary, just to describe as a generic wide-gap insulator
    else:
        offbot =  2*WFmet #J
    zgap = np.array([0, 0, -zins, -zins, 0])
    Vgap = np.array([Ec-Vs+EAsem-offbot, Ec-Vs+EAsem, -Vg+WFmet, -Vg+WFmet-offbot, Ec-Vs+EAsem-offbot])

    # Metal (gate)
    offgate = 20e-9 #m #  Arbitrary spatial drawing of the gate (z)
    zmet = np.array([-zins-offgate, -zins])
    Vmet = np.array([-Vg, -Vg])

    # Vacuum
    zvac = np.hstack((zmet,zsem))
    Vvac = np.hstack((Vmet+WFmet, Ec-Vsem+EAsem))

    #######################################################

    # Combined z
    zsemarray = zsem
    zinsarray = np.array([-zins, 0])
    zmetarray = np.array([-zins-offgate, -zins,-zins])
    zarray = np.hstack((zmetarray,zinsarray,zsemarray))

    # Combined E
    Esemarray = E_sem
    Einsarray = np.array([0, 0])
    Emetarray = np.array([0, 0, 0])
    Earray = np.hstack((Emetarray,Einsarray,Esemarray))

    # Combined Q
    Qsemarray = Q_sem
    Qinsarray = np.array([0, 0])
    Qmetarray = np.array([0, 0, 0])
    Qarray = np.hstack((Qmetarray,Qinsarray,Qsemarray))

    return zgap,Vgap, zvac,Vvac, zmet,Vmet, zarray,Earray,Qarray


#save_X = pd.DataFrame({"X": [str(x) for x in zsem]})
#save_Y = pd.DataFrame({"Y": [str(x) for x in E]})
#save = pd.concat([save_X,save_Y], axis=1, join="inner")
#save.to_csv('Xsave_test.csv',index=False)
