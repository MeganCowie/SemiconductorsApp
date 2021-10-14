################################################################################
################################################################################
# This script is not used in app.py. I am using it to collect frequency shift
# models for various different slider values in order to find the best fit for
# these values. Fitting itself done in Matlab.

# For a large parameter space, it is convenient to run several scripts in
# parallel. Create another script, replace every "Parallel1" in this file with
# "Parallel2, Parallel3", etc. and split up the for loop.
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

model_dg = pd.read_csv('XData_ExcitationvBias-Sweep315.csv')
model_dgx = model_dg.Bias
model_dgy = model_dg.Excitation

model_df = pd.read_csv('XData_FreqShiftvBias-Sweep315.csv')
model315_dfx = model_df.Bias
model315_dfy = model_df.FreqShift

# input (slider) parameters
Vg = -1.5
slider_donor = 0
mp = 1*Physics_Semiconductors.me # kg
mn = 1*Physics_Semiconductors.me # kg
T = 300 # K
sampletype = False #false = semiconducting, true = metallic
frequency = 330000 #Hz
Qfactor = 18000
tipradius =  10#nm
hop = 0.05
lag = 30/10**9*frequency #rad
steps = 50
EAsem = 3.5 #eV

# Load the parameters in the existing root files.
try:
    existsdatabias_df_1 = pd.read_csv("XFits_dfdgParametersResults_1.csv",nrows=17)
    existsdatabias_df_2 = pd.read_csv("XFits_dfdgParametersResults_2.csv",nrows=17)
    existsdatabias_df_3 = pd.read_csv("XFits_dfdgParametersResults_3.csv",nrows=17)
    existsdatabias_df_4 = pd.read_csv("XFits_dfdgParametersResults_4.csv",nrows=17)
    existsdatabias_df_5 = pd.read_csv("XFits_dfdgParametersResults_5.csv",nrows=17)
    existsdatabias_df = pd.concat([existsdatabias_df_1, existsdatabias_df_2, existsdatabias_df_3, existsdatabias_df_4, existsdatabias_df_5], axis=1)
    print('Five existing read files.')
except:
    try:
        existsdatabias_df_1 = pd.read_csv("XFits_dfdgParametersResults_1.csv",nrows=17)
        existsdatabias_df_2 = pd.read_csv("XFits_dfdgParametersResults_2.csv",nrows=17)
        existsdatabias_df_3 = pd.read_csv("XFits_dfdgParametersResults_3.csv",nrows=17)
        existsdatabias_df_4 = pd.read_csv("XFits_dfdgParametersResults_4.csv",nrows=17)
        existsdatabias_df = pd.concat([existsdatabias_df_1, existsdatabias_df_2, existsdatabias_df_3, existsdatabias_df_4], axis=1)
        print('Four existing read files.')
    except:
        try:
            existsdatabias_df_1 = pd.read_csv("XFits_dfdgParametersResults_1.csv",nrows=17)
            existsdatabias_df_2 = pd.read_csv("XFits_dfdgParametersResults_2.csv",nrows=17)
            existsdatabias_df_3 = pd.read_csv("XFits_dfdgParametersResults_3.csv",nrows=17)
            existsdatabias_df = pd.concat([existsdatabias_df_1, existsdatabias_df_2, existsdatabias_df_3], axis=1)
            print('Three existing read files.')
        except:
            try:
                existsdatabias_df_1 = pd.read_csv("XFits_dfdgParametersResults_1.csv",nrows=17)
                existsdatabias_df_2 = pd.read_csv("XFits_dfdgParametersResults_2.csv",nrows=17)
                existsdatabias_df = pd.concat([existsdatabias_df_1, existsdatabias_df_2], axis=1)
                print('Two existing read files.')
            except:
                try:
                    existsdatabias_df_1 = pd.read_csv("XFits_dfdgParametersResults_1.csv",nrows=17)
                    existsdatabias_df = pd.concat([existsdatabias_df_1], axis=1)
                    print('One existing read file.')
                except:
                    print('No existing read files.')
                    Vg_array = np.arange(100)/20-3 #eV
                    Vg_array = np.append(Vg_array, np.flipud(Vg_array))
                    Vg_array_string = [str(x) for x in Vg_array]
                    headers = ["zins", "bandgap", "epsilonsem", "WFmet", "EAsem", "donor", "acceptor", "mp", "mn", "T", "amplitude", "frequency", "springconst", "Qfactor", "tipradius", "hop", "lag", "Vg:"]
                    savestring = np.append(headers,Vg_array_string)
                    existsdatabias_df = pd.DataFrame({'Number': savestring})




# Load the parallel file if it exists. If not, create the template.
try:
    savedatabias_df = pd.read_csv("XFits_dfdgParametersResults_Parallel1.csv")
    print('Continuing existing write file.')
except:
    print('Creating a new write file.')
    Vg_array = np.arange(100)/20-3 #eV
    Vg_array = np.append(Vg_array, np.flipud(Vg_array))
    Vg_array_string = [str(x) for x in Vg_array]
    headers = ["zins", "bandgap", "epsilonsem", "WFmet", "EAsem", "donor", "acceptor", "mp", "mn", "T", "amplitude", "frequency", "springconst", "Qfactor", "tipradius", "hop", "lag", "Vg:"]
    savestring = np.append(headers,Vg_array_string)
    savedatabias_df = pd.DataFrame({'Number': savestring})


# Parameters to vary.
test_zins = [5.2] #nm
test_bandgap = [1.5] #eV
test_epsilonsem = [5.9] #
test_WFmet = [4.1] #eV
test_acceptor = [18.8]
test_springconst = [42] #N/m
test_amplitude = [6.0] #nm


