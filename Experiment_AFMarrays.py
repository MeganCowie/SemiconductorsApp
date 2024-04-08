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
# p-type:
button_presets = 5
Ec = 1.333346
Ef = 0.4166885
'''


button_presets = 2 # silicon surface
toggle_type, slider_Vg, slider_zins, slider_Eg, slider_epsilonsem, slider_WFmet, slider_EAsem, slider_donor, slider_acceptor, slider_emass, slider_hmass, slider_T, slider_alpha, button_presets, stylen, stylep, disabledn, disabledp = Presets.presets_surface(button_presets,0,0,0,0,0,0,0,0,0,0,0,0,0)

button_presets = 2 #silicon AFM
slider_timesteps, slider_amplitude, slider_resfreq, slider_lag, slider_springconst, slider_tipradius, slider_cantheight, slider_cantarea, slider_Qfactor,geometrybuttons = Presets.presets_afm(button_presets,0,0,0,0,0,0,0,0,0,0)


slider_biassteps = 256
slider_zinssteps = 128
slider_timesteps = 20000

slider_Vg_array = np.array([-8,-7,-6,-4,-3,-2,-1,0,1,2,3,4,5,6,7,8,9,10]) #np.linspace(-10,10,slider_biassteps)
slider_zins = slider_zins
slider_lag = 0

for slider_Vg in slider_Vg_array:

    thispath = "Xsave_AFMarrays_%.1f_%.2f_%.2f_%.2f_%.2f_%.2f_%.2f_%.3f_%.3f_%.1f_%.1f_%.1f_%.0f_%.2f_%.0f_%.0f_%.2f_%.2f_%.3f_%.0f/" % (slider_Vg, slider_zins, slider_alpha, slider_Eg, slider_epsilonsem, slider_WFmet, slider_EAsem, slider_donor, slider_acceptor, slider_emass, slider_hmass, slider_T, slider_amplitude, slider_resfreq, slider_lag, slider_springconst, slider_Qfactor, slider_tipradius, slider_cantheight, slider_cantarea)
    
    if not os.path.exists(thispath):
        os.mkdir(thispath)

        ################################################################################
        # AFMarrays

        # Input values and arrays
        Vg,zins,Eg,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T,sampletype,biassteps,zinssteps,Vg_array,zins_array=Organization_IntermValues.Surface_inputvalues(slider_Vg,slider_zins,slider_alpha,slider_Eg,slider_epsilonsem,slider_WFmet,slider_EAsem,slider_donor,slider_acceptor,slider_emass,slider_hmass,slider_T,slider_biassteps,slider_zinssteps)
        amplitude,frequency,lag,timesteps,tipradius,cantheight,cantarea,time_AFMarray,zins_AFMarray,zinslag_AFMarray=Organization_IntermValues.AFM1_inputvalues(slider_amplitude,slider_resfreq,slider_lag,slider_timesteps,slider_tipradius,slider_cantheight,slider_cantarea, zins)

        # Calculations and results
        NC,NV,Ec,Ev,Ei,Ef,no,po,ni,nb,pb,CPD,LD,Vs,Es,Qs,F,regime, zsem,Vsem,Esem,Qsem, P = Organization_IntermValues.Surface_calculations(Vg,zins,Eg,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T)
        Vs_AFMarray, Es_AFMarray, Qs_AFMarray, F_AFMarray, P_AFMarray = Organization_BuildArrays.AFM_timearrays(time_AFMarray,zins_AFMarray,zinslag_AFMarray,Vg,zins,Na,Nd,epsilon_sem,T,CPD,LD,nb,pb,ni)
        Vscant_AFMarray, Escant_AFMarray, Qscant_AFMarray, Fcant_AFMarray, Pcant_AFMarray = Organization_BuildArrays.AFM_timearrays(time_AFMarray,zins_AFMarray+cantheight,zinslag_AFMarray+cantheight,Vg,zins+cantheight,Na,Nd,epsilon_sem,T,CPD,LD,nb,pb,ni)
        zsem_AFMarray,Vsem_AFMarray,zgap_AFMarray,Vgap_AFMarray,zvac_AFMarray,Vvac_AFMarray,zmet_AFMarray,Vmet_AFMarray,zarray_AFMarray,Qarray_AFMarray,Earray_AFMarray = Organization_BuildArrays.AFM_banddiagramarrays(zins_AFMarray,Vg,T,Nd,Na,WFmet,EAsem,epsilon_sem, ni,nb,pb,Vs,Ec,Ev,Ei,Ef,Eg,CPD)


        # Stack arrays to show two periods
        time_AFMarray = np.hstack((time_AFMarray,time_AFMarray[1:]+2*np.pi/frequency))
        zins_AFMarray = np.hstack((zins_AFMarray,zins_AFMarray[1:]))
        zinslag_AFMarray = np.hstack((zinslag_AFMarray,zinslag_AFMarray[1:]))
        Vs_AFMarray = np.hstack((Vs_AFMarray,Vs_AFMarray[1:]))
        Es_AFMarray = np.hstack((Es_AFMarray,Es_AFMarray[1:]))
        Qs_AFMarray = np.hstack((Qs_AFMarray,Qs_AFMarray[1:]))
        F_AFMarray = np.hstack((F_AFMarray,F_AFMarray[1:]))*np.pi*tipradius**2
        P_AFMarray = np.hstack((P_AFMarray,P_AFMarray[1:]))
        Vscant_AFMarray = np.hstack((Vscant_AFMarray,Vscant_AFMarray[1:]))
        Escant_AFMarray = np.hstack((Escant_AFMarray,Escant_AFMarray[1:]))
        Qscant_AFMarray = np.hstack((Qscant_AFMarray,Qscant_AFMarray[1:]))
        Fcant_AFMarray = np.hstack((Fcant_AFMarray,Fcant_AFMarray[1:]))*cantarea
        Pcant_AFMarray = np.hstack((Pcant_AFMarray,Pcant_AFMarray[1:]))
        zsem_AFMarray = np.vstack((zsem_AFMarray,zsem_AFMarray[1:]))
        Vsem_AFMarray = np.vstack((Vsem_AFMarray,Vsem_AFMarray[1:]))
        zgap_AFMarray = np.vstack((zgap_AFMarray,zgap_AFMarray[1:]))
        Vgap_AFMarray = np.vstack((Vgap_AFMarray,Vgap_AFMarray[1:]))
        zvac_AFMarray = np.vstack((zvac_AFMarray,zvac_AFMarray[1:]))
        Vvac_AFMarray = np.vstack((Vvac_AFMarray,Vvac_AFMarray[1:]))
        zmet_AFMarray = np.vstack((zmet_AFMarray,zmet_AFMarray[1:]))
        Vmet_AFMarray = np.vstack((Vmet_AFMarray,Vmet_AFMarray[1:]))
        zarray_AFMarray = np.vstack((zarray_AFMarray,zarray_AFMarray[1:]))
        Qarray_AFMarray = np.vstack((Qarray_AFMarray,Qarray_AFMarray[1:]))
        Earray_AFMarray = np.vstack((Earray_AFMarray,Earray_AFMarray[1:]))

        Ftot_AFMarray = 0*time_AFMarray
        if 1 in geometrybuttons:
            Ftot_AFMarray+=F_AFMarray
        if 2 in geometrybuttons:
            Ftot_AFMarray+=Fcant_AFMarray

        # Unit conversions
        time_AFMarray = time_AFMarray
        zins_AFMarray = zins_AFMarray*1e9
        Vs_AFMarray = Vs_AFMarray/Physics_Semiconductors.e
        Es_AFMarray = Es_AFMarray
        Qs_AFMarray = Qs_AFMarray*(1e-9)**2
        F_AFMarray = F_AFMarray*1e12
        P_AFMarray = P_AFMarray
        Vscant_AFMarray = Vscant_AFMarray/Physics_Semiconductors.e
        Escant_AFMarray = Escant_AFMarray
        Qscant_AFMarray = Qscant_AFMarray*(1e-9)**2
        Fcant_AFMarray = Fcant_AFMarray*1e12
        Pcant_AFMarray = Pcant_AFMarray
        Ftot_AFMarray = Ftot_AFMarray*1e12

        # Organize arrays for saving
        save_AFMarray_time = pd.DataFrame({'time': [str(x) for x in time_AFMarray]})
        save_AFMarray_zins = pd.DataFrame({'zins': [str(x) for x in zins_AFMarray]})
        save_AFMarray_Vs = pd.DataFrame({'Vs': [str(x) for x in Vs_AFMarray]})
        save_AFMarray_Es = pd.DataFrame({'Es': [str(x) for x in Es_AFMarray]})
        save_AFMarray_Qs = pd.DataFrame({'Qs': [str(x) for x in Qs_AFMarray]})
        save_AFMarray_F = pd.DataFrame({'F': [str(x) for x in F_AFMarray]})
        save_AFMarray_P = pd.DataFrame({'P': [str(x) for x in P_AFMarray]})
        save_AFMarray_Vscant = pd.DataFrame({'Vscant': [str(x) for x in Vscant_AFMarray]})
        save_AFMarray_Escant = pd.DataFrame({'Escant': [str(x) for x in Escant_AFMarray]})
        save_AFMarray_Qscant = pd.DataFrame({'Qscant': [str(x) for x in Qscant_AFMarray]})
        save_AFMarray_Fcant = pd.DataFrame({'Fcant': [str(x) for x in Fcant_AFMarray]})
        save_AFMarray_Pcant = pd.DataFrame({'Pcant': [str(x) for x in Pcant_AFMarray]})
        save_AFMarray_Ftot = pd.DataFrame({'Ftot': [str(x) for x in Ftot_AFMarray]})
        save_AFMarrays = pd.concat([save_AFMarray_time,save_AFMarray_zins,save_AFMarray_Vs,save_AFMarray_Es,save_AFMarray_Qs,save_AFMarray_F,save_AFMarray_P,save_AFMarray_Vscant,save_AFMarray_Escant,save_AFMarray_Qscant,save_AFMarray_Fcant,save_AFMarray_Pcant,save_AFMarray_Ftot], axis=1, join="outer")

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
        zarray_AFMarray = pd.DataFrame(zarray_AFMarray*1e9)
        Qarray_AFMarray = pd.DataFrame(Qarray_AFMarray*1e9)
        Earray_AFMarray = pd.DataFrame(Earray_AFMarray*1e9)


        ################################################################################
        # Save

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
        zarray_AFMarray.to_csv(os.path.join(thispath,'_'.join(['banddiagram_zarray.csv'])), index=False)
        Qarray_AFMarray.to_csv(os.path.join(thispath,'_'.join(['banddiagram_Qarray.csv'])), index=False)
        Earray_AFMarray.to_csv(os.path.join(thispath,'_'.join(['banddiagram_Earray.csv'])), index=False)