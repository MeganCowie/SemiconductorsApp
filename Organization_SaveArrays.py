### What do I want to do here?

# I want to be able to search to see if I already have a solution.
# Only save solutions that match preset values.

# Save each experiment separately
# Each experiment comes with a different array (or pair of arrays)



# Saving results for AFM oscillations
save_zins_zinsarray = pd.DataFrame({"zins_zinsarray": [str(x) for x in zins_array*10**7]})
save_Vs_zinsarray = pd.DataFrame({"Vs_zinsarray": [str(x) for x in Vs_zinsarray]})
save_F_zinsarray = pd.DataFrame({"F_zinsarray": [str(x) for x in F_zinsarray]})
save_zinsarrays = pd.concat([save_zins_zinsarray,save_Vs_zinsarray,save_F_zinsarray], axis=1, join="inner")
save_zinsarrays.to_csv('Xsave_ncAFM_zinsarrays.csv',index=False)

save_time_timearray = pd.DataFrame({"time_timearray": [str(x) for x in time_AFMarray]})
save_zins_timearray = pd.DataFrame({"zins_timearray": [str(x) for x in zins_AFMarray*10**7]})
save_Vs_timearray = pd.DataFrame({"Vs_timearray": [str(x) for x in Vs_AFMarray]})
save_F_timearray = pd.DataFrame({"F_timearray": [str(x) for x in F_AFMarray]})
save_timearrays = pd.concat([save_time_timearray,save_zins_timearray,save_Vs_timearray,save_F_timearray], axis=1, join="inner")
save_timearrays.to_csv('Xsave_ncAFM_timearrays.csv',index=False)

save_Ec_AFMarray = pd.DataFrame({"Ec_AFMarray": [str(x) for x in Ec_AFMarray]})
save_Ev_AFMarray = pd.DataFrame({"Ev_AFMarray": [str(x) for x in Ev_AFMarray]})
save_Ef_AFMarray = pd.DataFrame({"Ef_AFMarray": [str(x) for x in Ef_AFMarray]})
save_Gatez1_AFMarray = pd.DataFrame({"Gatez1_AFMarray": [str(x) for x in Gatex_AFMarray[:,0]]})
save_GateE1_AFMarray = pd.DataFrame({"GateE1_AFMarray": [str(x) for x in Gatey_AFMarray[:,0]]})
save_Gatez2_AFMarray = pd.DataFrame({"Gatez2_AFMarray": [str(x) for x in Gatex_AFMarray[:,1]]})
save_GateE2_AFMarray = pd.DataFrame({"GateE2_AFMarray": [str(x) for x in Gatey_AFMarray[:,1]]})
save_Insulatorz1_AFMarray = pd.DataFrame({"Insulatorz1_AFMarray": [str(x) for x in Insulatorx_AFMarray[:,0]]})
save_InsulatorE1_AFMarray = pd.DataFrame({"InsulatorE1_AFMarray": [str(x) for x in Insulatory_AFMarray[:,0]]})
save_Insulatorz2_AFMarray = pd.DataFrame({"Insulatorz2_AFMarray": [str(x) for x in Insulatorx_AFMarray[:,1]]})
save_InsulatorE2_AFMarray = pd.DataFrame({"InsulatorE2_AFMarray": [str(x) for x in Insulatory_AFMarray[:,1]]})
save_Insulatorz3_AFMarray = pd.DataFrame({"Insulatorz3_AFMarray": [str(x) for x in Insulatorx_AFMarray[:,2]]})
save_InsulatorE3_AFMarray = pd.DataFrame({"InsulatorE3_AFMarray": [str(x) for x in Insulatory_AFMarray[:,2]]})
save_Insulatorz4_AFMarray = pd.DataFrame({"Insulatorz4_AFMarray": [str(x) for x in Insulatorx_AFMarray[:,3]]})
save_InsulatorE4_AFMarray = pd.DataFrame({"InsulatorE4_AFMarray": [str(x) for x in Insulatory_AFMarray[:,3]]})

