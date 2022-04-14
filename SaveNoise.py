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
