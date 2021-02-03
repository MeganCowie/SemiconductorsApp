# This script is not used in app.py. I am using it to test functions.

import numpy as np
import pandas as pd
from scipy.optimize import fsolve
from scipy.integrate import trapz
import Physics_Semiconductors
import Physics_SurfacepotForce
import Physics_FreqshiftDissipation
import Physics_AFMoscillation

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

Vg_array = np.arange(1000)/50-10 #eV
zins_array = (np.arange(200)/10+0.05)*1e-7 #cm

steps = 50
amplitude = 6 #nm
frequency = 300000 #Hz
springconst = 42 #N/m
Qfactor = 20000
tipradius = 2 #nm**2



#Vs_biasarray, F_biasarray, Vs_zinsarray, F_zinsarray = Physics_SurfacepotForce.VsF_arrays(Vg_array,zins_array,   Vg,zins,bandgap,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T)
df_biasarray, dg_biasarray = Physics_FreqshiftDissipation.dfdg(Vg_array,steps,amplitude,frequency,springconst,Qfactor,tipradius,  Vg,zins,bandgap,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T)

time_AFMarray = Physics_AFMoscillation.time_AFMarray(steps)
zins_AFMarray = Physics_AFMoscillation.zins_AFMarray(time_AFMarray,amplitude,zins)
Vs_AFMarray, F_AFMarray2 = Physics_AFMoscillation.SurfacepotForce_AFMarray(1,zins_AFMarray,   Vg,zins,bandgap,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T)

Vg = 0
Vs_AFMarray, F_AFMarray1 = Physics_AFMoscillation.SurfacepotForce_AFMarray(1,zins_AFMarray,   Vg,zins,bandgap,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T)



################################################################################
################################################################################
# Figures

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
fig = make_subplots(rows=2, cols=2, shared_yaxes=False, shared_xaxes=True)
fig.add_trace(go.Scatter(
    x = time_AFMarray, y = F_AFMarray1*np.sin(time_AFMarray),
    line_color=color_Ev), row=1, col=1)
fig.add_trace(go.Scatter(
    x = time_AFMarray, y = F_AFMarray1,
    line_color=color_met), row=1, col=1)
fig.add_trace(go.Scatter(
    x = time_AFMarray, y = F_AFMarray1*np.cos(time_AFMarray),
    line_color=color_Ec), row=2, col=1)
fig.add_trace(go.Scatter(
    x = time_AFMarray, y = F_AFMarray1,
    line_color=color_met), row=2, col=1)
fig.add_trace(go.Scatter(
    x = time_AFMarray, y = F_AFMarray2*np.sin(time_AFMarray),
    line_color=color_Ev), row=1, col=2)
fig.add_trace(go.Scatter(
    x = time_AFMarray, y = F_AFMarray2,
    line_color=color_met), row=1, col=2)
fig.add_trace(go.Scatter(
    x = time_AFMarray, y = F_AFMarray2*np.cos(time_AFMarray),
    line_color=color_Ec), row=2, col=2)
fig.add_trace(go.Scatter(
    x = time_AFMarray, y = F_AFMarray2,
    line_color=color_met), row=2, col=2)
fig.update_xaxes(title_text= "time", row=2, col=1)
fig.update_xaxes(title_text= "time", row=2, col=2)
fig.update_yaxes(title_text= "0V: sin", row=1, col=1)
fig.update_yaxes(title_text= "0V: cos", row=2, col=1)
fig.update_yaxes(title_text= "5V: sin", row=1, col=2)
fig.update_yaxes(title_text= "5V: cos", row=2, col=2)
fig.update_layout(showlegend=False)

fig.show()


fig = make_subplots(rows=2, cols=2, shared_yaxes=False, shared_xaxes=True)
fig.add_trace(go.Scatter(
    x = Vg_array, y = df_biasarray,
    line_color=color_Ev), row=1, col=1)
fig.add_trace(go.Scatter(
    x = Vg_array, y = dg_biasarray,
    line_color=color_met), row=2, col=1)
fig.update_xaxes(title_text= "Gate Bias (eV)", row=2, col=1)
fig.update_yaxes(title_text= "df", row=1, col=1)
fig.update_yaxes(title_text= "diss", row=2, col=1)
fig.update_layout(showlegend=False)

fig.show()
