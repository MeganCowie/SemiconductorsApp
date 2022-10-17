# Vary the dopant concentration of n-type silicon
import Physics_Semiconductors
import Organization_IntermValues
import Organization_BuildArrays
import numpy as np
import pandas as pd

################################################################################
# Haughton Si values

toggle_type = False
slider_Vg = 0
slider_zins = 12
slider_Eg = 1.12
slider_epsilonsem = 11.7
slider_WFmet = 4.15
slider_EAsem = 4.05
slider_emass = 0.98
slider_hmass = 0.19
slider_donor = 15.9615
slider_acceptor = 0
slider_T = 300
slider_alpha = 0
stylen = {'color': '#57c5f7', 'fontSize': 18, 'text-align': 'right'}
stylep = {'color': '#7f7f7f', 'fontSize': 18, 'text-align': 'right'}
disabledn = False
disabledp = True

slider_biassteps = 512#256
slider_zinssteps = 128
slider_timesteps = 200
slider_amplitude = 6
slider_resfreq = 300000
slider_lag = 0
slider_hop = 0
toggle_RTN = True
toggle_sampletype = False
slider_springconst = 42
slider_Qfactor = 23000
slider_tipradius = 20.2

################################################################################
# Inputs

#experiment = 'Nd'
#experiment = 'emass'
#experiment = 'hmass'
#experiment = 'Eg'
#experiment = 'epsilonsem'
#experiment = 'amplitude'
#experiment = 'zins'
experiment = 'lag'

#slider_zins = slider_zins+slider_amplitude

################################################################################
# Sweep ranges

if experiment=='Nd':
    ExperimentArray =  np.linspace(14,19,51)
elif experiment=='emass':
    ExperimentArray =  np.linspace(0.1,1.2,56)
elif experiment=='hmass':
    ExperimentArray =  np.linspace(0.1,1.2,56)
elif experiment=='Eg':
    ExperimentArray =  np.linspace(0.8,1.5,36)
elif experiment=='epsilonsem':
    ExperimentArray =  np.linspace(1,20,39)
elif experiment=='amplitude':
    ExperimentArray =  np.linspace(2,30,29)
elif experiment=='zins':
    ExperimentArray =  np.linspace(2,30,29)
elif experiment=='lag':
    ExperimentArray =  np.linspace(0,50,1)

################################################################################
# Input values and arrays

Vg,zins,Eg,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T,sampletype,biassteps,zinssteps,Vg_array,zins_array=Organization_IntermValues.Surface_inputvalues(slider_Vg,slider_zins,slider_alpha,slider_Eg,slider_epsilonsem,slider_WFmet,slider_EAsem,slider_donor,slider_acceptor,slider_emass,slider_hmass,slider_T,slider_biassteps,slider_zinssteps)
sampletype,RTN,amplitude,frequency,hop,lag,timesteps,time_AFMarray,zins_AFMarray,zinslag_AFMarray=Organization_IntermValues.AFM1_inputvalues(toggle_sampletype,False,slider_amplitude,slider_resfreq,slider_hop,slider_lag,slider_timesteps,  Vg,zins,Eg,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T)
springconst,Qfactor,tipradius=Organization_IntermValues.AFM2_inputvalues(slider_springconst,slider_Qfactor,slider_tipradius)

################################################################################
# Initialize arrays

save_Vs_biasarrays = pd.DataFrame({"Vg_array": [str(x) for x in Vg_array]})
save_F_biasarrays = pd.DataFrame({"Vg_array": [str(x) for x in Vg_array]})
save_df_biasarrays = pd.DataFrame({"Vg_array": [str(x) for x in Vg_array]})
save_dg_biasarrays = pd.DataFrame({"Vg_array": [str(x) for x in Vg_array]})
save_lag_biasarrays = pd.DataFrame({"Vg_array": [str(x) for x in Vg_array]})
save_Vstop_biasarrays = pd.DataFrame({"Vg_array": [str(x) for x in Vg_array]})
save_Vsbot_biasarrays = pd.DataFrame({"Vg_array": [str(x) for x in Vg_array]})
save_zQtop_biasarrays = pd.DataFrame({"Vg_array": [str(x) for x in Vg_array]})
save_zQbot_biasarrays = pd.DataFrame({"Vg_array": [str(x) for x in Vg_array]})
save_Qstop_biasarrays = pd.DataFrame({"Vg_array": [str(x) for x in Vg_array]})
save_Qsbot_biasarrays = pd.DataFrame({"Vg_array": [str(x) for x in Vg_array]})
#save_Vs_zinsarrays = pd.DataFrame({"zins_array": [str(x) for x in zins_array]})
#save_F_zinsarrays = pd.DataFrame({"zins_array": [str(x) for x in zins_array]})
#save_df_zinsarrays = pd.DataFrame({"zins_array": [str(x) for x in zins_array]})
#save_dg_zinsarrays = pd.DataFrame({"zins_array": [str(x) for x in zins_array]})
#save_lag_zinsarrays = pd.DataFrame({"zins_array": [str(x) for x in zins_array]})

