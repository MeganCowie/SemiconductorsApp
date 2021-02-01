# This script is not used in app.py. I am using it to test functions.

import numpy as np
import pandas as pd
from scipy.optimize import fsolve
import Physics_SemiconductorSurface
import Physics_SurfacepotForce
import Physics_AFM




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

steps = 100
amplitude = 6

time_AFMarray = Physics_AFM.time_AFMarray(steps)
position_AFMarray = Physics_AFM.position_AFMarray(time_AFMarray,amplitude)
zins_AFMarray = zins+position_AFMarray*1e-7 #cm


Vs_AFMarray, F_AFMarray = Physics_AFM.SurfacepotForce_AFMarray(1,zins_AFMarray,   Vg,zins,bandgap,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T)
#Ec_AFMarray,Ev_AFMarray,Ei_AFMarray,Ef_AFMarray,zsem_AFMarray,psi_AFMarray,Insulatorx_AFMarray,Insulatory_AFMarray,Vacuumx_AFMarray,Vacuumy_AFMarray,Gatex_AFMarray,Gatey_AFMarray = Physics_AFM.BandDiagram_AFMarray(Vs_AFMarray,zins_AFMarray,   Vg,zins,bandgap,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T)


################################################################################
################################################################################
# Figures

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
fig = make_subplots(rows=2, cols=2, shared_yaxes=False, shared_xaxes=False)
fig.add_trace(go.Scatter(
    x = time_AFMarray, y = position_AFMarray*-800000+13000000,
    name = "Position", mode='lines', showlegend=False,
    ), row=1, col=1)
fig.add_trace(go.Scatter(
    x = time_AFMarray, y = F_AFMarray,
    name = "Force", mode='lines', showlegend=False,
    ), row=1, col=1)

fig.show()
