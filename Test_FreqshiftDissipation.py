################################################################################
################################################################################
# This script is not used in app.py. I am using it to test functions.
# Right now it simply plots frequency shift and dissipation as a function of
# gate bias.
################################################################################
################################################################################

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


################################################################################
################################################################################
# Function being tested

df_biasarray, dg_biasarray = Physics_FreqshiftDissipation.dfdg_biasarray(Vg_array,steps,amplitude,frequency,springconst,Qfactor,tipradius,sampletype,hop,lag,  Vg,zins,bandgap,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T)

################################################################################
################################################################################
# Figures

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

fig = make_subplots(rows=2, cols=1, shared_yaxes=False, shared_xaxes=True)
fig.add_trace(go.Scatter(
    x = Vg_array, y = df_biasarray,
    line_color=color_Ev), row=1, col=1)
fig.add_trace(go.Scatter(
    x = Vg_array, y = dg_biasarray,
    line_color=color_met), row=2, col=1)
fig.update_xaxes(title_text= "Gate Bias (eV)", row=2, col=1)
fig.update_yaxes(title_text= "frequency shift (Hz)", row=1, col=1)
fig.update_yaxes(title_text= "dissipation", row=2, col=1)
fig.update_layout(showlegend=False)

fig.show()
