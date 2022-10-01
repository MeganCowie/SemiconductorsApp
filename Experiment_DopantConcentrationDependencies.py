# Vary the dopant concentration of n-type silicon
import Organization_IntermValues
import Organization_BuildArrays
import numpy as np
import pandas as pd

################################################################################

# Haughton Si
toggle_type = False
slider_Vg = -1.4
slider_zins = 6
slider_Eg = 1.1
slider_epsilonsem = 11.8
slider_WFmet = 4.1
slider_EAsem = 4.0
slider_emass = 1
slider_hmass = 1
slider_donor = 18.92
slider_acceptor = 0
slider_T = 300
slider_alpha = 0
stylen = {'color': '#57c5f7', 'fontSize': 18, 'text-align': 'right'}
stylep = {'color': '#7f7f7f', 'fontSize': 18, 'text-align': 'right'}
disabledn = False
disabledp = True
'''
# MoSe2
toggle_type = True
slider_Vg = -1.4
slider_zins = 5.2
slider_Eg = 1.5
slider_epsilonsem = 5.9
slider_WFmet = 4.1
slider_EAsem = 3.5
slider_emass = 1
slider_hmass = 1
slider_donor = 0
slider_acceptor = 18.8
slider_T = 300
slider_alpha = 0
stylen = {'color': '#7f7f7f', 'fontSize': 18, 'text-align': 'right'}
stylep = {'color': '#57c5f7', 'fontSize': 18, 'text-align': 'right'}
disabledn = True
disabledp = False
'''

slider_biassteps = 250
slider_zinssteps = 128
slider_timesteps = 200
slider_amplitude = 6
slider_resfreq = 330000
slider_lag = 30
slider_hop = 0.05
toggle_RTN = True
toggle_sampletype = False
slider_springconst = 42
slider_Qfactor = 18000
slider_tipradius = 10

# Input values and arrays
Vg,zins,Eg,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T,sampletype,biassteps,zinssteps,Vg_array,zins_array=Organization_IntermValues.Surface_inputvalues(slider_Vg,slider_zins,slider_alpha,slider_Eg,slider_epsilonsem,slider_WFmet,slider_EAsem,slider_donor,slider_acceptor,slider_emass,slider_hmass,slider_T,slider_biassteps,slider_zinssteps)
sampletype,RTN,amplitude,frequency,hop,lag,timesteps,time_AFMarray,zins_AFMarray,zinslag_AFMarray=Organization_IntermValues.AFM1_inputvalues(toggle_sampletype,False,slider_amplitude,slider_resfreq,slider_hop,slider_lag,slider_timesteps,zins)
springconst,Qfactor,tipradius=Organization_IntermValues.AFM2_inputvalues(slider_springconst,slider_Qfactor,slider_tipradius)


################################################################################
N_array = np.linspace(14,20,121) # Vary the dopant concentration

save_Vs_biasarrays = pd.DataFrame({"Vg_array": [str(x) for x in Vg_array]})
save_F_biasarrays = pd.DataFrame({"Vg_array": [str(x) for x in Vg_array]})
save_df_biasarrays = pd.DataFrame({"Vg_array": [str(x) for x in Vg_array]})
save_dg_biasarrays = pd.DataFrame({"Vg_array": [str(x) for x in Vg_array]})
save_Vs_zinsarrays = pd.DataFrame({"zins_array": [str(x) for x in zins_array]})
save_F_zinsarrays = pd.DataFrame({"zins_array": [str(x) for x in zins_array]})


for N_index in range(len(N_array)):
    # Calculations and results for before hop
    if disabledn == True:
        Na = round((10**(N_array[N_index])*10**8)/(1000**3))
    else:
        Nd = round((10**(N_array[N_index])*10**8)/(1000**3))

    Vg = -6*(1-slider_alpha)
    zins = 15*1e-7 #cm

    Vs_biasarray, F_biasarray, Vs_zinsarray, F_zinsarray = Organization_BuildArrays.VsF_arrays(Vg_array,zins_array,sampletype,Vg,zins,Eg,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T)
    Vs_biasarray, F_biasarray, df_biasarray, dg_biasarray = Organization_BuildArrays.VsFdfdg_biasarray(Vg_array,timesteps,amplitude,frequency,springconst,Qfactor,tipradius,sampletype,hop,lag,  Vg,zins,Eg,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T)


    # Organize arrays for saving
    save_Vs_biasarray = pd.DataFrame({str(N_array[N_index]): [str(x) for x in Vs_biasarray]})
    save_F_biasarray = pd.DataFrame({str(N_array[N_index]): [str(x) for x in F_biasarray]})
    save_df_biasarray = pd.DataFrame({str(N_array[N_index]): [str(x) for x in df_biasarray]})
    save_dg_biasarray = pd.DataFrame({str(N_array[N_index]): [str(x) for x in dg_biasarray]})
    save_Vs_zinsarray = pd.DataFrame({str(N_array[N_index]): [str(x) for x in Vs_zinsarray]})
    save_F_zinsarray = pd.DataFrame({str(N_array[N_index]): [str(x) for x in F_zinsarray]})

    save_Vs_biasarrays = pd.concat([save_Vs_biasarray,save_Vs_biasarrays], axis=1, join="inner")
    save_F_biasarrays = pd.concat([save_F_biasarray,save_F_biasarrays], axis=1, join="inner")
    save_df_biasarrays = pd.concat([save_df_biasarray,save_df_biasarrays], axis=1, join="inner")
    save_dg_biasarrays = pd.concat([save_dg_biasarray,save_dg_biasarrays], axis=1, join="inner")
    save_Vs_zinsarrays = pd.concat([save_Vs_zinsarray,save_Vs_zinsarrays], axis=1, join="inner")
    save_F_zinsarrays = pd.concat([save_F_zinsarray,save_F_zinsarrays], axis=1, join="inner")

    print(N_index+1,'/', len(N_array))


save_Vs_biasarrays.to_csv('Xsave_ExperimentDopantConcentration_Si_biasarrays_Vs_zins15nm.csv',index=False)
save_F_biasarrays.to_csv('Xsave_ExperimentDopantConcentration_Si_biasarrays_F_zins15nm.csv',index=False)
save_df_biasarrays.to_csv('Xsave_ExperimentDopantConcentration_Si_biasarrays_df_zins15nm.csv',index=False)
save_dg_biasarrays.to_csv('Xsave_ExperimentDopantConcentration_Si_biasarrays_dg_zins15nm.csv',index=False)
save_Vs_zinsarrays.to_csv('Xsave_ExperimentDopantConcentration_Si_zinsarrays_Vs_Vgneg6V.csv',index=False)
save_F_zinsarrays.to_csv('Xsave_ExperimentDopantConcentration_Si_zinsarrays_F_Vgneg6V.csv',index=False)