################################################################################
# Vary experimental parameter

for index in range(len(ExperimentArray)):

    if experiment=='Nd':
        Nd = round((10**(ExperimentArray[index])*10**8)/(1000**3)) #/cm^3
    elif experiment=='emass':
        mn = ExperimentArray[index]*Physics_Semiconductors.me #k
    elif experiment=='hmass':
        mp = ExperimentArray[index]*Physics_Semiconductors.me #kg
    elif experiment=='Eg':
        Eg = ExperimentArray[index] #eV
    elif experiment=='epsilonsem':
        epsilon_sem = ExperimentArray[index] #dimensionless
    elif experiment=='amplitude':
        amplitude = ExperimentArray[index] #nm
    elif experiment=='zins':
        zins = ExperimentArray[index]*1e-7 #cm
    elif experiment=='lag':
        lag = ExperimentArray[index]/10**9*frequency
    else:
        print('Error: Experiment not defined.')

    Vs_biasarray, F_biasarray, df_biasarray, dg_biasarray, lag_biasarray = Organization_BuildArrays.VsFdfdg_biasarray(Vg_array,timesteps,amplitude,frequency,springconst,Qfactor,tipradius,sampletype,hop,lag,  Vg,zins,Eg,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T)
    #Vs_zinsarray, F_zinsarray, df_zinsarray, dg_zinsarray, lag_zinsarray = Organization_BuildArrays.VsFdfdg_zinsarray(zins_array,timesteps,amplitude,frequency,springconst,Qfactor,tipradius,sampletype,hop,lag,  Vg,zins,Eg,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T)

    # Organize arrays for saving
    save_Vs_biasarray = pd.DataFrame({str(ExperimentArray[index]): [str(x) for x in Vs_biasarray]})
    save_F_biasarray = pd.DataFrame({str(ExperimentArray[index]): [str(x) for x in F_biasarray]})
    save_df_biasarray = pd.DataFrame({str(ExperimentArray[index]): [str(x) for x in df_biasarray]})
    save_dg_biasarray = pd.DataFrame({str(ExperimentArray[index]): [str(x) for x in dg_biasarray]})
    save_lag_biasarray = pd.DataFrame({str(ExperimentArray[index]): [str(x) for x in lag_biasarray]})
    #save_Vs_zinsarray = pd.DataFrame({str(ExperimentArray[index]): [str(x) for x in Vs_zinsarray]})
    #save_F_zinsarray = pd.DataFrame({str(ExperimentArray[index]): [str(x) for x in F_zinsarray]})
    #save_df_zinsarray = pd.DataFrame({str(ExperimentArray[index]): [str(x) for x in df_zinsarray]})
    #save_dg_zinsarray = pd.DataFrame({str(ExperimentArray[index]): [str(x) for x in dg_zinsarray]})
    #save_lag_zinsarray = pd.DataFrame({str(ExperimentArray[index]): [str(x) for x in lag_zinsarray]})

    save_Vs_biasarrays = pd.concat([save_Vs_biasarray,save_Vs_biasarrays], axis=1, join="inner")
    save_F_biasarrays = pd.concat([save_F_biasarray,save_F_biasarrays], axis=1, join="inner")
    save_df_biasarrays = pd.concat([save_df_biasarray,save_df_biasarrays], axis=1, join="inner")
    save_dg_biasarrays = pd.concat([save_dg_biasarray,save_dg_biasarrays], axis=1, join="inner")
    save_lag_biasarrays = pd.concat([save_lag_biasarray,save_lag_biasarrays], axis=1, join="inner")
    #save_Vs_zinsarrays = pd.concat([save_Vs_zinsarray,save_Vs_zinsarrays], axis=1, join="inner")
    #save_F_zinsarrays = pd.concat([save_F_zinsarray,save_F_zinsarrays], axis=1, join="inner")
    #save_df_zinsarrays = pd.concat([save_df_zinsarray,save_df_zinsarrays], axis=1, join="inner")
    #save_dg_zinsarrays = pd.concat([save_dg_zinsarray,save_dg_zinsarrays], axis=1, join="inner")
    #save_lag_zinsarrays = pd.concat([save_lag_zinsarray,save_lag_zinsarrays], axis=1, join="inner")

    print(index+1,'/', len(ExperimentArray))

