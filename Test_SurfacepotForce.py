################################################################################
################################################################################
# This script is not used in app.py. I am using it to test functions.
# Right now it simply plots surface potential and force as a function of Gate
# bias and tip-sample separation.
################################################################################
################################################################################

import numpy as np
import pandas as pd
from scipy.optimize import fsolve
import Physics_Semiconductors
import Physics_SurfacepotForce


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

Vs_biasarray, F_biasarray, Vs_zinsarray, F_zinsarray = Physics_SurfacepotForce.VsF_arrays(Vg_array,zins_array,sampletype,   Vg,zins,bandgap,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T)

################################################################################
################################################################################
# Figures

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

fig = make_subplots(rows=2, cols=2, shared_yaxes=False, shared_xaxes=False)
fig.add_trace(go.Scatter(
    x = Vg_array, y = Vs_biasarray,
    name = "Contact Potential (eV)", mode='lines', showlegend=False,
    ), row=1, col=1)
fig.add_trace(go.Scatter(
    x = Vg_array, y = F_biasarray,
    name = "Contact Potential (eV)", mode='lines', showlegend=False,
    ), row=2, col=1)
fig.add_trace(go.Scatter(
    x = zins_array, y = Vs_zinsarray,
    name = "Contact Potential (eV)", mode='lines', showlegend=False,
    ), row=1, col=2)
fig.add_trace(go.Scatter(
    x = zins_array, y = F_zinsarray,
    name = "Contact Potential (eV)", mode='lines', showlegend=False,
    ), row=2, col=2)
fig.update_xaxes(title_text= "Gate Bias (eV)", row=1, col=1)
fig.update_xaxes(title_text= "Gate Bias (eV)", row=2, col=1)
fig.update_xaxes(title_text= "Insulator Thickness (nm)", row=1, col=2)
fig.update_xaxes(title_text= "Insulator Thickness (nm)", row=2, col=2)
fig.update_yaxes(title_text= "Vs (V)", row=1, col=1)
fig.update_yaxes(title_text= "F (N/nm^2)", row=2, col=1)
fig.update_yaxes(title_text= "Vs (V)", row=1, col=2)
fig.update_yaxes(title_text= "F (N/nm^2)", row=2, col=2)


fig.show()
