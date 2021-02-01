# This script is not used in app.py. I am using it to test functions.

import numpy as np
import pandas as pd
import Physics_SemiconductorSurface
import Physics_BandDiagram
import Check2


################################################################################
################################################################################
# Input variables (would be slider values)

Vg = 5
zins = 1e-7 #cm
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

Vs = 0.1 #eV

Ec, Ev, Ei, Ef, zsem, psi, z_array, E_array, charge, Insulatorx, Insulatory, Vacuumx, Vacuumy, Gatex, Gatey \
 = Physics_BandDiagram.BandDiagram(zins,T,mn,mp,Nd,Na,epsilon_sem,bandgap,WFmet,EAsem, Vg, Vs)

################################################################################
################################################################################
# Figure

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
fig = make_subplots(rows=1, cols=1, shared_yaxes=False, shared_xaxes=True)
fig.add_trace(go.Scatter(
    x = z_array, y = E_array,
    name = "Contact Potential (zins)", mode='lines', showlegend=False,
    ), row=1, col=1)

#fig.update_xaxes(title_text= "Gate Bias (eV)", range=[min(z), max(z)], row=2, col=1)
#fig.update_yaxes(title_text= "Vs (eV)", row=1, col=1)
#fig.update_yaxes(title_text= "Guess", row=2, col=1)
#fig.update_yaxes(title_text= "Vs (eV)", row=1, col=2)
#fig.update_yaxes(title_text= "Guess", row=2, col=2)

fig.show()
