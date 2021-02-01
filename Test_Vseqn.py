# This script is not used in app.py. I am using it to test functions.

import numpy as np
import pandas as pd
from scipy.optimize import fsolve
import Physics_SemiconductorSurface
import Physics_SurfacepotForce


################################################################################
################################################################################
# Input variables (would be slider values)

kB = Physics_SemiconductorSurface.kB
hbar = Physics_SemiconductorSurface.hbar
me = Physics_SemiconductorSurface.me
e = Physics_SemiconductorSurface.e
epsilon_o = Physics_SemiconductorSurface.epsilon_o

Vg = 5
zins = 5e-7 #cm
bandgap = 2.5 #eV
epsilon_sem = 22 # dimensionless
WFmet = 5.5 #eV
EAsem = 2.7 #eV
Nd = round((10**19*10**8)/(1000**3))
Na = round((10**0*10**8)/(1000**3))
mn = 1.1*Physics_SemiconductorSurface.me #kg
mp = 1.2*Physics_SemiconductorSurface.me #kg
T = 300 # K


################################################################################
################################################################################
# Function being tested

Vg_array = np.arange(2000)/100-10 #eV
zins_array = (np.arange(200)/10+0.05)*1e-7 #cm

Vs_biasarray, guess_biasarray, Vs_array, guessarray, ni = Physics_SurfacepotForce.Experiments(zins,T,mn,mp,Nd,Na,epsilon_sem,bandgap,WFmet,EAsem,Vg, Vg_array,zins_array)

col_zins = np.where(zins_array==zins)
row_Vg = np.where(Vg_array==Vg)

################################################################################
################################################################################
# Figures

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
fig = make_subplots(rows=2, cols=2, shared_yaxes=False, shared_xaxes=True)
fig.add_trace(go.Scatter(
    x = Vg_array, y = [column[col_zins] for column in Vs_array],
    name = "Contact Potential (zins)", mode='lines', showlegend=False,
    ), row=1, col=1)
fig.add_trace(go.Scatter(
    x = Vg_array, y = [column[col_zins] for column in guessarray],
    name = "Guess", mode='lines', showlegend=False,
    ), row=2, col=1)
fig.add_trace(go.Scatter(
    x = Vg_array, y = Vs_biasarray,
    name = "Contact Potential (zins)", mode='lines', showlegend=False,
    ), row=1, col=2)
fig.add_trace(go.Scatter(
    x = Vg_array, y = guess_biasarray,
    name = "Guess", mode='lines', showlegend=False,
    ), row=2, col=2)

fig.update_xaxes(title_text= "Gate Bias (eV)", range=[min(Vg_array), max(Vg_array)], row=2, col=1)
fig.update_xaxes(title_text= "Gate Bias (eV)", range=[min(Vg_array), max(Vg_array)], row=2, col=2)
fig.update_yaxes(title_text= "Vs (eV)", row=1, col=1)
fig.update_yaxes(title_text= "Guess", row=2, col=1)
fig.update_yaxes(title_text= "Vs (eV)", row=1, col=2)
fig.update_yaxes(title_text= "Guess", row=2, col=2)

fig.show()
