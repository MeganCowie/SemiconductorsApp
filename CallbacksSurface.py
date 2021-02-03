import dash
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

import Physics_Semiconductors
import Physics_SurfacepotForce
import Physics_BandDiagram


################################################################################
################################################################################
# FIGURE

def fig_surface(slider_Vg, slider_zins, slider_bandgap, slider_epsilonsem, slider_WFmet, slider_EAsem, slider_donor, slider_acceptor, slider_emass, slider_hmass, slider_T):

    # input (slider) parameters
    Vg = slider_Vg
    zins = slider_zins*1e-7 # cm
    bandgap = slider_bandgap
    epsilon_sem = slider_epsilonsem
    WFmet = slider_WFmet #eV
    EAsem = slider_EAsem #eV
    Nd = round((10**slider_donor*10**8)/(1000**3))
    Na = round((10**slider_acceptor*10**8)/(1000**3))
    mn = slider_emass*Physics_Semiconductors.me # kg
    mp = slider_hmass*Physics_Semiconductors.me # kg
    T = slider_T # K

    Vg_array = np.arange(200)/10-10 #eV
    zins_array = (np.arange(200)/10+0.05)*1e-7 #cm


    Vs, F = Physics_SurfacepotForce.VsF(1,   Vg,zins,bandgap,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T)
    Vs_biasarray, F_biasarray, Vs_zinsarray, F_zinsarray = Physics_SurfacepotForce.VsF_arrays(Vg_array,zins_array,   Vg,zins,bandgap,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T)

    Ec, Ev, Ei, Ef, zsem, psi, z_array, E_array, Q_array, Insulatorx, Insulatory, Vacuumx, Vacuumy, Gatex, Gatey, ni = Physics_BandDiagram.BandDiagram(Vs,   Vg,zins,bandgap,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T)


    #########################################################
    #########################################################
    fig = make_subplots(
        rows=5, cols=3, shared_yaxes=False, shared_xaxes=True,
        column_widths=[0.2, 0.2, 0.2], row_heights=[0.5, 1, 0.5, 0.5, 0.5],
        specs=[[{"rowspan":2}, {"rowspan":2}, {"rowspan":2}], [None, {}, None], [{}, {"rowspan":3}, {"rowspan": 3}], [{}, None, None], [{}, None, None]])
    fig.add_trace(go.Scatter(
        x = zsem*1e7, y = Ev-psi,
        name = "Valence Band", mode='lines', showlegend=False,
        line_color=color_Ev
        ), row=1, col=1)
    fig.add_trace(go.Scatter(
        x = zsem*1e7, y = Ei-psi,
        name = "Intrinsic Energy", mode='lines', showlegend=False,
        line_color=color_Ei
        ), row=1, col=1)
    fig.add_trace(go.Scatter(
        x = zsem*1e7, y = Ec-psi,
        name = "Conduction Band", mode='lines', showlegend=False,
        line_color=color_Ec
        ), row=1, col=1)
    fig.add_trace(go.Scatter(
        x = zsem*1e7, y = 0*zsem+Ef,
        name = "Fermi Energy", mode='lines', showlegend=False,
        line_color=color_Ef
        ), row=1, col=1)
    fig.add_trace(go.Scatter(
        x = Insulatorx, y = Insulatory,
        name = "Insulator", mode='lines', showlegend=False,
        line_color=color_ox
        ), row=1, col=1)
    fig.add_trace(go.Scatter(
        x = Gatex, y = Gatey,
        name = "Gate Fermi Energy", mode='lines', showlegend=False,
        line_color=color_met
        ), row=1, col=1)
    fig.add_trace(go.Scatter(
        x = Vacuumx, y = Vacuumy,
        name = "Vacuum Energy", mode='lines', showlegend=False,
        line_color=color_vac
        ), row=1, col=1)
    fig.add_trace(go.Scatter(
        x = Vacuumx, y = Vacuumy,
        name = "Potential", mode='lines', showlegend=False,
        line_color=color_met
        ), row=3, col=1)
    fig.add_trace(go.Scatter(
        x = z_array, y = E_array,
        name = "Electric Field", mode='lines', showlegend=False,
        line_color=color_met
        ), row=4, col=1)
    fig.add_trace(go.Scatter(
        x = z_array, y = Q_array,
        name = "Charge Density", mode='lines', showlegend=False,
        line_color=color_met
        ), row=5, col=1)

    fig.add_trace(go.Scatter(
        x = Vg_array, y = Vs_biasarray,
        name = "Contact Potential (bias)", mode='lines', showlegend=False,
        line_color=color_other
        ), row=1, col=2)
    fig.add_trace(go.Scatter(
        x = [Vg], y = [Vs],
        name = "This Contact Potential (bias)", mode='markers', showlegend=False,
        marker=dict(color=color_indicator,size=10),
        ), row=1, col=2)
    fig.add_trace(go.Scatter(
        x = Vg_array, y = F_biasarray,
        name = "Force (bias)", mode='lines', showlegend=False,
        line_color=color_other
        ), row=3, col=2)
    fig.add_trace(go.Scatter(
        x = [Vg], y = [F],
        name = "This Force (bias)", mode='markers', showlegend=False,
        marker=dict(color=color_indicator,size=10),
        ), row=3, col=2)
    fig.add_trace(go.Scatter(
        x = zins_array*1e7, y = Vs_zinsarray,
        name = "Contact Potential (zins)", mode='lines', showlegend=False,
        line_color=color_other
        ), row=1, col=3)
    fig.add_trace(go.Scatter(
        x = [zins*1e7], y = [Vs],
        name = "This Contact Potential (zins)", mode='markers', showlegend=False,
        marker=dict(color=color_indicator,size=10),
        ), row=1, col=3)
    fig.add_trace(go.Scatter(
        x = zins_array*1e7, y = F_zinsarray,
        name = "Force (zins)", mode='lines', showlegend=False,
        line_color=color_other
        ), row=3, col=3)
    fig.add_trace(go.Scatter(
        x = [zins*1e7], y = [F],
        name = "This Force (zins)", mode='markers', showlegend=False,
        marker=dict(color=color_indicator,size=10),
        ), row=3, col=3)

    fig.update_layout(transition_duration=300, height=800,margin=dict(t=0), showlegend=False)

    fig.update_xaxes(title_text="", row=1, col=1)
    fig.update_xaxes(title_text="", row=3, col=1)
    fig.update_xaxes(title_text="", row=4, col=1)
    fig.update_xaxes(title_text="z (nm)", row=5, col=1, range=[-zins*1e7-10, 20])
    fig.update_xaxes(title_text="", row=1, col=2)
    fig.update_xaxes(title_text= "Gate Bias (eV)", range=[min(Vg_array), max(Vg_array)], row=3, col=2)
    fig.update_xaxes(title_text="", row=1, col=3)
    fig.update_xaxes(title_text= "Insulator Thickness (nm)", range=[min(zins_array*1e7), max(zins_array*1e7)], row=3, col=3)

    fig.update_yaxes(title_text="Energy (eV)", row=1, col=1, title_standoff = 5)
    fig.update_yaxes(title_text="Potential (V)", row=3, col=1, title_standoff = 5)
    fig.update_yaxes(title_text="Electric Field", row=4, col=1, title_standoff = 5)
    fig.update_yaxes(title_text="Charge", row=5, col=1, title_standoff = 5)
    fig.update_yaxes(title_text="Contact Potential (eV)", row=1, col=2, title_standoff = 5, range=[min(np.append(Vs_biasarray, Vs_zinsarray)), max(np.append(Vs_biasarray, Vs_zinsarray))])
    fig.update_yaxes(title_text="Force (N/nm^2)", row=3, col=2, title_standoff = 5, range=[min(F_biasarray), max(F_biasarray)])
    fig.update_yaxes(title_text="Contact Potential (eV)", row=1, col=3, title_standoff = 5, range=[min(np.append(Vs_biasarray, Vs_zinsarray)), max(np.append(Vs_biasarray, Vs_zinsarray))])
    fig.update_yaxes(title_text="Force (N/nm^2)", row=3, col=3, title_standoff = 5, range=[min(F_biasarray), max(F_biasarray)])

    return fig, format(ni, ".1E")




