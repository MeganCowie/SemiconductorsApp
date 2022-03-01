################################################################################
################################################################################
# I need to test all of my functions here.
# TThere's a lot of redundancy in how I listed all the test variables, but you
# know what? It's for testing and I want it to be clear as anything.
################################################################################
################################################################################

import numpy as np

import Physics_Semiconductors
import Physics_BandDiagram
import Physics_ncAFM
import Physics_Noise
import Physics_Optics

################################################################################
################################################################################
### Physics_Semiconductors
################################################################################
################################################################################
E = np.array([0.5])
Ef = 0.4
T = 300
fc,fv = Physics_Semiconductors.Func_fcfv(E,Ef,T)
assert np.round(fc,5) == np.round(0.020468792121107835,5)
assert np.round(fv,5) == np.round(0.9795312078788921,5)
del E,Ef,T,fc,fv
################################################################################
E = np.array([0.5])
Ef = 0.4
T = 300
fb = Physics_Semiconductors.Func_MaxwellBoltzmann(E,Ef,T)
assert np.round(fb,5) == np.round(0.02089651861672851,5)
del E,Ef,T,fb
################################################################################
E = np.array([0.5])
Ef = 0.4
T = 300
Ec = 2
Ev = 1
mn = 0.8*Physics_Semiconductors.me
mp = 0.8*Physics_Semiconductors.me
gc,gv = Physics_Semiconductors.Func_gcgv(E,Ec,Ev,mn,mp)
assert np.round(gc,5) == np.round(0,5)
assert np.round(gv/1e22,5) == np.round(5.60178745,5)
del E,Ef,T,Ec,Ev,mn,mp,gc,gv
################################################################################
E = np.array([2.5])
Ef = 0.4
T = 300
Ec = 2
Ev = 1
mn = 0.8*Physics_Semiconductors.me
mp = 0.8*Physics_Semiconductors.me
gc,gv = Physics_Semiconductors.Func_gcgv(E,Ec,Ev,mn,mp)
assert np.round(gc/1e22,5) == np.round(5.60178745,5)
assert np.round(gv,5) == np.round(0,5)
del E,Ef,T,Ec,Ev,mn,mp,gc,gv
################################################################################
E = np.array([0.5])
Ef = 0.4
T = 300
Ec = 2
Ev = 1
mn = 0.8*Physics_Semiconductors.me
mp = 0.8*Physics_Semiconductors.me
fc,fv = Physics_Semiconductors.Func_fcfv(E,Ef,T)
gc,gv = Physics_Semiconductors.Func_gcgv(E,Ec,Ev,mn,mp)
Ne,Nh = Physics_Semiconductors.Func_NeNh(E,fc,fv,gc,gv,Ec,Ev)
assert np.round(Ne,5) == np.round(0,5)
assert np.round(Nh/1e22,5) == np.round(5.48712562,5)
del E,Ef,T,Ec,Ev,mn,mp,fc,fv,gc,gv,Ne,Nh
################################################################################
E = np.array([2.5])
Ef = 1.9
T = 300
Ec = 2
Ev = 1
mn = 0.8*Physics_Semiconductors.me
mp = 0.8*Physics_Semiconductors.me
fc,fv = Physics_Semiconductors.Func_fcfv(E,Ef,T)
gc,gv = Physics_Semiconductors.Func_gcgv(E,Ec,Ev,mn,mp)
Ne,Nh = Physics_Semiconductors.Func_NeNh(E,fc,fv,gc,gv,Ec,Ev)
assert np.round(Ne/1e12,5) == np.round(4.6641258,5)
assert np.round(Nh,5) == np.round(0,5)
del E,Ef,T,Ec,Ev,mn,mp,fc,fv,gc,gv,Ne,Nh
################################################################################
T = 300
mn = 0.5*Physics_Semiconductors.me
mp = 0.8*Physics_Semiconductors.me
NC,NV = Physics_Semiconductors.Func_NCNV(T,mn,mp)
assert np.round(NC/1e26,5) == np.round(1.4419420471288237,5)
assert np.round(NV/1e26,5) == np.round(2.9182855186514808,5)
del T,mn,mp,NC,NV
################################################################################
Ef = 1.6
T = 300
Ec = 2
Ev = 1
mn = 0.8*Physics_Semiconductors.me
mp = 0.8*Physics_Semiconductors.me
NC,NV = Physics_Semiconductors.Func_NCNV(T,mn,mp)
n_o,p_o = Physics_Semiconductors.Func_nopo(NC,NV,Ec,Ev,Ef,T)
assert np.round(n_o/1e19,5) == np.round(5.564466508630463,5)
assert np.round(p_o/1e16,5) == np.round(2.4298049317785188,5)
del Ef,T,Ec,Ev,mn,mp,NC,NV,n_o,p_o
################################################################################
T = 300
Eg = 1.2
mn = 0.8*Physics_Semiconductors.me
mp = 0.8*Physics_Semiconductors.me
NC,NV = Physics_Semiconductors.Func_NCNV(T,mn,mp)
ni = Physics_Semiconductors.Func_ni(NC,NV,Eg,T)
assert np.round(ni/1e16,5) == np.round(2.429804931778527,5)
del T,Eg,mn,mp,NC,NV,ni
################################################################################
T = 300
Eg = 1.2
Ec,Ev = Physics_Semiconductors.Func_EcEv(T,Eg)
assert np.round(Ec,5) == np.round(1,5)
assert np.round(Ev,5) == np.round(-0.2,5)
del T,Eg,Ec,Ev
################################################################################
T = 300
Ec = 2.2
Ev = 1.5
mn = 0.8*Physics_Semiconductors.me
mp = 0.8*Physics_Semiconductors.me
Ei = Physics_Semiconductors.Func_Ei(Ev,Ec,T,mn,mp)
assert np.round(Ei,5) == np.round(1.85,5)
del T,Ec,Ev,mn,mp,Ei
################################################################################
T = 300
Eg = 1.5
mn = 0.8*Physics_Semiconductors.me
mp = 0.8*Physics_Semiconductors.me
Nd = round((10**20*10**8)/(1000**3))
Na = round((10**15*10**8)/(1000**3))
NC,NV = Physics_Semiconductors.Func_NCNV(T,mn,mp)
Ec,Ev = Physics_Semiconductors.Func_EcEv(T,Eg)
Ef = Physics_Semiconductors.Func_Ef(NC,NV,Ec,Ev,T,Nd,Na)
assert np.round(Ef,5) == np.round(0.5556273402313018,5)
del T,Eg,mn,mp,Nd,Na,NC,NV,Ec,Ev,Ef
################################################################################
T = 300
Eg = 1.5
WFmet = 2
EAsem = 1
mn = 0.8*Physics_Semiconductors.me
mp = 0.8*Physics_Semiconductors.me
Nd = round((10**20*10**8)/(1000**3))
Na = round((10**15*10**8)/(1000**3))
NC,NV = Physics_Semiconductors.Func_NCNV(T,mn,mp)
Ec,Ev = Physics_Semiconductors.Func_EcEv(T,Eg)
Ef = Physics_Semiconductors.Func_Ef(NC,NV,Ec,Ev,T,Nd,Na)
CPD = Physics_Semiconductors.Func_CPD(WFmet,EAsem,Ec,Ef)
assert np.round(CPD,5) == np.round(0.5556273402313017,5)
del T,Eg,WFmet,EAsem,mn,mp,Nd,Na,NC,NV,Ec,Ev,Ef,CPD
################################################################################
T = 300
Eg = 1.5
WFmet = 2
EAsem = 1
mn = 0.8*Physics_Semiconductors.me
mp = 0.8*Physics_Semiconductors.me
Nd = round((10**20*10**8)/(1000**3))
Na = round((10**15*10**8)/(1000**3))
NC,NV = Physics_Semiconductors.Func_NCNV(T,mn,mp)
Ec,Ev = Physics_Semiconductors.Func_EcEv(T,Eg)
Ef = Physics_Semiconductors.Func_Ef(NC,NV,Ec,Ev,T,Nd,Na)
CPD = Physics_Semiconductors.Func_CPD(WFmet,EAsem,Ec,Ef)
Vfb = Physics_Semiconductors.Func_Vfb(CPD)
assert np.round(Vfb,5) == np.round(0.5556273402313017,5)
del T,Eg,WFmet,EAsem,mn,mp,Nd,Na,NC,NV,Ec,Ev,Ef,CPD,Vfb
################################################################################
T = 300
Nd = round((10**5*10**8)/(1000**3))
Na = round((10**0*10**8)/(1000**3))
N_D = Nd*(100)**3
N_A = Na*(100)**3
epsilon_sem = 5.2
LD = Physics_Semiconductors.Func_LD(epsilon_sem,N_D,N_A,T)
assert np.round(LD,5) == np.round(0.019273159426954872,5)
del T,Nd,Na,N_D,N_A,epsilon_sem,LD
################################################################################
Vs = 1 # To check the function, only (not true to code)
T = 300
Eg = 1.5
mn = 0.8*Physics_Semiconductors.me
mp = 0.8*Physics_Semiconductors.me
Nd = round((10**20*10**8)/(1000**3))
Na = round((10**0*10**8)/(1000**3))
NC,NV = Physics_Semiconductors.Func_NCNV(T,mn,mp)
ni = Physics_Semiconductors.Func_ni(NC,NV,Eg,T)
n_i = ni*(100)**3
N_D = Nd*(100)**3
N_A = Na*(100)**3
u,f = Physics_Semiconductors.Func_uf(N_A,N_D,n_i,T,Vs)
assert np.round(u,5) == np.round(38.68172707248528,5)
assert np.round(f,5) == np.round(250974911.07976788,5)
del Vs,T,Eg,mn,mp,Nd,Na,NC,NV,ni,n_i,N_D,N_A,u,f
################################################################################
Vs = 1 # To check the function, only (not true to code)
T = 300
Eg = 1.5
mn = 0.8*Physics_Semiconductors.me
mp = 0.8*Physics_Semiconductors.me
Nd = round((10**20*10**8)/(1000**3))
Na = round((10**0*10**8)/(1000**3))
NC,NV = Physics_Semiconductors.Func_NCNV(T,mn,mp)
ni = Physics_Semiconductors.Func_ni(NC,NV,Eg,T)
n_i = ni*(100)**3
N_D = Nd*(100)**3
N_A = Na*(100)**3
epsilon_sem = 5.2
LD = Physics_Semiconductors.Func_LD(epsilon_sem,N_D,N_A,T)
u,f = Physics_Semiconductors.Func_uf(N_A,N_D,n_i,T,Vs)
Qs = Physics_Semiconductors.Func_Qs(u,f,epsilon_sem,T,LD)
assert np.round(Qs,5) == np.round(-490143.9115678268,5)
del Vs,T,Eg,mn,mp,Nd,Na,NC,NV,ni,n_i,N_D,N_A,epsilon_sem,LD,u,f,Qs
################################################################################
Vs = 1 # To check the function, only (not true to code)
T = 300
Eg = 1.5
mn = 0.8*Physics_Semiconductors.me
mp = 0.8*Physics_Semiconductors.me
Nd = round((10**20*10**8)/(1000**3))
Na = round((10**0*10**8)/(1000**3))
NC,NV = Physics_Semiconductors.Func_NCNV(T,mn,mp)
ni = Physics_Semiconductors.Func_ni(NC,NV,Eg,T)
n_i = ni*(100)**3
N_D = Nd*(100)**3
N_A = Na*(100)**3
epsilon_sem = 5.2
LD = Physics_Semiconductors.Func_LD(epsilon_sem,N_D,N_A,T)
u,f = Physics_Semiconductors.Func_uf(N_A,N_D,n_i,T,Vs)
F = Physics_Semiconductors.Func_F(f,epsilon_sem,T,LD)
assert np.round(F/1e22,5) == np.round(1.3566521239797213,5)
del Vs,T,Eg,mn,mp,Nd,Na,NC,NV,ni,n_i,N_D,N_A,epsilon_sem,LD,u,f,F
################################################################################
Vg = 5
zins = 5*1e-7
Eg = 1.5
epsilon_sem = 5.2
WFmet = 1.5
EAsem = 2
Nd = round((10**20*10**8)/(1000**3))
Na = round((10**0*10**8)/(1000**3))
mn = 0.8*Physics_Semiconductors.me
mp = 0.8*Physics_Semiconductors.me
T = 300
guess = 1
sampletype = False
Vs,F = Physics_Semiconductors.Func_VsF(guess,sampletype,   Vg,zins,Eg,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T)
assert np.round(Vs,5) == np.round(-0.322128035173296,5)
assert np.round(F/1e-12,5) == np.round(-2.468373841493694,5)
del Vg,zins,Eg,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T,guess,sampletype,Vs,F
################################################################################
Vg = -2
zins = 5*1e-7
Eg = 1.5
epsilon_sem = 5.2
WFmet = 1.5
EAsem = 2
Nd = round((10**0*10**8)/(1000**3))
Na = round((10**20*10**8)/(1000**3))
mn = 0.8*Physics_Semiconductors.me
mp = 0.8*Physics_Semiconductors.me
T = 300
guess = 1
sampletype = False
Vs,F = Physics_Semiconductors.Func_VsF(guess,sampletype,   Vg,zins,Eg,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T)
assert np.round(Vs,5) == np.round(0.2571116118436431,5)
assert np.round(F/1e-12,5) == np.round(-1.9267080511760098,5)
del Vg,zins,Eg,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T,guess,sampletype,Vs,F
################################################################################
Vs = 1 # To check the function, only (not true to code)
Nd = round((10**20*10**8)/(1000**3))
Na = round((10**0*10**8)/(1000**3))
Ei = 1
Ef = 2
regime = Physics_Semiconductors.Func_regime(Na,Nd,Vs,Ei,Ef)
assert np.round(regime) == np.round(1,5)
del Vs,Nd,Na,Ei,Ef,regime


