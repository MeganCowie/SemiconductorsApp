# Vary the dopant concentration of n-type silicon
import Physics_Semiconductors
import Organization_IntermValues
import Organization_BuildArrays
import numpy as np
import pandas as pd
import os


################################################################################
# Haughton Si values

toggle_type = False
slider_Vg_OG = 0
slider_zins_OG = 6
slider_Eg = 1.1
slider_epsilonsem = 11.7
slider_WFmet = 4.50
slider_EAsem = 4.05
slider_emass = 1.08
slider_hmass = 0.56
slider_donor = 30
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
slider_cantheight = 2.1
slider_cantarea = 3750

slider_biassteps = 101
slider_zinssteps = 79
slider_timesteps = 200

################################################################################
# Inputs

slider_zins_array = np.array([slider_zins_OG,slider_zins_OG+slider_amplitude])
slider_Vg_array = np.array([-9,-6,-3,0,3,6,9])

experiment = 'Nd'
#experiment = 'emass'
#experiment = 'hmass'
#experiment = 'Eg'
#experiment = 'epsilonsem'
#experiment = 'amplitude'
#experiment = 'zins'
#experiment = 'lag'

if experiment=='Nd':
    ExperimentArray =  np.linspace(30,36,121)
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
    ExperimentArray =  np.linspace(0,8,161)


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
    save_Es_biasarrays = pd.DataFrame({"Vg_array": [str(x) for x in Vg_array/Physics_Semiconductors.e]})
    save_Qs_biasarrays = pd.DataFrame({"Vg_array": [str(x) for x in Vg_array/Physics_Semiconductors.e]})
    save_P_biasarrays = pd.DataFrame({"Vg_array": [str(x) for x in Vg_array/Physics_Semiconductors.e]})
    save_df_biasarrays = pd.DataFrame({"Vg_array": [str(x) for x in Vg_array/Physics_Semiconductors.e]})
    save_dg_biasarrays = pd.DataFrame({"Vg_array": [str(x) for x in Vg_array/Physics_Semiconductors.e]})

    ##################
    # Vary experimental parameter

    for index in range(len(ExperimentArray)):

        if experiment=='Nd':
            slider_donor = ExperimentArray[index]
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
        elif experiment=='zins':
            zins = ExperimentArray[index]*1e-9 #m
        elif experiment=='lag':
            slider_lag = ExperimentArray[index] #ns
        else:
            print('Error: Experiment not defined.')


        # Input values and arrays
        Vg,zins,Eg,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T,sampletype,biassteps,zinssteps,Vg_array,zins_array=Organization_IntermValues.Surface_inputvalues(slider_Vg,slider_zins,slider_alpha,slider_Eg,slider_epsilonsem,slider_WFmet,slider_EAsem,slider_donor,slider_acceptor,slider_emass,slider_hmass,slider_T,slider_biassteps,slider_zinssteps)
        amplitude,frequency,lag,timesteps,time_AFMarray,zins_AFMarray,zinslag_AFMarray=Organization_IntermValues.AFM1_inputvalues(slider_amplitude,slider_resfreq,slider_lag,slider_timesteps,zins)
        springconst,Qfactor,tipradius,cantheight,cantarea=Organization_IntermValues.AFM2_inputvalues(slider_springconst,slider_Qfactor,slider_tipradius,slider_cantheight,slider_cantarea)

        # Calculations and results
        NC,NV,Ec,Ev,Ei,Ef,no,po,ni,nb,pb,CPD,LD,Vs,Es,Qs,F,regime, zsem,Vsem,Esem,Qsem, P = Organization_IntermValues.Surface_calculations(Vg,zins,Eg,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T)
        Vs_biasarray,F_biasarray,Es_biasarray,Qs_biasarray,P_biasarray,df_biasarray,dg_biasarray = Organization_BuildArrays.All_biasarrays(Vg_array,zins,Na,Nd,epsilon_sem,T,CPD,LD,nb,pb,ni,frequency,springconst,amplitude,Qfactor,tipradius,cantheight,cantarea,time_AFMarray,zinslag_AFMarray)

        # Unit conversions
        Vs_biasarray = Vs_biasarray/Physics_Semiconductors.e
        F_biasarray = F_biasarray*(1e-9)**2*1e12
        Es_biasarray = Es_biasarray*1e-9
        Qs_biasarray = Qs_biasarray/Physics_Semiconductors.e*(1e-9)**2
        P_biasarray = P_biasarray*1e9
        df_biasarray = df_biasarray
        dg_biasarray = dg_biasarray

        # Organize arrays for saving
        save_Vs_biasarray = pd.DataFrame({str(ExperimentArray[index]): [str(x) for x in Vs_biasarray]})
        save_F_biasarray = pd.DataFrame({str(ExperimentArray[index]): [str(x) for x in F_biasarray]})
        save_Es_biasarray = pd.DataFrame({str(ExperimentArray[index]): [str(x) for x in Es_biasarray]})
        save_Qs_biasarray = pd.DataFrame({str(ExperimentArray[index]): [str(x) for x in Qs_biasarray]})
        save_P_biasarray = pd.DataFrame({str(ExperimentArray[index]): [str(x) for x in P_biasarray]})
        save_df_biasarray = pd.DataFrame({str(ExperimentArray[index]): [str(x) for x in df_biasarray]})
        save_dg_biasarray = pd.DataFrame({str(ExperimentArray[index]): [str(x) for x in dg_biasarray]})

        save_Vs_biasarrays = pd.concat([save_Vs_biasarrays,save_Vs_biasarray], axis=1, join="outer")
        save_F_biasarrays = pd.concat([save_F_biasarrays,save_F_biasarray], axis=1, join="outer")
        save_Es_biasarrays = pd.concat([save_Es_biasarrays,save_Es_biasarray], axis=1, join="outer")
        save_Qs_biasarrays = pd.concat([save_Qs_biasarrays,save_Qs_biasarray], axis=1, join="outer")
        save_P_biasarrays = pd.concat([save_P_biasarrays,save_P_biasarray], axis=1, join="outer")
        save_df_biasarrays = pd.concat([save_df_biasarrays,save_df_biasarray], axis=1, join="outer")
        save_dg_biasarrays = pd.concat([save_dg_biasarrays,save_dg_biasarray], axis=1, join="outer")

        print(index+1,'/', len(ExperimentArray))

    ##################
    # Save

    thispath = "Xsave_Si_Experiment_AFMarrays/" 
    thisname = "%.0f_%.2f_%.2f_%.2f_%.2f_%.2f_%.2f_%.2f_%.1f_%.1f_%.0f_%.0f_%.0f_%.2f_%.0f_%.0f_%.2f_%.2f_%.3f_%.0f.csv" % (slider_Vg, slider_zins, slider_Eg, slider_epsilonsem, slider_WFmet, slider_EAsem, slider_donor, slider_acceptor, slider_emass, slider_hmass, slider_T, slider_amplitude, slider_resfreq, slider_lag, slider_springconst, slider_Qfactor, slider_tipradius, slider_alpha, slider_cantheight, slider_cantarea)

    if not os.path.exists(thispath):
        os.mkdir(thispath)

    save_Vs_biasarrays.to_csv(os.path.join(thispath,'_'.join(['biasarray_Vs',thisname])), index=False)
    save_F_biasarrays.to_csv(os.path.join(thispath,'_'.join(['biasarray_F',thisname])), index=False)
    save_Es_biasarrays.to_csv(os.path.join(thispath,'_'.join(['biasarray_Es',thisname])), index=False)
    save_Qs_biasarrays.to_csv(os.path.join(thispath,'_'.join(['biasarray_Qs',thisname])), index=False)
    save_P_biasarrays.to_csv(os.path.join(thispath,'_'.join(['biasarray_P',thisname])), index=False)
    save_df_biasarrays.to_csv(os.path.join(thispath,'_'.join(['biasarray_df',thisname])), index=False)
    save_dg_biasarrays.to_csv(os.path.join(thispath,'_'.join(['biasarray_dg',thisname])), index=False)



