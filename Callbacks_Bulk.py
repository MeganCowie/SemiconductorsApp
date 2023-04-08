import plotly.graph_objects as go
from plotly.subplots import make_subplots
import scipy.constants as sp
import numpy as np

import Physics_Semiconductors


################################################################################
################################################################################
# FIGURES

def fig_probabilitydistributions(slider_Ef, slider_T):

    # input (slider) parameters
    Ef, T = slider_Ef*Physics_Semiconductors.e, slider_T # J,K

    E = np.arange(500)/100*Physics_Semiconductors.e # J
    fc,fv = Physics_Semiconductors.Func_fcfv(E, Ef, T) # dimensionless
    fb = Physics_Semiconductors.Func_MaxwellBoltzmann(E, Ef, T) # dimensionless
    min_x, max_x, min_y, max_y = 0, 1, 0, 1.5

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x = E/Physics_Semiconductors.e, y = fc,
        name = "Fermi Dirac", mode='lines',
        line_color=color_fc
        ))
    fig.add_trace(go.Scatter(
        x = E/Physics_Semiconductors.e, y = fb,
        name = "Maxwell Boltzmann", mode='lines',
        line_color=color_other
        ))
    fig.add_trace(go.Scatter(
        x = np.array([1,1])*Ef/Physics_Semiconductors.e, y = np.array([min_y, max_y]),
        name = "Ef", mode='lines',
        line_color=color_Ef
        ))
    fig.add_trace(go.Scatter(
        x = np.array([1,1])*3*sp.value('Boltzmann constant in eV/K')*T+Ef/Physics_Semiconductors.e, y = np.array([min_y, max_y]),
        name = "3kBT+Ef", mode='lines',
        line_color=color_vac
        ))
    fig.update_layout(xaxis_title='Energy (eV)', yaxis_title='f(E)',
                      xaxis=dict(range=[min_x,max_x]), yaxis=dict(range=[min_y,max_y]),
                      transition_duration=500, margin=dict(t=0))
    return fig





def fig_carrierintegrals(slider_Ef, slider_T,slider_gc,slider_gv):

    # Input parameters
    Ef, T = slider_Ef*Physics_Semiconductors.e, slider_T # J,K
    E = (np.arange(500)/500+0.000000001)*Physics_Semiconductors.e # J
    Ec = 0.55*Physics_Semiconductors.e # J
    Ev = 0.45*Physics_Semiconductors.e # J
    mn = slider_gc*Physics_Semiconductors.me # kg
    mp = slider_gv*Physics_Semiconductors.me # kg

    # Calculated vaues
    fc,fv = Physics_Semiconductors.Func_fcfv(E, Ef, T) # dimensionless
    gc, gv = Physics_Semiconductors.Func_gcgv(E, Ec, Ev, mn, mp) # /(J*m**3)
    Ne, Nh = Physics_Semiconductors.Func_NeNh(E, fc, fv, gc, gv, Ec, Ev) # /(J*m**3)

    scaling = 1e28 # Just to display on the same axes
    min_x, max_x, min_y, max_y = 0, 1, 0, 1 #eV,dimensionless


    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Scatter(
        x = np.array([1,1])*Ef/Physics_Semiconductors.e, y = np.array([min_y, max_y]),
        name = "Ef", mode='lines',
        line_color=color_Ef
        ))
    fig.add_trace(go.Scatter(
        x = E/Physics_Semiconductors.e, y = fc,
        name = "f<sub>f</sub>(E)", mode='lines',
        line_color=color_fc
        ))
    fig.add_trace(go.Scatter(
        x = E/Physics_Semiconductors.e, y = gc*Physics_Semiconductors.e/scaling,
        name = "g<sub>c</sub>(E)", mode='lines',
        line_color=color_Ec
        ))
    fig.add_trace(go.Scatter(
        x = E/Physics_Semiconductors.e, y = gv*Physics_Semiconductors.e/scaling,
        name = "g<sub>v</sub>(E)", mode='lines',
        line_color=color_Ev
        ),secondary_y=True)
    fig.add_trace(go.Scatter(
        x=E/Physics_Semiconductors.e, y=Ne*Physics_Semiconductors.e/scaling,
        name = "n<sub>o</sub>", mode= 'none',
        fill='tozeroy', fillcolor=color_n,
        ))
    fig.add_trace(go.Scatter(
        x=E/Physics_Semiconductors.e, y=Nh*Physics_Semiconductors.e/scaling,
        name = "p<sub>o</sub>", mode= 'none',
        fill='tozeroy', fillcolor=color_p,
        ),secondary_y=True)
    fig.update_layout(xaxis_title='Energy (eV)',
                      xaxis=dict(range=[min_x,max_x]),
                      yaxis=dict(range=[min_y,max_y],title='f(E)'),
                      yaxis2=dict(range=[max_y,min_y],title='1-f(E)',side='right'),
                      transition_duration=500, margin=dict(t=0))
    fig.update_xaxes(showticklabels=False)
    return fig





