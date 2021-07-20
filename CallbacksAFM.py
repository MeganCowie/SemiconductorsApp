import dash
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import pandas as pd

import Physics_Semiconductors
import Physics_SurfacepotForce
import Physics_AFMoscillation
import Physics_FreqshiftDissipation


################################################################################
################################################################################
# FIGURE: ncAFM oscillations

def fig_AFM1(slider_Vg,slider_zins,slider_bandgap,slider_epsilonsem,slider_WFmet,slider_EAsem,slider_donor,slider_acceptor,slider_emass,slider_hmass,slider_T, slider_amplitude,slider_resfreq,slider_hop,slider_lag,calculatebutton,toggle_sampletype,toggle_RTN):

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
        mn = slider_emass*Physics_Semiconductors.me # kg
        mp = slider_hmass*Physics_Semiconductors.me # kg
        T = slider_T # K
        sampletype = toggle_sampletype #false = semiconducting, true = metallic
        RTN = toggle_RTN #false = off, true = on
        amplitude = slider_amplitude #nm
        frequency = slider_resfreq #Hz
        hop = slider_hop
        lag = slider_lag/10**9*frequency #radians
        steps = 50

        # Independent variable arrays
        Vg_array = np.arange(200)/10-10 #eV
        zins_array = (np.arange(200)/10+0.05)*1e-7 #cm
        time_AFMarray = Physics_AFMoscillation.time_AFMarray(steps)
        zins_AFMarray = Physics_AFMoscillation.zins_AFMarray(time_AFMarray,amplitude,zins)
        zinslag_AFMarray = Physics_AFMoscillation.zinslag_AFMarray(time_AFMarray,amplitude,zins, lag)

        # Dependent variable arrays calculations
        Vs_AFMarray, F_AFMarray = Physics_AFMoscillation.SurfacepotForce_AFMarray(1,zinslag_AFMarray,sampletype,RTN,hop,   Vg,zins,bandgap,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T)
        Ec_AFMarray,Ev_AFMarray,Ei_AFMarray,Ef_AFMarray,zsem_AFMarray,psi_AFMarray,Insulatorx_AFMarray,Insulatory_AFMarray,Vacuumx_AFMarray,Vacuumy_AFMarray,Gatex_AFMarray,Gatey_AFMarray = Physics_AFMoscillation.BandDiagram_AFMarray(Vs_AFMarray,zinslag_AFMarray,sampletype,   Vg,zins,bandgap,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T)
        Vs_biasarray, F_biasarray, Vs_zinsarray, F_zinsarray = Physics_SurfacepotForce.VsF_arrays(Vg_array,zins_array,sampletype,   Vg,zins,bandgap,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T)

        # Find traces for bottom and top of hop
        RTN = False
        Vs_AFMarray0, F_AFMarray0 = Physics_AFMoscillation.SurfacepotForce_AFMarray(1,zinslag_AFMarray,sampletype,RTN,hop,   Vg,zins,bandgap,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T)
        Nd = round((10**(slider_donor+hop)*10**8)/(1000**3))
        Vs_AFMarray1, F_AFMarray1 = Physics_AFMoscillation.SurfacepotForce_AFMarray(1,zinslag_AFMarray,sampletype,RTN,hop,   Vg,zins,bandgap,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T)
        Vs_biasarray1, F_biasarray1, Vs_zinsarray1, F_zinsarray1 = Physics_SurfacepotForce.VsF_arrays(Vg_array,zins_array,sampletype,   Vg,zins,bandgap,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T)

        # Display traces for bottom and top of hop
        Vs_zinsarray = np.append(Vs_zinsarray, np.flipud(Vs_zinsarray1))
        F_zinsarray = np.append(F_zinsarray, np.flipud(F_zinsarray1))
        zins_array = np.append(zins_array, np.flipud(zins_array))

        # stack AFM arrays to display two periods (with half calculation time)
        steps = steps*2
        time_AFMarray = np.append(time_AFMarray, time_AFMarray+2*np.pi)
        zins_AFMarray = np.append(zins_AFMarray, zins_AFMarray)
        zinslag_AFMarray = np.append(zinslag_AFMarray, zinslag_AFMarray)
        Vs_AFMarray = np.append(Vs_AFMarray, Vs_AFMarray)
        F_AFMarray = np.append(F_AFMarray, F_AFMarray)
        Ec_AFMarray = Ec_AFMarray + Ec_AFMarray
        Ev_AFMarray = Ev_AFMarray + Ev_AFMarray
        Ei_AFMarray = Ei_AFMarray + Ei_AFMarray
        Ef_AFMarray = Ef_AFMarray + Ef_AFMarray
        zsem_AFMarray = np.vstack([zsem_AFMarray, zsem_AFMarray])
        psi_AFMarray = np.vstack([psi_AFMarray, psi_AFMarray])
        Insulatorx_AFMarray = np.vstack([Insulatorx_AFMarray, Insulatorx_AFMarray])
        Insulatory_AFMarray = np.vstack([Insulatory_AFMarray, Insulatory_AFMarray])
        Vacuumx_AFMarray = np.vstack([Vacuumx_AFMarray, Vacuumx_AFMarray])
        Vacuumy_AFMarray = np.vstack([Vacuumy_AFMarray, Vacuumy_AFMarray])
        Gatex_AFMarray = np.vstack([Gatex_AFMarray, Gatex_AFMarray])
        Gatey_AFMarray = np.vstack([Gatey_AFMarray, Gatey_AFMarray])

        Vs_AFMarray0 = np.append(Vs_AFMarray0, Vs_AFMarray0)
        Vs_AFMarray1 = np.append(Vs_AFMarray1, Vs_AFMarray1)
        F_AFMarray0 = np.append(F_AFMarray0, F_AFMarray0)
        F_AFMarray1 = np.append(F_AFMarray1, F_AFMarray1)

        Vs_AFMarray = np.append(Vs_AFMarray, np.flipud(Vs_AFMarray0))
        F_AFMarray = np.append(F_AFMarray, np.flipud(F_AFMarray0))
        time_AFMarray = np.append(time_AFMarray, np.flipud(time_AFMarray))
        Vs_AFMarray = np.append(Vs_AFMarray, Vs_AFMarray1)
        F_AFMarray = np.append(F_AFMarray, F_AFMarray1)
        time_AFMarray = np.append(time_AFMarray, time_AFMarray)

        #########################################################
        #########################################################
        fig = make_subplots(
            rows=3, cols=2, shared_yaxes=False, shared_xaxes=False,
            column_widths=[0.3, 0.7], row_heights=[1,1,1],
            specs=[[{}, {}], [{}, {}], [{}, {}]])

        fig.add_trace(go.Scatter(
            y = zsem_AFMarray[0]*1e7, x = Ev_AFMarray[0]-psi_AFMarray[0],
            name = "ValenceBand", mode='lines', showlegend=False,
            line_color=color_Ev
            ), row=1, col=1)
        fig.add_trace(go.Scatter(
            y = zsem_AFMarray[0]*1e7, x = Ei_AFMarray[0]-psi_AFMarray[0],
            name = "IntrinsicEnergy", mode='lines', showlegend=False,
            line_color=color_Ei
            ), row=1, col=1)
        fig.add_trace(go.Scatter(
            y = zsem_AFMarray[0]*1e7, x = Ec_AFMarray[0]-psi_AFMarray[0],
            name = "ConductionBand", mode='lines', showlegend=False,
            line_color=color_Ec
            ), row=1, col=1)
        fig.add_trace(go.Scatter(
            y = zsem_AFMarray[0]*1e7, x = 0*zsem_AFMarray[0]+Ef_AFMarray[0],
            name = "FermiEnergy", mode='lines', showlegend=False,
            line_color=color_Ef
            ), row=1, col=1)
        fig.add_trace(go.Scatter(
            y = Insulatorx_AFMarray[0], x = Insulatory_AFMarray[0],
            name = "Insulator", mode='lines', showlegend=False,
            line_color=color_ox
            ), row=1, col=1)
        fig.add_trace(go.Scatter(
            y = Gatex_AFMarray[0], x = Gatey_AFMarray[0],
            name = "GateFermiEnergy", mode='lines', showlegend=False,
            line_color=color_met
            ), row=1, col=1)
        fig.add_trace(go.Scatter(
            y = Vacuumx_AFMarray[0], x = Vacuumy_AFMarray[0],
            name = "VacuumEnergy", mode='lines', showlegend=False,
            line_color=color_vac
            ), row=1, col=1)


        fig.add_trace(go.Scatter(
            x = zins_array*1e7, y = Vs_zinsarray,
            name = "ContactPotential", mode='lines', showlegend=False,
            line_color=color_vac
            ), row=2, col=1)
        fig.add_trace(go.Scatter(
            x = [zinslag_AFMarray[0]*1e7], y = [Vs_AFMarray[0]],
            name = "ContactPotential", mode='markers', marker_line_width=1, showlegend=False,
            marker=dict(color=color_indicator,size=10),
            ), row=2, col=1)
        fig.add_trace(go.Scatter(
            x = zins_array*1e7, y = F_zinsarray,
            name = "Force", mode='lines', showlegend=False,
            line_color=color_vac
            ), row=3, col=1)
        fig.add_trace(go.Scatter(
            x = [zinslag_AFMarray[0]*1e7], y = [F_AFMarray[0]],
            name = "Force", mode='markers', marker_line_width=1, showlegend=False,
            marker=dict(color=color_indicator,size=10),
            ), row=3, col=1)

        fig.add_trace(go.Scatter(
            x = time_AFMarray, y = zins_AFMarray*1e7,
            name = "Position", mode='lines', showlegend=False,
            line_color=color_other
            ), row=1, col=2),
        fig.add_trace(go.Scatter(
            x = [time_AFMarray[0]], y = [zins_AFMarray[0]*1e7],
            name = "Position", mode='markers',
            marker=dict(color=color_indicator,size=10),
            ), row=1, col=2)
        fig.add_trace(go.Scatter(
            x = time_AFMarray, y = Vs_AFMarray,
            name = "SurfacePotential", mode='lines', showlegend=False,
            line_color=color_other
            ), row=2, col=2),
        fig.add_trace(go.Scatter(
            x = [time_AFMarray[0]], y = [Vs_AFMarray[0]],
            name = "SurfacePotential", mode='markers',
            marker=dict(color=color_indicator,size=10),
            ), row=2, col=2)
        fig.add_trace(go.Scatter(
            x = time_AFMarray, y = F_AFMarray,
            name = "Force", mode='lines', showlegend=False,
            line_color=color_other
            ), row=3, col=2)
        fig.add_trace(go.Scatter(
            x = [time_AFMarray[0]], y = [F_AFMarray[0]],
            name = "Force", mode='markers',
            marker=dict(color=color_indicator,size=10),
            ), row=3, col=2)

        #savebanddiagdata(zsem_AFMarray*1e7,'savebandarray_zsem.csv')
        #savebanddiagdata(Ec_AFMarray,'savebandarray_Ec.csv')
        #savebanddiagdata(Ev_AFMarray,'savebandarray_Ev.csv')
        #savebanddiagdata(psi_AFMarray,'savebandarray_psi.csv')
        #savebanddiagdata(Ef_AFMarray,'savebandarray_Ef.csv')
        #savebanddiagdata(Gatex_AFMarray,'savebandarray_Gatez.csv')
        #savebanddiagdata(Gatey_AFMarray,'savebandarray_GateE.csv')
        #savebanddiagdata(Insulatorx_AFMarray,'savebandarray_Insulatorz.csv')
        #savebanddiagdata(Insulatory_AFMarray,'savebandarray_InsulatorE.csv')
        #savezinsdata(zins_array, Vs_zinsarray, F_zinsarray,'savezinsarray.csv')
        #savebanddiagdata(zinslag_AFMarray,'savezinsarray_zins.csv')
        #savebanddiagdata(Vs_AFMarray,'savezinsarray_Vs.csv')
        #savebanddiagdata(F_AFMarray,'savezinsarray_F.csv')
        #savetimedata(time_AFMarray[:100], zins_AFMarray[:100], Vs_AFMarray[:100], F_AFMarray[:100],'savetimearray.csv')

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
                go.Scatter(x=[zinslag_AFMarray[step]*1e7], y=[Vs_AFMarray[step]],mode="markers", marker=dict(color=color_indicator, size=10)),
                go.Scatter(x=zins_array*1e7, y=F_zinsarray,mode="lines", line_color=color_vac),
                go.Scatter(x=[zinslag_AFMarray[step]*1e7], y=[F_AFMarray[step]],mode="markers", marker=dict(color=color_indicator, size=10)),

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
        zins = 0
        amplitude = 0
        F_biasarray = [0, 0]

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

    fig.update_layout(transition_duration=300, height=800,margin=dict(t=0), showlegend=False)

    fig.update_yaxes(row=1, col=1, title_text= "Insulator Thickness (nm)", range=[-zins*1e7-10-amplitude, 20])
    fig.update_yaxes(row=2, col=1, title_text= "Contact Potential (eV)")
    fig.update_yaxes(row=3, col=1, title_text= "Force (N/nm^2)", range = [min(F_biasarray), max(F_biasarray)])
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
# FIGURE: Bias sweep experiment