save_banddiagram = pd.concat([save_Ec_AFMarray,save_Ev_AFMarray,save_Ef_AFMarray,save_Gatez1_AFMarray,save_GateE1_AFMarray,save_Gatez2_AFMarray,save_GateE2_AFMarray,save_Insulatorz1_AFMarray,save_InsulatorE1_AFMarray,save_Insulatorz2_AFMarray,save_InsulatorE2_AFMarray,save_Insulatorz3_AFMarray,save_InsulatorE3_AFMarray,save_Insulatorz4_AFMarray,save_InsulatorE4_AFMarray], axis=1, join="inner")
save_banddiagram.to_csv('Xsave_ncAFM_banddiagram.csv',index=False)
pd.DataFrame(zsem_AFMarray*10**7).to_csv("Xsave_ncAFM_banddiagram_zsem.csv")
pd.DataFrame(psi_AFMarray).to_csv("Xsave_ncAFM_banddiagram_psi.csv")




# Saving results for bias sweep
save_bias_biasarray = pd.DataFrame({"Vg_biasarray": [str(x) for x in Vg_array]})
save_Vs_biasarray = pd.DataFrame({"Vs_biasarray": [str(x) for x in Vs_biasarray]})
save_F_biasarray = pd.DataFrame({"F_biasarray": [str(x) for x in F_biasarray]})
save_df_biasarray = pd.DataFrame({"df_biasarray": [str(x) for x in df_biasarray]})
save_dg_biasarray = pd.DataFrame({"dg_biasarray": [str(x) for x in dg_biasarray]})
save_biasarrays = pd.concat([save_bias_biasarray,save_Vs_biasarray,save_F_biasarray,save_df_biasarray,save_dg_biasarray], axis=1, join="inner")
save_biasarrays.to_csv('Xsave_BiasSweep_biasarrays.csv',index=False)



