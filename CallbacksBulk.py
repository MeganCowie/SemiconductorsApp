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
    Ef, T = slider_Ef, slider_T

    E = np.arange(5000)/1000
    fc,fv = Physics_Semiconductors.fcfv(E, Ef, T)
    g = Physics_Semiconductors.MaxwellBoltzmann(E, Ef, T)
    min_x, max_x, min_y, max_y = 0, 1, 0, 1.5

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x = E, y = fc,
        name = "Fermi Dirac", mode='lines',
        line_color=color_fc
        ))
    fig.add_trace(go.Scatter(
        x = E, y = g,
        name = "Maxwell Boltzmann", mode='lines',
        line_color=color_other
        ))
    fig.add_trace(go.Scatter(
        x = np.array([1,1])*Ef, y = np.array([min_y, max_y]),
        name = "Ef", mode='lines',
        line_color=color_Ef
        ))
    fig.add_trace(go.Scatter(
        x = np.array([1,1])*3*sp.value('Boltzmann constant in eV/K')*T+Ef, y = np.array([min_y, max_y]),
        name = "3kBT+Ef", mode='lines',
        line_color=color_vac
        ))
    fig.update_layout(xaxis_title='Energy (eV)', yaxis_title='f(E)',
                      xaxis=dict(range=[min_x,max_x]), yaxis=dict(range=[min_y,max_y]),
                      transition_duration=500, margin=dict(t=0))
    return fig





def fig_carrierintegrals(slider_Ef, slider_T,slider_gc,slider_gv):

    # input (slider) parameters
    Ef, T = slider_Ef, slider_T

    E = np.arange(5000)/5000+0.000000001
    fc,fv = Physics_Semiconductors.fcfv(E, Ef, T)
    min_x, max_x, min_y, max_y = 0, 1, 0, 1

    gc_E=E-Ef-0.03
    gv_E=-E+Ef-0.03
    gc_E[gc_E<0] = 0
    gv_E[gv_E<0] = 0

    gc = slider_gc*(gc_E)**(1/2)
    gv = slider_gv*(gv_E)**(1/2)

    fcgc=fc*gc
    fvgv=(1-fc)*gv

    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Scatter(
        x = np.array([1,1])*Ef, y = np.array([min_y, max_y]),
        name = "Ef", mode='lines',
        line_color=color_Ef
        ))
    fig.add_trace(go.Scatter(
        x = E, y = fc,
        name = "f<sub>f</sub>(E)", mode='lines',
        line_color=color_fc
        ))
    fig.add_trace(go.Scatter(
        x = E, y = gc,
        name = "g<sub>c</sub>(E)", mode='lines',
        line_color=color_Ec
        ))
    fig.add_trace(go.Scatter(
        x = E, y = gv,
        name = "g<sub>v</sub>(E)", mode='lines',
        line_color=color_Ev
        ),secondary_y=True)
    fig.add_trace(go.Scatter(
        x=E[np.where(E>=Ef)], y=fcgc[np.where(E>=Ef)],
        name = "n", mode= 'none',
        fill='tozeroy', fillcolor=color_n,
        ))
    fig.add_trace(go.Scatter(
        x=E[np.where(E<=Ef)], y=fvgv[np.where(E<=Ef)],
        name = "p", mode= 'none',
        fill='tozeroy', fillcolor=color_p,
        ),secondary_y=True)
    fig.update_layout(xaxis_title='Energy (eV)',
                      xaxis=dict(range=[min_x,max_x]),
                      yaxis=dict(range=[min_y,max_y],title='f(E)'),
                      yaxis2=dict(range=[max_y,min_y],title='1-f(E)',side='right'),
                      transition_duration=500, margin=dict(t=0))
    return fig