def fig_AFM2(slider_Vg,slider_zins,slider_bandgap,slider_epsilonsem,slider_WFmet,slider_EAsem,slider_donor,slider_acceptor,slider_emass,slider_hmass,slider_T, slider_amplitude,slider_resfreq,slider_springconst,slider_tipradius,slider_Qfactor,calculatebutton,toggle_sampletype,slider_hop,slider_lag):

    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if 'AFMbutton_CalculateBiasExp' in changed_id:

        model_dg = pd.read_csv('XData_ExcitationvBias-Sweep315.csv')
        model_dgx = model_dg.Bias
        model_dgy = model_dg.Excitation

        model_df = pd.read_csv('XData_FreqShiftvBias-Sweep315.csv')
        model315_dfx = model_df.Bias
        model315_dfy = model_df.FreqShift

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
        sampletype = toggle_sampletype #false = semiconducting, true = metallic
        amplitude = slider_amplitude #nm
        frequency = slider_resfreq #Hz
        springconst = slider_springconst #N/m
        Qfactor = slider_Qfactor
        tipradius = slider_tipradius #nm
        hop = slider_hop
        lag = slider_lag/10**9*frequency #rad
        steps = 50

        Vg_array = np.arange(100)/20-3 #eV
        zins_array = (np.arange(200)/10+0.05)*1e-7 #cm

        Vs_biasarray0, F_biasarray0, Vs_zinsarray0, F_zinsarray0= Physics_SurfacepotForce.VsF_arrays(Vg_array,zins_array,sampletype,   Vg,zins,bandgap,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T)
        df_biasarray0, dg_biasarray0 = Physics_FreqshiftDissipation.dfdg_biasarray(Vg_array,steps,amplitude,frequency,springconst,Qfactor,tipradius,sampletype,hop,lag,  Vg,zins,bandgap,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T)

        Na = round((10**(slider_acceptor+hop)*10**8)/(1000**3))
        Vs_biasarray1, F_biasarray1, Vs_zinsarray1, F_zinsarray1 = Physics_SurfacepotForce.VsF_arrays(Vg_array,zins_array,sampletype,   Vg,zins,bandgap,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T)
        df_biasarray1, dg_biasarray1 =  Physics_FreqshiftDissipation.dfdg_biasarray(Vg_array,steps,amplitude,frequency,springconst,Qfactor,tipradius,sampletype,hop,lag,  Vg,zins,bandgap,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T)

        Vg_array = np.append(Vg_array, np.flipud(Vg_array))
        Vs_biasarray = np.append(Vs_biasarray0, np.flipud(Vs_biasarray1))
        F_biasarray = np.append(F_biasarray0, np.flipud(F_biasarray1))
        df_biasarray = np.append(df_biasarray0, np.flipud(df_biasarray1))-3.651 #Experimental offset, delete
        dg_biasarray = np.append(dg_biasarray0, np.flipud(dg_biasarray1))-0.16#Experimental offset, delete

        F_biasarray = F_biasarray0*np.pi*tipradius**2
        F_zinsarray = F_zinsarray0*np.pi*tipradius**2

        #savedata(Vg_array, df_biasarray, 'FreqShift.csv')
        #savedata(Vg_array, dg_biasarray, 'Excitation.csv')

        #########################################################
        #########################################################
        fig = make_subplots(
            rows=2, cols=2, shared_yaxes=False, shared_xaxes=False,
            column_widths=[0.5, 0.5], row_heights=[1,1],
            specs=[[{}, {}], [{}, {}]])

        fig.add_trace(go.Scatter(
            x = model315_dfx, y = model315_dfy,
            name = "FreqShift", mode='lines', showlegend=False,
            line_color=color_Ei
            ), row=1, col=2)

        fig.add_trace(go.Scatter(
            x = Vg_array, y = Vs_biasarray,
            name = "ContactPotential", mode='lines', showlegend=False,
            line_color=color_other
            ), row=1, col=1)
        fig.add_trace(go.Scatter(
            x = Vg_array, y = F_biasarray,
            name = "Force", mode='lines', showlegend=False,
            line_color=color_other
            ), row=2, col=1)
        fig.add_trace(go.Scatter(
            x = Vg_array, y = df_biasarray,
            name = "FrequencyShift", mode='lines', showlegend=False,
            line_color=color_other
            ), row=1, col=2)
        fig.add_trace(go.Scatter(
            x = Vg_array, y = dg_biasarray,
            name = "Dissipation", mode='lines', showlegend=False,
            line_color=color_other
            ), row=2, col=2)
        fig.add_trace(go.Scatter(
            x = model_dgx, y = model_dgy,
            name = "Dissipation", mode='lines', showlegend=False,
            line_color=color_Ei
            ), row=2, col=2)

    ############################################################################

    else:
        fig = make_subplots(
            rows=2, cols=2, shared_yaxes=False, shared_xaxes=False,
            column_widths=[0.5, 0.5], row_heights=[1,1],
            specs=[[{}, {}], [{}, {}]])
        fig.add_trace(go.Scatter(y=[], x=[]), row=1, col=1)
        fig.add_trace(go.Scatter(y=[], x=[]), row=2, col=1)
        fig.add_trace(go.Scatter(y=[], x=[]), row=1, col=2)
        fig.add_trace(go.Scatter(y=[], x=[]), row=2, col=2)

    ############################################################################

    fig.update_layout(transition_duration=300, height=600,margin=dict(t=0),showlegend=False)

    fig.update_yaxes(row=1, col=1, title_text= "Contact Potential (eV)")
    fig.update_yaxes(row=2, col=1, title_text= "Force (N)")
    fig.update_yaxes(row=1, col=2, title_text = "Frequency Shift (Hz)")
    fig.update_yaxes(row=2, col=2, title_text = "Dissipation")

    fig.update_xaxes(row=1, col=1,showticklabels=True,range=[-3,2])
    fig.update_xaxes(row=2, col=1,title_text= "Gate Bias (V)",range=[-3,2])
    fig.update_xaxes(row=1, col=2,showticklabels=True,range=[-3,2])
    fig.update_xaxes(row=2, col=2,title_text= "Gate Bias (V)",range=[-3,2])


    return fig

