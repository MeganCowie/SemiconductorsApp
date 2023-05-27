# Vary the dopant concentration of n-type silicon
import Presets
import Physics_Semiconductors
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
#CPD = slider_WFmet - (slider_EAsem + (Ec-Ef)) # J

button_presets = 2 #silicon AFM
slider_timesteps, slider_amplitude, slider_resfreq, slider_lag, slider_springconst, slider_tipradius, slider_cantheight, slider_cantarea, slider_Qfactor,geometrybuttons = Presets.presets_afm(button_presets,0,0,0,0,0,0,0,0,0,0)

slider_biassteps = 1024
slider_zinssteps = 1#512
slider_timesteps = 200

slider_lag = 0

slider_zins_OG = 12+6
slider_Vg_OG = 0


slider_donor = np.log10(10**15*  1.00*10**19)

################################################################################
# Inputs

slider_zins_array = np.array([slider_zins_OG])
slider_Vg_array = np.array([])

experiment = 'single'
#experiment = 'Nd'
#experiment = 'Na'
#experiment = 'emass'
#experiment = 'hmass'
#experiment = 'Eg'
#experiment = 'epsilonsem'
#experiment = 'amplitude'
#experiment = 'lag'

if experiment=='single':
    ExperimentArray =  np.linspace(1,1,1)
elif experiment=='Nd':
    ExperimentArray =  np.linspace(33,33,1)
elif experiment=='Na':
    ExperimentArray =  np.linspace(33,33,1)
elif experiment=='emass':
    ExperimentArray =  np.linspace(0.1,1.2,23)
elif experiment=='hmass':
    ExperimentArray =  np.linspace(0.1,1.2,23)
elif experiment=='Eg':
    ExperimentArray =  np.linspace(0.2,1.5,27)
elif experiment=='epsilonsem':
    ExperimentArray =  np.linspace(1,20,39)
elif experiment=='amplitude':
    ExperimentArray =  np.linspace(2,30,29)
elif experiment=='zins':
    ExperimentArray =  np.linspace(4,20,17)
elif experiment=='lag':
    ExperimentArray =  np.linspace(125,174,25)

################################################################################
# biasarrays

slider_Vg = slider_Vg_OG
slider_zins = slider_zins_OG

