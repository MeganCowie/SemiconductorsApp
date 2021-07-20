################################################################################
################################################################################
# This script is not used in app.py. I am using it to test functions.
# Right now it simply plots frequency shift and dissipation as a function of
# time and bias .
################################################################################
################################################################################

import numpy as np
import pandas as pd
from scipy.optimize import fsolve
import Physics_Semiconductors
import Physics_SurfacepotForce
import Physics_AFMoscillation
import Physics_FreqshiftDissipation

################################################################################
################################################################################
# Constants & Variables

# Constants
kB = Physics_Semiconductors.kB
hbar = Physics_Semiconductors.hbar
me = Physics_Semiconductors.me
e = Physics_Semiconductors.e
epsilon_o = Physics_Semiconductors.epsilon_o

# Variables (would be slider values)
Vg = -1.5
zins = 6e-7 #cm
bandgap = 1.6 #eV
epsilon_sem = 5.7 # dimensionless
WFmet = 4.2 #eV
EAsem = 3.5 #eV
Nd = round((10**0*10**8)/(1000**3))
Na = round((10**19*10**8)/(1000**3))
mn = 1.1*Physics_Semiconductors.me #kg
mp = 1.2*Physics_Semiconductors.me #kg
T = 300 #K
amplitude = 6 #nm
frequency = 330000 #Hz
lag = 0
hop = 0.1
RTN = False
sampletype = False #False = semiconducting
springconst = 42 #N/m
Qfactor = 18000 #dimensionless
tipradius = 10 #nm**2

# Static values or arrays set inside callbacks
steps = 50
guess = 1
Vg_array = np.arange(200)/10-10 #eV
zins_array = (np.arange(200)/10+0.05)*1e-7 #cm



################################################################################
################################################################################
# Function being tested

time_AFMarray = Physics_AFMoscillation.time_AFMarray(steps)
zins_AFMarray = Physics_AFMoscillation.zins_AFMarray(time_AFMarray,amplitude, zins)

Vs_AFMarray, F_AFMarray = Physics_AFMoscillation.SurfacepotForce_AFMarray(guess,zins_AFMarray,sampletype,RTN,hop,   Vg,zins,bandgap,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T)
df_biasarray, dg_biasarray = Physics_FreqshiftDissipation.dfdg_biasarray(Vg_array,steps,amplitude,frequency,springconst,Qfactor,tipradius,sampletype,hop,lag,  Vg,zins,bandgap,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T)

time_AFMarray = np.append(time_AFMarray, time_AFMarray+2*np.pi)
zins_AFMarray = np.append(zins_AFMarray, zins_AFMarray)
Vs_AFMarray = np.append(Vs_AFMarray, Vs_AFMarray)
F_AFMarray = np.append(F_AFMarray, F_AFMarray)

################################################################################
################################################################################
# Figures

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

fig = make_subplots(rows=2, cols=2, shared_yaxes=False, shared_xaxes=False)
fig.add_trace(go.Scatter(
    x = time_AFMarray, y = zins_AFMarray,
    name = "Position", mode='lines', showlegend=False,
    ), row=1, col=1)
fig.add_trace(go.Scatter(
    x = time_AFMarray, y = F_AFMarray,
    name = "SC_F", mode='lines', showlegend=False,
    ), row=2, col=1)
fig.add_trace(go.Scatter(
    x = Vg_array, y = df_biasarray,
    name = "SC_df", mode='lines', showlegend=False,
    ), row=1, col=2)
fig.add_trace(go.Scatter(
    x = Vg_array, y = dg_biasarray,
    name = "SC_dg", mode='lines', showlegend=False,
    ), row=2, col=2)

fig.update_xaxes(title_text= "time", row=1, col=1)
fig.update_xaxes(title_text= "time", row=2, col=1)
fig.update_xaxes(title_text= "Bias (V)", row=1, col=2)
fig.update_xaxes(title_text= "Bias (V)", row=2, col=2)
fig.update_yaxes(title_text= "Frequency Shift (Hz)", row=1, col=1)
fig.update_yaxes(title_text= "Dissipation", row=2, col=1)
fig.update_yaxes(title_text= "Frequency Shift (Hz)", row=1, col=2)
fig.update_yaxes(title_text= "Dissipation", row=2, col=2)

fig.show()
