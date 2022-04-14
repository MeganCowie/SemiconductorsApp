import dash
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import pandas as pd

import Physics_Semiconductors
import Physics_ncAFM
import Physics_Noise
import Physics_Optics


import Organization_BuildArrays

################################################################################
################################################################################
# FIGURE: ncAFM oscillations

def fig1_AFM(slider_Vg,slider_zins,slider_Eg,slider_epsilonsem,slider_WFmet,slider_EAsem,slider_donor,slider_acceptor,slider_emass,slider_hmass,slider_T,slider_alpha,slider_biassteps,slider_zinssteps, slider_timesteps,slider_amplitude,slider_resfreq,slider_hop,slider_lag,calculatebutton,toggle_sampletype,toggle_RTN):

    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if 'AFMbutton_Calculate' in changed_id:
        # input (slider) parameters
        Vg = slider_Vg #eV
        zins = slider_zins*1e-7 # cm
        Eg = slider_Eg
        epsilon_sem = slider_epsilonsem
        WFmet = slider_WFmet #eV
        EAsem = slider_EAsem #eV
        Nd = round((10**slider_donor*10**8)/(1000**3)) #/cm^3
        Na = round((10**slider_acceptor*10**8)/(1000**3)) #/cm^3
        mn = slider_emass*Physics_Semiconductors.me # kg
        mp = slider_hmass*Physics_Semiconductors.me # kg
        T = slider_T # K
        sampletype = toggle_sampletype #false = semiconducting, true = metallic
        RTN = toggle_RTN #false = off, true = on
        amplitude = slider_amplitude #nm
        frequency = slider_resfreq #Hz
        hop = slider_hop
        lag = slider_lag/10**9*frequency #radians
        biassteps = slider_biassteps
        zinssteps = slider_zinssteps
        timesteps = slider_timesteps


        # Independent variable arrays
        Vg_array = np.linspace(-10,10,biassteps)*(1-slider_alpha) #eV
        zins_array = np.linspace(0.05,20,zinssteps)*1e-7 #nm
        time_AFMarray = Physics_ncAFM.time_AFMarray(timesteps)
        zins_AFMarray = Physics_ncAFM.zins_AFMarray(time_AFMarray,amplitude,zins)
        zinslag_AFMarray = Physics_ncAFM.zinslag_AFMarray(time_AFMarray,amplitude,zins, lag)

        # Dependent variable arrays calculations
        Vs_AFMarray, F_AFMarray = Physics_ncAFM.SurfacepotForce_AFMarray(1,zinslag_AFMarray,sampletype,RTN,hop,   Vg,zins,Eg,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T)
        Ec_AFMarray,Ev_AFMarray,Ei_AFMarray,Ef_AFMarray,zsem_AFMarray,psi_AFMarray,Insulatorx_AFMarray,Insulatory_AFMarray,Vacuumx_AFMarray,Vacuumy_AFMarray,Gatex_AFMarray,Gatey_AFMarray = Organization_BuildArrays.BandDiagram_AFMarray(Vs_AFMarray,zinslag_AFMarray,sampletype,   Vg,zins,Eg,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T)
        Vs_biasarray, F_biasarray, Vs_zinsarray, F_zinsarray = Organization_BuildArrays.VsF_arrays(Vg_array,zins_array,sampletype,   Vg,zins,Eg,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T)

        # Find traces for top of hop
        #Na = round((10**(slider_acceptor+hop)*10**8)/(1000**3))
        #Vs_AFMarray1, F_AFMarray1 = Physics_ncAFM.SurfacepotForce_AFMarray(1,zinslag_AFMarray,sampletype,RTN,hop,   Vg,zins,Eg,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T)
        #Vs_biasarray1, F_biasarray1, Vs_zinsarray1, F_zinsarray1 = Physics_SurfacepotForce.VsF_arrays(Vg_array,zins_array,sampletype,   Vg,zins,Eg,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T)

        Vs_AFMarray1, F_AFMarray1 = Vs_AFMarray, F_AFMarray
        Vs_biasarray1, F_biasarray1, Vs_zinsarray1, F_zinsarray1 = Vs_biasarray, F_biasarray, Vs_zinsarray, F_zinsarray

        # Stack arrays at bottom and top of hop
        Vs_zinsarray = np.append(Vs_zinsarray, np.flipud(Vs_zinsarray1))
        F_zinsarray = np.append(F_zinsarray, np.flipud(F_zinsarray1))
        zins_array = np.append(zins_array, np.flipud(zins_array))

        # Stack AFM arrays to display two periods (with half calculation time)
        timesteps = timesteps*2
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

        Vs_AFMarray0 = np.append(Vs_AFMarray, Vs_AFMarray)
        Vs_AFMarray1 = np.append(Vs_AFMarray1, Vs_AFMarray1)
        F_AFMarray0 = np.append(F_AFMarray, F_AFMarray)
        F_AFMarray1 = np.append(F_AFMarray1, F_AFMarray1)

        zins_AFMarray = np.append(zins_AFMarray, np.flipud(zins_AFMarray))
        Vs_AFMarray = np.append(Vs_AFMarray, np.flipud(Vs_AFMarray))
        F_AFMarray = np.append(F_AFMarray, np.flipud(F_AFMarray))
        time_AFMarray = np.append(time_AFMarray, np.flipud(time_AFMarray))
        zins_AFMarray = np.append(zins_AFMarray, np.flipud(zins_AFMarray))
        Vs_AFMarray = np.append(Vs_AFMarray, Vs_AFMarray1)
        F_AFMarray = np.append(F_AFMarray, F_AFMarray1)
        time_AFMarray = np.append(time_AFMarray, time_AFMarray)

        #########################################################
        #########################################################
        fig1 = make_subplots(
            rows=3, cols=2, shared_yaxes=False, shared_xaxes=False,
            column_widths=[0.3, 0.7], row_heights=[1,1,1],
            specs=[[{}, {}], [{}, {}], [{}, {}]])

        fig1.add_trace(go.Scatter(
            y = zsem_AFMarray[0]*1e7, x = Ev_AFMarray[0]-psi_AFMarray[0],
            name = "ValenceBand", mode='lines', showlegend=False,
            line_color=color_Ev
            ), row=1, col=1)
        fig1.add_trace(go.Scatter(
            y = zsem_AFMarray[0]*1e7, x = Ei_AFMarray[0]-psi_AFMarray[0],
            name = "IntrinsicEnergy", mode='lines', showlegend=False,
            line_color=color_Ei
            ), row=1, col=1)
        fig1.add_trace(go.Scatter(
            y = zsem_AFMarray[0]*1e7, x = Ec_AFMarray[0]-psi_AFMarray[0],
            name = "ConductionBand", mode='lines', showlegend=False,
            line_color=color_Ec
            ), row=1, col=1)
        fig1.add_trace(go.Scatter(
            y = zsem_AFMarray[0]*1e7, x = 0*zsem_AFMarray[0]+Ef_AFMarray[0],
            name = "FermiEnergy", mode='lines', showlegend=False,
            line_color=color_Ef
            ), row=1, col=1)
        fig1.add_trace(go.Scatter(
            y = Insulatorx_AFMarray[0], x = Insulatory_AFMarray[0],
            name = "Insulator", mode='lines', showlegend=False,
            line_color=color_ox
            ), row=1, col=1)
        fig1.add_trace(go.Scatter(
            y = Gatex_AFMarray[0], x = Gatey_AFMarray[0],
            name = "GateFermiEnergy", mode='lines', showlegend=False,
            line_color=color_met
            ), row=1, col=1)
        fig1.add_trace(go.Scatter(
            y = Vacuumx_AFMarray[0], x = Vacuumy_AFMarray[0],
            name = "VacuumEnergy", mode='lines', showlegend=False,
            line_color=color_vac
            ), row=1, col=1)

        fig1.add_trace(go.Scatter(
            x = zins_array*1e7, y = Vs_zinsarray,
            name = "ContactPotential", mode='lines', showlegend=False,
            line_color=color_vac
            ), row=2, col=1)
        fig1.add_trace(go.Scatter(
            x = [zinslag_AFMarray[0]*1e7], y = [Vs_AFMarray[0]],
            name = "ContactPotential", mode='markers', marker_line_width=1, showlegend=False,
            marker=dict(color=color_indicator,size=10),
            ), row=2, col=1)
        fig1.add_trace(go.Scatter(
            x = zins_array*1e7, y = F_zinsarray,
            name = "Force", mode='lines', showlegend=False,
            line_color=color_vac
            ), row=3, col=1)
        fig1.add_trace(go.Scatter(
            x = [zinslag_AFMarray[0]*1e7], y = [F_AFMarray[0]],
            name = "Force", mode='markers', marker_line_width=1, showlegend=False,
            marker=dict(color=color_indicator,size=10),
            ), row=3, col=1)

        fig1.add_trace(go.Scatter(
            x = time_AFMarray, y = zins_AFMarray*1e7,
            name = "Position", mode='lines', showlegend=False,
            line_color=color_other
            ), row=1, col=2),
        fig1.add_trace(go.Scatter(
            x = [time_AFMarray[0]], y = [zins_AFMarray[0]*1e7],
            name = "Position", mode='markers',
            marker=dict(color=color_indicator,size=10),
            ), row=1, col=2)
        fig1.add_trace(go.Scatter(
            x = time_AFMarray, y = Vs_AFMarray,
            name = "SurfacePotential", mode='lines', showlegend=False,
            line_color=color_other
            ), row=2, col=2),
        fig1.add_trace(go.Scatter(
            x = [time_AFMarray[0]], y = [Vs_AFMarray[0]],
            name = "SurfacePotential", mode='markers',
            marker=dict(color=color_indicator,size=10),
            ), row=2, col=2)
        fig1.add_trace(go.Scatter(
            x = time_AFMarray, y = F_AFMarray,
            name = "Force", mode='lines', showlegend=False,
            line_color=color_other
            ), row=3, col=2)
        fig1.add_trace(go.Scatter(
            x = [time_AFMarray[0]], y = [F_AFMarray[0]],
            name = "Force", mode='markers',
            marker=dict(color=color_indicator,size=10),
            ), row=3, col=2)

        fig1.frames=[
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
                for step in range(timesteps)]

    ############################################################################

    else:
        zins = 0
        amplitude = 0
        F_biasarray = [0, 0]
        timesteps = 1

        fig1 = make_subplots(
            rows=3, cols=2, shared_yaxes=False, shared_xaxes=False,
            column_widths=[0.3, 0.7], row_heights=[1,1,1],
            specs=[[{}, {}], [{}, {}], [{}, {}]])
        fig1.add_trace(go.Scatter(y=[], x=[]), row=1, col=1)
        fig1.add_trace(go.Scatter(y=[], x=[]), row=2, col=1)
        fig1.add_trace(go.Scatter(y=[], x=[]), row=3, col=1)
        fig1.add_trace(go.Scatter(y=[], x=[]), row=1, col=2)
        fig1.add_trace(go.Scatter(y=[], x=[]), row=2, col=2)
        fig1.add_trace(go.Scatter(y=[], x=[]), row=3, col=2)

    ############################################################################

    fig1.update_layout(
    updatemenus=[
        dict(visible = True, type="buttons", buttons=[dict(label="Play" , method="animate", args=[None, {"frame": {"duration": 10000/timesteps, "redraw": True},"fromcurrent": True, "transition": {"duration": 0}}])],x=0,y=1.1),
        dict(type="buttons", buttons=[dict(label="Pause", method="animate", args=[[None], {"frame": {"duration": 0, "redraw": False},"mode": "immediate","transition": {"duration": 0}}])],x=0.1,y=1.1)
        ])

    fig1.update_layout(transition_duration=300, height=800,margin=dict(t=0), showlegend=False)

    fig1.update_yaxes(row=1, col=1, title_text= "Insulator Thickness (nm)", range=[-zins*1e7-10-amplitude, 20])
    fig1.update_yaxes(row=2, col=1, title_text= "Contact Potential (eV)")
    fig1.update_yaxes(row=3, col=1, title_text= "Force (N/nm^2)", range = [min(F_biasarray), max(F_biasarray)])
    fig1.update_yaxes(row=1, col=2)
    fig1.update_yaxes(row=2, col=2)
    fig1.update_yaxes(row=3, col=2)

    fig1.update_xaxes(row=1, col=1, title_text= "Energy (eV)")
    fig1.update_xaxes(row=2, col=1, title_text= "Insulator Thickness (nm)")
    fig1.update_xaxes(row=3, col=1, title_text= "Insulator Thickness (nm)")
    fig1.update_xaxes(row=1, col=2, title_text= "Time", showticklabels=False, range=[0, 4*np.pi])
    fig1.update_xaxes(row=2, col=2, title_text= "Time", showticklabels=False, range=[0, 4*np.pi])
    fig1.update_xaxes(row=3, col=2, title_text= "Time", showticklabels=False, range=[0, 4*np.pi])

    return fig1