################################################################################
################################################################################
# FIGURE: Time trace experiment

def fig_AFM3(slider_Vg,slider_zins,slider_bandgap,slider_epsilonsem,slider_WFmet,slider_EAsem,slider_donor,slider_acceptor,slider_emass,slider_hmass,slider_T, slider_amplitude,slider_resfreq,slider_springconst,slider_tipradius,slider_Qfactor,calculatebutton,toggle_sampletype,slider_hop,slider_lag):

    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if 'AFMbutton_CalculateTimeExp' in changed_id:

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
        sampletype = toggle_sampletype #false = semiconducting, true = metallic
        amplitude = slider_amplitude #nm
        frequency = slider_resfreq #Hz
        springconst = slider_springconst #N/m
        Qfactor = slider_Qfactor
        tipradius = slider_tipradius #nm
        hop = slider_hop
        lag = slider_lag/10**9*frequency #rad
        steps = 50

        Vg_array = np.arange(200)/10-10 #eV
        zins_array = (np.arange(200)/10+0.05)*1e-7 #cm
        time_array = np.arange(200)/10

        df_AFMtimearray, dg_AFMtimearray = Physics_FreqshiftDissipation.dfdg_timearray(time_array,steps,amplitude,frequency,springconst,Qfactor,tipradius,sampletype,hop,lag,  Vg,zins,bandgap,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T)

        #########################################################
        #########################################################
        fig = make_subplots(
            rows=2, cols=1, shared_yaxes=False, shared_xaxes=False,
            column_widths=[1], row_heights=[0.5,0.5],
            specs=[[{}],[{}]])

        fig.add_trace(go.Scatter(
            x = time_array, y = df_AFMtimearray,
            name = "FrequencyShift", mode='lines', showlegend=False,
            line_color=color_other
            ), row=1, col=1)
        fig.add_trace(go.Scatter(
            x = time_array, y = dg_AFMtimearray,
            name = "Dissipation", mode='lines', showlegend=False,
            line_color=color_other
            ), row=2, col=1)

    ############################################################################

    else:
        fig = make_subplots(
            rows=2, cols=1, shared_yaxes=False, shared_xaxes=False,
            column_widths=[1], row_heights=[0.5,0.5],
            specs=[[{}],[{}]])
        fig.add_trace(go.Scatter(y=[], x=[]), row=1, col=1)
        fig.add_trace(go.Scatter(y=[], x=[]), row=2, col=1)

    ############################################################################

    fig.update_layout(transition_duration=100, height=400,margin=dict(t=0),showlegend=False)

    fig.update_yaxes(row=1, col=1, title_text= "df (Hz)")
    fig.update_yaxes(row=2, col=1, title_text = "dg", range=[0,20*10**-12])

    fig.update_xaxes(row=1, col=1, showticklabels=False, title_text= "Time")
    fig.update_xaxes(row=2, col=1, showticklabels=False, title_text= "Time")

    return fig


