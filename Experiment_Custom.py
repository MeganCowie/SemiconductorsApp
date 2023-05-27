# Vary the dopant concentration of n-type silicon
import Presets
import Physics_Semiconductors
import Organization_IntermValues
import Organization_BuildArrays
import numpy as np
import pandas as pd
import os
from joblib import Parallel, delayed


################################################################################

button_presets = 3 # silicon surface
toggle_type, slider_Vg, slider_zins, slider_Eg, slider_epsilonsem, slider_WFmet, slider_EAsem, slider_donor, slider_acceptor, slider_emass, slider_hmass, slider_T, slider_alpha, button_presets, stylen, stylep, disabledn, disabledp = Presets.presets_surface(button_presets,0,0,0,0,0,0,0,0,0,0,0,0,0)

button_presets = 2 #silicon AFM
slider_timesteps, slider_amplitude, slider_resfreq, slider_lag, slider_springconst, slider_tipradius, slider_cantheight, slider_cantarea, slider_Qfactor,geometrybuttons = Presets.presets_afm(button_presets,0,0,0,0,0,0,0,0,0,0)

slider_biassteps = 1024
slider_zinssteps = 1
slider_timesteps = 1

slider_lag = 0
slider_zins = 12


################################################################################
# biasarray

Vg_array = np.linspace(-10,10,slider_biassteps)*Physics_Semiconductors.e #J

save_P_biasarrays = pd.DataFrame({"Vg_array": [str(x) for x in Vg_array/Physics_Semiconductors.e]})
save_Qtot_biasarrays = pd.DataFrame({"Vg_array": [str(x) for x in Vg_array/Physics_Semiconductors.e]})
save_wd_biasarrays = pd.DataFrame({"Vg_array": [str(x) for x in Vg_array/Physics_Semiconductors.e]})
save_regime_biasarrays = pd.DataFrame({"Vg_array": [str(x) for x in Vg_array/Physics_Semiconductors.e]})
save_Qs_biasarrays = pd.DataFrame({"Vg_array": [str(x) for x in Vg_array/Physics_Semiconductors.e]})
save_Vs_biasarrays = pd.DataFrame({"Vg_array": [str(x) for x in Vg_array/Physics_Semiconductors.e]})


# Input values and arrays
Vg,zins,Eg,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T,sampletype,biassteps,zinssteps,Vg_array,zins_array=Organization_IntermValues.Surface_inputvalues(slider_Vg,slider_zins,slider_alpha,slider_Eg,slider_epsilonsem,slider_WFmet,slider_EAsem,slider_donor,slider_acceptor,slider_emass,slider_hmass,slider_T,slider_biassteps,slider_zinssteps)
amplitude,frequency,lag,timesteps,tipradius,cantheight,cantarea,time_AFMarray,zins_AFMarray,zinslag_AFMarray=Organization_IntermValues.AFM1_inputvalues(slider_amplitude,slider_resfreq,slider_lag,slider_timesteps,slider_tipradius,slider_cantheight,slider_cantarea, zins)
springconst,Qfactor=Organization_IntermValues.AFM2_inputvalues(slider_springconst,slider_Qfactor)

P_biasarray = np.array([])
Qtot_biasarray = np.array([])
wd_biasarray = np.array([])
regime_biasarray = np.array([])
Qs_biasarray = np.array([])
Vs_biasarray = np.array([])
for Vg_variable in Vg_array:
    NC,NV,Ec,Ev,Ei,Ef,no,po,ni,nb,pb,CPD,LD,Vs,Es,Qs,F,regime_soln, zsem_soln,Vsem_soln,Esem_soln,Qsem_soln, P_soln = Organization_IntermValues.Surface_calculations(Vg_variable,zins,Eg,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T)
    p_soln = zsem_soln*Qsem_soln #electric dipole  #Cm 
    P_soln = np.sum(p_soln) #electric polarization #Cm
    Qtot_soln = np.sum(Qsem_soln)
    wd_soln = zsem_soln[-1]
    P_biasarray= np.append(P_biasarray,P_soln)
    Qtot_biasarray= np.append(Qtot_biasarray,Qtot_soln)
    wd_biasarray= np.append(wd_biasarray,wd_soln)
    regime_biasarray = np.append(regime_biasarray,regime_soln)
    Qs_biasarray= np.append(Qs_biasarray,Qs)
    Vs_biasarray= np.append(Vs_biasarray,Vs)


