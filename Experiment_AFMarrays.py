# Vary the dopant concentration of n-type silicon
import Presets
import Physics_Semiconductors
import Physics_BandDiagram
import Organization_IntermValues
import Organization_BuildArrays
import numpy as np
import pandas as pd
import os

################################################################################
'''

# n-type:
button_presets = 4
Ec = -0.3333455
Ef = -0.4166885
'''
# p-type:
button_presets = 5
Ec = 1.333346
Ef = 0.4166885

toggle_type, slider_Vg, slider_zins, slider_Eg, slider_epsilonsem, slider_WFmet, slider_EAsem, slider_donor, slider_acceptor, slider_emass, slider_hmass, slider_T, slider_alpha, button_presets, stylen, stylep, disabledn, disabledp = Presets.presets_surface(button_presets,0,0,0,0,0,0,0,0,0,0,0,0,0)
CPD = slider_WFmet - (slider_EAsem + (Ec-Ef)) # J

button_presets = 1 #AFM
slider_timesteps, slider_amplitude, slider_resfreq, slider_lag, slider_springconst, slider_tipradius, slider_cantheight, slider_cantarea, slider_Qfactor = Presets.presets_afm(button_presets,0,0,0,0,0,0,0,0,0)


slider_biassteps = 1024
slider_zinssteps = 1024
slider_timesteps = 200

slider_zins = slider_zins#+slider_amplitude
slider_Vg = 0

slider_lag = 300

################################################################################
# AFMarrays

# Input values and arrays
Vg,zins,Eg,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T,sampletype,biassteps,zinssteps,Vg_array,zins_array=Organization_IntermValues.Surface_inputvalues(slider_Vg,slider_zins,slider_alpha,slider_Eg,slider_epsilonsem,slider_WFmet,slider_EAsem,slider_donor,slider_acceptor,slider_emass,slider_hmass,slider_T,slider_biassteps,slider_zinssteps)
amplitude,frequency,lag,timesteps,time_AFMarray,zins_AFMarray,zinslag_AFMarray=Organization_IntermValues.AFM1_inputvalues(slider_amplitude,slider_resfreq,slider_lag,slider_timesteps,  zins)

# Calculations and results
NC,NV,Ec,Ev,Ei,Ef,no,po,ni,nb,pb,CPD,LD,Vs,Es,Qs,F,regime, zsem,Vsem,Esem,Qsem, P = Organization_IntermValues.Surface_calculations(Vg,zins,Eg,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T)
Vs_AFMarray, F_AFMarray, Fcant_AFMarray, P_AFMarray = Organization_BuildArrays.AFM_timearrays(zinslag_AFMarray,Vg,zins,Na,Nd,epsilon_sem,T,CPD,LD,nb,pb,ni,0)
zsem_AFMarray,Vsem_AFMarray,zgap_AFMarray,Vgap_AFMarray,zvac_AFMarray,Vvac_AFMarray,zmet_AFMarray,Vmet_AFMarray = Organization_BuildArrays.AFM_banddiagrams(zins_AFMarray,Vg,T,Nd,Na,WFmet,EAsem,epsilon_sem, ni,nb,pb,Vs,Ec,Ev,Ei,Ef,Eg,CPD)

# Account for alpha
Vg = slider_Vg*Physics_Semiconductors.e #J
Vg_array = np.linspace(-10,10,biassteps)*Physics_Semiconductors.e #J

# Stack arrays to show two periods
zsem_AFMarray = np.vstack((zsem_AFMarray,zsem_AFMarray[1:]))
Vsem_AFMarray = np.vstack((Vsem_AFMarray,Vsem_AFMarray[1:]))
zgap_AFMarray = np.vstack((zgap_AFMarray,zgap_AFMarray[1:]))
Vgap_AFMarray = np.vstack((Vgap_AFMarray,Vgap_AFMarray[1:]))
zvac_AFMarray = np.vstack((zvac_AFMarray,zvac_AFMarray[1:]))
Vvac_AFMarray = np.vstack((Vvac_AFMarray,Vvac_AFMarray[1:]))
zmet_AFMarray = np.vstack((zmet_AFMarray,zmet_AFMarray[1:]))
Vmet_AFMarray = np.vstack((Vmet_AFMarray,Vmet_AFMarray[1:]))
time_AFMarray = np.hstack((time_AFMarray,time_AFMarray[1:]+2*np.pi/frequency))
zins_AFMarray = np.hstack((zins_AFMarray,zins_AFMarray[1:]))
Vs_AFMarray = np.hstack((Vs_AFMarray,Vs_AFMarray[1:]))
F_AFMarray = np.hstack((F_AFMarray,F_AFMarray[1:]))
P_AFMarray = np.hstack((P_AFMarray,P_AFMarray[1:]))