################################################################################
# zinsarrays

slider_Vg = slider_Vg_OG
slider_zins = slider_zins_OG

for slider_Vg in slider_Vg_array:

    print('\n'+'zinsarrays')
    print('Vg = ' + str(slider_Vg))

    ##################
    # Initialize arrays

    zins_array = np.linspace(0.5,20,slider_zinssteps)*1e-9 #m

    save_Vs_zinsarrays = pd.DataFrame({"zins_array": [str(x) for x in zins_array*1e9]})
    save_F_zinsarrays = pd.DataFrame({"zins_array": [str(x) for x in zins_array*1e9]})
    save_Es_zinsarrays = pd.DataFrame({"zins_array": [str(x) for x in zins_array*1e9]})
    save_Qs_zinsarrays = pd.DataFrame({"zins_array": [str(x) for x in zins_array*1e9]})
    save_P_zinsarrays = pd.DataFrame({"zins_array": [str(x) for x in zins_array*1e9]})
    save_df_zinsarrays = pd.DataFrame({"zins_array": [str(x) for x in zins_array*1e9]})
    save_dg_zinsarrays = pd.DataFrame({"zins_array": [str(x) for x in zins_array*1e9]})

    ##################
    # Vary experimental parameter

    for index in range(len(ExperimentArray)):

        if experiment=='Nd':
            slider_donor = ExperimentArray[index]
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
        elif experiment=='zins':
            zins = ExperimentArray[index]*1e-9 #m
        elif experiment=='lag':
            slider_lag = ExperimentArray[index] #ns
        else:
            print('Error: Experiment not defined.')


        # Input values and arrays
        Vg,zins,Eg,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T,sampletype,biassteps,zinssteps,Vg_array,zins_array=Organization_IntermValues.Surface_inputvalues(slider_Vg,slider_zins,slider_alpha,slider_Eg,slider_epsilonsem,slider_WFmet,slider_EAsem,slider_donor,slider_acceptor,slider_emass,slider_hmass,slider_T,slider_biassteps,slider_zinssteps)
        amplitude,frequency,lag,timesteps,time_AFMarray,zins_AFMarray,zinslag_AFMarray=Organization_IntermValues.AFM1_inputvalues(slider_amplitude,slider_resfreq,slider_lag,slider_timesteps,zins)
        springconst,Qfactor,tipradius,cantheight,cantarea=Organization_IntermValues.AFM2_inputvalues(slider_springconst,slider_Qfactor,slider_tipradius,slider_cantheight,slider_cantarea)

        # Calculations and results
        NC,NV,Ec,Ev,Ei,Ef,no,po,ni,nb,pb,CPD,LD,Vs,Es,Qs,F,regime, zsem,Vsem,Esem,Qsem, P = Organization_IntermValues.Surface_calculations(Vg,zins,Eg,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T)
        Vs_zinsarray,F_zinsarray,Es_zinsarray,Qs_zinsarray,P_zinsarray,df_zinsarray,dg_zinsarray = Organization_BuildArrays.All_zinsarrays(Vg,zins,zins_array,Na,Nd,epsilon_sem,T,CPD,LD,nb,pb,ni,frequency,springconst,amplitude,Qfactor,tipradius,cantheight,cantarea,time_AFMarray,zinslag_AFMarray)

        # Unit conversions
        Vs_zinsarray = Vs_zinsarray/Physics_Semiconductors.e
        F_zinsarray = F_zinsarray*(1e-9)**2*1e12
        Es_zinsarray = Es_zinsarray*1e-9
        Qs_zinsarray = Qs_zinsarray/Physics_Semiconductors.e*(1e-9)**2
        P_zinsarray = P_zinsarray*1e9
        df_zinsarray = df_zinsarray
        dg_zinsarray = dg_zinsarray

        # Organize arrays for saving
        save_Vs_zinsarray = pd.DataFrame({str(ExperimentArray[index]): [str(x) for x in Vs_zinsarray]})
        save_F_zinsarray = pd.DataFrame({str(ExperimentArray[index]): [str(x) for x in F_zinsarray]})
        save_Es_zinsarray = pd.DataFrame({str(ExperimentArray[index]): [str(x) for x in Es_zinsarray]})
        save_Qs_zinsarray = pd.DataFrame({str(ExperimentArray[index]): [str(x) for x in Qs_zinsarray]})
        save_P_zinsarray = pd.DataFrame({str(ExperimentArray[index]): [str(x) for x in P_zinsarray]})
        save_df_zinsarray = pd.DataFrame({str(ExperimentArray[index]): [str(x) for x in df_zinsarray]})
        save_dg_zinsarray = pd.DataFrame({str(ExperimentArray[index]): [str(x) for x in dg_zinsarray]})

        save_Vs_zinsarrays = pd.concat([save_Vs_zinsarrays,save_Vs_zinsarray], axis=1, join="outer")
        save_F_zinsarrays = pd.concat([save_F_zinsarrays,save_F_zinsarray], axis=1, join="outer")
        save_Es_zinsarrays = pd.concat([save_Es_zinsarrays,save_Es_zinsarray], axis=1, join="outer")
        save_Qs_zinsarrays = pd.concat([save_Qs_zinsarrays,save_Qs_zinsarray], axis=1, join="outer")
        save_P_zinsarrays = pd.concat([save_P_zinsarrays,save_P_zinsarray], axis=1, join="outer")
        save_df_zinsarrays = pd.concat([save_df_zinsarrays,save_df_zinsarray], axis=1, join="outer")
        save_dg_zinsarrays = pd.concat([save_dg_zinsarrays,save_dg_zinsarray], axis=1, join="outer")

        print(index+1,'/', len(ExperimentArray))

    ##################
    # Save

    thispath = "Xsave_Si_Experiment_AFMarrays/" 
    thisname = "%.0f_%.2f_%.2f_%.2f_%.2f_%.2f_%.2f_%.2f_%.1f_%.1f_%.0f_%.0f_%.0f_%.2f_%.0f_%.0f_%.2f_%.2f_%.3f_%.0f.csv" % (slider_Vg, slider_zins, slider_Eg, slider_epsilonsem, slider_WFmet, slider_EAsem, slider_donor, slider_acceptor, slider_emass, slider_hmass, slider_T, slider_amplitude, slider_resfreq, slider_lag, slider_springconst, slider_Qfactor, slider_tipradius, slider_alpha, slider_cantheight, slider_cantarea)

    if not os.path.exists(thispath):
        os.mkdir(thispath)

    save_Vs_zinsarrays.to_csv(os.path.join(thispath,'_'.join(['zinsarray_Vs',thisname])), index=False)
    save_F_zinsarrays.to_csv(os.path.join(thispath,'_'.join(['zinsarray_F',thisname])), index=False)
    save_Es_zinsarrays.to_csv(os.path.join(thispath,'_'.join(['zinsarray_Es',thisname])), index=False)
    save_Qs_zinsarrays.to_csv(os.path.join(thispath,'_'.join(['zinsarray_Qs',thisname])), index=False)
    save_P_zinsarrays.to_csv(os.path.join(thispath,'_'.join(['zinsarray_P',thisname])), index=False)
    save_df_zinsarrays.to_csv(os.path.join(thispath,'_'.join(['zinsarray_df',thisname])), index=False)
    save_dg_zinsarrays.to_csv(os.path.join(thispath,'_'.join(['zinsarray_dg',thisname])), index=False)