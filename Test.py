import Physics_Semiconductors

import numpy as np
from numpy import random
from scipy.optimize import fsolve


kB = Physics_Semiconductors.kB
hbar = Physics_Semiconductors.hbar
me = Physics_Semiconductors.me
e = Physics_Semiconductors.e
epsilon_o = Physics_Semiconductors.epsilon_o

Vg = 10 #[-1.71, -0.5235271835511259]
zins = 5e-7 #cm
bandgap = 2.5 #eV
epsilon_sem = 22 # dimensionless
WFmet = 5.5 #eV
EAsem = 2.7 #eV
Nd = 0#round((10**0*10**8)/(1000**3))
Na = round((10**19*10**8)/(1000**3))
mn = 1.1*Physics_Semiconductors.me #kg
mp = 1.2*Physics_Semiconductors.me #kg
T = 300 # K


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
    f = (np.exp(u)-u-1+(n_i**2/(N_D**2-N_A**2))*(np.exp(-1*u)+u-1)**(1/2)) #dimensionless
    Qs = np.sign(u)*kB*T*epsilon_sem*epsilon_o*100/L_D*f #eV*C/Vm**2
        
    expression = Vg_variable+CPD_metsem-Vs-Qs/(C_l) #eV (I incorporated the CPD, not included in Hudlet)
    
    return expression


import warnings
warnings.filterwarnings("error")

try: 
    Vs = fsolve(Vs_eqn, 0, args=(Vg,zins))[0]
    print('1')
except:
    try:
        Vs = fsolve(Vs_eqn, 0.1, args=(Vg,zins))[0]
        print('2')
    except:
        Vs = fsolve(Vs_eqn, -0.1, args=(Vg,zins))[0]
        print('3')    



#Vs = 0.2511
#C_l= epsilon_o*100/(zins/100) #C/Vm**2
#u = Vs/(kB*T) #dimensionless
#f = np.longdouble((np.exp(u)-u-1+(n_i**2/(N_D**2+N_A**2))*(np.exp(-1*u)+u-1))**(1/2)) #dimensionless
#Qs = -np.sign(u)*kB*T*epsilon_sem*epsilon_o*100/L_D*f #eV*C/Vm**2



print(Vs)
