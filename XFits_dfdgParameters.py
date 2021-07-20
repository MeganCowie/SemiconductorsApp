################################################################################
################################################################################
# This script is not used in app.py. I am using it to collect frequency shift
# models for various different slider values in order to find the best fit for
# these values. Fitting itself done in Matlab.
################################################################################
################################################################################

import dash
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import pandas as pd

import Physics_Semiconductors
import Physics_SurfacepotForce
import Physics_AFMoscillation
import Physics_FreqshiftDissipation


###############################################################################
################################################################################
# Bias sweep experiment

model_dg = pd.read_csv('Excitation_Bias-Sweep315.csv')
model_dgx = model_dg.Bias
model_dgy = model_dg.Excitation

model_df = pd.read_csv('FreqShift_Bias-Sweep315.csv')
model315_dfx = model_df.Bias
model315_dfy = model_df.FreqShift

# input (slider) parameters
Vg = -1.5
slider_donor = 0
mp = 1*Physics_Semiconductors.me # kg
mn = 1*Physics_Semiconductors.me # kg
T = 300 # K
sampletype = False #false = semiconducting, true = metallic
amplitude = 6 #nm
frequency = 330000 #Hz
springconst = 42 #N/m
Qfactor = 18000
tipradius = 10 #nm
hop = 0.1
lag = 0/10**9*frequency #rad
steps = 50

slider_zins = 5.6
slider_bandgap = 1.6
slider_epsilonsem = 5.7
slider_WFmet = 4.2
slider_EAsem = 3.5
slider_acceptor = 19

Vg_array = np.arange(100)/20-3 #eV
Vg_array_string = [str(x) for x in Vg_array]
headers = ["zins", "bandgap", "epsilonsem", "WFmet", "EAsem", "donor", "acceptor", "mp", "mn", "T", "amplitude", "frequency", "springconst", "Qfactor", "tipradius", "hop", "lag", "Vg:"]
savestring = np.append(headers,Vg_array_string)
savedatabias_df = pd.DataFrame({'Number': savestring})

test_zins = [5.5, 5.6, 5.7, 5.8, 5.9] #5
test_bandgap = [1.5, 1.6, 1.7, 1.8, 1.9] #5
test_epsilonsem = [5.5, 5.6, 5.7, 5.8, 5.9] #5
test_WFmet = [4.2] #1
test_acceptor = [18.8, 18.9, 19.0, 19.1, 19.2] #5

this_number = 0
for i_zins in range(len(test_zins)):
    for i_bandgap in range(len(test_bandgap)):
        for i_epsilonsem in range(len(test_epsilonsem)):
            for i_WFmet in range(len(test_WFmet)):
                for i_acceptor in range(len(test_acceptor)):
                    this_number += 1
                    print("{:.2f}".format(this_number/(len(test_zins)*len(test_bandgap)*len(test_epsilonsem)*len(test_WFmet)*len(test_acceptor))*100))

                    slider_zins = test_zins[i_zins]
                    slider_bandgap = test_bandgap[i_bandgap]
                    slider_epsilonsem = test_epsilonsem[i_epsilonsem]
                    slider_WFmet = test_WFmet[i_WFmet]
                    slider_acceptor = test_acceptor[i_acceptor]

                    zins = slider_zins*1e-7 # cm
                    bandgap = slider_bandgap
                    epsilon_sem = slider_epsilonsem
                    WFmet = slider_WFmet #eV
                    EAsem = slider_EAsem #eV
                    Nd = round((10**slider_donor*10**8)/(1000**3))
                    Na = round((10**slider_acceptor*10**8)/(1000**3))

                    Vg_array = np.arange(100)/20-3 #eV
                    zins_array = (np.arange(200)/10+0.05)*1e-7 #cm

                    Vs_biasarray0, F_biasarray0, Vs_zinsarray0, F_zinsarray0= Physics_SurfacepotForce.VsF_arrays(Vg_array,zins_array,sampletype,   Vg,zins,bandgap,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T)
                    df_biasarray0, dg_biasarray0 = Physics_FreqshiftDissipation.dfdg_biasarray(Vg_array,steps,amplitude,frequency,springconst,Qfactor,tipradius,sampletype,hop,lag,  Vg,zins,bandgap,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T)

                    #Na = round((10**(slider_acceptor+hop)*10**8)/(1000**3))
                    #Vs_biasarray1, F_biasarray1, Vs_zinsarray1, F_zinsarray1 = Physics_SurfacepotForce.VsF_arrays(Vg_array,zins_array,sampletype,   Vg,zins,bandgap,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T)
                    #df_biasarray1, dg_biasarray1 =  Physics_FreqshiftDissipation.dfdg_biasarray(Vg_array,steps,amplitude,frequency,springconst,Qfactor,tipradius,sampletype,hop,lag,  Vg,zins,bandgap,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T)

                    #Vg_array = np.append(Vg_array, np.flipud(Vg_array))
                    #Vs_biasarray = np.append(Vs_biasarray0, np.flipud(Vs_biasarray1))
                    #F_biasarray = np.append(F_biasarray0, np.flipud(F_biasarray1))
                    #df_biasarray = np.append(df_biasarray0, np.flipud(df_biasarray1))-3.651 #Experimental offset, delete
                    #dg_biasarray = np.append(dg_biasarray0, np.flipud(dg_biasarray1))-0.16#Experimental offset, delete

                    #F_biasarray = F_biasarray0*np.pi*tipradius**2
                    #F_zinsarray = F_zinsarray0*np.pi*tipradius**2s

                    # Save
                    this_headers = [slider_zins, slider_bandgap, slider_epsilonsem, slider_WFmet, slider_EAsem, slider_donor, slider_acceptor,  mp, mn, T, amplitude, frequency, springconst, Qfactor, tipradius, hop, lag, "df:"]
                    this_headers = [str(x) for x in this_headers]
                    this_df_biasarray_string = [str(x) for x in df_biasarray0-3.561]
                    this_savestring = np.append(this_headers,this_df_biasarray_string)
                    this_savedatabias_df = pd.DataFrame({str(this_number): this_savestring})

                    savedatabias_df = pd.concat([savedatabias_df,this_savedatabias_df], axis=1, join="inner")
                    savedatabias_df.to_csv('XFits_dfdgParametersResults.csv',index=False)