################################################################################
################################################################################
# FIGURE: Bias sweep experiment

def fig2_AFM(slider_Vg,slider_zins,slider_Eg,slider_epsilonsem,slider_WFmet,slider_EAsem,slider_donor,slider_acceptor,slider_emass,slider_hmass,slider_T,slider_alpha,slider_biassteps,slider_zinssteps, slider_timesteps,slider_amplitude,slider_resfreq,slider_springconst,slider_tipradius,slider_Qfactor,calculatebutton,toggle_sampletype,slider_hop,slider_lag):

    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if 'AFMbutton_CalculateBiasExp' in changed_id:

        # input (slider) parameters
        Vg = slider_Vg
        zins = slider_zins*1e-7 # cm
        Eg = slider_Eg
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

        biassteps = slider_biassteps
        zinssteps = slider_zinssteps
        timesteps = slider_timesteps

        Vg_array = np.linspace(-10,10,biassteps)*(1-slider_alpha) #eV
        zins_array = np.linspace(0.05,20,zinssteps)*1e-7 #nm

        Vs_biasarray0, F_biasarray0, df_biasarray0, dg_biasarray0 = Organization_BuildArrays.VsFdfdg_biasarray(Vg_array,timesteps,amplitude,frequency,springconst,Qfactor,tipradius,sampletype,hop,lag,  Vg,zins,Eg,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T)

        #Na = round((10**(slider_acceptor+hop)*10**8)/(1000**3))
        #Vs_biasarray1, F_biasarray1, Vs_zinsarray1, F_zinsarray1 = Physics_SurfacepotForce.VsF_arrays(Vg_array,zins_array,sampletype,   Vg,zins,Eg,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T)
        #df_biasarray1, dg_biasarray1 =  Physics_FreqshiftDissipation.dfdg_biasarray(Vg_array,steps,amplitude,frequency,springconst,Qfactor,tipradius,sampletype,hop,lag,  Vg,zins,Eg,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T)

        Vs_biasarray1 = Vs_biasarray0
        F_biasarray1 = F_biasarray0
        df_biasarray1 = df_biasarray0
        dg_biasarray1 = dg_biasarray0

        Vg_array = np.linspace(-10,10,biassteps) #eV

        Vg_array = np.append(Vg_array, np.flipud(Vg_array))
        Vs_biasarray = np.append(Vs_biasarray0, np.flipud(Vs_biasarray1))
        F_biasarray = np.append(F_biasarray0, np.flipud(F_biasarray1))
        df_biasarray = np.append(df_biasarray0, np.flipud(df_biasarray1))
        dg_biasarray = np.append(dg_biasarray0, np.flipud(dg_biasarray1))


        #########################################################
        #########################################################
        fig2 = make_subplots(
            rows=2, cols=2, shared_yaxes=False, shared_xaxes=True,
            column_widths=[0.5, 0.5], row_heights=[1,1],
            specs=[[{}, {}], [{}, {}]])
        fig2.add_trace(go.Scatter(
            x = Vg_array, y = Vs_biasarray,
            name = "ContactPotential", mode='lines', showlegend=False,
            line_color=color_other
            ), row=1, col=1)
        fig2.add_trace(go.Scatter(
            x = Vg_array, y = F_biasarray,
            name = "Force", mode='lines', showlegend=False,
            line_color=color_other
            ), row=2, col=1)
        fig2.add_trace(go.Scatter(
            x = Vg_array, y = df_biasarray,
            name = "FrequencyShift", mode='lines', showlegend=False,
            line_color=color_other
            ), row=1, col=2)
        fig2.add_trace(go.Scatter(
            x = Vg_array, y = dg_biasarray,
            name = "Dissipation", mode='lines', showlegend=False,
            line_color=color_other
            ), row=2, col=2)

        # Saving results
        save_bias_biasarray = pd.DataFrame({"Vg_biasarray": [str(x) for x in Vg_array]})
        save_Vs_biasarray = pd.DataFrame({"Vs_biasarray": [str(x) for x in Vs_biasarray]})
        save_F_biasarray = pd.DataFrame({"F_biasarray": [str(x) for x in F_biasarray]})
        save_df_biasarray = pd.DataFrame({"df_biasarray": [str(x) for x in df_biasarray]})
        save_dg_biasarray = pd.DataFrame({"dg_biasarray": [str(x) for x in dg_biasarray]})
        save_biasarrays = pd.concat([save_bias_biasarray,save_Vs_biasarray,save_F_biasarray,save_df_biasarray,save_dg_biasarray], axis=1, join="inner")
        save_biasarrays.to_csv('Xsave_BiasSweep_biasarrays.csv',index=False)


    ############################################################################

    else:
        Vg_array = np.linspace(-10,10,10) #placeholder
        Vs_biasarray = np.linspace(-10,10,10) #placeholder
        F_biasarray = np.linspace(-10,10,10) #placeholder
        df_biasarray = np.linspace(-10,10,10) #placeholder
        dg_biasarray = np.linspace(-10,10,10) #placeholder

        fig2 = make_subplots(
            rows=2, cols=2, shared_yaxes=False, shared_xaxes=False,
            column_widths=[0.5, 0.5], row_heights=[1,1],
            specs=[[{}, {}], [{}, {}]])
        fig2.add_trace(go.Scatter(y=[], x=[]), row=1, col=1)
        fig2.add_trace(go.Scatter(y=[], x=[]), row=2, col=1)
        fig2.add_trace(go.Scatter(y=[], x=[]), row=1, col=2)
        fig2.add_trace(go.Scatter(y=[], x=[]), row=2, col=2)

    ############################################################################

    # Automated axis scaling
    biasmin = -3
    biasmax = +3
    biasrange_indexmin = find_nearest(Vg_array,biasmin)
    biasrange_indexmax = find_nearest(Vg_array,biasmax)

    fig2.update_layout(transition_duration=300, height=600,margin=dict(t=0),showlegend=False)

    fig2.update_yaxes(row=1, col=1, title_text= "Contact Potential (eV)", range=[min(Vs_biasarray[biasrange_indexmin], Vs_biasarray[biasrange_indexmax]), max(Vs_biasarray)])
    fig2.update_yaxes(row=2, col=1, title_text= "Force (N)", range=[min(F_biasarray[biasrange_indexmin], F_biasarray[biasrange_indexmax]), max(F_biasarray)])
    fig2.update_yaxes(row=1, col=2, title_text = "Frequency Shift (Hz)", range=[min(df_biasarray[biasrange_indexmin], df_biasarray[biasrange_indexmax]), max(df_biasarray)])
    fig2.update_yaxes(row=2, col=2, title_text = "Dissipation (meV / cycle)", range=[min(dg_biasarray), max(dg_biasarray[biasrange_indexmin], dg_biasarray[biasrange_indexmax])])

    fig2.update_xaxes(row=1, col=1, showticklabels=True)
    fig2.update_xaxes(row=2, col=1, title_standoff=5, title_text= "Gate Bias (eV)", range=[Vg_array[biasrange_indexmin], Vg_array[biasrange_indexmax]])
    fig2.update_xaxes(row=1, col=2, showticklabels=True)
    fig2.update_xaxes(row=2, col=2, title_standoff=5, title_text= "Gate Bias (eV)", range=[Vg_array[biasrange_indexmin], Vg_array[biasrange_indexmax]])

    return fig2