# Save noise
'''
import dash
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import pandas as pd

import Physics_Semiconductors
import Physics_ncAFM
import Physics_Noise
import Physics_Optics


import Organization_BuildArrays

#########################################################
#########################################################

sigma = 1
mu = 1
points = 20000

#names_list = ['01','02','03','04','05','06','07','08','09','10','00','01_02_03_04_05_06_07_08_09_10']
names_list = ['11','12','13','14','15','16','17','18','19','20','00','01_02_03_04_05_06_07_08_09_10']

RTS1mag_list = [2.000, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2.000]
RTS1per_list = [0.995, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.995]
RTS2mag_list = [0, 10.00, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10.00]
RTS2per_list = [0, 0.999, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.999]
RTS3mag_list = [0, 0, 0.500, 0, 0, 0, 0, 0, 0, 0, 0, 0.500]
RTS3per_list = [0, 0, 0.994, 0, 0, 0, 0, 0, 0, 0, 0, 0.994]
RTS4mag_list = [0, 0, 0, 8.000, 0, 0, 0, 0, 0, 0, 0, 8.000]
RTS4per_list = [0, 0, 0, 0.990, 0, 0, 0, 0, 0, 0, 0, 0.990]
RTS5mag_list = [0, 0, 0, 0, 5.000, 0, 0, 0, 0, 0, 0, 5.000]
RTS5per_list = [0, 0, 0, 0, 0.992, 0, 0, 0, 0, 0, 0, 0.992]
RTS6mag_list = [0, 0, 0, 0, 0, 2.000, 0, 0, 0, 0, 0, 2.000]
RTS6per_list = [0, 0, 0, 0, 0, 0.989, 0, 0, 0, 0, 0, 0.989]
RTS7mag_list = [0, 0, 0, 0, 0, 0, 4.000, 0, 0, 0, 0, 4.000]
RTS7per_list = [0, 0, 0, 0, 0, 0, 0.982, 0, 0, 0, 0, 0.982]
RTS8mag_list = [0, 0, 0, 0, 0, 0, 0, 6.000, 0, 0, 0, 6.000]
RTS8per_list = [0, 0, 0, 0, 0, 0, 0, 0.996, 0, 0, 0, 0.996]
RTS9mag_list = [0, 0, 0, 0, 0, 0, 0, 0, 7.000, 0, 0, 7.000]
RTS9per_list = [0, 0, 0, 0, 0, 0, 0, 0, 0.997, 0, 0, 0.997]
RTS10mag_list= [0, 0, 0, 0, 0, 0, 0, 0, 0, 4.000, 0, 4.000]
RTS10per_list= [0, 0, 0, 0, 0, 0, 0, 0, 0, 0.978, 0, 0.978]


for index in range(len(names_list)):

    RTS1mag = RTS1mag_list[index]
    RTS1per = RTS1per_list[index]
    RTS2mag = RTS2mag_list[index]
    RTS2per = RTS2per_list[index]
    RTS3mag = RTS3mag_list[index]
    RTS3per = RTS3per_list[index]
    RTS4mag = RTS4mag_list[index]
    RTS4per = RTS4per_list[index]
    RTS5mag = RTS5mag_list[index]
    RTS5per = RTS5per_list[index]
    RTS6mag = RTS6mag_list[index]
    RTS6per = RTS6per_list[index]
    RTS7mag = RTS7mag_list[index]
    RTS7per = RTS7per_list[index]
    RTS8mag = RTS8mag_list[index]
    RTS8per = RTS8per_list[index]
    RTS9mag = RTS9mag_list[index]
    RTS9per = RTS9per_list[index]
    RTS10mag= RTS10mag_list[index]
    RTS10per= RTS10per_list[index]

    noise_Signalbins = np.linspace(mu-5*sigma,mu+5*sigma,100)
    noise_Gaussianbins = np.linspace(mu-5*sigma,mu+5*sigma,100)
    noise_TwoLevelbins = np.linspace(mu-5*sigma-RTS1mag-RTS2mag-RTS3mag-RTS4mag-RTS5mag-RTS6mag-RTS7mag-RTS8mag-RTS9mag-RTS10mag,mu+5*sigma+RTS1mag+RTS2mag+RTS3mag+RTS4mag+RTS5mag+RTS6mag+RTS7mag+RTS8mag+RTS9mag+RTS10mag,100)

    noise_timearray = Physics_Noise.Array_timearray()

    noise_Signalarray = Physics_Noise.Array_Signalarray(noise_timearray,mu,points)
    noise_SignalHistogram = Physics_Noise.Func_Histogram(noise_Signalarray,noise_Signalbins)
    PSD_Signalfreqs,PSD_Signalps = Physics_Noise.Func_PSD(noise_Signalarray)
    Allan_Signaltau, Allan_Signalvar = Physics_Noise.Func_AllanDev(noise_Signalarray)

    noise_Gaussianarray = Physics_Noise.Array_Gaussianarray(sigma,mu,noise_timearray)
    noise_GaussianHistogram = Physics_Noise.Func_Histogram(noise_Gaussianarray,noise_Gaussianbins)
    PSD_Gaussianfreqs,PSD_Gaussianps = Physics_Noise.Func_PSD(noise_Gaussianarray)
    Allan_Gaussiantau, Allan_Gaussianvar = Physics_Noise.Func_AllanDev(noise_Gaussianarray)

    noise_TwoLevelarray = Physics_Noise.Array_TwoLevelarray(RTS1mag,RTS1per,noise_Gaussianarray)
    noise_TwoLevelarray = Physics_Noise.Array_TwoLevelarray(RTS2mag,RTS2per,noise_TwoLevelarray)
    noise_TwoLevelarray = Physics_Noise.Array_TwoLevelarray(RTS3mag,RTS3per,noise_TwoLevelarray)
    noise_TwoLevelarray = Physics_Noise.Array_TwoLevelarray(RTS4mag,RTS4per,noise_TwoLevelarray)
    noise_TwoLevelarray = Physics_Noise.Array_TwoLevelarray(RTS5mag,RTS5per,noise_TwoLevelarray)
    noise_TwoLevelarray = Physics_Noise.Array_TwoLevelarray(RTS6mag,RTS6per,noise_TwoLevelarray)
    noise_TwoLevelarray = Physics_Noise.Array_TwoLevelarray(RTS7mag,RTS7per,noise_TwoLevelarray)
    noise_TwoLevelarray = Physics_Noise.Array_TwoLevelarray(RTS8mag,RTS8per,noise_TwoLevelarray)
    noise_TwoLevelarray = Physics_Noise.Array_TwoLevelarray(RTS9mag,RTS9per,noise_TwoLevelarray)
    noise_TwoLevelarray = Physics_Noise.Array_TwoLevelarray(RTS10mag,RTS10per,noise_TwoLevelarray)
    noise_TwoLevelHistogram = Physics_Noise.Func_Histogram(noise_TwoLevelarray,noise_TwoLevelbins)
    PSD_TwoLevelfreqs,PSD_TwoLevelps = Physics_Noise.Func_PSD(noise_TwoLevelarray)
    Allan_TwoLeveltau, Allan_TwoLevelvar = Physics_Noise.Func_AllanDev(noise_TwoLevelarray)
    AC_TwoLeveltau, AC_TwoLevelamp = Physics_Noise.Func_AC(noise_timearray,noise_TwoLevelarray)


    # Saving results
    noise_magparamarray = np.array([RTS1mag,RTS2mag,RTS3mag,RTS4mag,RTS5mag,RTS6mag,RTS7mag,RTS8mag,RTS9mag,RTS10mag])
    noise_perparamarray = np.array([RTS1per,RTS2per,RTS3per,RTS4per,RTS5per,RTS6per,RTS7per,RTS8per,RTS9per,RTS10per])
    save_noise_magparam = pd.DataFrame({"noise_magparamarray": [str(x) for x in noise_magparamarray]})
    save_noise_perparam = pd.DataFrame({"noise_perparamarray": [str(x) for x in noise_perparamarray]})
    save_noise_paramarrays = pd.concat([save_noise_magparam,save_noise_perparam], axis=1, join="inner")

    save_noise_timearray = pd.DataFrame({"noise_timearray": [str(x) for x in noise_timearray]})
    save_noise_TwoLevelarray = pd.DataFrame({"noise_TwoLevelarray": [str(x) for x in noise_TwoLevelarray]})
    save_noise_timearrays = pd.concat([save_noise_timearray,save_noise_TwoLevelarray], axis=1, join="inner")

    save_noise_TwoLevelbins = pd.DataFrame({"noise_TwoLevelbins": [str(x) for x in noise_TwoLevelbins]})
    save_noise_TwoLevelhist = pd.DataFrame({"noise_TwoLevelHistogram": [str(x) for x in noise_TwoLevelHistogram[0]]})
    save_noise_histarrays = pd.concat([save_noise_TwoLevelbins,save_noise_TwoLevelhist], axis=1, join="inner")

    save_noise_PSDarray_TwoLevelfreqs = pd.DataFrame({"PSD_TwoLevelfreqs": [str(x) for x in PSD_TwoLevelfreqs]})
    save_noise_PSDarray_TwoLevelps = pd.DataFrame({"PSD_TwoLevelps": [str(x) for x in PSD_TwoLevelps]})
    save_noise_PSDarrays = pd.concat([save_noise_PSDarray_TwoLevelfreqs,save_noise_PSDarray_TwoLevelps], axis=1, join="inner")

    save_noise_Allanarray_TwoLeveltau = pd.DataFrame({"Allan_TwoLeveltau": [str(x) for x in Allan_TwoLeveltau]})
    save_noise_Allanarray_TwoLevelvar = pd.DataFrame({"Allan_TwoLevelvar": [str(x) for x in Allan_TwoLevelvar]})
    save_noise_Allanarrays = pd.concat([save_noise_Allanarray_TwoLeveltau,save_noise_Allanarray_TwoLevelvar], axis=1, join="inner")

    save_noise_ACarray_TwoLeveltau = pd.DataFrame({"AC_TwoLeveltau": [str(x) for x in AC_TwoLeveltau]})
    save_noise_ACarray_TwoLevelamp = pd.DataFrame({"AC_TwoLevelamp": [str(x) for x in AC_TwoLevelamp]})
    save_noise_ACarrays = pd.concat([save_noise_ACarray_TwoLeveltau,save_noise_ACarray_TwoLevelamp], axis=1, join="inner")

    save_noisearrays = pd.concat([save_noise_paramarrays,save_noise_timearrays,save_noise_histarrays,save_noise_PSDarrays,save_noise_Allanarrays,save_noise_ACarrays], axis=0)
    save_noisearrays.to_csv('Xsave_Noisearrays_%s.csv' % (names_list[index]),index=False)

hopchance_array = np.random.uniform(low=0,high=1,size=points)
save_hopchancearray = pd.DataFrame({"hopchance_array": [str(x) for x in hopchance_array]})
save_hopchancearray.to_csv('Xsave_hopchancearray.csv',index=False)

'''