def fig_carriers(slider_donor, slider_acceptor, slider_T, slider_emass, slider_hmass, toggle_type):

    # input (slider) parameters
    ND_ion=round((10**slider_donor*10**8))/(1000**3) #cm-3
    NA_ion=round((10**slider_acceptor*10**8)/(1000**3)) #cm-3
    T = slider_T #K
    mn = slider_emass*Physics_Semiconductors.me #kg
    mp = slider_hmass*Physics_Semiconductors.me #kg
    type=toggle_type

    E = np.arange(5000)/1000
    Ec,Ev = 2,1

    NC,NV = Physics_Semiconductors.NCNV(T, mn, mp)
    NC = NC/(100**3)
    NV = NV/(100**3)

    Eg = Physics_Semiconductors.Eg(Ec, Ev)
    Ei = Physics_Semiconductors.Ei(Ev, Ec, T, mn, mp)
    Ef = Physics_Semiconductors.Ef(NC, NV, Ec, Ev, T, ND_ion, NA_ion)

    gc, gv = Physics_Semiconductors.gcgv(E, Ec, Ev, mn, mp)
    fc,fv = Physics_Semiconductors.fcfv(E, Ef, T)

    ni = Physics_Semiconductors.ni(NC, NV, Eg, T)
    n,p = Physics_Semiconductors.nopo(NC, NV, Ec, Ev, Ef, T)
    Ne,Nh = Physics_Semiconductors.NeNh(E, fc, fv, gc, gv, Ec, Ev)

    min_x, max_x, min_y, max_y = 0, 1, 0, 3

    fig = make_subplots(
        rows=1, cols=3, shared_yaxes=True,
        column_widths=[0.2, 0.1, 0.1])
    fig.add_trace(go.Scatter(
        x = fc, y = E,
        name = "f(E)", mode='lines',
        line_color=color_fc
        ), row=1, col=1)
    fig.add_trace(go.Scatter(
        x = fv, y = E,
        name = "1-f(E)", mode='lines',
        line_color=color_fv
        ), row=1, col=1)
    fig.add_trace(go.Scatter(
        x = np.array([min_x, max_x]), y = np.array([1,1])*Ec,
        name = "Conduction Band", mode='lines',
        line_color=color_Ec
        ), row=1, col=1)
    fig.add_trace(go.Scatter(
        x = np.array([min_x, max_x]), y = np.array([1,1])*Ev,
        name = "Valence Band", mode='lines',
        line_color=color_Ev
        ), row=1, col=1)
    fig.add_trace(go.Scatter(
        x = np.array([min_x, max_x]), y = np.array([1,1])*Ef,
        name = "Fermi Energy", mode='lines',
        line_color=color_Ef
        ), row=1, col=1)
    fig.add_trace(go.Scatter(
        x = np.array([min_x, max_x]), y = np.array([1,1])*Ei,
        name = "Intrinsic Energy", mode='lines',
        line_color=color_Ei
        ), row=1, col=1)
    fig.add_trace(go.Scatter(
        x = gc, y = E,
        name = "DOS_cond", mode='lines',
        line_color=color_Ec, showlegend=False
        ), row=1, col=2)
    fig.add_trace(go.Scatter(
        x = gv, y = E,
        name = "DOS_val", mode='lines',
        line_color=color_Ev, showlegend=False
        ), row=1, col=2)
    fig.add_trace(go.Scatter(
        x = Ne, y = E,
        name = "Electrons", mode='lines',
        line_color=color_n
        ), row=1, col=3)
    fig.add_trace(go.Scatter(
        x = Nh, y = E,
        name = "Holes", mode='lines',
        line_color=color_p
        ), row=1, col=3)
    fig.update_layout(yaxis_title='Energy (eV)',
                      yaxis=dict(range=[min_y,max_y]), transition_duration=100, margin=dict(t=0))
    fig.update_xaxes(title_text="f(E)", range=[min_x,max_x], row=1, col=1)
    fig.update_xaxes(title_text="g(E)", row=1, col=2)
    fig.update_xaxes(title_text="Carriers", row=1, col=3)
    return fig


################################################################################
################################################################################
# READOUTS

def readouts_probabilitydistributions(slider_Ef, slider_T):
    readout_Ef = '{0:.4g}'.format(slider_Ef)
    readout_T = '{0:.4g}'.format(slider_T)
    return readout_Ef, readout_T

def readouts_carriers(slider_donor, slider_acceptor, slider_T, slider_emass, slider_hmass):
    readout_donor = '{0:.0e}'.format(round((10**slider_donor*10**8)/(1000**3)))
    readout_acceptor ='{0:.0e}'.format(round((10**slider_acceptor*10**8)/(1000**3)))
    readout_T ='{0:.4g}'.format(slider_T)
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
        stylen = {'color': '#7f7f7f', 'fontSize': 20, 'text-align': 'right'}
        stylep = {'color': '#57c5f7', 'fontSize': 20, 'text-align': 'right'}
        disabledn = True
        disabledp = False
    elif toggle == False:
        stylen = {'color': '#57c5f7', 'fontSize': 20, 'text-align': 'right'}
        stylep = {'color': '#7f7f7f', 'fontSize': 20, 'text-align': 'right'}
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
