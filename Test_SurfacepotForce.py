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

Vg = 0
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
sampletype = False

Vs_biasarray, F_biasarray, Vs_zinsarray, F_zinsarray = Physics_SurfacepotForce.VsF_arrays(Vg_array,zins_array,sampletype,   Vg,zins,bandgap,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T)

slider_donor = 19+ 1*0.5
Nd = round((10**slider_donor*10**8)/(1000**3))
Vs_biasarray1, F_biasarray1, Vs_zinsarray1, F_zinsarray1 = Physics_SurfacepotForce.VsF_arrays(Vg_array,zins_array,sampletype,   Vg,zins,bandgap,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T)

Vs_zinsarray = np.append(Vs_zinsarray, np.flipud(Vs_zinsarray1))
zins_array = np.append(zins_array, np.flipud(zins_array))

################################################################################
################################################################################
# Figures

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
fig = make_subplots(rows=2, cols=2, shared_yaxes=False, shared_xaxes=False)
fig.add_trace(go.Scatter(
    x = zins_array, y = Vs_zinsarray,
    name = "Contact Potential (eV)", mode='lines', showlegend=False,
    ), row=1, col=1)

fig.update_xaxes(title_text= "Gate Bias (eV)", row=1, col=1)
fig.update_xaxes(title_text= "Insulator Thickness (nm)", row=1, col=2)
fig.update_yaxes(title_text= "F (N/nm^2)", row=1, col=1)


fig.show()