################################################################################
################################################################################
# READOUTS

def readouts_AFM(slider_Vg, slider_zins, slider_amplitude, slider_hop, slider_lag, slider_resfreq, slider_springconst, slider_Qfactor, slider_tipradius):
    readout_Vg = '{0:.4g}'.format(slider_Vg)
    readout_zins = '{0:.1f}'.format(slider_zins)
    readout_amplitude = '{0:.1f}'.format(slider_amplitude)
    readout_lag = '{0:.0f}'.format(slider_lag)
    readout_hop = '{0:.2f}'.format(slider_hop)
    readout_resfreq = '{0:.0f}'.format(slider_resfreq)
    readout_springconst = '{0:.0f}'.format(slider_springconst)
    readout_Qfactor = '{0:.0f}'.format(slider_Qfactor)
    readout_tipradius = '{0:.0f}'.format(slider_tipradius)
    return readout_Vg, readout_zins, readout_amplitude, readout_hop, readout_lag, readout_resfreq, readout_springconst, readout_Qfactor, readout_tipradius


################################################################################
################################################################################
# FUNCTIONALITY

def togglefunctions(toggle):
    if toggle == True:
        style_L = {'color': '#7f7f7f', 'fontSize': 14, 'width':130, 'text-align': 'center'}
        style_R = {'color': '#57c5f7', 'fontSize': 14, 'width':60, 'text-align': 'left'}
    elif toggle == False:
        style_L = {'color': '#57c5f7', 'fontSize': 14, 'width':130, 'text-align': 'center'}
        style_R = {'color': '#7f7f7f', 'fontSize': 14, 'width':60, 'text-align': 'left'}
    return style_L, style_R