################################################################################
################################################################################
# FIGURE: Time trace experiment

def fig3_AFM(calculatebutton,slider_sigma,slider_RTS1mag,slider_RTS1per,slider_RTS2mag,slider_RTS2per,slider_RTS3mag,slider_RTS3per,slider_RTS4mag,slider_RTS4per,slider_RTS5mag,slider_RTS5per,slider_f0y,slider_f1y,slider_f2y):

    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if 'AFMbutton_CalculateTimeExp' in changed_id:
        mu = 1 # signal (e.g. frequency shift)
    else:
        mu = 1 # signal (e.g. frequency shift)

    #########################################################
    #########################################################

    sigma = 2#slider_sigma
    points = 1000

    RTS1mag = 1   #slider_RTS1mag
    RTS1per = 0.905 #slider_RTS1per
    RTS2mag = 0#10  #slider_RTS2mag
    RTS2per = 0#0.992 #slider_RTS2per
    RTS3mag = 0#0.5 #slider_RTS3mag
    RTS3per = 0#0.974 #slider_RTS3per
    RTS4mag = 0#8   #slider_RTS4mag
    RTS4per = 0#0.975 #slider_RTS4per
    RTS5mag = 0#5   #slider_RTS5mag
    RTS5per = 0#0.892 #slider_RTS5per
    RTS6mag = 0#2
    RTS6per = 0#0.989
    RTS7mag = 0#4
    RTS7per = 0#0.942
    RTS8mag = 0#6
    RTS8per = 0#0.985
    RTS9mag = 0#7
    RTS9per = 0#0.899
    RTS10mag = 0#4
    RTS10per = 0#0.982

    f0y = 10**(-1*slider_f0y)
    f1y = 10**(-1*slider_f1y)
    f2y = 10**(-1*slider_f2y)

    noise_Signalbins = np.linspace(mu-5*sigma,mu+5*sigma,100)
    noise_Gaussianbins = np.linspace(mu-5*sigma,mu+5*sigma,100)
    noise_TwoLevelbins = np.linspace(mu-5*sigma,mu+5*sigma+RTS1mag+RTS2mag+RTS3mag+RTS4mag+RTS5mag,100)

    noise_timearray = Physics_Noise.Array_timearray()

    noise_Signalarray = Physics_Noise.Array_Signalarray(noise_timearray,mu,points)
    noise_SignalHistogram = Physics_Noise.Func_Histogram(noise_Signalarray,noise_Signalbins)
    PSD_Signalfreqs,PSD_Signalps = Physics_Noise.Func_PSD(noise_Signalarray)
    Allan_Signaltau, Allan_Signalvar = Physics_Noise.Func_AllanDev(noise_Signalarray)

    noise_Gaussianarray = Physics_Noise.Array_Gaussianarray(sigma,mu,noise_timearray)
    noise_GaussianHistogram = Physics_Noise.Func_Histogram(noise_Gaussianarray,noise_Gaussianbins)
    PSD_Gaussianfreqs,PSD_Gaussianps = Physics_Noise.Func_PSD(noise_Gaussianarray)
    Allan_Gaussiantau, Allan_Gaussianvar = Physics_Noise.Func_AllanDev(noise_Gaussianarray)

    noise_TwoLevelarray = Physics_Noise.Array_TwoLevelarray(RTS1mag,RTS1per,noise_Gaussianarray)
    noise_TwoLevelarray = Physics_Noise.Array_TwoLevelarray(RTS2mag,RTS2per,noise_TwoLevelarray)
    noise_TwoLevelarray = Physics_Noise.Array_TwoLevelarray(RTS3mag,RTS3per,noise_TwoLevelarray)
    noise_TwoLevelarray = Physics_Noise.Array_TwoLevelarray(RTS4mag,RTS4per,noise_TwoLevelarray)
    noise_TwoLevelarray = Physics_Noise.Array_TwoLevelarray(RTS5mag,RTS5per,noise_TwoLevelarray)
    noise_TwoLevelarray = Physics_Noise.Array_TwoLevelarray(RTS6mag,RTS6per,noise_TwoLevelarray)
    noise_TwoLevelarray = Physics_Noise.Array_TwoLevelarray(RTS7mag,RTS7per,noise_TwoLevelarray)
    noise_TwoLevelarray = Physics_Noise.Array_TwoLevelarray(RTS8mag,RTS8per,noise_TwoLevelarray)
    noise_TwoLevelarray = Physics_Noise.Array_TwoLevelarray(RTS9mag,RTS9per,noise_TwoLevelarray)
    noise_TwoLevelarray = Physics_Noise.Array_TwoLevelarray(RTS10mag,RTS10per,noise_TwoLevelarray)
    noise_TwoLevelHistogram = Physics_Noise.Func_Histogram(noise_TwoLevelarray,noise_TwoLevelbins)
    PSD_TwoLevelfreqs,PSD_TwoLevelps = Physics_Noise.Func_PSD(noise_TwoLevelarray)
    Allan_TwoLeveltau, Allan_TwoLevelvar = Physics_Noise.Func_AC(noise_timearray,noise_TwoLevelarray)