################################################################################
################################################################################
### Physics_BandDiagram
################################################################################
################################################################################




################################################################################
################################################################################
### Physics_ncAFM
################################################################################
################################################################################
timesteps = 200
time_AFMarray = Physics_ncAFM.time_AFMarray(timesteps)
guess = 1
sampletype = False
RTN = False
hop = 0
Vg = -0.8
zins = 5*1e-7
Eg = 1.5
epsilon_sem = 9
WFmet = 2
EAsem = 1.2
Nd = round((10**15*10**8)/(1000**3))
Na = round((10**0*10**8)/(1000**3))
mn = 0.8*Physics_Semiconductors.me
mp = 0.8*Physics_Semiconductors.me
T = 300
amplitude = 6
lag = 30
zins_AFMarray = Physics_ncAFM.zins_AFMarray(time_AFMarray, amplitude, zins)
zinslag_AFMarray = Physics_ncAFM.zinslag_AFMarray(time_AFMarray, amplitude, zins, lag)
Vs_AFMarray,F_AFMarray = Physics_ncAFM.SurfacepotForce_AFMarray(guess,zinslag_AFMarray,sampletype,RTN,hop,   Vg,zins,Eg,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T)
frequency = 300000
springconst = 42
Qfactor = 18000
tipradius = 5
df,dg = Physics_ncAFM.dfdg(time_AFMarray,F_AFMarray,frequency,springconst,amplitude,Qfactor,tipradius)
assert np.round(df,5) == np.round(-0.11750920128020204,5)
assert np.round(dg/1e-11,5) == np.round(1.2735488607206874,5)
del timesteps,time_AFMarray,guess,sampletype,RTN,hop,Vg,zins,Eg,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T,amplitude,lag,zins_AFMarray,zinslag_AFMarray,Vs_AFMarray,F_AFMarray,frequency,springconst,Qfactor,tipradius,df,dg

################################################################################
################################################################################
all_variables = dir()
for name in all_variables:
    if not name.startswith('__'):
        if not name.startswith('Physics_'):
            if not name.startswith('np'):
                myvalue = eval(name)
                print(name, "is", type(myvalue), "and is equal to ", myvalue)