def fig_carriers(slider_donor, slider_acceptor, slider_T, slider_emass, slider_hmass, toggle_type):

    # input (slider) parameters
    Nd = round(10**slider_donor)/(1e9) #m-3
    Na = round(10**slider_acceptor)/(1e9) #m-3
    T = slider_T #K
    mn = slider_emass*Physics_Semiconductors.me #kg
    mp = slider_hmass*Physics_Semiconductors.me #kg
    type = toggle_type

    E = (np.arange(300)/80)*Physics_Semiconductors.e #J
    Eg = 1.1*Physics_Semiconductors.e  #J

    # Calculated results
    Ec,Ev = Physics_Semiconductors.Func_EcEv(Eg)
    NC,NV = Physics_Semiconductors.Func_NCNV(T, mn, mp)
    Ei = Physics_Semiconductors.Func_Ei(Ev, Ec, T, mn, mp)
    Ef = Physics_Semiconductors.Func_Ef(NC, NV, Ec, Ev, T, Nd, Na)
    gc, gv = Physics_Semiconductors.Func_gcgv(E, Ec, Ev, mn, mp)
    fc, fv = Physics_Semiconductors.Func_fcfv(E, Ef, T)
    Ne, Nh = Physics_Semiconductors.Func_NeNh(E, fc, fv, gc, gv, Ec, Ev)

    min_x, max_x, min_y, max_y = 0, 1, 0, 3

    fig = make_subplots(
        rows=1, cols=3, shared_yaxes=True,
        column_widths=[0.2, 0.1, 0.1])
    fig.add_trace(go.Scatter(
        x = fc, y = E/Physics_Semiconductors.e,
        name = "f(E)", mode='lines',
        line_color=color_fc
        ), row=1, col=1)
    fig.add_trace(go.Scatter(
        x = fv, y = E/Physics_Semiconductors.e,
        name = "1-f(E)", mode='lines',
        line_color=color_fv
        ), row=1, col=1)
    fig.add_trace(go.Scatter(
        x = np.array([min_x, max_x]), y = np.array([1,1])*Ec/Physics_Semiconductors.e,
        name = "Conduction Band", mode='lines',
        line_color=color_Ec
        ), row=1, col=1)
    fig.add_trace(go.Scatter(
        x = np.array([min_x, max_x]), y = np.array([1,1])*Ev/Physics_Semiconductors.e,
        name = "Valence Band", mode='lines',
        line_color=color_Ev
        ), row=1, col=1)
    fig.add_trace(go.Scatter(
        x = np.array([min_x, max_x]), y = np.array([1,1])*Ei/Physics_Semiconductors.e,
        name = "Intrinsic Energy", mode='lines',
        line_color=color_Ei
        ), row=1, col=1)
    fig.add_trace(go.Scatter(
        x = np.array([min_x, max_x]), y = np.array([1,1])*Ef/Physics_Semiconductors.e,
        name = "Fermi Energy", mode='lines',
        line_color=color_Ef
        ), row=1, col=1)
    fig.add_trace(go.Scatter(
        x = gc*Physics_Semiconductors.e/(1000**3), y = E/Physics_Semiconductors.e,
        name = "DOS_cond", mode='lines',
        line_color=color_Ec, showlegend=False
        ), row=1, col=2)
    fig.add_trace(go.Scatter(
        x = gv*Physics_Semiconductors.e/(1000**3), y = E/Physics_Semiconductors.e,
        name = "DOS_val", mode='lines',
        line_color=color_Ev, showlegend=False
        ), row=1, col=2)
    fig.add_trace(go.Scatter(
        x = Ne*Physics_Semiconductors.e/(1000**3), y = E/Physics_Semiconductors.e,
        name = "Electrons (n<sub>o</sub>)", mode='lines',
        line_color=color_n
        ), row=1, col=3)
    fig.add_trace(go.Scatter(
        x = Nh*Physics_Semiconductors.e/(1000**3), y = E/Physics_Semiconductors.e,
        name = "Holes (p<sub>o</sub>)", mode='lines',
        line_color=color_p
        ), row=1, col=3)
    fig.update_layout(yaxis_title='Energy (eV)',
                      yaxis=dict(range=[min_y,max_y]), transition_duration=100, margin=dict(t=0))
    fig.update_xaxes(title_text="f(E)", range=[min_x,max_x], row=1, col=1)
    fig.update_xaxes(title_text="g(E) (/eV cm^3)", row=1, col=2)
    fig.update_xaxes(title_text="Carriers (/cm^3)", row=1, col=3)
    
    return fig


################################################################################
################################################################################
# READOUTS

def readouts_probabilitydistributions(slider_Ef, slider_T):
    readout_Ef = '{0:.4g}'.format(slider_Ef)
    readout_T = '{0:.4g}'.format(slider_T)
    return readout_Ef, readout_T

def readouts_carriers(slider_donor, slider_acceptor, slider_T, slider_emass, slider_hmass):
    readout_donor = '{0:.0e}'.format(round((10**slider_donor)/(1e15))) #/cm**3
    readout_acceptor ='{0:.0e}'.format(round((10**slider_acceptor)/(1e15))) #/cm**3
    readout_T ='{0:.4g}'.format(slider_T) #K
    readout_emass = '{0:.1f}'.format(slider_emass)
    readout_hmass = '{0:.1f}'.format(slider_hmass)
    return readout_donor, readout_acceptor, readout_T, readout_emass, readout_hmass


################################################################################
################################################################################
# FUNCTIONALITY

def togglefunctions(toggle):
    valuen = 0
    valuep = 0
    if toggle == True:
        stylen = {'color': '#7f7f7f'}
        stylep = {'color': '#57c5f7'}
        disabledn = True
        disabledp = False
    elif toggle == False:
        stylen = {'color': '#57c5f7'}
        stylep = {'color': '#7f7f7f'}
        disabledn = False
        disabledp = True
    return stylen, stylep, disabledn, disabledp, valuen, valuep


################################################################################
################################################################################
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