Vstop_biasarray,Vsbot_biasarray,zQtop_biasarray,zQbot_biasarray,Qstop_biasarray,Qsbot_biasarray = Organization_BuildArrays.VstopVsbot_biasarray(Vg_array,timesteps,amplitude,frequency,springconst,Qfactor,tipradius,sampletype,hop,lag,  Vg,zins,Eg,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T)

save_Vstop_biasarray = pd.DataFrame({str(ExperimentArray[index]): [str(x) for x in Vstop_biasarray]})
save_Vsbot_biasarray = pd.DataFrame({str(ExperimentArray[index]): [str(x) for x in Vsbot_biasarray]})
save_zQtop_biasarray = pd.DataFrame({str(ExperimentArray[index]): [str(x) for x in zQtop_biasarray]})
save_zQbot_biasarray = pd.DataFrame({str(ExperimentArray[index]): [str(x) for x in zQbot_biasarray]})
save_Qstop_biasarray = pd.DataFrame({str(ExperimentArray[index]): [str(x) for x in Qstop_biasarray]})
save_Qsbot_biasarray = pd.DataFrame({str(ExperimentArray[index]): [str(x) for x in Qsbot_biasarray]})

save_Vstop_biasarrays = pd.concat([save_Vstop_biasarray,save_Vstop_biasarrays], axis=1, join="inner")
save_Vsbot_biasarrays = pd.concat([save_Vsbot_biasarray,save_Vsbot_biasarrays], axis=1, join="inner")
save_zQtop_biasarrays = pd.concat([save_zQtop_biasarray,save_zQtop_biasarrays], axis=1, join="inner")
save_zQbot_biasarrays = pd.concat([save_zQbot_biasarray,save_zQbot_biasarrays], axis=1, join="inner")
save_Qstop_biasarrays = pd.concat([save_Qstop_biasarray,save_Qstop_biasarrays], axis=1, join="inner")
save_Qsbot_biasarrays = pd.concat([save_Qsbot_biasarray,save_Qsbot_biasarrays], axis=1, join="inner")

################################################################################
# Save

name = "%d_%d_%d_%d_%d_%d_%d_%d_%d_%d_%d_%d" % (slider_Vg, slider_zins, slider_Eg, slider_epsilonsem, slider_WFmet, slider_EAsem, slider_emass, slider_hmass, slider_donor*10000, slider_T, slider_amplitude, slider_lag)

save_Vs_biasarrays.to_csv('_'.join(['Xsave_Experiment',experiment,'Si',name,'biasarrays_Vs.csv']),index=False)
save_F_biasarrays.to_csv('_'.join(['Xsave_Experiment',experiment,'Si',name,'biasarrays_F.csv']),index=False)
save_df_biasarrays.to_csv('_'.join(['Xsave_Experiment',experiment,'Si',name,'biasarrays_df.csv']),index=False)
save_dg_biasarrays.to_csv('_'.join(['Xsave_Experiment',experiment,'Si',name,'biasarrays_dg.csv']),index=False)
save_lag_biasarrays.to_csv('_'.join(['Xsave_Experiment',experiment,'Si',name,'biasarrays_lag.csv']),index=False)
#save_Vs_zinsarrays.to_csv('_'.join(['Xsave_Experiment',experiment,'Si',name,'zinsarrays_Vs.csv']),index=False)
#save_F_zinsarrays.to_csv('_'.join(['Xsave_Experiment',experiment,'Si',name,'zinsarrays_F.csv']),index=False)
#save_df_zinsarrays.to_csv('_'.join(['Xsave_Experiment',experiment,'Si',name,'zinsarrays_df.csv']),index=False)
#save_dg_zinsarrays.to_csv('_'.join(['Xsave_Experiment',experiment,'Si',name,'zinsarrays_dg.csv']),index=False)
#save_lag_zinsarrays.to_csv('_'.join(['Xsave_Experiment',experiment,'Si',name,'zinsarrays_lag.csv']),index=False)

save_Vstop_biasarrays.to_csv('_'.join(['Xsave_Experiment',experiment,'Si',name,'biasarrays_Vstop.csv']),index=False)
save_Vsbot_biasarrays.to_csv('_'.join(['Xsave_Experiment',experiment,'Si',name,'biasarrays_Vsbot.csv']),index=False)
save_zQtop_biasarrays.to_csv('_'.join(['Xsave_Experiment',experiment,'Si',name,'biasarrays_zQtop.csv']),index=False)
save_zQbot_biasarrays.to_csv('_'.join(['Xsave_Experiment',experiment,'Si',name,'biasarrays_zQbot.csv']),index=False)
save_Qstop_biasarrays.to_csv('_'.join(['Xsave_Experiment',experiment,'Si',name,'biasarrays_Qstop.csv']),index=False)
save_Qsbot_biasarrays.to_csv('_'.join(['Xsave_Experiment',experiment,'Si',name,'biasarrays_Qsbot.csv']),index=False)