def savedata(xdata,ydata,filenamestr):
    xstr = [str(xi) for xi in xdata]
    ystr = [str(yi) for yi in ydata]
    save = pd.DataFrame({'x': xstr, 'y': ystr})
    save.to_csv(filenamestr,index=False)
    return

def savebanddiagdata(x,filenamestr):
    np.savetxt(filenamestr,x,delimiter=",")
    return 1

def savezinsdata(zins,Vs,F,filenamestr):
    zins_str = [str(x) for x in zins]
    Vs_str = [str(x) for x in Vs]
    F_str = [str(x) for x in F]
    save = pd.DataFrame({'zins': zins_str, 'Vs': Vs_str, 'F': F_str})
    save.to_csv(filenamestr,index=False)
    return 1

def savetimedata(time,zins,Vs,F,filenamestr):
    time_str = [str(x) for x in time]
    zins_str = [str(x) for x in zins]
    Vs_str = [str(x) for x in Vs]
    F_str = [str(x) for x in F]
    save = pd.DataFrame({'time': time_str, 'zins': zins_str, 'Vs': Vs_str, 'F': F_str})
    save.to_csv(filenamestr,index=False)
    return 1

def savepointdata(xdata,ydata,filenamestr):
    xstr = [str(xi) for xi in xdata]
    ystr = [str(yi) for yi in ydata]
    save = pd.DataFrame({'x': xstr, 'y': ystr})
    save.to_csv(filenamestr,index=False)
    return

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