#    Allan_TwoLeveltau, Allan_TwoLevelvar = Physics_Noise.Func_AllanDev(noise_TwoLevelarray)


    # Saving results
    noise_magparamarray = np.array([RTS1mag,RTS2mag,RTS3mag,RTS4mag,RTS5mag,RTS6mag,RTS7mag,RTS8mag,RTS9mag,RTS10mag])
    noise_perparamarray = np.array([RTS1per,RTS2per,RTS3per,RTS4per,RTS5per,RTS6per,RTS7per,RTS8per,RTS9per,RTS10per])
    save_noise_magparam = pd.DataFrame({"noise_magparamarray": [str(x) for x in noise_magparamarray]})
    save_noise_perparam = pd.DataFrame({"noise_perparamarray": [str(x) for x in noise_perparamarray]})
    save_noise_paramarrays = pd.concat([save_noise_magparam,save_noise_perparam], axis=1, join="inner")

    save_noise_timearray = pd.DataFrame({"noise_timearray": [str(x) for x in noise_timearray]})
    save_noise_TwoLevelarray = pd.DataFrame({"noise_TwoLevelarray": [str(x) for x in noise_TwoLevelarray]})
    save_noise_timearrays = pd.concat([save_noise_timearray,save_noise_TwoLevelarray], axis=1, join="inner")

    save_noise_TwoLevelbins = pd.DataFrame({"noise_TwoLevelbins": [str(x) for x in noise_TwoLevelbins]})
    save_noise_TwoLevelhist = pd.DataFrame({"noise_TwoLevelHistogram": [str(x) for x in noise_TwoLevelHistogram[0]]})
    save_noise_histarrays = pd.concat([save_noise_TwoLevelbins,save_noise_TwoLevelhist], axis=1, join="inner")

    save_noise_PSDarray_TwoLevelfreqs = pd.DataFrame({"PSD_TwoLevelfreqs": [str(x) for x in PSD_TwoLevelfreqs]})
    save_noise_PSDarray_TwoLevelps = pd.DataFrame({"PSD_TwoLevelps": [str(x) for x in PSD_TwoLevelps]})
    save_noise_PSDarrays = pd.concat([save_noise_PSDarray_TwoLevelfreqs,save_noise_PSDarray_TwoLevelps], axis=1, join="inner")

    save_noise_Allanarray_TwoLeveltau = pd.DataFrame({"Allan_TwoLeveltau": [str(x) for x in Allan_TwoLeveltau]})
    save_noise_Allanarray_TwoLevelvar = pd.DataFrame({"Allan_TwoLevelvar": [str(x) for x in Allan_TwoLevelvar]})
    save_noise_Allanarrays = pd.concat([save_noise_Allanarray_TwoLeveltau,save_noise_Allanarray_TwoLevelvar], axis=1, join="inner")

    save_noisearrays = pd.concat([save_noise_paramarrays,save_noise_timearrays,save_noise_histarrays,save_noise_PSDarrays,save_noise_Allanarrays], axis=0)
    save_noisearrays.to_csv('Xsave_Noisearrays.csv',index=False)

    hopchance_array = np.random.uniform(low=0,high=1,size=10000)
    save_hopchancearray = pd.DataFrame({"hopchance_array": [str(x) for x in hopchance_array]})
    save_hopchancearray.to_csv('Xsave_hopchancearray.csv',index=False)

    # http://www.scholarpedia.org/article/1/f_noise#1.2Ff_noise_in_solids.2C_condensed_matter_and_electronic_devices

    #########################################################
    #########################################################
    fig3 = make_subplots(
        rows=3, cols=6, shared_yaxes=False, shared_xaxes=False,
        column_widths=[0.8, 0.2, 0.1, 0.4, 0.1, 0.4], row_heights=[0.7, 0.7, 0.7],
        vertical_spacing=0.1, horizontal_spacing=0,
        specs=[
        [{},{},{},{},{},{}],
        [{},{},{},{},{},{}],
        [{},{},{},{},{},{}]])

    fig3.add_trace(go.Scatter(
        x = noise_timearray, y = noise_Signalarray,
        name = "TrueSignal TimeTrace", mode='lines', showlegend=False,
        line_color=color_other
        ), row=1, col=1)
    fig3.add_trace(go.Scatter(
        x = noise_SignalHistogram[0], y = noise_Signalbins,
        name = "TrueSignal Distrubution", mode='lines', showlegend=False,
        line_color=color_other
        ), row=1, col=2)
    fig3.add_trace(go.Scatter(
        x = PSD_Signalfreqs, y = PSD_Signalps,
        name = "TrueSignal PSD", mode='lines', showlegend=False,
        line_color=color_other
        ), row=1, col=4)
    fig3.add_trace(go.Scatter(
        x = Allan_Signaltau, y = Allan_Signalvar,
        name = "TrueSignal Allan", mode='lines', showlegend=False,
        line_color=color_other
        ), row=1, col=6)


    fig3.add_trace(go.Scatter(
        x = noise_timearray, y = noise_Gaussianarray,
        name = "WhiteNoise TimeTrace", mode='lines', showlegend=False,
        line_color=color_other
        ), row=2, col=1)
    fig3.add_trace(go.Scatter(
        x = noise_GaussianHistogram[0], y = noise_Gaussianbins,
        name = "WhiteNoise Distrubution", mode='lines', showlegend=False,
        line_color=color_other
        ), row=2, col=2)
    fig3.add_trace(go.Scatter(
        x = PSD_Gaussianfreqs, y = PSD_Gaussianps,
        name = "WhiteNoise PSD", mode='lines', showlegend=False,
        line_color=color_other
        ), row=2, col=4)
    fig3.add_trace(go.Scatter(
        x = PSD_TwoLevelfreqs, y = 1/(f0y*PSD_TwoLevelfreqs**0),
        name = "1/f^0 line", mode='lines', showlegend=False,
        line_color=color_Ef
        ), row=2, col=4)
    fig3.add_trace(go.Scatter(
        x = PSD_TwoLevelfreqs, y = 1/(f1y*PSD_TwoLevelfreqs**1),
        name = "1/f^1 line", mode='lines', showlegend=False,
        line_color=color_Ev
        ), row=2, col=4)
    fig3.add_trace(go.Scatter(
        x = PSD_TwoLevelfreqs, y = 1/(f2y*PSD_TwoLevelfreqs**2),
        name = "1/f^2 line", mode='lines', showlegend=False,
        line_color=color_Ec
        ), row=2, col=4)
    fig3.add_trace(go.Scatter(
        x = Allan_Gaussiantau, y = Allan_Gaussianvar,
        name = "WhiteNoise Allan", mode='markers', showlegend=False,
        line_color=color_other
        ), row=2, col=6)
    fig3.add_trace(go.Scatter(
        x = PSD_TwoLevelfreqs, y = 1/(f2y*PSD_TwoLevelfreqs**2),
        name = "1/f^2 line", mode='lines', showlegend=False,
        line_color=color_Ec
        ), row=2, col=6)

    fig3.add_trace(go.Scatter(
        x = noise_timearray, y = noise_TwoLevelarray,
        name = "PinkNoise TimeTrace", mode='lines', showlegend=False,
        line_color=color_other
        ), row=3, col=1)
    fig3.add_trace(go.Scatter(
        x = noise_TwoLevelHistogram[0], y = noise_TwoLevelbins,
        name = "PinkNoise Distrubution", mode='lines', showlegend=False,
        line_color=color_other
        ), row=3, col=2)
    fig3.add_trace(go.Scatter(
        x = PSD_TwoLevelfreqs, y = PSD_TwoLevelps,
        name = "PinkNoise PSD", mode='lines', showlegend=False,
        line_color=color_other
        ), row=3, col=4)
    fig3.add_trace(go.Scatter(
        x = PSD_TwoLevelfreqs, y = 1/(f0y*PSD_TwoLevelfreqs**0),
        name = "1/f^0 line", mode='lines', showlegend=False,
        line_color=color_Ef
        ), row=3, col=4)
    fig3.add_trace(go.Scatter(
        x = PSD_TwoLevelfreqs, y = 1/(f1y*PSD_TwoLevelfreqs**1),
        name = "1/f^1 line", mode='lines', showlegend=False,
        line_color=color_Ev
        ), row=3, col=4)
    fig3.add_trace(go.Scatter(
        x = PSD_TwoLevelfreqs, y = 1/(f2y*PSD_TwoLevelfreqs**2),
        name = "1/f^2 line", mode='lines', showlegend=False,
        line_color=color_Ec
        ), row=3, col=4)
    fig3.add_trace(go.Scatter(
        x = Allan_TwoLeveltau, y = Allan_TwoLevelvar,
        name = "PinkNoise Allan", mode='markers', showlegend=False,
        line_color=color_other
        ), row=3, col=6)
    # fig3.add_trace(go.Scatter(
    #     x = PSD_TwoLevelfreqs, y = 1/(f1y*PSD_TwoLevelfreqs**1),
    #     name = "1/f^1 line", mode='lines', showlegend=False,
    #     line_color=color_Ev
    #     ), row=3, col=6)
    # fig3.add_trace(go.Scatter(
    #     x = PSD_TwoLevelfreqs, y = 1/(f2y*PSD_TwoLevelfreqs**2),
    #     name = "1/f^2 line", mode='lines', showlegend=False,
    #     line_color=color_Ec
    #     ), row=3, col=6)

    ############################################################################
    ############################################################################

    fig3.update_layout(transition_duration=100, height=800,margin=dict(t=0),showlegend=False)

    fig3.update_yaxes(title_standoff=0,row=1, col=1, title_text= "Signal")
    fig3.update_yaxes(title_standoff=0,row=2, col=1, title_text = "White noise")
    fig3.update_yaxes(title_standoff=0,row=3, col=1, title_text = "Pink noise")
    fig3.update_yaxes(title_standoff=0,row=1, col=4, title_text = "PSD",type="log")
    fig3.update_yaxes(title_standoff=0,row=2, col=4, title_text = "PSD",type="log")
    fig3.update_yaxes(title_standoff=0,row=3, col=4, title_text = "PSD",type="log")
    fig3.update_yaxes(title_standoff=0,row=1, col=6, title_text = "sigma^2",type="log")
    fig3.update_yaxes(title_standoff=0,row=2, col=6, title_text = "sigma^2",type="log")
    #fig3.update_yaxes(title_standoff=0,row=3, col=6, title_text = "sigma^2",type="log")

    fig3.update_xaxes(title_standoff=5,row=1, col=1, showticklabels=True, title_text= "Time (s)")
    fig3.update_xaxes(title_standoff=5,row=2, col=1, showticklabels=True, title_text= "Time (s)")
    fig3.update_xaxes(title_standoff=5,row=1, col=2, showticklabels=True, title_text= "Time (s)")
    fig3.update_xaxes(title_standoff=5,row=2, col=2, showticklabels=True, title_text= "Count")
    fig3.update_xaxes(title_standoff=5,row=2, col=2, showticklabels=True, title_text= "Count")
    fig3.update_xaxes(title_standoff=5,row=1, col=4, showticklabels=True, title_text= "freq",type="log")
    fig3.update_xaxes(title_standoff=5,row=2, col=4, showticklabels=True, title_text= "freq",type="log")
    fig3.update_xaxes(title_standoff=5,row=3, col=4, showticklabels=True, title_text= "freq",type="log")
    fig3.update_xaxes(title_standoff=5,row=1, col=6, showticklabels=True, title_text= "tau",type="log")
    fig3.update_xaxes(title_standoff=5,row=2, col=6, showticklabels=True, title_text= "tau",type="log")
    #fig3.update_xaxes(title_standoff=5,row=3, col=6, showticklabels=True, title_text= "tau",type="log")

    return fig3