# Unit conversions
P_biasarray = P_biasarray #?
Qtot_biasarray = Qtot_biasarray/Physics_Semiconductors.e*(1e-9)**2 #/nm^2
wd_biasarray = wd_biasarray*10**9 #nm
Qs_biasarray = Qs_biasarray/Physics_Semiconductors.e*(1e-9)**2 #/nm^2
Vs_biasarray = Vs_biasarray/Physics_Semiconductors.e

# Organize arrays for saving
save_P_biasarray = pd.DataFrame({str(1): [str(x) for x in P_biasarray]})
save_Qtot_biasarray = pd.DataFrame({str(1): [str(x) for x in Qtot_biasarray]})
save_wd_biasarray = pd.DataFrame({str(1): [str(x) for x in wd_biasarray]})
save_regime_biasarray = pd.DataFrame({str(1): [str(x) for x in regime_biasarray]})
save_Qs_biasarray = pd.DataFrame({str(1): [str(x) for x in Qs_biasarray]})
save_Vs_biasarray = pd.DataFrame({str(1): [str(x) for x in Vs_biasarray]})

save_P_biasarrays = pd.concat([save_P_biasarrays,save_P_biasarray], axis=1, join="outer")
save_Qtot_biasarrays = pd.concat([save_Qtot_biasarrays,save_Qtot_biasarray], axis=1, join="outer")
save_wd_biasarrays = pd.concat([save_wd_biasarrays,save_wd_biasarray], axis=1, join="outer")
save_regime_biasarrays = pd.concat([save_regime_biasarrays,save_regime_biasarray], axis=1, join="outer")
save_Qs_biasarrays = pd.concat([save_Qs_biasarrays,save_Qs_biasarray], axis=1, join="outer")
save_Vs_biasarrays = pd.concat([save_Vs_biasarrays,save_Vs_biasarray], axis=1, join="outer")

##################
# Save

thispath = "Xsave_Sweeps_%s_%.1f_%.2f_%.2f_%.2f_%.2f_%.2f_%.2f_%.3f_%.3f_%.1f_%.1f_%.1f_%.0f_%.2f_%.0f_%.0f_%.2f_%.2f_%.3f_%.0f/" % ('custom',slider_Vg, slider_zins, slider_alpha, slider_Eg, slider_epsilonsem, slider_WFmet, slider_EAsem, slider_donor, slider_acceptor, slider_emass, slider_hmass, slider_T, slider_amplitude, slider_resfreq, slider_lag, slider_springconst, slider_Qfactor, slider_tipradius, slider_cantheight, slider_cantarea)

if not os.path.exists(thispath):
    os.mkdir(thispath)

save_P_biasarrays.to_csv(os.path.join(thispath,'_'.join(['biasarray_P.csv'])), index=False)
save_Qtot_biasarrays.to_csv(os.path.join(thispath,'_'.join(['biasarray_Qtot.csv'])), index=False)
save_wd_biasarrays.to_csv(os.path.join(thispath,'_'.join(['biasarray_wd.csv'])), index=False)
save_regime_biasarrays.to_csv(os.path.join(thispath,'_'.join(['biasarray_regime.csv'])), index=False)
save_Qs_biasarrays.to_csv(os.path.join(thispath,'_'.join(['biasarray_Qs.csv'])), index=False)
save_Vs_biasarrays.to_csv(os.path.join(thispath,'_'.join(['biasarray_Vs.csv'])), index=False)