this_number = 0
for i_zins in range(len(test_zins)):
    for i_bandgap in range(len(test_bandgap)):
        for i_epsilonsem in range(len(test_epsilonsem)):
            for i_WFmet in range(len(test_WFmet)):
                for i_acceptor in range(len(test_acceptor)):
                    for i_springconst in range(len(test_springconst)):
                        for i_amplitude in range(len(test_amplitude)):

                            slider_zins = test_zins[i_zins]
                            slider_bandgap = test_bandgap[i_bandgap]
                            slider_epsilonsem = test_epsilonsem[i_epsilonsem]
                            slider_WFmet = test_WFmet[i_WFmet]
                            slider_acceptor = test_acceptor[i_acceptor]
                            slider_springconst = test_springconst[i_springconst]
                            slider_amplitude = test_amplitude[i_amplitude]

                            # Check if this set of parameters has already been saved (in a previous run)
                            savedatabias_df_exists = (savedatabias_df.iloc[0]==str(slider_zins))*1 * (savedatabias_df.iloc[1]==str(slider_bandgap))*1  * (savedatabias_df.iloc[2]==str(slider_epsilonsem))*1  * (savedatabias_df.iloc[3]==str(slider_WFmet))*1  * (savedatabias_df.iloc[6]==str(slider_acceptor))*1 * (savedatabias_df.iloc[12]==str(slider_springconst))*1  * (savedatabias_df.iloc[10]==str(slider_amplitude))*1
                            #print(savedatabias_df_exists)

                            # Check if this set of parameters has already been saved (in exsting file)
                            existsdatabias_df_exists = (existsdatabias_df.iloc[0]==slider_zins)*1 * (existsdatabias_df.iloc[1]==slider_bandgap)*1  * (existsdatabias_df.iloc[2]==slider_epsilonsem)*1  * (existsdatabias_df.iloc[3]==slider_WFmet)*1  * (existsdatabias_df.iloc[6]==slider_acceptor)*1 * (existsdatabias_df.iloc[12]==slider_springconst)*1  * (existsdatabias_df.iloc[10]==slider_amplitude)*1

                            #if sum(savedatabias_df_exists)>0:
                            #    this_number += 1
                            #    print('Parameter set already exists in this file.')
                            #elif sum(existsdatabias_df_exists)>0:
                            #    this_number += 1
                                #print('Parameter set already exists in saved file.')
                            #else:
                            this_number += 1
                            print("{:.2f}".format((this_number)/(len(test_zins)*len(test_bandgap)*len(test_epsilonsem)*len(test_WFmet)*len(test_acceptor)*len(test_springconst)*len(test_amplitude))*100))

                            zins = slider_zins*1e-7 # cm
                            bandgap = slider_bandgap
                            epsilon_sem = slider_epsilonsem
                            WFmet = slider_WFmet #eV
                            Nd = round((10**slider_donor*10**8)/(1000**3))
                            springconst = slider_springconst
                            amplitude = slider_amplitude

                            Vg_array = np.arange(100)/20-3 #eV
                            zins_array = (np.arange(200)/10+0.05)*1e-7 #cm

                            #Pre-hop
                            Na = round((10**slider_acceptor*10**8)/(1000**3))
                            Vs_biasarray0, F_biasarray0, Vs_zinsarray0, F_zinsarray0= Physics_SurfacepotForce.VsF_arrays(Vg_array,zins_array,sampletype,   Vg,zins,bandgap,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T)
                            df_biasarray0, dg_biasarray0 = Physics_FreqshiftDissipation.dfdg_biasarray(Vg_array,steps,amplitude,frequency,springconst,Qfactor,tipradius,sampletype,hop,lag,  Vg,zins,bandgap,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T)

                            # Hop
                            Na = round((10**(slider_acceptor+hop)*10**8)/(1000**3))
                            Vs_biasarray1, F_biasarray1, Vs_zinsarray1, F_zinsarray1 = Physics_SurfacepotForce.VsF_arrays(Vg_array,zins_array,sampletype,   Vg,zins,bandgap,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T)
                            df_biasarray1, dg_biasarray1 =  Physics_FreqshiftDissipation.dfdg_biasarray(Vg_array,steps,amplitude,frequency,springconst,Qfactor,tipradius,sampletype,hop,lag,  Vg,zins,bandgap,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T)

                            Vg_array = np.append(Vg_array, np.flipud(Vg_array))
                            Vs_biasarray = np.append(Vs_biasarray0, np.flipud(Vs_biasarray1))
                            F_biasarray = np.append(F_biasarray0, np.flipud(F_biasarray1))
                            df_biasarray = np.append(df_biasarray0, np.flipud(df_biasarray1))-3.651 #Experimental offset, delete
                            dg_biasarray = np.append(dg_biasarray0, np.flipud(dg_biasarray1))

                            #F_biasarray = F_biasarray0*np.pi*tipradius**2
                            #F_zinsarray = F_zinsarray0*np.pi*tipradius**2s

                            # Save
                            this_headers = [slider_zins, slider_bandgap, slider_epsilonsem, slider_WFmet, EAsem, slider_donor, slider_acceptor,  mp, mn, T, amplitude, frequency, springconst, Qfactor, tipradius, hop, lag, "df:"]
                            this_headers = [str(x) for x in this_headers]
                            this_df_biasarray_string = [str(x) for x in dg_biasarray]
                            this_savestring = np.append(this_headers,this_df_biasarray_string)
                            this_savedatabias_df = pd.DataFrame({str(this_number): this_savestring})

                            savedatabias_df = pd.concat([savedatabias_df,this_savedatabias_df], axis=1, join="inner")
                            savedatabias_df.to_csv('XFits_dfdgParametersResults.csv',index=False)