for slider_zins in slider_zins_array:

    print('\n'+'biasarrays')
    print('zins = ' + str(slider_zins))

    ##################
    # Initialize arrays

    Vg_array = np.linspace(-10,10,slider_biassteps)*Physics_Semiconductors.e #J

    save_Vs_biasarrays = pd.DataFrame({"Vg_array": [str(x) for x in Vg_array/Physics_Semiconductors.e]})
    save_F_biasarrays = pd.DataFrame({"Vg_array": [str(x) for x in Vg_array/Physics_Semiconductors.e]})
    save_P_biasarrays = pd.DataFrame({"Vg_array": [str(x) for x in Vg_array/Physics_Semiconductors.e]})
    save_Vscant_biasarrays = pd.DataFrame({"Vg_array": [str(x) for x in Vg_array/Physics_Semiconductors.e]})
    save_Fcant_biasarrays = pd.DataFrame({"Vg_array": [str(x) for x in Vg_array/Physics_Semiconductors.e]})
    save_Pcant_biasarrays = pd.DataFrame({"Vg_array": [str(x) for x in Vg_array/Physics_Semiconductors.e]})
    save_Ftot_biasarrays = pd.DataFrame({"Vg_array": [str(x) for x in Vg_array/Physics_Semiconductors.e]})
    save_Es_biasarrays = pd.DataFrame({"Vg_array": [str(x) for x in Vg_array/Physics_Semiconductors.e]})
    save_Qs_biasarrays = pd.DataFrame({"Vg_array": [str(x) for x in Vg_array/Physics_Semiconductors.e]})
    save_df_biasarrays = pd.DataFrame({"Vg_array": [str(x) for x in Vg_array/Physics_Semiconductors.e]})
    save_dg_biasarrays = pd.DataFrame({"Vg_array": [str(x) for x in Vg_array/Physics_Semiconductors.e]})

    ##################
    # Vary experimental parameter

    for index in range(len(ExperimentArray)):

        if experiment=='single':
            pass 
        elif experiment=='Nd':
            slider_donor = ExperimentArray[index]
        elif experiment=='Na':
            slider_acceptor = ExperimentArray[index]
        elif experiment=='emass':
            mn = ExperimentArray[index]*Physics_Semiconductors.me #kg
        elif experiment=='hmass':
            mp = ExperimentArray[index]*Physics_Semiconductors.me #kg
        elif experiment=='Eg':
            Eg = ExperimentArray[index]*Physics_Semiconductors.e #J
        elif experiment=='epsilonsem':
            epsilon_sem = ExperimentArray[index] #dimensionless
        elif experiment=='amplitude':
            slider_amplitude = ExperimentArray[index]  #nm
        elif experiment=='lag':
            slider_lag = ExperimentArray[index] #ns
        else:
            print('Error: Experiment not defined.')


        # Input values and arrays
        Vg,zins,Eg,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T,sampletype,biassteps,zinssteps,Vg_array,zins_array=Organization_IntermValues.Surface_inputvalues(slider_Vg,slider_zins,slider_alpha,slider_Eg,slider_epsilonsem,slider_WFmet,slider_EAsem,slider_donor,slider_acceptor,slider_emass,slider_hmass,slider_T,slider_biassteps,slider_zinssteps)
        amplitude,frequency,lag,timesteps,tipradius,cantheight,cantarea,time_AFMarray,zins_AFMarray,zinslag_AFMarray=Organization_IntermValues.AFM1_inputvalues(slider_amplitude,slider_resfreq,slider_lag,slider_timesteps,slider_tipradius,slider_cantheight,slider_cantarea, zins)
        springconst,Qfactor=Organization_IntermValues.AFM2_inputvalues(slider_springconst,slider_Qfactor)

        # Calculations and results
        NC,NV,Ec,Ev,Ei,Ef,no,po,ni,nb,pb,CPD,LD,Vs,Es,Qs,F,regime, zsem,Vsem,Esem,Qsem, P = Organization_IntermValues.Surface_calculations(Vg,zins,Eg,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T)
        Vs_biasarray,F_biasarray,P_biasarray,Vscant_biasarray,Fcant_biasarray,Pcant_biasarray,Es_biasarray,Qs_biasarray,df_biasarray,dg_biasarray = Organization_BuildArrays.All_biasarrays(Vg_array,zins,Na,Nd,epsilon_sem,T,CPD,LD,nb,pb,ni,frequency,springconst,amplitude,Qfactor,tipradius,time_AFMarray,zins_AFMarray,zinslag_AFMarray,cantheight,cantarea,timesteps,geometrybuttons)

        # Account for alpha
        Vg = slider_Vg*Physics_Semiconductors.e #J
        Vg_array = np.linspace(-10,10,biassteps)*Physics_Semiconductors.e #J

        # Unit conversions
        Vs_biasarray = Vs_biasarray/Physics_Semiconductors.e
        F_biasarray = F_biasarray*np.pi*tipradius**2*1e12
        P_biasarray = P_biasarray*1e9
        Vscant_biasarray = Vscant_biasarray/Physics_Semiconductors.e
        Fcant_biasarray = Fcant_biasarray*cantarea*1e12
        Pcant_biasarray = Pcant_biasarray*1e9
        Es_biasarray = Es_biasarray*1e-9
        Qs_biasarray = Qs_biasarray/Physics_Semiconductors.e*(1e-9)**2
        df_biasarray = df_biasarray
        dg_biasarray = dg_biasarray

        Ftot_biasarray = 0*Vg_array
        if 1 in geometrybuttons:
            Ftot_biasarray+=F_biasarray
        if 2 in geometrybuttons:
            Ftot_biasarray+=Fcant_biasarray

        # Organize arrays for saving
        save_Vs_biasarray = pd.DataFrame({str(ExperimentArray[index]): [str(x) for x in Vs_biasarray]})
        save_F_biasarray = pd.DataFrame({str(ExperimentArray[index]): [str(x) for x in F_biasarray]})
        save_P_biasarray = pd.DataFrame({str(ExperimentArray[index]): [str(x) for x in P_biasarray]})
        save_Vscant_biasarray = pd.DataFrame({str(ExperimentArray[index]): [str(x) for x in Vscant_biasarray]})
        save_Fcant_biasarray = pd.DataFrame({str(ExperimentArray[index]): [str(x) for x in Fcant_biasarray]})
        save_Pcant_biasarray = pd.DataFrame({str(ExperimentArray[index]): [str(x) for x in Pcant_biasarray]})
        save_Ftot_biasarray = pd.DataFrame({str(ExperimentArray[index]): [str(x) for x in Ftot_biasarray]})
        save_Es_biasarray = pd.DataFrame({str(ExperimentArray[index]): [str(x) for x in Es_biasarray]})
        save_Qs_biasarray = pd.DataFrame({str(ExperimentArray[index]): [str(x) for x in Qs_biasarray]})
        save_df_biasarray = pd.DataFrame({str(ExperimentArray[index]): [str(x) for x in df_biasarray]})
        save_dg_biasarray = pd.DataFrame({str(ExperimentArray[index]): [str(x) for x in dg_biasarray]})

        save_Vs_biasarrays = pd.concat([save_Vs_biasarrays,save_Vs_biasarray], axis=1, join="outer")
        save_F_biasarrays = pd.concat([save_F_biasarrays,save_F_biasarray], axis=1, join="outer")
        save_P_biasarrays = pd.concat([save_P_biasarrays,save_P_biasarray], axis=1, join="outer")
        save_Vscant_biasarrays = pd.concat([save_Vscant_biasarrays,save_Vscant_biasarray], axis=1, join="outer")
        save_Fcant_biasarrays = pd.concat([save_Fcant_biasarrays,save_Fcant_biasarray], axis=1, join="outer")
        save_Pcant_biasarrays = pd.concat([save_Pcant_biasarrays,save_Pcant_biasarray], axis=1, join="outer")
        save_Ftot_biasarrays = pd.concat([save_Ftot_biasarrays,save_Ftot_biasarray], axis=1, join="outer")
        save_Es_biasarrays = pd.concat([save_Es_biasarrays,save_Es_biasarray], axis=1, join="outer")
        save_Qs_biasarrays = pd.concat([save_Qs_biasarrays,save_Qs_biasarray], axis=1, join="outer")
        save_df_biasarrays = pd.concat([save_df_biasarrays,save_df_biasarray], axis=1, join="outer")
        save_dg_biasarrays = pd.concat([save_dg_biasarrays,save_dg_biasarray], axis=1, join="outer")

        print(index+1,'/', len(ExperimentArray))

    ##################
    # Save

    thispath = "Xsave_Sweeps_%s_%.1f_%.2f_%.2f_%.2f_%.2f_%.2f_%.2f_%.3f_%.3f_%.1f_%.1f_%.1f_%.0f_%.2f_%.0f_%.0f_%.2f_%.2f_%.3f_%.0f/" % (experiment,slider_Vg, slider_zins, slider_alpha, slider_Eg, slider_epsilonsem, slider_WFmet, slider_EAsem, slider_donor, slider_acceptor, slider_emass, slider_hmass, slider_T, slider_amplitude, slider_resfreq, slider_lag, slider_springconst, slider_Qfactor, slider_tipradius, slider_cantheight, slider_cantarea)

    if not os.path.exists(thispath):
        os.mkdir(thispath)

    save_Vs_biasarrays.to_csv(os.path.join(thispath,'_'.join(['biasarray_Vs.csv'])), index=False)
    save_F_biasarrays.to_csv(os.path.join(thispath,'_'.join(['biasarray_F.csv'])), index=False)
    save_P_biasarrays.to_csv(os.path.join(thispath,'_'.join(['biasarray_P.csv'])), index=False)
    save_Vscant_biasarrays.to_csv(os.path.join(thispath,'_'.join(['biasarray_Vscant.csv'])), index=False)
    save_Fcant_biasarrays.to_csv(os.path.join(thispath,'_'.join(['biasarray_Fcant.csv'])), index=False)
    save_Pcant_biasarrays.to_csv(os.path.join(thispath,'_'.join(['biasarray_Pcant.csv'])), index=False)
    save_Ftot_biasarrays.to_csv(os.path.join(thispath,'_'.join(['biasarray_Ftot.csv'])), index=False)
    save_Es_biasarrays.to_csv(os.path.join(thispath,'_'.join(['biasarray_Es.csv'])), index=False)
    save_Qs_biasarrays.to_csv(os.path.join(thispath,'_'.join(['biasarray_Qs.csv'])), index=False)
    save_df_biasarrays.to_csv(os.path.join(thispath,'_'.join(['biasarray_df.csv'])), index=False)
    save_dg_biasarrays.to_csv(os.path.join(thispath,'_'.join(['biasarray_dg.csv'])), index=False)