################################################################################
################################################################################
# FIGURE: Delay sweep experiment

def fig4_AFM(slider_Vg,slider_zins,slider_Eg,slider_epsilonsem,slider_WFmet,slider_EAsem,slider_donor,slider_acceptor,slider_emass,slider_hmass,slider_T,slider_alpha, slider_timesteps, slider_amplitude,slider_resfreq,slider_springconst,slider_tipradius,slider_Qfactor,calculatebutton,toggle_sampletype,slider_hop,slider_lag,slider_pulsetimesteps,slider_delaysteps):

    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if 'AFMbutton_CalculateDelayExp' in changed_id:

        # input (slider) parameters
        Vg = slider_Vg*(1-slider_alpha)
        zins = slider_zins*1e-7 # cm
        Eg = slider_Eg
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
        timesteps = slider_timesteps
        pulsetimesteps = slider_pulsetimesteps
        delaysteps = slider_delaysteps

        pulsetime_array = np.linspace(-5,5,pulsetimesteps)
        delay_array = np.linspace(-5,5,delaysteps)

        intensity_delayarray = Physics_Optics.intensity_delayarray(pulsetime_array,delay_array)
        Vs_delayarray, F_delayarray, df_delayarray, dg_delayarray =  Organization_BuildArrays.VsFdfdg_delayarrays(delay_array,intensity_delayarray,timesteps,amplitude,frequency,springconst,Qfactor,tipradius,sampletype,hop,lag,  Vg,zins,Eg,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T)

        #########################################################
        #########################################################
        fig4 = make_subplots(
            rows=6, cols=1, shared_yaxes=False, shared_xaxes=True,
            column_widths=[0.5], row_heights=[1,1,1,1,1,1],
            vertical_spacing=0.03,
            specs=[[{}], [{}], [{}], [{}], [{}], [{}]])

        fig4.add_trace(go.Scatter(
            x = pulsetime_array, y = Physics_Optics.Epulse_array(pulsetime_array,0),
            name = "Pulse1 2 delay", mode='lines', showlegend=False,
            line_color=color_Ec
            ), row=1, col=1)
        fig4.add_trace(go.Scatter(
            x = pulsetime_array, y = Physics_Optics.Epulse_array(pulsetime_array,2),
            name = "Pulse2 2 delay", mode='lines', showlegend=False,
            line_color=color_Ev
            ), row=1, col=1)
        fig4.add_trace(go.Scatter(
            x = delay_array, y = intensity_delayarray,
            name = "Collinear Optical Autocorrelation Function", mode='lines', showlegend=False,
            line_color=color_other
            ), row=2, col=1)
        fig4.add_trace(go.Scatter(
            x = delay_array, y = Vs_delayarray,
            name = "ContactPotential", mode='lines', showlegend=False,
            line_color=color_other
            ), row=3, col=1)
        fig4.add_trace(go.Scatter(
            x = delay_array, y = F_delayarray,
            name = "Force", mode='lines', showlegend=False,
            line_color=color_other
            ), row=4, col=1)
        fig4.add_trace(go.Scatter(
            x = delay_array, y = df_delayarray,
            name = "FrequencyShift", mode='lines', showlegend=False,
            line_color=color_other
            ), row=5, col=1)
        fig4.add_trace(go.Scatter(
            x = delay_array, y = dg_delayarray,
            name = "Dissipation", mode='lines', showlegend=False,
            line_color=color_other
            ), row=6, col=1)

    ############################################################################

    else:
        fig4 = make_subplots(
            rows=6, cols=1, shared_yaxes=False, shared_xaxes=True,
            column_widths=[0.5], row_heights=[1,1,1,1,1,1],
            vertical_spacing=0.03,
            specs=[[{}], [{}], [{}], [{}], [{}], [{}]])
        fig4.add_trace(go.Scatter(y=[], x=[]), row=1, col=1)
        fig4.add_trace(go.Scatter(y=[], x=[]), row=2, col=1)
        fig4.add_trace(go.Scatter(y=[], x=[]), row=3, col=1)
        fig4.add_trace(go.Scatter(y=[], x=[]), row=4, col=1)
        fig4.add_trace(go.Scatter(y=[], x=[]), row=5, col=1)
        fig4.add_trace(go.Scatter(y=[], x=[]), row=6, col=1)

    ############################################################################

    fig4.update_layout(transition_duration=300, height=1400,margin=dict(t=0),showlegend=False)

    fig4.update_yaxes(row=1, col=1, title_text= "Pulse Examples")
    fig4.update_yaxes(row=2, col=1, title_text= "Illumination Intensity")
    fig4.update_yaxes(row=3, col=1, title_text= "Contact Potential (eV)")
    fig4.update_yaxes(row=4, col=1, title_text= "Force (N)")
    fig4.update_yaxes(row=5, col=1, title_text = "Frequency Shift (Hz)")
    fig4.update_yaxes(row=6, col=1, title_text = "Dissipation (meV / cycle)")

    fig4.update_xaxes(row=1, col=1,showticklabels=True)
    fig4.update_xaxes(row=2, col=1,showticklabels=True)
    fig4.update_xaxes(row=3, col=1,showticklabels=True)
    fig4.update_xaxes(row=4, col=1,showticklabels=True)
    fig4.update_xaxes(row=5, col=1,showticklabels=True)
    fig4.update_xaxes(row=6, col=1,title_text= "Delay (arb)")

    return fig4


################################################################################
################################################################################
# READOUTS

def readouts_AFM(slider_timesteps, slider_amplitude, slider_hop, slider_lag, slider_resfreq, slider_springconst, slider_Qfactor, slider_tipradius, slider_pulsetimesteps, slider_delaysteps):
    readout_timesteps = '{0:.0f}'.format(slider_timesteps)
    readout_amplitude = '{0:.1f}'.format(slider_amplitude)
    readout_lag = '{0:.0f}'.format(slider_lag)
    readout_hop = '{0:.2f}'.format(slider_hop)
    readout_resfreq = '{0:.0f}'.format(slider_resfreq)
    readout_springconst = '{0:.0f}'.format(slider_springconst)
    readout_Qfactor = '{0:.0f}'.format(slider_Qfactor)
    readout_tipradius = '{0:.0f}'.format(slider_tipradius)
    readout_pulsetimesteps = '{0:.0f}'.format(slider_pulsetimesteps)
    readout_delaysteps = '{0:.0f}'.format(slider_delaysteps)
    return readout_timesteps, readout_amplitude, readout_hop, readout_lag, readout_resfreq, readout_springconst, readout_Qfactor, readout_tipradius, readout_pulsetimesteps, readout_delaysteps


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