# Unit conversions
time_AFMarray = time_AFMarray
zins_AFMarray = zins_AFMarray*1e9
Vs_AFMarray = Vs_AFMarray/Physics_Semiconductors.e
F_AFMarray = F_AFMarray*(1e-9)**2*1e12
P_AFMarray = P_AFMarray #units?

 # Organize arrays for saving
save_AFMarray_time = pd.DataFrame({'time': [str(x) for x in time_AFMarray]})
save_AFMarray_zins = pd.DataFrame({'zins': [str(x) for x in zins_AFMarray]})
save_AFMarray_Vs = pd.DataFrame({'Vs': [str(x) for x in Vs_AFMarray]})
save_AFMarray_F = pd.DataFrame({'F': [str(x) for x in F_AFMarray]})
save_AFMarray_P = pd.DataFrame({'P': [str(x) for x in P_AFMarray]})
save_AFMarrays = pd.concat([save_AFMarray_time,save_AFMarray_zins,save_AFMarray_Vs,save_AFMarray_F,save_AFMarray_P], axis=1, join="outer")

zsem_AFMarray = pd.DataFrame(zsem_AFMarray*1e9)
Evsem_AFMarray = pd.DataFrame((Ev-Vsem_AFMarray)/Physics_Semiconductors.e)
Eisem_AFMarray = pd.DataFrame((Ei-Vsem_AFMarray)/Physics_Semiconductors.e)
Ecsem_AFMarray = pd.DataFrame((Ec-Vsem_AFMarray)/Physics_Semiconductors.e)
Efsem_AFMarray = pd.DataFrame(0*zsem_AFMarray+Ef/Physics_Semiconductors.e)
zgap_AFMarray = pd.DataFrame(zgap_AFMarray*1e9)
Vgap_AFMarray = pd.DataFrame(Vgap_AFMarray/Physics_Semiconductors.e)
zmet_AFMarray = pd.DataFrame(zmet_AFMarray*1e9)
Vmet_AFMarray = pd.DataFrame(Vmet_AFMarray/Physics_Semiconductors.e)
zvac_AFMarray = pd.DataFrame(zvac_AFMarray*1e9)
Vvac_AFMarray = pd.DataFrame(Vvac_AFMarray/Physics_Semiconductors.e)


################################################################################
# Save

thispath = "Xsave_AFMarrays_%.1f_%.2f_%.2f_%.2f_%.2f_%.2f_%.2f_%.3f_%.3f_%.1f_%.1f_%.1f_%.0f_%.2f_%.0f_%.0f_%.2f_%.2f_%.3f_%.0f/" % (slider_Vg, slider_zins, slider_alpha, slider_Eg, slider_epsilonsem, slider_WFmet, slider_EAsem, slider_donor, slider_acceptor, slider_emass, slider_hmass, slider_T, slider_amplitude, slider_resfreq, slider_lag, slider_springconst, slider_Qfactor, slider_tipradius, slider_cantheight, slider_cantarea)

if not os.path.exists(thispath):
    os.mkdir(thispath)

save_AFMarrays.to_csv(os.path.join(thispath,'_'.join(['timearrays.csv'])), index=False)
zsem_AFMarray.to_csv(os.path.join(thispath,'_'.join(['banddiagram_zsem.csv'])), index=False)
Evsem_AFMarray.to_csv(os.path.join(thispath,'_'.join(['banddiagram_Evsem.csv'])), index=False)
Eisem_AFMarray.to_csv(os.path.join(thispath,'_'.join(['banddiagram_Eisem.csv'])), index=False)
Ecsem_AFMarray.to_csv(os.path.join(thispath,'_'.join(['banddiagram_Ecsem.csv'])), index=False)
Efsem_AFMarray.to_csv(os.path.join(thispath,'_'.join(['banddiagram_Efsem.csv'])), index=False)
zgap_AFMarray.to_csv(os.path.join(thispath,'_'.join(['banddiagram_zgap.csv'])), index=False)
Vgap_AFMarray.to_csv(os.path.join(thispath,'_'.join(['banddiagram_Vgap.csv'])), index=False)
zmet_AFMarray.to_csv(os.path.join(thispath,'_'.join(['banddiagram_zmet.csv'])), index=False)
Vmet_AFMarray.to_csv(os.path.join(thispath,'_'.join(['banddiagram_Vmet.csv'])), index=False)
zvac_AFMarray.to_csv(os.path.join(thispath,'_'.join(['banddiagram_zvac.csv'])), index=False)
Vvac_AFMarray.to_csv(os.path.join(thispath,'_'.join(['banddiagram_Vvac.csv'])), index=False)