################################################################################
# zinsarrays

slider_Vg = slider_Vg_OG
slider_zins = slider_zins_OG

for slider_Vg in slider_Vg_array:

    print('\n'+'zinsarrays')
    print('Vg = ' + str(slider_Vg))

    ##################
    # Initialize arrays

    zins_array = np.linspace(0.01,25,slider_zinssteps)*1e-9 #m

    save_Vs_zinsarrays = pd.DataFrame({"zins_array": [str(x) for x in zins_array*1e9]})
    save_F_zinsarrays = pd.DataFrame({"zins_array": [str(x) for x in zins_array*1e9]})
    save_P_zinsarrays = pd.DataFrame({"zins_array": [str(x) for x in zins_array*1e9]})
    save_Vscant_zinsarrays = pd.DataFrame({"zins_array": [str(x) for x in zins_array*1e9]})
    save_Fcant_zinsarrays = pd.DataFrame({"zins_array": [str(x) for x in zins_array*1e9]})
    save_Pcant_zinsarrays = pd.DataFrame({"zins_array": [str(x) for x in zins_array*1e9]})
    save_Ftot_zinsarrays = pd.DataFrame({"zins_array": [str(x) for x in zins_array*1e9]})
    save_Es_zinsarrays = pd.DataFrame({"zins_array": [str(x) for x in zins_array*1e9]})
    save_Qs_zinsarrays = pd.DataFrame({"zins_array": [str(x) for x in zins_array*1e9]})
    save_df_zinsarrays = pd.DataFrame({"zins_array": [str(x) for x in zins_array*1e9]})
    save_dg_zinsarrays = pd.DataFrame({"zins_array": [str(x) for x in zins_array*1e9]})

    ##################
    # Vary experimental parameter

    for index in range(len(ExperimentArray)):

        if experiment=='single':
            pass
        elif experiment=='Nd':
            slider_donor = ExperimentArray[index]
        elif experiment=='Na':
            slider_acceptor = ExperimentArray[index]
        elif experiment=='emass':
            mn = ExperimentArray[index]*Physics_Semiconductors.me #kg
        elif experiment=='hmass':
            mp = ExperimentArray[index]*Physics_Semiconductors.me #kg
        elif experiment=='Eg':
            Eg = ExperimentArray[index]*Physics_Semiconductors.e #J
        elif experiment=='epsilonsem':
            epsilon_sem = ExperimentArray[index] #dimensionless
        elif experiment=='amplitude':
            slider_amplitude = ExperimentArray[index]  #nm
        elif experiment=='lag':
            slider_lag = ExperimentArray[index] #ns
        else:
            print('Error: Experiment not defined.')


        # Input values and arrays
        Vg,zins,Eg,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T,sampletype,biassteps,zinssteps,Vg_array,zins_array=Organization_IntermValues.Surface_inputvalues(slider_Vg,slider_zins,slider_alpha,slider_Eg,slider_epsilonsem,slider_WFmet,slider_EAsem,slider_donor,slider_acceptor,slider_emass,slider_hmass,slider_T,slider_biassteps,slider_zinssteps)
        amplitude,frequency,lag,timesteps,tipradius,cantheight,cantarea,time_AFMarray,zins_AFMarray,zinslag_AFMarray=Organization_IntermValues.AFM1_inputvalues(slider_amplitude,slider_resfreq,slider_lag,slider_timesteps,slider_tipradius,slider_cantheight,slider_cantarea, zins)
        springconst,Qfactor=Organization_IntermValues.AFM2_inputvalues(slider_springconst,slider_Qfactor)

        # Calculations and results
        NC,NV,Ec,Ev,Ei,Ef,no,po,ni,nb,pb,CPD,LD,Vs,Es,Qs,F,regime, zsem,Vsem,Esem,Qsem, P = Organization_IntermValues.Surface_calculations(Vg,zins,Eg,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T)
        Vs_zinsarray,F_zinsarray,P_zinsarray,Vscant_zinsarray,Fcant_zinsarray,Pcant_zinsarray,Es_zinsarray,Qs_zinsarray,df_zinsarray,dg_zinsarray  = Organization_BuildArrays.All_zinsarrays(Vg,zins,zins_array,Na,Nd,epsilon_sem,T,CPD,LD,nb,pb,ni,frequency,springconst,amplitude,Qfactor,tipradius,time_AFMarray,zins_AFMarray,zinslag_AFMarray,cantheight,cantarea,timesteps,geometrybuttons)

        # Account for alpha
        Vg = slider_Vg*Physics_Semiconductors.e #J
        Vg_array = np.linspace(-10,10,biassteps)*Physics_Semiconductors.e #J

        # Unit conversions
        Vs_zinsarray = Vs_zinsarray/Physics_Semiconductors.e
        F_zinsarray = F_zinsarray*np.pi*tipradius**2*1e12
        P_zinsarray = P_zinsarray*1e9
        Vscant_zinsarray = Vscant_zinsarray/Physics_Semiconductors.e
        Fcant_zinsarray = Fcant_zinsarray*cantarea*1e12
        Pcant_zinsarray = Pcant_zinsarray*1e9
        Es_zinsarray = Es_zinsarray*1e-9
        Qs_zinsarray = Qs_zinsarray/Physics_Semiconductors.e*(1e-9)**2
        df_zinsarray = df_zinsarray
        dg_zinsarray = dg_zinsarray

        Ftot_zinsarray = 0*zins_array
        if 1 in geometrybuttons:
            Ftot_zinsarray+=F_zinsarray
        if 2 in geometrybuttons:
            Ftot_zinsarray+=Fcant_zinsarray

        # Organize arrays for saving
        save_Vs_zinsarray = pd.DataFrame({str(ExperimentArray[index]): [str(x) for x in Vs_zinsarray]})
        save_F_zinsarray = pd.DataFrame({str(ExperimentArray[index]): [str(x) for x in F_zinsarray]})
        save_P_zinsarray = pd.DataFrame({str(ExperimentArray[index]): [str(x) for x in P_zinsarray]})
        save_Vscant_zinsarray = pd.DataFrame({str(ExperimentArray[index]): [str(x) for x in Vscant_zinsarray]})
        save_Fcant_zinsarray = pd.DataFrame({str(ExperimentArray[index]): [str(x) for x in Fcant_zinsarray]})
        save_Pcant_zinsarray = pd.DataFrame({str(ExperimentArray[index]): [str(x) for x in Pcant_zinsarray]})
        save_Ftot_zinsarray = pd.DataFrame({str(ExperimentArray[index]): [str(x) for x in Ftot_zinsarray]})
        save_Es_zinsarray = pd.DataFrame({str(ExperimentArray[index]): [str(x) for x in Es_zinsarray]})
        save_Qs_zinsarray = pd.DataFrame({str(ExperimentArray[index]): [str(x) for x in Qs_zinsarray]})
        save_df_zinsarray = pd.DataFrame({str(ExperimentArray[index]): [str(x) for x in df_zinsarray]})
        save_dg_zinsarray = pd.DataFrame({str(ExperimentArray[index]): [str(x) for x in dg_zinsarray]})

        save_Vs_zinsarrays = pd.concat([save_Vs_zinsarrays,save_Vs_zinsarray], axis=1, join="outer")
        save_F_zinsarrays = pd.concat([save_F_zinsarrays,save_F_zinsarray], axis=1, join="outer")
        save_P_zinsarrays = pd.concat([save_P_zinsarrays,save_P_zinsarray], axis=1, join="outer")
        save_Vscant_zinsarrays = pd.concat([save_Vscant_zinsarrays,save_Vscant_zinsarray], axis=1, join="outer")
        save_Fcant_zinsarrays = pd.concat([save_Fcant_zinsarrays,save_Fcant_zinsarray], axis=1, join="outer")
        save_Pcant_zinsarrays = pd.concat([save_Pcant_zinsarrays,save_Pcant_zinsarray], axis=1, join="outer")
        save_Ftot_zinsarrays = pd.concat([save_Ftot_zinsarrays,save_Ftot_zinsarray], axis=1, join="outer")
        save_Es_zinsarrays = pd.concat([save_Es_zinsarrays,save_Es_zinsarray], axis=1, join="outer")
        save_Qs_zinsarrays = pd.concat([save_Qs_zinsarrays,save_Qs_zinsarray], axis=1, join="outer")
        save_df_zinsarrays = pd.concat([save_df_zinsarrays,save_df_zinsarray], axis=1, join="outer")
        save_dg_zinsarrays = pd.concat([save_dg_zinsarrays,save_dg_zinsarray], axis=1, join="outer")

        print(index+1,'/', len(ExperimentArray))

    ##################
    # Save

    thispath = "Xsave_Sweeps_%s_%.1f_%.2f_%.2f_%.2f_%.2f_%.2f_%.2f_%.3f_%.3f_%.1f_%.1f_%.1f_%.0f_%.2f_%.0f_%.0f_%.2f_%.2f_%.3f_%.0f/" % (experiment,slider_Vg, slider_zins, slider_alpha, slider_Eg, slider_epsilonsem, slider_WFmet, slider_EAsem, slider_donor, slider_acceptor, slider_emass, slider_hmass, slider_T, slider_amplitude, slider_resfreq, slider_lag, slider_springconst, slider_Qfactor, slider_tipradius, slider_cantheight, slider_cantarea)

    if not os.path.exists(thispath):
        os.mkdir(thispath)

    save_Vs_zinsarrays.to_csv(os.path.join(thispath,'_'.join(['zinsarray_Vs.csv'])), index=False)
    save_F_zinsarrays.to_csv(os.path.join(thispath,'_'.join(['zinsarray_F.csv'])), index=False)
    save_P_zinsarrays.to_csv(os.path.join(thispath,'_'.join(['zinsarray_P.csv'])), index=False)
    save_Vscant_zinsarrays.to_csv(os.path.join(thispath,'_'.join(['zinsarray_Vscant.csv'])), index=False)
    save_Fcant_zinsarrays.to_csv(os.path.join(thispath,'_'.join(['zinsarray_Fcant.csv'])), index=False)
    save_Pcant_zinsarrays.to_csv(os.path.join(thispath,'_'.join(['zinsarray_Pcant.csv'])), index=False)
    save_Ftot_zinsarrays.to_csv(os.path.join(thispath,'_'.join(['zinsarray_Ftot.csv'])), index=False)
    save_Es_zinsarrays.to_csv(os.path.join(thispath,'_'.join(['zinsarray_Es.csv'])), index=False)
    save_Qs_zinsarrays.to_csv(os.path.join(thispath,'_'.join(['zinsarray_Qs.csv'])), index=False)
    save_df_zinsarrays.to_csv(os.path.join(thispath,'_'.join(['zinsarray_df.csv'])), index=False)
    save_dg_zinsarrays.to_csv(os.path.join(thispath,'_'.join(['zinsarray_dg.csv'])), index=False)
