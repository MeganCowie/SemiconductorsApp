import dash
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

import Physics_SemiconductorSurface
import Physics_SurfacepotForce
import Physics_AFM


################################################################################
################################################################################
# FIGURE

def fig_AFM(slider_Vg, slider_zins, slider_bandgap, slider_epsilonsem, slider_WFmet, slider_EAsem, slider_donor, slider_acceptor, slider_emass, slider_hmass, slider_T, slider_amplitude, calculatebutton):

    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if 'AFMbutton_Calculate' in changed_id:

        # input (slider) parameters
        Vg = slider_Vg
        zins = slider_zins*1e-7 # cm
        bandgap = slider_bandgap
        epsilon_sem = slider_epsilonsem
        WFmet = slider_WFmet #eV
        EAsem = slider_EAsem #eV
        Nd = round((10**slider_donor*10**8)/(1000**3))
        Na = round((10**slider_acceptor*10**8)/(1000**3))
        mn = slider_emass*Physics_SemiconductorSurface.me # kg
        mp = slider_hmass*Physics_SemiconductorSurface.me # kg
        T = slider_T # K

        amplitude = slider_amplitude #nm
        steps = 100

        Vg_array = np.arange(2000)/100-10 #eV
        zins_array = (np.arange(200)/10+0.05)*1e-7 #cm
        time_AFMarray = Physics_AFM.time_AFMarray(steps)
        zins_AFMarray = Physics_AFM.zins_AFMarray(time_AFMarray,amplitude,zins)

        Vs_AFMarray, F_AFMarray = Physics_AFM.SurfacepotForce_AFMarray(1,zins_AFMarray,   Vg,zins,bandgap,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T)
        Ec_AFMarray,Ev_AFMarray,Ei_AFMarray,Ef_AFMarray,zsem_AFMarray,psi_AFMarray,Insulatorx_AFMarray,Insulatory_AFMarray,Vacuumx_AFMarray,Vacuumy_AFMarray,Gatex_AFMarray,Gatey_AFMarray = Physics_AFM.BandDiagram_AFMarray(Vs_AFMarray,zins_AFMarray,   Vg,zins,bandgap,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T)

        Vs_biasarray, F_biasarray, Vs_zinsarray, F_zinsarray = Physics_SurfacepotForce.VsF_arrays(Vg_array,zins_array,   Vg,zins,bandgap,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T)



        #########################################################
        #########################################################
        fig = make_subplots(
            rows=3, cols=2, shared_yaxes=False, shared_xaxes=False,
            column_widths=[0.3, 0.7], row_heights=[1,1,1],
            specs=[[{}, {}], [{}, {}], [{}, {}]])

        fig.add_trace(go.Scatter(
            y = zsem_AFMarray[0]*1e7, x = Ev_AFMarray[0]-psi_AFMarray[0],
            name = "ThisValenceBand", mode='lines', showlegend=False,
            line_color=color_Ev
            ), row=1, col=1)
        fig.add_trace(go.Scatter(
            y = zsem_AFMarray[0]*1e7, x = Ei_AFMarray[0]-psi_AFMarray[0],
            name = "ThisIntrinsicEnergy", mode='lines', showlegend=False,
            line_color=color_Ei
            ), row=1, col=1)
        fig.add_trace(go.Scatter(
            y = zsem_AFMarray[0]*1e7, x = Ec_AFMarray[0]-psi_AFMarray[0],
            name = "ThisConductionBand", mode='lines', showlegend=False,
            line_color=color_Ec
            ), row=1, col=1)
        fig.add_trace(go.Scatter(
            y = zsem_AFMarray[0]*1e7, x = 0*zsem_AFMarray[0]+Ef_AFMarray[0],
            name = "ThisFermiEnergy", mode='lines', showlegend=False,
            line_color=color_Ef
            ), row=1, col=1)
        fig.add_trace(go.Scatter(
            y = Insulatorx_AFMarray[0], x = Insulatory_AFMarray[0],
            name = "ThisInsulator", mode='lines', showlegend=False,
            line_color=color_ox
            ), row=1, col=1)
        fig.add_trace(go.Scatter(
            y = Gatex_AFMarray[0], x = Gatey_AFMarray[0],
            name = "ThisGateFermiEnergy", mode='lines', showlegend=False,
            line_color=color_met
            ), row=1, col=1)
        fig.add_trace(go.Scatter(
            y = Vacuumx_AFMarray[0], x = Vacuumy_AFMarray[0],
            name = "ThisVacuumEnergy", mode='lines', showlegend=False,
            line_color=color_vac
            ), row=1, col=1)


        fig.add_trace(go.Scatter(
            x = zins_array*1e7, y = Vs_zinsarray,
            name = "Contact Potential", mode='lines', showlegend=False,
            line_color=color_vac
            ), row=2, col=1)
        fig.add_trace(go.Scatter(
            x = [zins_AFMarray[0]*1e7], y = [Vs_AFMarray[0]],
            name = "This Contact Potential", mode='markers', marker_line_width=1, showlegend=False,
            marker=dict(color=color_indicator,size=10),
            ), row=2, col=1)
        fig.add_trace(go.Scatter(
            x = zins_array*1e7, y = F_zinsarray,
            name = "Force", mode='lines', showlegend=False,
            line_color=color_vac
            ), row=3, col=1)
        fig.add_trace(go.Scatter(
            x = [zins_AFMarray[0]*1e7], y = [F_AFMarray[0]],
            name = "This Force", mode='markers', marker_line_width=1, showlegend=False,
            marker=dict(color=color_indicator,size=10),
            ), row=3, col=1)

        fig.add_trace(go.Scatter(
            x = time_AFMarray, y = zins_AFMarray*1e7,
            name = "PositionTime", mode='lines', showlegend=False,
            line_color=color_other
            ), row=1, col=2),
        fig.add_trace(go.Scatter(
            x = [time_AFMarray[0]], y = [zins_AFMarray[0]*1e7],
            name = "ThisPositionTime", mode='markers',
            marker=dict(color=color_indicator,size=10),
            ), row=1, col=2)
        fig.add_trace(go.Scatter(
            x = time_AFMarray, y = Vs_AFMarray,
            name = "SurfacePotentialTime", mode='lines', showlegend=False,
            line_color=color_other
            ), row=2, col=2),
        fig.add_trace(go.Scatter(
            x = [time_AFMarray[0]], y = [Vs_AFMarray[0]],
            name = "ThisSurfacePotentialTime", mode='markers',
            marker=dict(color=color_indicator,size=10),
            ), row=2, col=2)
        fig.add_trace(go.Scatter(
            x = time_AFMarray, y = F_AFMarray,
            name = "ForceTime", mode='lines', showlegend=False,
            line_color=color_other
            ), row=3, col=2)
        fig.add_trace(go.Scatter(
            x = [time_AFMarray[0]], y = [F_AFMarray[0]],
            name = "ThisForceTime", mode='markers',
            marker=dict(color=color_indicator,size=10),
            ), row=3, col=2)

        fig.frames=[
            go.Frame(data=[

                go.Scatter(y=zsem_AFMarray[step]*1e7, x=Ev_AFMarray[step]-psi_AFMarray[step],mode="lines", line_color=color_Ev),
                go.Scatter(y=zsem_AFMarray[step]*1e7, x=Ei_AFMarray[step]-psi_AFMarray[step],mode="lines", line_color=color_Ei),
                go.Scatter(y=zsem_AFMarray[step]*1e7, x=Ec_AFMarray[step]-psi_AFMarray[step],mode="lines", line_color=color_Ec),
                go.Scatter(y=zsem_AFMarray[step]*1e7, x = 0*zsem_AFMarray[step]+Ef_AFMarray[step],mode="lines", line_color=color_Ef),
                go.Scatter(y=Insulatorx_AFMarray[step], x=Insulatory_AFMarray[step],mode="lines", line_color=color_ox),
                go.Scatter(y=Gatex_AFMarray[step], x=Gatey_AFMarray[step],mode="lines", line_color=color_met),
                go.Scatter(y=Vacuumx_AFMarray[step], x=Vacuumy_AFMarray[step],mode="lines", line_color=color_vac),

                go.Scatter(x=zins_array*1e7, y=Vs_zinsarray,mode="lines", line_color=color_vac),
                go.Scatter(x=[zins_AFMarray[step]*1e7], y=[Vs_AFMarray[step]],mode="markers", marker=dict(color=color_indicator, size=10)),
                go.Scatter(x=zins_array*1e7, y=F_zinsarray,mode="lines", line_color=color_vac),
                go.Scatter(x=[zins_AFMarray[step]*1e7], y=[F_AFMarray[step]],mode="markers", marker=dict(color=color_indicator, size=10)),

                go.Scatter(x=time_AFMarray,y=zins_AFMarray*1e7,mode="lines", line_color=color_other),
                go.Scatter(x=[time_AFMarray[step]],y=[zins_AFMarray[step]*1e7],mode="markers", marker=dict(color=color_indicator, size=10)),
                go.Scatter(x=time_AFMarray,y=Vs_AFMarray,mode="lines", line_color=color_other),
                go.Scatter(x=[time_AFMarray[step]],y=[Vs_AFMarray[step]],mode="markers", marker=dict(color=color_indicator, size=10)),
                go.Scatter(x=time_AFMarray,y=F_AFMarray,mode="lines", line_color=color_other),
                go.Scatter(x=[time_AFMarray[step]],y=[F_AFMarray[step]],mode="markers", marker=dict(color=color_indicator, size=10)),
                ],traces=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16])
                for step in range(steps)]


    ############################################################################

    else:

        fig = make_subplots(
            rows=3, cols=2, shared_yaxes=False, shared_xaxes=False,
            column_widths=[0.3, 0.7], row_heights=[1,1,1],
            specs=[[{}, {}], [{}, {}], [{}, {}]])
        fig.add_trace(go.Scatter(y=[], x=[]), row=1, col=1)
        fig.add_trace(go.Scatter(y=[], x=[]), row=2, col=1)
        fig.add_trace(go.Scatter(y=[], x=[]), row=3, col=1)
        fig.add_trace(go.Scatter(y=[], x=[]), row=1, col=2)
        fig.add_trace(go.Scatter(y=[], x=[]), row=2, col=2)
        fig.add_trace(go.Scatter(y=[], x=[]), row=3, col=2)

    ############################################################################

    fig.update_layout(
    updatemenus=[
        dict(visible = True, type="buttons", buttons=[dict(label="Play" , method="animate", args=[None, {"frame": {"duration": 100, "redraw": True},"fromcurrent": True, "transition": {"duration": 0}}])],x=0,y=1.1),
        dict(type="buttons", buttons=[dict(label="Pause", method="animate", args=[[None], {"frame": {"duration": 0, "redraw": False},"mode": "immediate","transition": {"duration": 0}}])],x=0.1,y=1.1)
        ])

    fig.update_layout(transition_duration=300, height=800,)
    fig.update_layout({"showlegend": False},
        annotations=[
            dict(x=0, y=1.03, xref="paper", yref="paper", showarrow=False, font=dict(size=5), xanchor="left", text=" "),
            dict(x=0, y=0.65, xref="paper", yref="paper", showarrow=False, font=dict(size=5), xanchor="left", text=" "),
            dict(x=0, y=0.27, xref="paper", yref="paper", showarrow=False, font=dict(size=5), xanchor="left", text=" "),
            dict(x=0.37, y=1.03, xref="paper", yref="paper", showarrow=False, font=dict(size=5), xanchor="left", text=" "),
            dict(x=0.37, y=0.65, xref="paper", yref="paper", showarrow=False, font=dict(size=5), xanchor="left", text=" "),
            dict(x=0.37, y=0.27, xref="paper", yref="paper", showarrow=False, font=dict(size=5), xanchor="left", text=" "),
        ])


    fig.update_yaxes(row=1, col=1, title_text= "Insulator Thickness (nm)", range=[-20, 20])
    fig.update_yaxes(row=2, col=1, title_text= "Contact Potential (eV)")
    fig.update_yaxes(row=3, col=1, title_text= "Force (N/cm^2)")
    fig.update_yaxes(row=1, col=2)
    fig.update_yaxes(row=2, col=2)
    fig.update_yaxes(row=3, col=2)

    fig.update_xaxes(row=1, col=1, title_text= "Energy (eV)")
    fig.update_xaxes(row=2, col=1, title_text= "Insulator Thickness (nm)")
    fig.update_xaxes(row=3, col=1, title_text= "Insulator Thickness (nm)")
    fig.update_xaxes(row=1, col=2, title_text= "Time", showticklabels=False, range=[0, 4*np.pi])
    fig.update_xaxes(row=2, col=2, title_text= "Time", showticklabels=False, range=[0, 4*np.pi])
    fig.update_xaxes(row=3, col=2, title_text= "Time", showticklabels=False, range=[0, 4*np.pi])



    return fig



################################################################################
################################################################################
# READOUTS

def readouts_AFM(slider_Vg, slider_zins, slider_amplitude):
    readout_Vg = '{0:.4g}'.format(slider_Vg)
    readout_zins = '{0:.1f}'.format(slider_zins)
    readout_amplitude = '{0:.1f}'.format(slider_amplitude)
    return readout_Vg, readout_zins, readout_amplitude

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