################################################################################
################################################################################
# READOUTS

def readouts_surface(slider_Vg, slider_zins, slider_bandgap, slider_epsilonsem, slider_WFmet, slider_EAsem, slider_donor, slider_acceptor, slider_emass, slider_hmass, slider_T):
    readout_Vg = '{0:.4g}'.format(slider_Vg)
    readout_zins = '{0:.0f}'.format(slider_zins)
    readout_bandgap = '{0:.1f}'.format(slider_bandgap)
    readout_epsilonsem = '{0:.1f}'.format(slider_epsilonsem)
    readout_WFmet = '{0:.2f}'.format(slider_WFmet)
    readout_EAsem = '{0:.2f}'.format(slider_EAsem)
    readout_donor = '{0:.0e}'.format(round((10**slider_donor*10**8)/(1000**3)))
    readout_acceptor = '{0:.0e}'.format(round((10**slider_acceptor*10**8)/(1000**3)))
    readout_emass = '{0:.1f}'.format(slider_emass)
    readout_hmass = '{0:.1f}'.format(slider_hmass)
    readout_T = '{0:.4g}'.format(slider_T)
    return readout_Vg, readout_zins, readout_bandgap, readout_epsilonsem, readout_WFmet, readout_EAsem, readout_donor, readout_acceptor, readout_emass, readout_hmass, readout_T


################################################################################
################################################################################
# FUNCTIONALITY


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
