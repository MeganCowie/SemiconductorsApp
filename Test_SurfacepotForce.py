# This script is not used in app.py. I am using it to test functions.

import numpy as np
import pandas as pd
from scipy.optimize import fsolve
import Physics_Semiconductors
import Physics_SurfacepotForce


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

Vg_array = np.arange(2000)/100-10 #eV
zins_array = (np.arange(200)/10+0.05)*1e-7 #cm

Vs_biasarray, F_biasarray, Vs_zinsarray, F_zinsarray = Physics_SurfacepotForce.VsF_arrays(Vg_array,zins_array,   Vg,zins,bandgap,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T)

################################################################################
################################################################################
# Figures

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
fig = make_subplots(rows=2, cols=2, shared_yaxes=False, shared_xaxes=True)
fig.add_trace(go.Scatter(
    x = Vg_array, y = Vs_biasarray,
    name = "Contact Potential (zins)", mode='lines', showlegend=False,
    ), row=1, col=1)
fig.add_trace(go.Scatter(
    x = Vg_array, y = F_biasarray,
    name = "Guess", mode='lines', showlegend=False,
    ), row=2, col=1)

fig.update_xaxes(title_text= "Gate Bias (eV)", range=[min(Vg_array), 8], row=2, col=1)
fig.update_xaxes(title_text= "Gate Bias (eV)", range=[min(Vg_array), 8], row=2, col=2)
fig.update_yaxes(title_text= "Vs (eV)", row=1, col=1)
fig.update_yaxes(title_text= "F", row=2, col=1)


fig.show()
