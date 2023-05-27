import dash
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import pandas as pd

import Physics_Semiconductors
import Physics_BandDiagram
import Organization_IntermValues
import Organization_BuildArrays


################################################################################
################################################################################
# FIGURE

def fig0_surface(slider_Vg, slider_zins, slider_Eg, slider_epsilonsem, slider_WFmet, slider_EAsem, slider_donor, slider_acceptor, slider_emass, slider_hmass, slider_T, slider_alpha, slider_biassteps, slider_zinssteps):


    #########################################################
    # Input values
    Vg,zins,Eg,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T,sampletype,biassteps,zinssteps,Vg_array,zins_array=Organization_IntermValues.Surface_inputvalues(slider_Vg,slider_zins+6,slider_alpha,slider_Eg,slider_epsilonsem,slider_WFmet,slider_EAsem,slider_donor,slider_acceptor,slider_emass,slider_hmass,slider_T,slider_biassteps,slider_zinssteps)

    # Calculations and results
    NC,NV,Ec,Ev,Ei,Ef,no,po,ni,nb,pb,CPD,LD,Vs,Es,Qs,F,regime, zsem,Vsem,Esem,Qsem, P = Organization_IntermValues.Surface_calculations(Vg,zins,Eg,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T)
    Vs_biasarray_top,F_biasarray_top,Es_biasarray_top,Qs_biasarray_top,P_biasarray_top = Organization_BuildArrays.Surface_biasarrays(Vg_array,zins,Na,Nd,epsilon_sem,T,CPD,LD,nb,pb,ni)
    #########################################################

    # Input values
    Vg,zins,Eg,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T,sampletype,biassteps,zinssteps,Vg_array,zins_array=Organization_IntermValues.Surface_inputvalues(slider_Vg,slider_zins,slider_alpha,slider_Eg,slider_epsilonsem,slider_WFmet,slider_EAsem,slider_donor,slider_acceptor,slider_emass,slider_hmass,slider_T,slider_biassteps,slider_zinssteps)

    # Calculations and results
    NC,NV,Ec,Ev,Ei,Ef,no,po,ni,nb,pb,CPD,LD,Vs,Es,Qs,F,regime, zsem,Vsem,Esem,Qsem, P = Organization_IntermValues.Surface_calculations(Vg,zins,Eg,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T)
    Vs_biasarray,F_biasarray,Es_biasarray,Qs_biasarray,P_biasarray = Organization_BuildArrays.Surface_biasarrays(Vg_array,zins,Na,Nd,epsilon_sem,T,CPD,LD,nb,pb,ni)
    Vs_zinsarray,F_zinsarray,Es_zinsarray,Qs_zinsarray,P_zinsarray = Organization_BuildArrays.Surface_zinsarrays(zins_array,Vg,Na,Nd,epsilon_sem,T,CPD,LD,nb,pb,ni)
    zgap,Vgap, zvac,Vvac, zmet,Vmet, zarray,Earray,Qarray  = Physics_BandDiagram.BandDiagram(Vg,zins,T,Nd,Na,WFmet,EAsem,epsilon_sem, ni,nb,pb,Vs,Ec,Ev,Ef,Ei,Eg,CPD, zsem,Vsem,Esem,Qsem)

    # Account for alpha
    Vg = slider_Vg*Physics_Semiconductors.e #J
    Vg_array = np.linspace(-10,10,biassteps)*Physics_Semiconductors.e #J

    #########################################################
    #########################################################
    fig0 = make_subplots(
        rows=8, cols=3, shared_yaxes=False, shared_xaxes=False,
        column_widths=[0.2, 0.2, 0.2], row_heights=[0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7],
        vertical_spacing=0.03,
        specs=[
        [{"rowspan":3}, {"rowspan":2}, {"rowspan":2}],
        [None, None, None],
        [None, {"rowspan":2}, {"rowspan":2}],
        [{}, None, None],
        [{}, {}, {}],
        [{}, {}, {}],
        [{"rowspan":2}, {"rowspan":2}, {"rowspan":2}],
        [None, None, None]])


    fig0.add_trace(go.Scatter(
        x = zsem*1e9, y = (Ev-Vsem)/Physics_Semiconductors.e,
        name = "Valence Band", mode='lines', showlegend=False,
        line_color=color_Ev
        ), row=1, col=1)
    fig0.add_trace(go.Scatter(
        x = zsem*1e9, y = (Ei-Vsem)/Physics_Semiconductors.e,
        name = "Intrinsic Energy", mode='lines', showlegend=False,
        line_color=color_Ei
        ), row=1, col=1)
    fig0.add_trace(go.Scatter(
        x = zsem*1e9, y = (Ec-Vsem)/Physics_Semiconductors.e,
        name = "Conduction Band", mode='lines', showlegend=False,
        line_color=color_Ec
        ), row=1, col=1)
    fig0.add_trace(go.Scatter(
        x = zsem*1e9, y = 0*zsem+Ef/Physics_Semiconductors.e,
        name = "Fermi Energy", mode='lines', showlegend=False,
        line_color=color_Ef
        ), row=1, col=1)
    fig0.add_trace(go.Scatter(
        x = zgap*1e9, y = Vgap/Physics_Semiconductors.e,
        name = "Insulator", mode='lines', showlegend=False,
        line_color=color_ox
        ), row=1, col=1)
    fig0.add_trace(go.Scatter(
        x = zmet*1e9, y = Vmet/Physics_Semiconductors.e,
        name = "Gate Fermi Energy", mode='lines', showlegend=False,
        line_color=color_met
        ), row=1, col=1)
    fig0.add_trace(go.Scatter(
        x = zvac*1e9, y = Vvac/Physics_Semiconductors.e,
        name = "Vacuum Energy", mode='lines', showlegend=False,
        line_color=color_vac
        ), row=1, col=1)
    fig0.add_trace(go.Scatter(
        x = zvac*1e9, y = Vvac/Physics_Semiconductors.e,
        name = "Potential", mode='lines', showlegend=False,
        line_color=color_met
        ), row=4, col=1)
    fig0.add_trace(go.Scatter(
        x = zarray*1e9, y = Earray*1e-9,
        name = "Electric Field", mode='lines', showlegend=False,
        line_color=color_met
        ), row=5, col=1)
    fig0.add_trace(go.Scatter(
        x = zarray*1e9, y = Qarray/Physics_Semiconductors.e*(1e-9)**2,
        name = "Charge Density", mode='lines', showlegend=False,
        line_color=color_met
        ), row=6, col=1)


    fig0.add_trace(go.Scatter(
        x = Vg_array/Physics_Semiconductors.e, y = Vs_biasarray/Physics_Semiconductors.e,
        name = "Contact Potential (bias)", mode='lines', showlegend=False,
        line_color=color_other
        ), row=1, col=2, secondary_y=False)
    fig0.add_trace(go.Scatter(
        x = [Vg/Physics_Semiconductors.e], y = [Vs/Physics_Semiconductors.e],
        name = "This Contact Potential (bias)", mode='markers', showlegend=False,
        marker=dict(color=color_indicator,size=10),
        ), row=1, col=2, secondary_y=False)
    fig0.add_trace(go.Scatter(
        x = Vg_array/Physics_Semiconductors.e, y = F_biasarray*(1e-9)**2*1e12,
        name = "Force (bias)", mode='lines', showlegend=False,
        line_color=color_other
        ), row=3, col=2)
    fig0.add_trace(go.Scatter(
        x = [Vg/Physics_Semiconductors.e], y = [F*(1e-9)**2*1e12],
        name = "This Force (bias)", mode='markers', showlegend=False,
        marker=dict(color=color_indicator,size=10),
        ), row=3, col=2)
    fig0.add_trace(go.Scatter(
        x = Vg_array/Physics_Semiconductors.e, y = Es_biasarray*1e-9,
        name = "Es (bias)", mode='lines', showlegend=False,
        line_color=color_other
        ), row=5, col=2)
    fig0.add_trace(go.Scatter(
        x = [Vg/Physics_Semiconductors.e], y = [Es*1e-9],
        name = "This Es (bias)", mode='markers', showlegend=False,
        marker=dict(color=color_indicator,size=10),
        ), row=5, col=2)
    fig0.add_trace(go.Scatter(
        x = Vg_array/Physics_Semiconductors.e, y = Qs_biasarray/Physics_Semiconductors.e*(1e-9)**2,
        name = "Qs (bias)", mode='lines', showlegend=False,
        line_color=color_other
        ), row=6, col=2)
    fig0.add_trace(go.Scatter(
        x = [Vg/Physics_Semiconductors.e], y = [Qs/Physics_Semiconductors.e*(1e-9)**2],
        name = "This Qs (bias)", mode='markers', showlegend=False,
        marker=dict(color=color_indicator,size=10),
        ), row=6, col=2)
    
    fig0.add_trace(go.Scatter(
        x = Vg_array/Physics_Semiconductors.e, y =np.abs(Vs_biasarray-Vs_biasarray_top),
        name = "P (bias)", mode='lines', showlegend=False,
        line_color=color_other
        ), row=7, col=2)
    fig0.add_trace(go.Scatter(
        x = [Vg/Physics_Semiconductors.e], y = [Vs],
        name = "This P (bias)", mode='markers', showlegend=False,
        marker=dict(color=color_indicator,size=10),
        ), row=7, col=2)

    fig0.add_trace(go.Scatter(
        x = zins_array*1e9, y = Vs_zinsarray/Physics_Semiconductors.e,
        name = "Contact Potential (zins)", mode='lines', showlegend=False,
        line_color=color_other
        ), row=1, col=3, secondary_y=False)
    fig0.add_trace(go.Scatter(
        x = [zins*1e9], y = [Vs/Physics_Semiconductors.e],
        name = "This Contact Potential (zins)", mode='markers', showlegend=False,
        marker=dict(color=color_indicator,size=10),
        ), row=1, col=3, secondary_y=False)
    fig0.add_trace(go.Scatter(
        x = zins_array*1e9, y = F_zinsarray*(1e-9)**2*1e12,
        name = "Force (zins)", mode='lines', showlegend=False,
        line_color=color_other
        ), row=3, col=3)
    fig0.add_trace(go.Scatter(
        x = [zins*1e9], y = [F*(1e-9)**2*1e12],
        name = "This Force (zins)", mode='markers', showlegend=False,
        marker=dict(color=color_indicator,size=10),
        ), row=3, col=3)
    fig0.add_trace(go.Scatter(
        x = zins_array*1e9, y = Es_zinsarray*1e-9,
        name = "Qs (zins)", mode='lines', showlegend=False,
        line_color=color_other
        ), row=5, col=3)
    fig0.add_trace(go.Scatter(
        x = [zins*1e9], y = [Es*1e-9],
        name = "This Qs (zins)", mode='markers', showlegend=False,
        marker=dict(color=color_indicator,size=10),
        ), row=5, col=3)
    fig0.add_trace(go.Scatter(
        x = zins_array*1e9, y = Qs_zinsarray/Physics_Semiconductors.e*(1e-9)**2,
        name = "Qs (zins)", mode='lines', showlegend=False,
        line_color=color_other
        ), row=6, col=3)
    fig0.add_trace(go.Scatter(
        x = [zins*1e9], y = [Qs/Physics_Semiconductors.e*(1e-9)**2],
        name = "This Qs (zins)", mode='markers', showlegend=False,
        marker=dict(color=color_indicator,size=10),
        ), row=6, col=3)
    fig0.add_trace(go.Scatter(
        x = zins_array*1e9, y = P_zinsarray,
        name = "P (zins)", mode='lines', showlegend=False,
        line_color=color_other
        ), row=7, col=3)
    fig0.add_trace(go.Scatter(
        x = [zins*1e9], y = [P],
        name = "This P (zins)", mode='markers', showlegend=False,
        marker=dict(color=color_indicator,size=10),
        ), row=7, col=3)
    
    fig0.add_trace(go.Scatter(
        x = Vs_biasarray/Physics_Semiconductors.e, y = np.abs(Qs_biasarray/Physics_Semiconductors.e*(1e-9)**2),
        name = "Vs-Qs", mode='lines', showlegend=False,
        line_color=color_other
        ), row=7, col=1)
    fig0.add_trace(go.Scatter(
        x = [Vs/Physics_Semiconductors.e], y = [np.abs(Qs/Physics_Semiconductors.e*(1e-9)**2)],
        name = "This Vs-Qs", mode='markers', showlegend=False,
        marker=dict(color=color_indicator,size=10),
        ), row=7, col=1)

    # Automated axis scaling
    #biasmin = -10
    #biasmax = +10
    #if biasmin<Vg and Vg>biasmax:
    #    biasrange_indexmin = find_nearest(Vg_array,biasmin)
    #    biasrange_indexmax = find_nearest(Vg_array,Vg+1)
    #elif biasmin>Vg and Vg<biasmax:
    #    biasrange_indexmin = find_nearest(Vg_array,Vg-1)
    #    biasrange_indexmax = find_nearest(Vg_array,biasmax)
    #else:
    #    biasrange_indexmin = find_nearest(Vg_array,biasmin)
    #    biasrange_indexmax = find_nearest(Vg_array,biasmax)

    fig0.update_layout(transition_duration=300, height=1000, margin=dict(t=0), showlegend=False)

    fig0.update_xaxes(title_standoff=5, title_text="", row=1, col=1)
    fig0.update_xaxes(title_standoff=5, title_text="", row=3, col=1)
    fig0.update_xaxes(title_standoff=5, title_text="z (nm)", row=6, col=1)
    fig0.update_xaxes(title_standoff=5, title_text="", row=1, col=2, range=[-10, 10])
    fig0.update_xaxes(title_standoff=5, title_text="", row=3, col=2, range=[-10, 10])
    fig0.update_xaxes(title_standoff=5, title_text= "Gate Bias (eV)",row=7,col=2, range=[-10, 10])
    fig0.update_xaxes(title_standoff=5, title_text="", row=1, col=3)
    fig0.update_xaxes(title_standoff=5, title_text="", row=3, col=3)
    fig0.update_xaxes(title_standoff=5, title_text= "Insulator Thickness (nm)", range=[min(zins_array*1e9), max(zins_array*1e9)], row=7, col=3)
    fig0.update_xaxes(title_standoff=5, title_text="Vs (eV)", row=7, col=1)

    fig0.update_yaxes(title_standoff=5, title_text="E (eV)", row=1, col=1)
    fig0.update_yaxes(title_standoff=5, title_text="V (V)", row=4, col=1)
    fig0.update_yaxes(title_standoff=5, title_text="E (V/nm)", row=5, col=1)
    fig0.update_yaxes(title_standoff=5, title_text="Q (e/nm^2)", row=6, col=1)
    fig0.update_yaxes(title_standoff=5, title_text="Vs (eV)", row=1, col=2)
    fig0.update_yaxes(title_standoff=5, title_text="F (pN/nm^2)", row=3, col=2)#, range=[min(F_biasarray[biasrange_indexmin], F_biasarray[biasrange_indexmax]), max(F_biasarray)])
    fig0.update_yaxes(title_standoff=5, title_text="Es (V/nm)", row=5, col=2)
    fig0.update_yaxes(title_standoff=5, title_text="Qs (e/nm^2)", row=6, col=2)
    fig0.update_yaxes(title_standoff=5, title_text="Vs (eV)", row=1, col=3)
    fig0.update_yaxes(title_standoff=5, title_text="F (pN/nm^2)", row=3, col=3)#, range=[min(F_biasarray[biasrange_indexmin], F_biasarray[biasrange_indexmax]), max(F_biasarray)])
    fig0.update_yaxes(title_standoff=5, title_text="Es (V/nm)", row=5, col=3)
    fig0.update_yaxes(title_standoff=5, title_text="Qs (e/nm^2)", row=6, col=3)
    fig0.update_yaxes(title_standoff=5, title_text="|Qs| (e/nm^2)", row=7, col=1)
    fig0.update_yaxes(title_standoff=5, title_text="P", row=7, col=2)
    fig0.update_yaxes(title_standoff=5, title_text="P", row=7, col=3)

   
   
    #########################################################
    #########################################################
    zQ = 1

    if regime == 1:
        regime = "accumulation"
    elif regime == 2:
        regime = "flatband"
    elif regime == 3:
        regime = "depletion"
    elif regime == 4:
        regime = "threshold"
    elif regime == 5:
        regime = "weak inversion"
    elif regime == 6:
        regime = "strong inversion"

    return fig0, regime, format(ni, ".1E"), format(LD*10**9, ".1f"), format(zQ, ".1f")




