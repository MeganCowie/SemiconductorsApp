# This script is not used in app.py. I am using it to test functions.

import numpy as np
import pandas as pd
from scipy.optimize import fsolve
import Physics_Semiconductors
import Physics_SurfacepotForce
import Physics_AFMoscillation
import Physics_FreqshiftDissipation



# APPEARANCE
color_fc='#2ca02c'
color_fv='#bcbd22'
color_Ef='#1f77b4'
color_Ei='#17becf'
color_Ev='#9467bd'
color_Ec='#e377c2'
color_n='#ff7f0e'
color_p='#8c564b'
color_ox='#a9a9a9'
color_met='#2f4f4f'
color_vac='#888888'
color_indicator='#2ca02c'
color_other='#2f4f4f'

################################################################################
################################################################################
# Input variables (would be slider values)

kB = Physics_Semiconductors.kB
hbar = Physics_Semiconductors.hbar
me = Physics_Semiconductors.me
e = Physics_Semiconductors.e
epsilon_o = Physics_Semiconductors.epsilon_o

Vg = 5
zins = 5e-7 #cm
bandgap = 2.5 #eV
epsilon_sem = 22 # dimensionless
WFmet = 5.5 #eV
EAsem = 2.7 #eV
Nd = round((10**19*10**8)/(1000**3))
Na = round((10**0*10**8)/(1000**3))
mn = 1.1*Physics_Semiconductors.me #kg
mp = 1.2*Physics_Semiconductors.me #kg
T = 300 # K


################################################################################
################################################################################
# Function being tested

steps = 50
amplitude = 6 #nm
frequency = 300000 #Hz
springconst = 42 #N/m
Qfactor = 20000
tipradius = 2 #nm**2
steps = 50

Vg_array = np.arange(1000)/50-10 #eV
zins_array = (np.arange(200)/10+0.05)*1e-7 #cm
time_AFMarray = Physics_AFMoscillation.time_AFMarray(steps)
zins_AFMarray = Physics_AFMoscillation.zins_AFMarray(time_AFMarray,amplitude, zins)

sampletype = False
Vs_AFMarray, F_AFMarray = Physics_AFMoscillation.SurfacepotForce_AFMarray(1,zins_AFMarray,sampletype,   Vg,zins,bandgap,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T)
df_biasarray, dg_biasarray = Physics_FreqshiftDissipation.dfdg(Vg_array,steps,amplitude,frequency,springconst,Qfactor,tipradius,sampletype,  Vg,zins,bandgap,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T)


time_AFMarray = np.append(time_AFMarray, time_AFMarray+2*np.pi)
zins_AFMarray = np.append(zins_AFMarray, zins_AFMarray)
Vs_AFMarray = np.append(Vs_AFMarray, Vs_AFMarray)
F_AFMarray = np.append(F_AFMarray, F_AFMarray)
F1_AFMarray = np.append(F1_AFMarray, F1_AFMarray)

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
    name = "SC_F", mode='lines', showlegend=True,
    ), row=2, col=1)
fig.add_trace(go.Scatter(
    x = time_AFMarray, y = F1_AFMarray,
    name = "M_F", mode='lines', showlegend=True,
    ), row=2, col=1)
fig.add_trace(go.Scatter(
    x = Vg_array, y = df_biasarray,
    name = "SC_df", mode='lines', showlegend=True,
    ), row=1, col=2)
fig.add_trace(go.Scatter(
    x = Vg_array, y = df1_biasarray,
    name = "M_df", mode='lines', showlegend=True,
    ), row=1, col=2)
fig.add_trace(go.Scatter(
    x = Vg_array, y = dg_biasarray,
    name = "SC_dg", mode='lines', showlegend=True,
    ), row=2, col=2)
fig.add_trace(go.Scatter(
    x = Vg_array, y = dg1_biasarray,
    name = "M_dg", mode='lines', showlegend=True,
    ), row=2, col=2)
fig.show()
