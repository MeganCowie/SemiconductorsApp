# Vary the dopant concentration of n-type silicon
import Physics_Semiconductors
import Physics_BandDiagram
import Organization_IntermValues
import Organization_BuildArrays
import numpy as np
import pandas as pd
import os

################################################################################
# Haughton Si values

toggle_type = False
slider_Vg = 0
slider_zins = 6
slider_Eg = 1.1
slider_epsilonsem = 11.7
slider_WFmet = 4.64
slider_EAsem = 4.05
slider_emass = 1.08
slider_hmass = 0.56
slider_donor = 32.7
slider_acceptor = 0
slider_T = 300
slider_alpha = 0.3
stylen = {'color': '#57c5f7'}
stylep = {'color': '#7f7f7f'}
disabledn = False
disabledp = True

slider_amplitude = 6
slider_resfreq = 300000
slider_lag = 0
slider_hop = 0
toggle_RTN = True
toggle_sampletype = False
slider_springconst = 42
slider_Qfactor = 18000
slider_tipradius = 6.25
slider_cantheight = 500
slider_cantarea = 50

slider_biassteps = 10#1024
slider_zinssteps = 1
slider_timesteps = 10#200

#slider_zins = slider_zins+slider_amplitude


################################################################################
# Input values
Vg,zins,Eg,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T,sampletype,biassteps,zinssteps,Vg_array,zins_array=Organization_IntermValues.Surface_inputvalues(slider_Vg,slider_zins,slider_alpha,slider_Eg,slider_epsilonsem,slider_WFmet,slider_EAsem,slider_donor,slider_acceptor,slider_emass,slider_hmass,slider_T,slider_biassteps,slider_zinssteps)

# Calculations and results
NC,NV,Ec,Ev,Ei,Ef,no,po,ni,nb,pb,CPD,LD,Vs,Es,Qs,F,regime, zsem,Vsem,Esem,Qsem, P = Organization_IntermValues.Surface_calculations(Vg,zins,Eg,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T)
Vs_biasarray,F_biasarray,Es_biasarray,Qs_biasarray,P_biasarray = Organization_BuildArrays.Surface_biasarrays(Vg_array,zins,Na,Nd,epsilon_sem,T,CPD,LD,nb,pb,ni)
Vs_zinsarray,F_zinsarray,Es_zinsarray,Qs_zinsarray,P_zinsarray = Organization_BuildArrays.Surface_zinsarrays(zins_array,Vg,Na,Nd,epsilon_sem,T,CPD,LD,nb,pb,ni)
zgap,Vgap, zvac,Vvac, zmet,Vmet, zarray,Earray,Qarray  = Physics_BandDiagram.BandDiagram(Vg,zins,T,Nd,Na,WFmet,EAsem,epsilon_sem, ni,nb,pb,Vs,Ec,Ev,Ef,CPD, zsem,Vsem,Esem,Qsem)

# Unit conversions
zgap = zgap*1e9
Vgap = Vgap/Physics_Semiconductors.e
zvac = zvac*1e9
Vvac = Vvac/Physics_Semiconductors.e
zmet = zmet*1e9
Vmet = Vmet/Physics_Semiconductors.e
zsem = zsem*1e9
Esem = Esem*1e-9
Qsem = Qsem/Physics_Semiconductors.e*(1e-9)**2
Vsem_Ev = (Ev-Vsem)/Physics_Semiconductors.e
Vsem_Ei = (Ei-Vsem)/Physics_Semiconductors.e
Vsem_Ec = (Ec-Vsem)/Physics_Semiconductors.e
Vsem_Ef = 0*zsem+Ef/Physics_Semiconductors.e

# Organize arrays for saving
save_gaparray_z = pd.DataFrame({'zgap': [str(x) for x in zgap]})
save_gaparray_V = pd.DataFrame({'Vgap': [str(x) for x in Vgap]})
save_vacarray_z = pd.DataFrame({'zvac': [str(x) for x in zgap]})
save_vacarray_V = pd.DataFrame({'Vvac': [str(x) for x in Vgap]})
save_metarray_z = pd.DataFrame({'zmet': [str(x) for x in zmet]})
save_metarray_V = pd.DataFrame({'Vmet': [str(x) for x in Vmet]})
save_semarray_z = pd.DataFrame({'zsem': [str(x) for x in zsem]})
save_semarray_Ev = pd.DataFrame({'Vsem_Ev': [str(x) for x in Vsem_Ev]})
save_semarray_Ei = pd.DataFrame({'Vsem_Ei': [str(x) for x in Vsem_Ei]})
save_semarray_Ec = pd.DataFrame({'Vsem_Ec': [str(x) for x in Vsem_Ec]})
save_semarray_Ef = pd.DataFrame({'Vsem_Ef': [str(x) for x in Vsem_Ef]})
save_semarray_E = pd.DataFrame({'Esem': [str(x) for x in Esem]})
save_semarray_Q = pd.DataFrame({'Qsem': [str(x) for x in Qsem]})

save_gaparrays = pd.concat([save_gaparray_z,save_gaparray_V], axis=1, join="outer")
save_vacarrays = pd.concat([save_vacarray_z,save_vacarray_V], axis=1, join="outer")
save_metarrays = pd.concat([save_metarray_z,save_metarray_V], axis=1, join="outer")
save_semarrays = pd.concat([save_semarray_z,save_semarray_Ev,save_semarray_Ei,save_semarray_Ec,save_semarray_Ef,save_semarray_E,save_semarray_Q], axis=1, join="outer")
    

################################################################################
# Save

thispath = "Xsave_Si_BandDiagram_%.1f_%.2f_%.2f_%.2f_%.2f_%.2f_%.3f_%.3f_%.1f_%.1f_%.0f_%.0f_%.0f_%.0f_%.0f_%.0f_%.2f/" % (slider_Vg, slider_zins, slider_Eg, slider_epsilonsem, slider_WFmet, slider_EAsem, slider_donor, slider_acceptor, slider_emass, slider_hmass, slider_T, slider_amplitude, slider_resfreq, slider_lag, slider_springconst, slider_Qfactor, slider_tipradius)
thisname = "%.1f_%.2f_%.2f_%.2f_%.2f_%.2f_%.3f_%.3f_%.1f_%.1f_%.0f_%.0f_%.0f_%.0f_%.0f_%.0f_%.2f.csv" % (slider_Vg, slider_zins, slider_Eg, slider_epsilonsem, slider_WFmet, slider_EAsem, slider_donor, slider_acceptor, slider_emass, slider_hmass, slider_T, slider_amplitude, slider_resfreq, slider_lag, slider_springconst, slider_Qfactor, slider_tipradius)

if not os.path.exists(thispath):
    os.mkdir(thispath)

save_gaparrays.to_csv(os.path.join(thispath,'_'.join(['gaparrays_Vs',thisname])), index=False)
save_vacarrays.to_csv(os.path.join(thispath,'_'.join(['vacarrays_Vs',thisname])), index=False)
save_metarrays.to_csv(os.path.join(thispath,'_'.join(['metarrays_Vs',thisname])), index=False)
save_semarrays.to_csv(os.path.join(thispath,'_'.join(['semarrays_Vs',thisname])), index=False)