################################################################################
################################################################################
# READOUTS

def readouts_surface(slider_Vg, slider_zins, slider_Eg, slider_epsilonsem, slider_WFmet, slider_EAsem, slider_donor, slider_acceptor, slider_emass, slider_hmass, slider_T, slider_alpha, slider_biassteps, slider_zinssteps):
    readout_Vg = '{0:.4g}'.format(slider_Vg)
    readout_zins = '{0:.1f}'.format(slider_zins)
    readout_Eg = '{0:.1f}'.format(slider_Eg)
    readout_epsilonsem = '{0:.1f}'.format(slider_epsilonsem)
    readout_WFmet = '{0:.2f}'.format(slider_WFmet)
    readout_EAsem = '{0:.2f}'.format(slider_EAsem)
    readout_donor = '{0:.2e}'.format(round((10**slider_donor)/(1e15))) #/cm**3
    readout_acceptor ='{0:.2e}'.format(round((10**slider_acceptor)/(1e15))) #/cm**3
    readout_emass = '{0:.1f}'.format(slider_emass)
    readout_hmass = '{0:.1f}'.format(slider_hmass)
    readout_T = '{0:.4g}'.format(slider_T)
    readout_alpha = '{0:.4g}'.format(slider_alpha)
    readout_biassteps = '{0:.4g}'.format(slider_biassteps)
    readout_zinssteps = '{0:.4g}'.format(slider_zinssteps)
    return readout_Vg, readout_zins, readout_Eg, readout_epsilonsem, readout_WFmet, readout_EAsem, readout_donor, readout_acceptor, readout_emass, readout_hmass, readout_T, readout_alpha, readout_biassteps, readout_zinssteps


################################################################################
################################################################################
# FUNCTIONALITY

def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return idx

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
