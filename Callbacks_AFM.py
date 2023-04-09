import dash
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import pandas as pd

import Physics_Semiconductors
import Physics_ncAFM
import Physics_Noise
import Physics_Optics

import Organization_IntermValues
import Organization_BuildArrays

################################################################################
################################################################################
# FIGURE: ncAFM oscillations

def fig1_AFM(slider_Vg, slider_zins, slider_Eg, slider_epsilonsem, slider_WFmet, slider_EAsem, slider_donor, slider_acceptor, slider_emass, slider_hmass, slider_T, slider_alpha, slider_biassteps,slider_zinssteps, slider_timesteps, slider_amplitude, slider_resfreq, slider_lag, slider_tipradius, slider_cantheight, slider_cantarea, geometrybuttons, calculatebutton):

    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if 'AFMbutton_Calculate' in changed_id:

          
        # Input values and arrays
        Vg,zins,Eg,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T,sampletype,biassteps,zinssteps,Vg_array,zins_array=Organization_IntermValues.Surface_inputvalues(slider_Vg,slider_zins,slider_alpha,slider_Eg,slider_epsilonsem,slider_WFmet,slider_EAsem,slider_donor,slider_acceptor,slider_emass,slider_hmass,slider_T,slider_biassteps,slider_zinssteps)
        amplitude,frequency,lag,timesteps,tipradius,cantheight,cantarea,time_AFMarray,zins_AFMarray,zinslag_AFMarray=Organization_IntermValues.AFM1_inputvalues(slider_amplitude,slider_resfreq,slider_lag,slider_timesteps,slider_tipradius,slider_cantheight,slider_cantarea, zins)

        # Calculations and results
        NC,NV,Ec,Ev,Ei,Ef,no,po,ni,nb,pb,CPD,LD,Vs,Es,Qs,F,regime, zsem,Vsem,Esem,Qsem, P = Organization_IntermValues.Surface_calculations(Vg,zins,Eg,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T)
        Vs_zinsarray,F_zinsarray,Es_zinsarray,Qs_zinsarray,P_zinsarray = Organization_BuildArrays.Surface_zinsarrays(zins_array,Vg,Na,Nd,epsilon_sem,T,CPD,LD,nb,pb,ni)
        Vs_AFMarray, F_AFMarray, Fcant_AFMarray, Fover_AFMarray, P_AFMarray = Organization_BuildArrays.AFM_timearrays(time_AFMarray,zins_AFMarray,zinslag_AFMarray,Vg,zins,Na,Nd,epsilon_sem,T,CPD,LD,nb,pb,ni,cantheight)
        zsem_AFMarray,Vsem_AFMarray,zgap_AFMarray,Vgap_AFMarray,zvac_AFMarray,Vvac_AFMarray,zmet_AFMarray,Vmet_AFMarray = Organization_BuildArrays.AFM_banddiagrams(zins_AFMarray,Vg,T,Nd,Na,WFmet,EAsem,epsilon_sem, ni,nb,pb,Vs,Ec,Ev,Ei,Ef,Eg,CPD)

        # Account for alpha
        Vg = slider_Vg*Physics_Semiconductors.e #J
        Vg_array = np.linspace(-10,10,biassteps)*Physics_Semiconductors.e #J
    
        # Stack arrays to show two periods
        time_AFMarray = np.hstack((time_AFMarray,time_AFMarray[1:]+2*np.pi/frequency))
        zins_AFMarray = np.hstack((zins_AFMarray,zins_AFMarray[1:]))
        zinslag_AFMarray = np.hstack((zinslag_AFMarray,zinslag_AFMarray[1:]))
        Vs_AFMarray = np.hstack((Vs_AFMarray,Vs_AFMarray[1:]))
        F_AFMarray = np.hstack((F_AFMarray,F_AFMarray[1:]))*np.pi*tipradius**2
        Fcant_AFMarray = np.hstack((Fcant_AFMarray,Fcant_AFMarray[1:]))*cantarea
        Fover_AFMarray = np.hstack((Fover_AFMarray,Fover_AFMarray[1:]))*np.pi*tipradius**2        
        zsem_AFMarray_steps = np.vstack((zsem_AFMarray,zsem_AFMarray[1:]))
        Vsem_AFMarray_steps = np.vstack((Vsem_AFMarray,Vsem_AFMarray[1:]))
        zgap_AFMarray_steps = np.vstack((zgap_AFMarray,zgap_AFMarray[1:]))
        Vgap_AFMarray_steps = np.vstack((Vgap_AFMarray,Vgap_AFMarray[1:]))
        zvac_AFMarray_steps = np.vstack((zvac_AFMarray,zvac_AFMarray[1:]))
        Vvac_AFMarray_steps = np.vstack((Vvac_AFMarray,Vvac_AFMarray[1:]))
        zmet_AFMarray_steps = np.vstack((zmet_AFMarray,zmet_AFMarray[1:]))
        Vmet_AFMarray_steps = np.vstack((Vmet_AFMarray,Vmet_AFMarray[1:]))
    
        Ftot_AFMarray = 0*time_AFMarray
        if 1 in geometrybuttons:
            Ftot_AFMarray+=F_AFMarray
        if 2 in geometrybuttons:
            Ftot_AFMarray+=Fcant_AFMarray
        if 3 in geometrybuttons:
            Ftot_AFMarray+=Fover_AFMarray
        if 4 in geometrybuttons:
            Ftot_AFMarray+=F_AFMarray+Fcant_AFMarray+Fover_AFMarray


        #########################################################
        #########################################################
        fig1 = make_subplots(
            rows=3, cols=2, shared_yaxes=False, shared_xaxes=False,
            column_widths=[0.3, 0.7], row_heights=[1,1,1],
            specs=[[{}, {}], [{}, {}], [{}, {}]])
    
        fig1.add_trace(go.Scatter(
            y = zsem_AFMarray[0]*1e9, x = (Ev-Vsem_AFMarray[0])/Physics_Semiconductors.e,
            name = "ValenceBand", mode='lines', showlegend=False,
            line_color=color_Ev
            ), row=1, col=1)
        fig1.add_trace(go.Scatter(
            y = zsem_AFMarray[0]*1e9, x = (Ei-Vsem_AFMarray[0])/Physics_Semiconductors.e,
            name = "IntrinsicEnergy", mode='lines', showlegend=False,
            line_color=color_Ei
            ), row=1, col=1)
        fig1.add_trace(go.Scatter(
            y = zsem_AFMarray[0]*1e9, x = (Ec-Vsem_AFMarray[0])/Physics_Semiconductors.e,
            name = "ConductionBand", mode='lines', showlegend=False,
            line_color=color_Ec
            ), row=1, col=1)
        fig1.add_trace(go.Scatter(
            y = zsem_AFMarray[0]*1e9, x = 0*zsem_AFMarray[0]+Ef/Physics_Semiconductors.e,
            name = "FermiEnergy", mode='lines', showlegend=False,
            line_color=color_Ef
            ), row=1, col=1)
        fig1.add_trace(go.Scatter(
            y = zgap_AFMarray[0]*1e9, x = Vgap_AFMarray[0]/Physics_Semiconductors.e,
            name = "Insulator", mode='lines', showlegend=False,
            line_color=color_ox
            ), row=1, col=1)
        fig1.add_trace(go.Scatter(
            y = zmet_AFMarray[0]*1e9, x = Vmet_AFMarray[0]/Physics_Semiconductors.e,
            name = "GateFermiEnergy", mode='lines', showlegend=False,
            line_color=color_met
            ), row=1, col=1)
        fig1.add_trace(go.Scatter(
            y = zvac_AFMarray[0]*1e9, x = Vvac_AFMarray[0]/Physics_Semiconductors.e,
            name = "VacuumEnergy", mode='lines', showlegend=False,
            line_color=color_vac
            ), row=1, col=1)

        fig1.add_trace(go.Scatter(
            x = zins_array*1e9, y = Vs_zinsarray/Physics_Semiconductors.e,
            name = "ContactPotential", mode='lines', showlegend=False,
            line_color=color_vac
            ), row=2, col=1)
        fig1.add_trace(go.Scatter(
            x = [zinslag_AFMarray[0]*1e9], y = [Vs_AFMarray[0]/Physics_Semiconductors.e],
            name = "ContactPotential", mode='markers', showlegend=False,
            marker=dict(color=color_indicator,size=10),
            ), row=2, col=1)
        fig1.add_trace(go.Scatter(
            x = zins_array*1e9, y = F_zinsarray*(1e-9)**2*1e12,
            name = "Force", mode='lines', showlegend=False,
            line_color=color_vac
            ), row=3, col=1)
        fig1.add_trace(go.Scatter(
            x = [zinslag_AFMarray[0]*1e9], y = [F_AFMarray[0]*(1e-9)**2*1e12],
            name = "Force", mode='markers', showlegend=False,
            marker=dict(color=color_indicator,size=10),
            ), row=3, col=1)

        fig1.add_trace(go.Scatter(
            x = time_AFMarray, y = zins_AFMarray*1e9,
            name = "Position", mode='lines', showlegend=False,
            line_color=color_other
            ), row=1, col=2),
        fig1.add_trace(go.Scatter(
            x = [time_AFMarray[0]], y = [zins_AFMarray[0]*1e9],
            name = "Position", mode='markers',
            marker=dict(color=color_indicator,size=10),
            ), row=1, col=2)
        fig1.add_trace(go.Scatter(
            x = time_AFMarray, y = Vs_AFMarray/Physics_Semiconductors.e,
            name = "SurfacePotential", mode='lines', showlegend=False,
            line_color=color_other
            ), row=2, col=2),
        fig1.add_trace(go.Scatter(
            x = [time_AFMarray[0]], y = [Vs_AFMarray[0]/Physics_Semiconductors.e],
            name = "SurfacePotential", mode='markers',
            marker=dict(color=color_indicator,size=10),
            ), row=2, col=2)
        if 1 in geometrybuttons:
            fig1.add_trace(go.Scatter(
                x = time_AFMarray, y = F_AFMarray*(1e-9)**2*1e12,
                name = "Sample Force", mode='lines', showlegend=False,
                line_color=color_Ef
                ), row=3, col=2)
        if 2 in geometrybuttons:
            fig1.add_trace(go.Scatter(
                x = time_AFMarray, y = Fcant_AFMarray*(1e-9)**2*1e12,
                name = "Cantilever Force", mode='lines', showlegend=False,
                line_color=color_n
                ), row=3, col=2)
        if 3 in geometrybuttons:
            fig1.add_trace(go.Scatter(
                x = time_AFMarray, y = Fover_AFMarray*(1e-9)**2*1e12,
                name = "Overlayer Force", mode='lines', showlegend=False,
                line_color=color_p
                ), row=3, col=2)
        if 4 in geometrybuttons:
            fig1.add_trace(go.Scatter(
                x = time_AFMarray, y = Ftot_AFMarray*(1e-9)**2*1e12,
                name = "Total Force", mode='lines', showlegend=False,
                line_color=color_other
                ), row=3, col=2)
        fig1.add_trace(go.Scatter(
            x = [time_AFMarray[0]], y = [Ftot_AFMarray[0]*(1e-9)**2*1e12],
            name = "Total Force", mode='markers',
            marker=dict(color=color_indicator,size=10),
            ), row=3, col=2)

        fig1.frames=[
            go.Frame(data=[
                go.Scatter(y=zsem_AFMarray_steps[step]*1e9, x=(Ev-Vsem_AFMarray_steps[step])/Physics_Semiconductors.e,mode="lines", line_color=color_Ev),
                go.Scatter(y=zsem_AFMarray_steps[step]*1e9, x=(Ei-Vsem_AFMarray_steps[step])/Physics_Semiconductors.e,mode="lines", line_color=color_Ei),
                go.Scatter(y=zsem_AFMarray_steps[step]*1e9, x=(Ec-Vsem_AFMarray_steps[step])/Physics_Semiconductors.e,mode="lines", line_color=color_Ec),
                go.Scatter(y=zsem_AFMarray_steps[step]*1e9, x=(0*zsem_AFMarray_steps[step]+Ef)/Physics_Semiconductors.e,mode="lines", line_color=color_Ef),
                go.Scatter(y=zgap_AFMarray_steps[step]*1e9, x=Vgap_AFMarray_steps[step]/Physics_Semiconductors.e,mode="lines", line_color=color_ox),
                go.Scatter(y=zmet_AFMarray_steps[step]*1e9, x=Vmet_AFMarray_steps[step]/Physics_Semiconductors.e,mode="lines", line_color=color_met),
                go.Scatter(y=zvac_AFMarray_steps[step]*1e9, x=Vvac_AFMarray_steps[step]/Physics_Semiconductors.e,mode="lines", line_color=color_vac),

                go.Scatter(x=zins_array*1e9, y=Vs_zinsarray/Physics_Semiconductors.e,mode="lines", line_color=color_vac),
                go.Scatter(x=[zinslag_AFMarray[step]*1e9], y=[Vs_AFMarray[step]/Physics_Semiconductors.e],mode="markers", marker=dict(color=color_indicator, size=10)),
                go.Scatter(x=zins_array*1e9, y=F_zinsarray*(1e-9)**2*1e12,mode="lines", line_color=color_vac),
                go.Scatter(x=[zinslag_AFMarray[step]*1e9], y=[F_AFMarray[step]*(1e-9)**2*1e12],mode="markers", marker=dict(color=color_indicator, size=10)),

                go.Scatter(x=time_AFMarray,y=zins_AFMarray*1e9,mode="lines", line_color=color_other),
                go.Scatter(x=[time_AFMarray[step]],y=[zins_AFMarray[step]*1e9],mode="markers", marker=dict(color=color_indicator, size=10)),
                go.Scatter(x=time_AFMarray,y=Vs_AFMarray/Physics_Semiconductors.e,mode="lines", line_color=color_other),
                go.Scatter(x=[time_AFMarray[step]],y=[Vs_AFMarray[step]/Physics_Semiconductors.e],mode="markers", marker=dict(color=color_indicator, size=10)),
                go.Scatter(x=time_AFMarray,y=F_AFMarray*(1e-9)**2*1e12,mode="lines", line_color=color_other),
                go.Scatter(x=[time_AFMarray[step]],y=[F_AFMarray[step]*(1e-9)**2*1e12],mode="markers", marker=dict(color=color_indicator, size=10)),
                ],traces=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16])
                for step in range(2*timesteps-1)]
        
    ############################################################################

    else:
        zins = 0
        amplitude = 0
        Vs_zinsarray = [0, 0]
        F_biasarray = [0, 0]
        timesteps = 1
        frequency = 1
        
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

    fig1.update_yaxes(row=1, col=1, title_text= "Insulator Thickness (nm)")
    fig1.update_yaxes(row=2, col=1, title_text= "Contact Potential (eV)")#, range=[min(Vs_zinsarray), max(Vs_zinsarray)])
    fig1.update_yaxes(row=3, col=1, title_text= "Force (N/nm^2)")
    fig1.update_yaxes(row=1, col=2)
    fig1.update_yaxes(row=2, col=2)
    fig1.update_yaxes(row=3, col=2)

    fig1.update_xaxes(row=1, col=1, title_text= "Energy (eV)")
    fig1.update_xaxes(row=2, col=1, title_text= "Insulator Thickness (nm)")
    fig1.update_xaxes(row=3, col=1, title_text= "Insulator Thickness (nm)")
    fig1.update_xaxes(row=1, col=2, title_text= "Time", showticklabels=False, range=[0, 4*np.pi/frequency])
    fig1.update_xaxes(row=2, col=2, title_text= "Time", showticklabels=False, range=[0, 4*np.pi/frequency])
    fig1.update_xaxes(row=3, col=2, title_text= "Time", showticklabels=False, range=[0, 4*np.pi/frequency])

    return fig1


################################################################################
################################################################################
# FIGURE: Bias sweep experiment

def fig2_AFM(slider_Vg,slider_zins,slider_Eg,slider_epsilonsem,slider_WFmet,slider_EAsem,slider_donor,slider_acceptor,slider_emass,slider_hmass,slider_T,slider_alpha,slider_biassteps,slider_zinssteps, slider_timesteps,slider_amplitude,slider_resfreq,slider_springconst,slider_tipradius,slider_cantheight, slider_cantarea, slider_Qfactor,slider_lag,geometrybuttons,experimentbuttons,calculatebutton):

    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if 'AFMbutton_CalculateBiasExp' in changed_id:

        # Input values and arrays
        Vg,zins,Eg,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T,sampletype,biassteps,zinssteps,Vg_array,zins_array=Organization_IntermValues.Surface_inputvalues(slider_Vg,slider_zins,slider_alpha,slider_Eg,slider_epsilonsem,slider_WFmet,slider_EAsem,slider_donor,slider_acceptor,slider_emass,slider_hmass,slider_T,slider_biassteps,slider_zinssteps)
        amplitude,frequency,lag,timesteps,tipradius,cantheight,cantarea,time_AFMarray,zins_AFMarray,zinslag_AFMarray=Organization_IntermValues.AFM1_inputvalues(slider_amplitude,slider_resfreq,slider_lag,slider_timesteps,slider_tipradius,slider_cantheight,slider_cantarea, zins)
        springconst,Qfactor=Organization_IntermValues.AFM2_inputvalues(slider_springconst,slider_Qfactor)

        # Calculations and results
        NC,NV,Ec,Ev,Ei,Ef,no,po,ni,nb,pb,CPD,LD,Vs,Es,Qs,F,regime, zsem,Vsem,Esem,Qsem, P = Organization_IntermValues.Surface_calculations(Vg,zins,Eg,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T)
        Vs_biasarray,F_biasarray,df_biasarray,dg_biasarray = Organization_BuildArrays.AFM_biasarrays(Vg_array,zins,Na,Nd,epsilon_sem,T,CPD,LD,nb,pb,ni,frequency,springconst,amplitude,Qfactor,tipradius,time_AFMarray,zins_AFMarray,zinslag_AFMarray,cantheight,cantarea,timesteps,geometrybuttons)
        
        # Account for alpha
        Vg = slider_Vg*Physics_Semiconductors.e #J
        Vg_array = np.linspace(-10,10,biassteps)*Physics_Semiconductors.e #J


        #########################################################
        #########################################################
        fig2 = make_subplots(
            rows=2, cols=2, shared_yaxes=False, shared_xaxes=True,
            column_widths=[0.5, 0.5], row_heights=[1,1],
            specs=[[{}, {}], [{}, {}]])
        fig2.add_trace(go.Scatter(
            x = Vg_array/Physics_Semiconductors.e, y = Vs_biasarray/Physics_Semiconductors.e,
            name = "ContactPotential", mode='lines', showlegend=False,
            line_color=color_other
            ), row=1, col=1)
        fig2.add_trace(go.Scatter(
            x = Vg_array/Physics_Semiconductors.e, y = F_biasarray*(1e-9)**2*1e12,
            name = "Force", mode='lines', showlegend=False,
            line_color=color_other
            ), row=2, col=1)
        


    ####################### # zins experiment 1

        if 1 in experimentbuttons:
            Data_Vg = np.genfromtxt ('Data/Si_zins1/Data_zins_Vg.csv', delimiter=",")
            Data_df_0 = np.genfromtxt ('Data/Si_zins1/Data_zins0_df.csv', delimiter=",")
            Data_df_1 = np.genfromtxt ('Data/Si_zins1/Data_zins1_df.csv', delimiter=",")
            Data_df_2 = np.genfromtxt ('Data/Si_zins1/Data_zins2_df.csv', delimiter=",")
            Data_df_3 = np.genfromtxt ('Data/Si_zins1/Data_zins3_df.csv', delimiter=",")
            Data_df_4 = np.genfromtxt ('Data/Si_zins1/Data_zins4_df.csv', delimiter=",")
            Data_df_5 = np.genfromtxt ('Data/Si_zins1/Data_zins5_df.csv', delimiter=",")
            Data_df_6 = np.genfromtxt ('Data/Si_zins1/Data_zins6_df.csv', delimiter=",")
            Data_dg_0 = np.genfromtxt ('Data/Si_zins1/Data_zins0_dg.csv', delimiter=",")
            Data_dg_1 = np.genfromtxt ('Data/Si_zins1/Data_zins1_dg.csv', delimiter=",")
            Data_dg_2 = np.genfromtxt ('Data/Si_zins1/Data_zins2_dg.csv', delimiter=",")
            Data_dg_3 = np.genfromtxt ('Data/Si_zins1/Data_zins3_dg.csv', delimiter=",")
            Data_dg_4 = np.genfromtxt ('Data/Si_zins1/Data_zins4_dg.csv', delimiter=",")
            Data_dg_5 = np.genfromtxt ('Data/Si_zins1/Data_zins5_dg.csv', delimiter=",")
            Data_dg_6 = np.genfromtxt ('Data/Si_zins1/Data_zins6_dg.csv', delimiter=",")

            fig2.add_trace(go.Scatter(
                x = Data_Vg, y = Data_df_0+2.1633, name = "df_0", mode='lines', showlegend=False, line_color=color_0
                ), row=1, col=2)
            fig2.add_trace(go.Scatter(
                x = Data_Vg, y = Data_df_1+1.7296, name = "df_1", mode='lines', showlegend=False, line_color=color_1
                ), row=1, col=2)
            fig2.add_trace(go.Scatter(
                x = Data_Vg, y = Data_df_2+1.3667, name = "df_2", mode='lines', showlegend=False, line_color=color_2
                ), row=1, col=2)
            fig2.add_trace(go.Scatter(
                x = Data_Vg, y = Data_df_3+1.1592, name = "df_3", mode='lines', showlegend=False, line_color=color_3
                ), row=1, col=2)
            fig2.add_trace(go.Scatter(
                x = Data_Vg, y = Data_df_4+0.9784, name = "df_4", mode='lines', showlegend=False, line_color=color_4
                ), row=1, col=2)
            fig2.add_trace(go.Scatter(
                x = Data_Vg, y = Data_df_5+0.8258, name = "df_5", mode='lines', showlegend=False, line_color=color_5
                ), row=1, col=2)
            fig2.add_trace(go.Scatter(
                x = Data_Vg, y = Data_df_6+0.7484, name = "df_6", mode='lines', showlegend=False, line_color=color_6
                ), row=1, col=2)
            fig2.add_trace(go.Scatter(
                x = Data_Vg, y = Data_dg_0-0.027, name = "dg_0", mode='lines', showlegend=False, line_color=color_0
                ), row=2, col=2)
            fig2.add_trace(go.Scatter(
                x = Data_Vg, y = Data_dg_1-0.027, name = "dg_1", mode='lines', showlegend=False, line_color=color_1
                ), row=2, col=2)
            fig2.add_trace(go.Scatter(
                x = Data_Vg, y = Data_dg_2-0.027, name = "dg_2", mode='lines', showlegend=False, line_color=color_2
                ), row=2, col=2)
            fig2.add_trace(go.Scatter(
                x = Data_Vg, y = Data_dg_3-0.027, name = "dg_3", mode='lines', showlegend=False, line_color=color_3
                ), row=2, col=2)
            fig2.add_trace(go.Scatter(
                x = Data_Vg, y = Data_dg_4-0.027, name = "dg_4", mode='lines', showlegend=False, line_color=color_4
                ), row=2, col=2)
            fig2.add_trace(go.Scatter(
                x = Data_Vg, y = Data_dg_5-0.027, name = "dg_5", mode='lines', showlegend=False, line_color=color_5
                ), row=2, col=2)
            fig2.add_trace(go.Scatter(
                x = Data_Vg, y = Data_dg_6-0.027, name = "dg_6", mode='lines', showlegend=False, line_color=color_6
                ), row=2, col=2)

        if 1.5 in experimentbuttons:

            slider_zins = slider_zins+2   
            Vg,zins,Eg,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T,sampletype,biassteps,zinssteps,Vg_array,zins_array=Organization_IntermValues.Surface_inputvalues(slider_Vg,slider_zins,slider_alpha,slider_Eg,slider_epsilonsem,slider_WFmet,slider_EAsem,slider_donor,slider_acceptor,slider_emass,slider_hmass,slider_T,slider_biassteps,slider_zinssteps)
            amplitude,frequency,lag,timesteps,tipradius,cantheight,cantarea,time_AFMarray,zins_AFMarray,zinslag_AFMarray=Organization_IntermValues.AFM1_inputvalues(slider_amplitude,slider_resfreq,slider_lag,slider_timesteps,slider_tipradius,slider_cantheight,slider_cantarea, zins)
            springconst,Qfactor=Organization_IntermValues.AFM2_inputvalues(slider_springconst,slider_Qfactor)
            NC,NV,Ec,Ev,Ei,Ef,no,po,ni,nb,pb,CPD,LD,Vs,Es,Qs,F,regime, zsem,Vsem,Esem,Qsem, P = Organization_IntermValues.Surface_calculations(Vg,zins,Eg,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T)
            Vs_biasarray,F_biasarray,df_biasarray_2,dg_biasarray_2 = Organization_BuildArrays.AFM_biasarrays(Vg_array,zins,Na,Nd,epsilon_sem,T,CPD,LD,nb,pb,ni,frequency,springconst,amplitude,Qfactor,tipradius,time_AFMarray,zins_AFMarray,zinslag_AFMarray,cantheight,cantarea,timesteps,geometrybuttons)
            Vg = slider_Vg*Physics_Semiconductors.e #J
            Vg_array = np.linspace(-10,10,biassteps)*Physics_Semiconductors.e #J
            fig2.add_trace(go.Scatter(
                x = Vg_array/Physics_Semiconductors.e, y = df_biasarray_2,
                name = "FrequencyShift", mode='lines', showlegend=False,
                line_color=color_other
                ), row=1, col=2)
            fig2.add_trace(go.Scatter(
                x = Vg_array/Physics_Semiconductors.e, y = dg_biasarray_2,
                name = "Excitation", mode='lines', showlegend=False,
                line_color=color_other
                ), row=2, col=2)  
            
            slider_zins = slider_zins-2+4   
            Vg,zins,Eg,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T,sampletype,biassteps,zinssteps,Vg_array,zins_array=Organization_IntermValues.Surface_inputvalues(slider_Vg,slider_zins,slider_alpha,slider_Eg,slider_epsilonsem,slider_WFmet,slider_EAsem,slider_donor,slider_acceptor,slider_emass,slider_hmass,slider_T,slider_biassteps,slider_zinssteps)
            amplitude,frequency,lag,timesteps,tipradius,cantheight,cantarea,time_AFMarray,zins_AFMarray,zinslag_AFMarray=Organization_IntermValues.AFM1_inputvalues(slider_amplitude,slider_resfreq,slider_lag,slider_timesteps,slider_tipradius,slider_cantheight,slider_cantarea, zins)
            springconst,Qfactor=Organization_IntermValues.AFM2_inputvalues(slider_springconst,slider_Qfactor)
            NC,NV,Ec,Ev,Ei,Ef,no,po,ni,nb,pb,CPD,LD,Vs,Es,Qs,F,regime, zsem,Vsem,Esem,Qsem, P = Organization_IntermValues.Surface_calculations(Vg,zins,Eg,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T)
            Vs_biasarray,F_biasarray,df_biasarray_4,dg_biasarray_4 = Organization_BuildArrays.AFM_biasarrays(Vg_array,zins,Na,Nd,epsilon_sem,T,CPD,LD,nb,pb,ni,frequency,springconst,amplitude,Qfactor,tipradius,time_AFMarray,zins_AFMarray,zinslag_AFMarray,cantheight,cantarea,timesteps,geometrybuttons)
            Vg = slider_Vg*Physics_Semiconductors.e #J
            Vg_array = np.linspace(-10,10,biassteps)*Physics_Semiconductors.e #J
            fig2.add_trace(go.Scatter(
                x = Vg_array/Physics_Semiconductors.e, y = df_biasarray_4,
                name = "FrequencyShift", mode='lines', showlegend=False,
                line_color=color_other
                ), row=1, col=2)
            fig2.add_trace(go.Scatter(
                x = Vg_array/Physics_Semiconductors.e, y = dg_biasarray_4,
                name = "Excitation", mode='lines', showlegend=False,
                line_color=color_other
                ), row=2, col=2)  
            
            slider_zins = slider_zins-4+6   
            Vg,zins,Eg,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T,sampletype,biassteps,zinssteps,Vg_array,zins_array=Organization_IntermValues.Surface_inputvalues(slider_Vg,slider_zins,slider_alpha,slider_Eg,slider_epsilonsem,slider_WFmet,slider_EAsem,slider_donor,slider_acceptor,slider_emass,slider_hmass,slider_T,slider_biassteps,slider_zinssteps)
            amplitude,frequency,lag,timesteps,tipradius,cantheight,cantarea,time_AFMarray,zins_AFMarray,zinslag_AFMarray=Organization_IntermValues.AFM1_inputvalues(slider_amplitude,slider_resfreq,slider_lag,slider_timesteps,slider_tipradius,slider_cantheight,slider_cantarea, zins)
            springconst,Qfactor=Organization_IntermValues.AFM2_inputvalues(slider_springconst,slider_Qfactor)
            NC,NV,Ec,Ev,Ei,Ef,no,po,ni,nb,pb,CPD,LD,Vs,Es,Qs,F,regime, zsem,Vsem,Esem,Qsem, P = Organization_IntermValues.Surface_calculations(Vg,zins,Eg,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T)
            Vs_biasarray,F_biasarray,df_biasarray_6,dg_biasarray_6 = Organization_BuildArrays.AFM_biasarrays(Vg_array,zins,Na,Nd,epsilon_sem,T,CPD,LD,nb,pb,ni,frequency,springconst,amplitude,Qfactor,tipradius,time_AFMarray,zins_AFMarray,zinslag_AFMarray,cantheight,cantarea,timesteps,geometrybuttons)
            Vg = slider_Vg*Physics_Semiconductors.e #J
            Vg_array = np.linspace(-10,10,biassteps)*Physics_Semiconductors.e #J
            fig2.add_trace(go.Scatter(
                x = Vg_array/Physics_Semiconductors.e, y = df_biasarray_6,
                name = "FrequencyShift", mode='lines', showlegend=False,
                line_color=color_other
                ), row=1, col=2)
            fig2.add_trace(go.Scatter(
                x = Vg_array/Physics_Semiconductors.e, y = dg_biasarray_6,
                name = "Excitation", mode='lines', showlegend=False,
                line_color=color_other
                ), row=2, col=2)             



    ####################### # zins experiment 2

        if 2 in experimentbuttons:
            Data_Vg = np.genfromtxt ('Data/Si_zins2/Data_zins_A_Vg.csv', delimiter=",")
            Data_df_0 = np.genfromtxt ('Data/Si_zins2/Data_zins0_A06_df.csv', delimiter=",")
            Data_df_2 = np.genfromtxt ('Data/Si_zins2/Data_zins2_A06_df.csv', delimiter=",")
            Data_df_4 = np.genfromtxt ('Data/Si_zins2/Data_zins4_A06_df.csv', delimiter=",")
            Data_df_6 = np.genfromtxt ('Data/Si_zins2/Data_zins6_A06_df.csv', delimiter=",")
            Data_dg_0 = np.genfromtxt ('Data/Si_zins2/Data_zins0_A06_dg.csv', delimiter=",")
            Data_dg_2 = np.genfromtxt ('Data/Si_zins2/Data_zins2_A06_dg.csv', delimiter=",")
            Data_dg_4 = np.genfromtxt ('Data/Si_zins2/Data_zins4_A06_dg.csv', delimiter=",")
            Data_dg_6 = np.genfromtxt ('Data/Si_zins2/Data_zins6_A06_dg.csv', delimiter=",")

            fig2.add_trace(go.Scatter(
                x = Data_Vg, y = Data_df_0+2.1633, name = "df_0", mode='lines', showlegend=False, line_color=color_0
                ), row=1, col=2)
            fig2.add_trace(go.Scatter(
                x = Data_Vg, y = Data_df_2+1.3667, name = "df_2", mode='lines', showlegend=False, line_color=color_2
                ), row=1, col=2)
            fig2.add_trace(go.Scatter(
                x = Data_Vg, y = Data_df_4+0.9784, name = "df_4", mode='lines', showlegend=False, line_color=color_4
                ), row=1, col=2)
            fig2.add_trace(go.Scatter(
                x = Data_Vg, y = Data_df_6+0.7484, name = "df_6", mode='lines', showlegend=False, line_color=color_6
                ), row=1, col=2)
            fig2.add_trace(go.Scatter(
                x = Data_Vg, y = Data_dg_0, name = "dg_0", mode='lines', showlegend=False, line_color=color_0
                ), row=2, col=2)
            fig2.add_trace(go.Scatter(
                x = Data_Vg, y = Data_dg_2, name = "dg_2", mode='lines', showlegend=False, line_color=color_2
                ), row=2, col=2)
            fig2.add_trace(go.Scatter(
                x = Data_Vg, y = Data_dg_4, name = "dg_4", mode='lines', showlegend=False, line_color=color_4
                ), row=2, col=2)
            fig2.add_trace(go.Scatter(
                x = Data_Vg, y = Data_dg_6, name = "dg_6", mode='lines', showlegend=False, line_color=color_6
                ), row=2, col=2)

        if 2.5 in experimentbuttons:

            slider_zins = slider_zins  
            Vg,zins,Eg,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T,sampletype,biassteps,zinssteps,Vg_array,zins_array=Organization_IntermValues.Surface_inputvalues(slider_Vg,slider_zins,slider_alpha,slider_Eg,slider_epsilonsem,slider_WFmet,slider_EAsem,slider_donor,slider_acceptor,slider_emass,slider_hmass,slider_T,slider_biassteps,slider_zinssteps)
            amplitude,frequency,lag,timesteps,tipradius,cantheight,cantarea,time_AFMarray,zins_AFMarray,zinslag_AFMarray=Organization_IntermValues.AFM1_inputvalues(slider_amplitude,slider_resfreq,slider_lag,slider_timesteps,slider_tipradius,slider_cantheight,slider_cantarea, zins)
            springconst,Qfactor=Organization_IntermValues.AFM2_inputvalues(slider_springconst,slider_Qfactor)
            NC,NV,Ec,Ev,Ei,Ef,no,po,ni,nb,pb,CPD,LD,Vs,Es,Qs,F,regime, zsem,Vsem,Esem,Qsem, P = Organization_IntermValues.Surface_calculations(Vg,zins,Eg,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T)
            Vs_biasarray,F_biasarray,df_biasarray_2,dg_biasarray_2 = Organization_BuildArrays.AFM_biasarrays(Vg_array,zins,Na,Nd,epsilon_sem,T,CPD,LD,nb,pb,ni,frequency,springconst,amplitude,Qfactor,tipradius,time_AFMarray,zins_AFMarray,zinslag_AFMarray,cantheight,cantarea,timesteps,geometrybuttons)
            Vg = slider_Vg*Physics_Semiconductors.e #J
            Vg_array = np.linspace(-10,10,biassteps)*Physics_Semiconductors.e #J
            fig2.add_trace(go.Scatter(
                x = Vg_array/Physics_Semiconductors.e, y = df_biasarray_2,
                name = "FrequencyShift", mode='lines', showlegend=False,
                line_color=color_other
                ), row=1, col=2)
            fig2.add_trace(go.Scatter(
                x = Vg_array/Physics_Semiconductors.e, y = dg_biasarray_2,
                name = "Excitation", mode='lines', showlegend=False,
                line_color=color_other
                ), row=2, col=2) 

            slider_zins = slider_zins+2   
            Vg,zins,Eg,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T,sampletype,biassteps,zinssteps,Vg_array,zins_array=Organization_IntermValues.Surface_inputvalues(slider_Vg,slider_zins,slider_alpha,slider_Eg,slider_epsilonsem,slider_WFmet,slider_EAsem,slider_donor,slider_acceptor,slider_emass,slider_hmass,slider_T,slider_biassteps,slider_zinssteps)
            amplitude,frequency,lag,timesteps,tipradius,cantheight,cantarea,time_AFMarray,zins_AFMarray,zinslag_AFMarray=Organization_IntermValues.AFM1_inputvalues(slider_amplitude,slider_resfreq,slider_lag,slider_timesteps,slider_tipradius,slider_cantheight,slider_cantarea, zins)
            springconst,Qfactor=Organization_IntermValues.AFM2_inputvalues(slider_springconst,slider_Qfactor)
            NC,NV,Ec,Ev,Ei,Ef,no,po,ni,nb,pb,CPD,LD,Vs,Es,Qs,F,regime, zsem,Vsem,Esem,Qsem, P = Organization_IntermValues.Surface_calculations(Vg,zins,Eg,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T)
            Vs_biasarray,F_biasarray,df_biasarray_2,dg_biasarray_2 = Organization_BuildArrays.AFM_biasarrays(Vg_array,zins,Na,Nd,epsilon_sem,T,CPD,LD,nb,pb,ni,frequency,springconst,amplitude,Qfactor,tipradius,time_AFMarray,zins_AFMarray,zinslag_AFMarray,cantheight,cantarea,timesteps,geometrybuttons)
            Vg = slider_Vg*Physics_Semiconductors.e #J
            Vg_array = np.linspace(-10,10,biassteps)*Physics_Semiconductors.e #J
            fig2.add_trace(go.Scatter(
                x = Vg_array/Physics_Semiconductors.e, y = df_biasarray_2,
                name = "FrequencyShift", mode='lines', showlegend=False,
                line_color=color_other
                ), row=1, col=2)
            fig2.add_trace(go.Scatter(
                x = Vg_array/Physics_Semiconductors.e, y = dg_biasarray_2,
                name = "Excitation", mode='lines', showlegend=False,
                line_color=color_other
                ), row=2, col=2)  
            
            slider_zins = slider_zins-2+4   
            Vg,zins,Eg,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T,sampletype,biassteps,zinssteps,Vg_array,zins_array=Organization_IntermValues.Surface_inputvalues(slider_Vg,slider_zins,slider_alpha,slider_Eg,slider_epsilonsem,slider_WFmet,slider_EAsem,slider_donor,slider_acceptor,slider_emass,slider_hmass,slider_T,slider_biassteps,slider_zinssteps)
            amplitude,frequency,lag,timesteps,tipradius,cantheight,cantarea,time_AFMarray,zins_AFMarray,zinslag_AFMarray=Organization_IntermValues.AFM1_inputvalues(slider_amplitude,slider_resfreq,slider_lag,slider_timesteps,slider_tipradius,slider_cantheight,slider_cantarea, zins)
            springconst,Qfactor=Organization_IntermValues.AFM2_inputvalues(slider_springconst,slider_Qfactor)
            NC,NV,Ec,Ev,Ei,Ef,no,po,ni,nb,pb,CPD,LD,Vs,Es,Qs,F,regime, zsem,Vsem,Esem,Qsem, P = Organization_IntermValues.Surface_calculations(Vg,zins,Eg,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T)
            Vs_biasarray,F_biasarray,df_biasarray_4,dg_biasarray_4 = Organization_BuildArrays.AFM_biasarrays(Vg_array,zins,Na,Nd,epsilon_sem,T,CPD,LD,nb,pb,ni,frequency,springconst,amplitude,Qfactor,tipradius,time_AFMarray,zins_AFMarray,zinslag_AFMarray,cantheight,cantarea,timesteps,geometrybuttons)
            Vg = slider_Vg*Physics_Semiconductors.e #J
            Vg_array = np.linspace(-10,10,biassteps)*Physics_Semiconductors.e #J
            fig2.add_trace(go.Scatter(
                x = Vg_array/Physics_Semiconductors.e, y = df_biasarray_4,
                name = "FrequencyShift", mode='lines', showlegend=False,
                line_color=color_other
                ), row=1, col=2)
            fig2.add_trace(go.Scatter(
                x = Vg_array/Physics_Semiconductors.e, y = dg_biasarray_4,
                name = "Excitation", mode='lines', showlegend=False,
                line_color=color_other
                ), row=2, col=2)  
            
            slider_zins = slider_zins-4+6   
            Vg,zins,Eg,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T,sampletype,biassteps,zinssteps,Vg_array,zins_array=Organization_IntermValues.Surface_inputvalues(slider_Vg,slider_zins,slider_alpha,slider_Eg,slider_epsilonsem,slider_WFmet,slider_EAsem,slider_donor,slider_acceptor,slider_emass,slider_hmass,slider_T,slider_biassteps,slider_zinssteps)
            amplitude,frequency,lag,timesteps,tipradius,cantheight,cantarea,time_AFMarray,zins_AFMarray,zinslag_AFMarray=Organization_IntermValues.AFM1_inputvalues(slider_amplitude,slider_resfreq,slider_lag,slider_timesteps,slider_tipradius,slider_cantheight,slider_cantarea, zins)
            springconst,Qfactor=Organization_IntermValues.AFM2_inputvalues(slider_springconst,slider_Qfactor)
            NC,NV,Ec,Ev,Ei,Ef,no,po,ni,nb,pb,CPD,LD,Vs,Es,Qs,F,regime, zsem,Vsem,Esem,Qsem, P = Organization_IntermValues.Surface_calculations(Vg,zins,Eg,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T)
            Vs_biasarray,F_biasarray,df_biasarray_6,dg_biasarray_6 = Organization_BuildArrays.AFM_biasarrays(Vg_array,zins,Na,Nd,epsilon_sem,T,CPD,LD,nb,pb,ni,frequency,springconst,amplitude,Qfactor,tipradius,time_AFMarray,zins_AFMarray,zinslag_AFMarray,cantheight,cantarea,timesteps,geometrybuttons)
            Vg = slider_Vg*Physics_Semiconductors.e #J
            Vg_array = np.linspace(-10,10,biassteps)*Physics_Semiconductors.e #J
            fig2.add_trace(go.Scatter(
                x = Vg_array/Physics_Semiconductors.e, y = df_biasarray_6,
                name = "FrequencyShift", mode='lines', showlegend=False,
                line_color=color_other
                ), row=1, col=2)
            fig2.add_trace(go.Scatter(
                x = Vg_array/Physics_Semiconductors.e, y = dg_biasarray_6,
                name = "Excitation", mode='lines', showlegend=False,
                line_color=color_other
                ), row=2, col=2)             

    ####################### # amplitude 1 experiment

        if 3 in experimentbuttons:
            Data_Vg = np.genfromtxt ('Data/Si_zins2/Data_zins_A_Vg.csv', delimiter=",")
            Data_df_2 = np.genfromtxt ('Data/Si_zins2/Data_zins0_A02_df.csv', delimiter=",")
            Data_df_6 = np.genfromtxt ('Data/Si_zins2/Data_zins0_A06_df.csv', delimiter=",")
            Data_df_10 = np.genfromtxt ('Data/Si_zins2/Data_zins0_A10_df.csv', delimiter=",")
            Data_dg_2 = np.genfromtxt ('Data/Si_zins2/Data_zins0_A02_dg.csv', delimiter=",")
            Data_dg_6 = np.genfromtxt ('Data/Si_zins2/Data_zins0_A06_dg.csv', delimiter=",")
            Data_dg_10 = np.genfromtxt ('Data/Si_zins2/Data_zins0_A10_dg.csv', delimiter=",")

            fig2.add_trace(go.Scatter(
                x = Data_Vg, y = Data_df_2, name = "df_2", mode='lines', showlegend=False, line_color=color_0
                ), row=1, col=2)
            fig2.add_trace(go.Scatter(
                x = Data_Vg, y = Data_df_6, name = "df_6", mode='lines', showlegend=False, line_color=color_2
                ), row=1, col=2)
            fig2.add_trace(go.Scatter(
                x = Data_Vg, y = Data_df_10, name = "df_10", mode='lines', showlegend=False, line_color=color_4
                ), row=1, col=2)
            fig2.add_trace(go.Scatter(
                x = Data_Vg, y = Data_dg_2, name = "dg_2", mode='lines', showlegend=False, line_color=color_0
                ), row=2, col=2)
            fig2.add_trace(go.Scatter(
                x = Data_Vg, y = Data_dg_6, name = "dg_6", mode='lines', showlegend=False, line_color=color_2
                ), row=2, col=2)
            fig2.add_trace(go.Scatter(
                x = Data_Vg, y = Data_dg_10, name = "dg_10", mode='lines', showlegend=False, line_color=color_4
                ), row=2, col=2)

        if 3.5 in experimentbuttons:

            slider_amplitude = 2   
            Vg,zins,Eg,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T,sampletype,biassteps,zinssteps,Vg_array,zins_array=Organization_IntermValues.Surface_inputvalues(slider_Vg,slider_zins,slider_alpha,slider_Eg,slider_epsilonsem,slider_WFmet,slider_EAsem,slider_donor,slider_acceptor,slider_emass,slider_hmass,slider_T,slider_biassteps,slider_zinssteps)
            amplitude,frequency,lag,timesteps,tipradius,cantheight,cantarea,time_AFMarray,zins_AFMarray,zinslag_AFMarray=Organization_IntermValues.AFM1_inputvalues(slider_amplitude,slider_resfreq,slider_lag,slider_timesteps,slider_tipradius,slider_cantheight,slider_cantarea, zins)
            springconst,Qfactor=Organization_IntermValues.AFM2_inputvalues(slider_springconst,slider_Qfactor)
            NC,NV,Ec,Ev,Ei,Ef,no,po,ni,nb,pb,CPD,LD,Vs,Es,Qs,F,regime, zsem,Vsem,Esem,Qsem, P = Organization_IntermValues.Surface_calculations(Vg,zins,Eg,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T)
            Vs_biasarray,F_biasarray,df_biasarray_2,dg_biasarray_2 = Organization_BuildArrays.AFM_biasarrays(Vg_array,zins,Na,Nd,epsilon_sem,T,CPD,LD,nb,pb,ni,frequency,springconst,amplitude,Qfactor,tipradius,time_AFMarray,zins_AFMarray,zinslag_AFMarray,cantheight,cantarea,timesteps,geometrybuttons)
            Vg = slider_Vg*Physics_Semiconductors.e #J
            Vg_array = np.linspace(-10,10,biassteps)*Physics_Semiconductors.e #J
            fig2.add_trace(go.Scatter(
                x = Vg_array/Physics_Semiconductors.e, y = df_biasarray_2,
                name = "FrequencyShift", mode='lines', showlegend=False,
                line_color=color_other
                ), row=1, col=2)
            fig2.add_trace(go.Scatter(
                x = Vg_array/Physics_Semiconductors.e, y = dg_biasarray_2,
                name = "Excitation", mode='lines', showlegend=False,
                line_color=color_other
                ), row=2, col=2)  
            
            slider_amplitude = 6   
            Vg,zins,Eg,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T,sampletype,biassteps,zinssteps,Vg_array,zins_array=Organization_IntermValues.Surface_inputvalues(slider_Vg,slider_zins,slider_alpha,slider_Eg,slider_epsilonsem,slider_WFmet,slider_EAsem,slider_donor,slider_acceptor,slider_emass,slider_hmass,slider_T,slider_biassteps,slider_zinssteps)
            amplitude,frequency,lag,timesteps,tipradius,cantheight,cantarea,time_AFMarray,zins_AFMarray,zinslag_AFMarray=Organization_IntermValues.AFM1_inputvalues(slider_amplitude,slider_resfreq,slider_lag,slider_timesteps,slider_tipradius,slider_cantheight,slider_cantarea, zins)
            springconst,Qfactor=Organization_IntermValues.AFM2_inputvalues(slider_springconst,slider_Qfactor)
            NC,NV,Ec,Ev,Ei,Ef,no,po,ni,nb,pb,CPD,LD,Vs,Es,Qs,F,regime, zsem,Vsem,Esem,Qsem, P = Organization_IntermValues.Surface_calculations(Vg,zins,Eg,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T)
            Vs_biasarray,F_biasarray,df_biasarray_4,dg_biasarray_4 = Organization_BuildArrays.AFM_biasarrays(Vg_array,zins,Na,Nd,epsilon_sem,T,CPD,LD,nb,pb,ni,frequency,springconst,amplitude,Qfactor,tipradius,time_AFMarray,zins_AFMarray,zinslag_AFMarray,cantheight,cantarea,timesteps,geometrybuttons)
            Vg = slider_Vg*Physics_Semiconductors.e #J
            Vg_array = np.linspace(-10,10,biassteps)*Physics_Semiconductors.e #J
            fig2.add_trace(go.Scatter(
                x = Vg_array/Physics_Semiconductors.e, y = df_biasarray_4,
                name = "FrequencyShift", mode='lines', showlegend=False,
                line_color=color_other
                ), row=1, col=2)
            fig2.add_trace(go.Scatter(
                x = Vg_array/Physics_Semiconductors.e, y = dg_biasarray_4,
                name = "Excitation", mode='lines', showlegend=False,
                line_color=color_other
                ), row=2, col=2)  
            
            slider_amplitude = 10  
            Vg,zins,Eg,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T,sampletype,biassteps,zinssteps,Vg_array,zins_array=Organization_IntermValues.Surface_inputvalues(slider_Vg,slider_zins,slider_alpha,slider_Eg,slider_epsilonsem,slider_WFmet,slider_EAsem,slider_donor,slider_acceptor,slider_emass,slider_hmass,slider_T,slider_biassteps,slider_zinssteps)
            amplitude,frequency,lag,timesteps,tipradius,cantheight,cantarea,time_AFMarray,zins_AFMarray,zinslag_AFMarray=Organization_IntermValues.AFM1_inputvalues(slider_amplitude,slider_resfreq,slider_lag,slider_timesteps,slider_tipradius,slider_cantheight,slider_cantarea, zins)
            springconst,Qfactor=Organization_IntermValues.AFM2_inputvalues(slider_springconst,slider_Qfactor)
            NC,NV,Ec,Ev,Ei,Ef,no,po,ni,nb,pb,CPD,LD,Vs,Es,Qs,F,regime, zsem,Vsem,Esem,Qsem, P = Organization_IntermValues.Surface_calculations(Vg,zins,Eg,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T)
            Vs_biasarray,F_biasarray,df_biasarray_6,dg_biasarray_6 = Organization_BuildArrays.AFM_biasarrays(Vg_array,zins,Na,Nd,epsilon_sem,T,CPD,LD,nb,pb,ni,frequency,springconst,amplitude,Qfactor,tipradius,time_AFMarray,zins_AFMarray,zinslag_AFMarray,cantheight,cantarea,timesteps,geometrybuttons)
            Vg = slider_Vg*Physics_Semiconductors.e #J
            Vg_array = np.linspace(-10,10,biassteps)*Physics_Semiconductors.e #J
            fig2.add_trace(go.Scatter(
                x = Vg_array/Physics_Semiconductors.e, y = df_biasarray_6,
                name = "FrequencyShift", mode='lines', showlegend=False,
                line_color=color_other
                ), row=1, col=2)
            fig2.add_trace(go.Scatter(
                x = Vg_array/Physics_Semiconductors.e, y = dg_biasarray_6,
                name = "Excitation", mode='lines', showlegend=False,
                line_color=color_other
                ), row=2, col=2)             

    ####################### # amplitude 2 experiment

        if 4 in experimentbuttons:
            Data_Vg = np.genfromtxt ('Data/Si_zins2/Data_zins_A_Vg.csv', delimiter=",")
            Data_df_2 = np.genfromtxt ('Data/Si_zins2/Data_zins2_A02_df.csv', delimiter=",")
            Data_df_6 = np.genfromtxt ('Data/Si_zins2/Data_zins2_A06_df.csv', delimiter=",")
            Data_df_10 = np.genfromtxt ('Data/Si_zins2/Data_zins2_A10_df.csv', delimiter=",")
            Data_dg_2 = np.genfromtxt ('Data/Si_zins2/Data_zins2_A02_dg.csv', delimiter=",")
            Data_dg_6 = np.genfromtxt ('Data/Si_zins2/Data_zins2_A06_dg.csv', delimiter=",")
            Data_dg_10 = np.genfromtxt ('Data/Si_zins2/Data_zins2_A10_dg.csv', delimiter=",")

            fig2.add_trace(go.Scatter(
                x = Data_Vg, y = Data_df_2, name = "df_2", mode='lines', showlegend=False, line_color=color_0
                ), row=1, col=2)
            fig2.add_trace(go.Scatter(
                x = Data_Vg, y = Data_df_6, name = "df_6", mode='lines', showlegend=False, line_color=color_2
                ), row=1, col=2)
            fig2.add_trace(go.Scatter(
                x = Data_Vg, y = Data_df_10, name = "df_10", mode='lines', showlegend=False, line_color=color_4
                ), row=1, col=2)
            fig2.add_trace(go.Scatter(
                x = Data_Vg, y = Data_dg_2, name = "dg_2", mode='lines', showlegend=False, line_color=color_0
                ), row=2, col=2)
            fig2.add_trace(go.Scatter(
                x = Data_Vg, y = Data_dg_6, name = "dg_6", mode='lines', showlegend=False, line_color=color_2
                ), row=2, col=2)
            fig2.add_trace(go.Scatter(
                x = Data_Vg, y = Data_dg_10, name = "dg_10", mode='lines', showlegend=False, line_color=color_4
                ), row=2, col=2)

        if 4.5 in experimentbuttons:

            slider_amplitude = 2   
            Vg,zins,Eg,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T,sampletype,biassteps,zinssteps,Vg_array,zins_array=Organization_IntermValues.Surface_inputvalues(slider_Vg,slider_zins,slider_alpha,slider_Eg,slider_epsilonsem,slider_WFmet,slider_EAsem,slider_donor,slider_acceptor,slider_emass,slider_hmass,slider_T,slider_biassteps,slider_zinssteps)
            amplitude,frequency,lag,timesteps,tipradius,cantheight,cantarea,time_AFMarray,zins_AFMarray,zinslag_AFMarray=Organization_IntermValues.AFM1_inputvalues(slider_amplitude,slider_resfreq,slider_lag,slider_timesteps,slider_tipradius,slider_cantheight,slider_cantarea, zins)
            springconst,Qfactor=Organization_IntermValues.AFM2_inputvalues(slider_springconst,slider_Qfactor)
            NC,NV,Ec,Ev,Ei,Ef,no,po,ni,nb,pb,CPD,LD,Vs,Es,Qs,F,regime, zsem,Vsem,Esem,Qsem, P = Organization_IntermValues.Surface_calculations(Vg,zins,Eg,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T)
            Vs_biasarray,F_biasarray,df_biasarray_2,dg_biasarray_2 = Organization_BuildArrays.AFM_biasarrays(Vg_array,zins,Na,Nd,epsilon_sem,T,CPD,LD,nb,pb,ni,frequency,springconst,amplitude,Qfactor,tipradius,time_AFMarray,zins_AFMarray,zinslag_AFMarray,cantheight,cantarea,timesteps,geometrybuttons)
            Vg = slider_Vg*Physics_Semiconductors.e #J
            Vg_array = np.linspace(-10,10,biassteps)*Physics_Semiconductors.e #J
            fig2.add_trace(go.Scatter(
                x = Vg_array/Physics_Semiconductors.e, y = df_biasarray_2,
                name = "FrequencyShift", mode='lines', showlegend=False,
                line_color=color_other
                ), row=1, col=2)
            fig2.add_trace(go.Scatter(
                x = Vg_array/Physics_Semiconductors.e, y = dg_biasarray_2,
                name = "Excitation", mode='lines', showlegend=False,
                line_color=color_other
                ), row=2, col=2)  
            
            slider_amplitude = 6   
            Vg,zins,Eg,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T,sampletype,biassteps,zinssteps,Vg_array,zins_array=Organization_IntermValues.Surface_inputvalues(slider_Vg,slider_zins,slider_alpha,slider_Eg,slider_epsilonsem,slider_WFmet,slider_EAsem,slider_donor,slider_acceptor,slider_emass,slider_hmass,slider_T,slider_biassteps,slider_zinssteps)
            amplitude,frequency,lag,timesteps,tipradius,cantheight,cantarea,time_AFMarray,zins_AFMarray,zinslag_AFMarray=Organization_IntermValues.AFM1_inputvalues(slider_amplitude,slider_resfreq,slider_lag,slider_timesteps,slider_tipradius,slider_cantheight,slider_cantarea, zins)
            springconst,Qfactor=Organization_IntermValues.AFM2_inputvalues(slider_springconst,slider_Qfactor)
            NC,NV,Ec,Ev,Ei,Ef,no,po,ni,nb,pb,CPD,LD,Vs,Es,Qs,F,regime, zsem,Vsem,Esem,Qsem, P = Organization_IntermValues.Surface_calculations(Vg,zins,Eg,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T)
            Vs_biasarray,F_biasarray,df_biasarray_4,dg_biasarray_4 = Organization_BuildArrays.AFM_biasarrays(Vg_array,zins,Na,Nd,epsilon_sem,T,CPD,LD,nb,pb,ni,frequency,springconst,amplitude,Qfactor,tipradius,time_AFMarray,zins_AFMarray,zinslag_AFMarray,cantheight,cantarea,timesteps,geometrybuttons)
            Vg = slider_Vg*Physics_Semiconductors.e #J
            Vg_array = np.linspace(-10,10,biassteps)*Physics_Semiconductors.e #J
            fig2.add_trace(go.Scatter(
                x = Vg_array/Physics_Semiconductors.e, y = df_biasarray_4,
                name = "FrequencyShift", mode='lines', showlegend=False,
                line_color=color_other
                ), row=1, col=2)
            fig2.add_trace(go.Scatter(
                x = Vg_array/Physics_Semiconductors.e, y = dg_biasarray_4,
                name = "Excitation", mode='lines', showlegend=False,
                line_color=color_other
                ), row=2, col=2)  
            
            slider_amplitude = 10  
            Vg,zins,Eg,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T,sampletype,biassteps,zinssteps,Vg_array,zins_array=Organization_IntermValues.Surface_inputvalues(slider_Vg,slider_zins,slider_alpha,slider_Eg,slider_epsilonsem,slider_WFmet,slider_EAsem,slider_donor,slider_acceptor,slider_emass,slider_hmass,slider_T,slider_biassteps,slider_zinssteps)
            amplitude,frequency,lag,timesteps,tipradius,cantheight,cantarea,time_AFMarray,zins_AFMarray,zinslag_AFMarray=Organization_IntermValues.AFM1_inputvalues(slider_amplitude,slider_resfreq,slider_lag,slider_timesteps,slider_tipradius,slider_cantheight,slider_cantarea, zins)
            springconst,Qfactor=Organization_IntermValues.AFM2_inputvalues(slider_springconst,slider_Qfactor)
            NC,NV,Ec,Ev,Ei,Ef,no,po,ni,nb,pb,CPD,LD,Vs,Es,Qs,F,regime, zsem,Vsem,Esem,Qsem, P = Organization_IntermValues.Surface_calculations(Vg,zins,Eg,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T)
            Vs_biasarray,F_biasarray,df_biasarray_6,dg_biasarray_6 = Organization_BuildArrays.AFM_biasarrays(Vg_array,zins,Na,Nd,epsilon_sem,T,CPD,LD,nb,pb,ni,frequency,springconst,amplitude,Qfactor,tipradius,time_AFMarray,zins_AFMarray,zinslag_AFMarray,cantheight,cantarea,timesteps,geometrybuttons)
            Vg = slider_Vg*Physics_Semiconductors.e #J
            Vg_array = np.linspace(-10,10,biassteps)*Physics_Semiconductors.e #J
            fig2.add_trace(go.Scatter(
                x = Vg_array/Physics_Semiconductors.e, y = df_biasarray_6,
                name = "FrequencyShift", mode='lines', showlegend=False,
                line_color=color_other
                ), row=1, col=2)
            fig2.add_trace(go.Scatter(
                x = Vg_array/Physics_Semiconductors.e, y = dg_biasarray_6,
                name = "Excitation", mode='lines', showlegend=False,
                line_color=color_other
                ), row=2, col=2)          

    ####################### # amplitude 2 experiment

        if 5 in experimentbuttons:
            Data_Vg = np.genfromtxt ('Data/Si_zins2/Data_zins_A_Vg.csv', delimiter=",")
            Data_df_2 = np.genfromtxt ('Data/Si_zins2/Data_zins4_A02_df.csv', delimiter=",")
            Data_df_6 = np.genfromtxt ('Data/Si_zins2/Data_zins4_A06_df.csv', delimiter=",")
            Data_df_10 = np.genfromtxt ('Data/Si_zins2/Data_zins4_A10_df.csv', delimiter=",")
            Data_dg_2 = np.genfromtxt ('Data/Si_zins2/Data_zins4_A02_dg.csv', delimiter=",")
            Data_dg_6 = np.genfromtxt ('Data/Si_zins2/Data_zins4_A06_dg.csv', delimiter=",")
            Data_dg_10 = np.genfromtxt ('Data/Si_zins2/Data_zins4_A10_dg.csv', delimiter=",")

            fig2.add_trace(go.Scatter(
                x = Data_Vg, y = Data_df_2, name = "df_2", mode='lines', showlegend=False, line_color=color_0
                ), row=1, col=2)
            fig2.add_trace(go.Scatter(
                x = Data_Vg, y = Data_df_6, name = "df_6", mode='lines', showlegend=False, line_color=color_2
                ), row=1, col=2)
            fig2.add_trace(go.Scatter(
                x = Data_Vg, y = Data_df_10, name = "df_10", mode='lines', showlegend=False, line_color=color_4
                ), row=1, col=2)
            fig2.add_trace(go.Scatter(
                x = Data_Vg, y = Data_dg_2, name = "dg_2", mode='lines', showlegend=False, line_color=color_0
                ), row=2, col=2)
            fig2.add_trace(go.Scatter(
                x = Data_Vg, y = Data_dg_6, name = "dg_6", mode='lines', showlegend=False, line_color=color_2
                ), row=2, col=2)
            fig2.add_trace(go.Scatter(
                x = Data_Vg, y = Data_dg_10, name = "dg_10", mode='lines', showlegend=False, line_color=color_4
                ), row=2, col=2)

        if 5.5 in experimentbuttons:

            slider_amplitude = 2   
            Vg,zins,Eg,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T,sampletype,biassteps,zinssteps,Vg_array,zins_array=Organization_IntermValues.Surface_inputvalues(slider_Vg,slider_zins,slider_alpha,slider_Eg,slider_epsilonsem,slider_WFmet,slider_EAsem,slider_donor,slider_acceptor,slider_emass,slider_hmass,slider_T,slider_biassteps,slider_zinssteps)
            amplitude,frequency,lag,timesteps,tipradius,cantheight,cantarea,time_AFMarray,zins_AFMarray,zinslag_AFMarray=Organization_IntermValues.AFM1_inputvalues(slider_amplitude,slider_resfreq,slider_lag,slider_timesteps,slider_tipradius,slider_cantheight,slider_cantarea, zins)
            springconst,Qfactor=Organization_IntermValues.AFM2_inputvalues(slider_springconst,slider_Qfactor)
            NC,NV,Ec,Ev,Ei,Ef,no,po,ni,nb,pb,CPD,LD,Vs,Es,Qs,F,regime, zsem,Vsem,Esem,Qsem, P = Organization_IntermValues.Surface_calculations(Vg,zins,Eg,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T)
            Vs_biasarray,F_biasarray,df_biasarray_2,dg_biasarray_2 = Organization_BuildArrays.AFM_biasarrays(Vg_array,zins,Na,Nd,epsilon_sem,T,CPD,LD,nb,pb,ni,frequency,springconst,amplitude,Qfactor,tipradius,time_AFMarray,zins_AFMarray,zinslag_AFMarray,cantheight,cantarea,timesteps,geometrybuttons)
            Vg = slider_Vg*Physics_Semiconductors.e #J
            Vg_array = np.linspace(-10,10,biassteps)*Physics_Semiconductors.e #J
            fig2.add_trace(go.Scatter(
                x = Vg_array/Physics_Semiconductors.e, y = df_biasarray_2,
                name = "FrequencyShift", mode='lines', showlegend=False,
                line_color=color_other
                ), row=1, col=2)
            fig2.add_trace(go.Scatter(
                x = Vg_array/Physics_Semiconductors.e, y = dg_biasarray_2,
                name = "Excitation", mode='lines', showlegend=False,
                line_color=color_other
                ), row=2, col=2)  
            
            slider_amplitude = 6   
            Vg,zins,Eg,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T,sampletype,biassteps,zinssteps,Vg_array,zins_array=Organization_IntermValues.Surface_inputvalues(slider_Vg,slider_zins,slider_alpha,slider_Eg,slider_epsilonsem,slider_WFmet,slider_EAsem,slider_donor,slider_acceptor,slider_emass,slider_hmass,slider_T,slider_biassteps,slider_zinssteps)
            amplitude,frequency,lag,timesteps,tipradius,cantheight,cantarea,time_AFMarray,zins_AFMarray,zinslag_AFMarray=Organization_IntermValues.AFM1_inputvalues(slider_amplitude,slider_resfreq,slider_lag,slider_timesteps,slider_tipradius,slider_cantheight,slider_cantarea, zins)
            springconst,Qfactor=Organization_IntermValues.AFM2_inputvalues(slider_springconst,slider_Qfactor)
            NC,NV,Ec,Ev,Ei,Ef,no,po,ni,nb,pb,CPD,LD,Vs,Es,Qs,F,regime, zsem,Vsem,Esem,Qsem, P = Organization_IntermValues.Surface_calculations(Vg,zins,Eg,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T)
            Vs_biasarray,F_biasarray,df_biasarray_4,dg_biasarray_4 = Organization_BuildArrays.AFM_biasarrays(Vg_array,zins,Na,Nd,epsilon_sem,T,CPD,LD,nb,pb,ni,frequency,springconst,amplitude,Qfactor,tipradius,time_AFMarray,zins_AFMarray,zinslag_AFMarray,cantheight,cantarea,timesteps,geometrybuttons)
            Vg = slider_Vg*Physics_Semiconductors.e #J
            Vg_array = np.linspace(-10,10,biassteps)*Physics_Semiconductors.e #J
            fig2.add_trace(go.Scatter(
                x = Vg_array/Physics_Semiconductors.e, y = df_biasarray_4,
                name = "FrequencyShift", mode='lines', showlegend=False,
                line_color=color_other
                ), row=1, col=2)
            fig2.add_trace(go.Scatter(
                x = Vg_array/Physics_Semiconductors.e, y = dg_biasarray_4,
                name = "Excitation", mode='lines', showlegend=False,
                line_color=color_other
                ), row=2, col=2)  
            
            slider_amplitude = 10  
            Vg,zins,Eg,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T,sampletype,biassteps,zinssteps,Vg_array,zins_array=Organization_IntermValues.Surface_inputvalues(slider_Vg,slider_zins,slider_alpha,slider_Eg,slider_epsilonsem,slider_WFmet,slider_EAsem,slider_donor,slider_acceptor,slider_emass,slider_hmass,slider_T,slider_biassteps,slider_zinssteps)
            amplitude,frequency,lag,timesteps,tipradius,cantheight,cantarea,time_AFMarray,zins_AFMarray,zinslag_AFMarray=Organization_IntermValues.AFM1_inputvalues(slider_amplitude,slider_resfreq,slider_lag,slider_timesteps,slider_tipradius,slider_cantheight,slider_cantarea, zins)
            springconst,Qfactor=Organization_IntermValues.AFM2_inputvalues(slider_springconst,slider_Qfactor)
            NC,NV,Ec,Ev,Ei,Ef,no,po,ni,nb,pb,CPD,LD,Vs,Es,Qs,F,regime, zsem,Vsem,Esem,Qsem, P = Organization_IntermValues.Surface_calculations(Vg,zins,Eg,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T)
            Vs_biasarray,F_biasarray,df_biasarray_6,dg_biasarray_6 = Organization_BuildArrays.AFM_biasarrays(Vg_array,zins,Na,Nd,epsilon_sem,T,CPD,LD,nb,pb,ni,frequency,springconst,amplitude,Qfactor,tipradius,time_AFMarray,zins_AFMarray,zinslag_AFMarray,cantheight,cantarea,timesteps,geometrybuttons)
            Vg = slider_Vg*Physics_Semiconductors.e #J
            Vg_array = np.linspace(-10,10,biassteps)*Physics_Semiconductors.e #J
            fig2.add_trace(go.Scatter(
                x = Vg_array/Physics_Semiconductors.e, y = df_biasarray_6,
                name = "FrequencyShift", mode='lines', showlegend=False,
                line_color=color_other
                ), row=1, col=2)
            fig2.add_trace(go.Scatter(
                x = Vg_array/Physics_Semiconductors.e, y = dg_biasarray_6,
                name = "Excitation", mode='lines', showlegend=False,
                line_color=color_other
                ), row=2, col=2)          
            
    ####################### # amplitude 2 experiment

        if 6 in experimentbuttons:
            Data_Vg = np.genfromtxt ('Data/Si_zins2/Data_zins_A_Vg.csv', delimiter=",")
            Data_df_2 = np.genfromtxt ('Data/Si_zins2/Data_zins6_A02_df.csv', delimiter=",")
            Data_df_6 = np.genfromtxt ('Data/Si_zins2/Data_zins6_A06_df.csv', delimiter=",")
            Data_df_10 = np.genfromtxt ('Data/Si_zins2/Data_zins6_A10_df.csv', delimiter=",")
            Data_dg_2 = np.genfromtxt ('Data/Si_zins2/Data_zins6_A02_dg.csv', delimiter=",")
            Data_dg_6 = np.genfromtxt ('Data/Si_zins2/Data_zins6_A06_dg.csv', delimiter=",")
            Data_dg_10 = np.genfromtxt ('Data/Si_zins2/Data_zins6_A10_dg.csv', delimiter=",")

            fig2.add_trace(go.Scatter(
                x = Data_Vg, y = Data_df_2, name = "df_2", mode='lines', showlegend=False, line_color=color_0
                ), row=1, col=2)
            fig2.add_trace(go.Scatter(
                x = Data_Vg, y = Data_df_6, name = "df_6", mode='lines', showlegend=False, line_color=color_2
                ), row=1, col=2)
            fig2.add_trace(go.Scatter(
                x = Data_Vg, y = Data_df_10, name = "df_10", mode='lines', showlegend=False, line_color=color_4
                ), row=1, col=2)
            fig2.add_trace(go.Scatter(
                x = Data_Vg, y = Data_dg_2, name = "dg_2", mode='lines', showlegend=False, line_color=color_0
                ), row=2, col=2)
            fig2.add_trace(go.Scatter(
                x = Data_Vg, y = Data_dg_6, name = "dg_6", mode='lines', showlegend=False, line_color=color_2
                ), row=2, col=2)
            fig2.add_trace(go.Scatter(
                x = Data_Vg, y = Data_dg_10, name = "dg_10", mode='lines', showlegend=False, line_color=color_4
                ), row=2, col=2)

        if 6.5 in experimentbuttons:

            slider_amplitude = 2   
            Vg,zins,Eg,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T,sampletype,biassteps,zinssteps,Vg_array,zins_array=Organization_IntermValues.Surface_inputvalues(slider_Vg,slider_zins,slider_alpha,slider_Eg,slider_epsilonsem,slider_WFmet,slider_EAsem,slider_donor,slider_acceptor,slider_emass,slider_hmass,slider_T,slider_biassteps,slider_zinssteps)
            amplitude,frequency,lag,timesteps,tipradius,cantheight,cantarea,time_AFMarray,zins_AFMarray,zinslag_AFMarray=Organization_IntermValues.AFM1_inputvalues(slider_amplitude,slider_resfreq,slider_lag,slider_timesteps,slider_tipradius,slider_cantheight,slider_cantarea, zins)
            springconst,Qfactor=Organization_IntermValues.AFM2_inputvalues(slider_springconst,slider_Qfactor)
            NC,NV,Ec,Ev,Ei,Ef,no,po,ni,nb,pb,CPD,LD,Vs,Es,Qs,F,regime, zsem,Vsem,Esem,Qsem, P = Organization_IntermValues.Surface_calculations(Vg,zins,Eg,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T)
            Vs_biasarray,F_biasarray,df_biasarray_2,dg_biasarray_2 = Organization_BuildArrays.AFM_biasarrays(Vg_array,zins,Na,Nd,epsilon_sem,T,CPD,LD,nb,pb,ni,frequency,springconst,amplitude,Qfactor,tipradius,time_AFMarray,zins_AFMarray,zinslag_AFMarray,cantheight,cantarea,timesteps,geometrybuttons)
            Vg = slider_Vg*Physics_Semiconductors.e #J
            Vg_array = np.linspace(-10,10,biassteps)*Physics_Semiconductors.e #J
            fig2.add_trace(go.Scatter(
                x = Vg_array/Physics_Semiconductors.e, y = df_biasarray_2,
                name = "FrequencyShift", mode='lines', showlegend=False,
                line_color=color_other
                ), row=1, col=2)
            fig2.add_trace(go.Scatter(
                x = Vg_array/Physics_Semiconductors.e, y = dg_biasarray_2,
                name = "Excitation", mode='lines', showlegend=False,
                line_color=color_other
                ), row=2, col=2)  
            
            slider_amplitude = 6   
            Vg,zins,Eg,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T,sampletype,biassteps,zinssteps,Vg_array,zins_array=Organization_IntermValues.Surface_inputvalues(slider_Vg,slider_zins,slider_alpha,slider_Eg,slider_epsilonsem,slider_WFmet,slider_EAsem,slider_donor,slider_acceptor,slider_emass,slider_hmass,slider_T,slider_biassteps,slider_zinssteps)
            amplitude,frequency,lag,timesteps,tipradius,cantheight,cantarea,time_AFMarray,zins_AFMarray,zinslag_AFMarray=Organization_IntermValues.AFM1_inputvalues(slider_amplitude,slider_resfreq,slider_lag,slider_timesteps,slider_tipradius,slider_cantheight,slider_cantarea, zins)
            springconst,Qfactor=Organization_IntermValues.AFM2_inputvalues(slider_springconst,slider_Qfactor)
            NC,NV,Ec,Ev,Ei,Ef,no,po,ni,nb,pb,CPD,LD,Vs,Es,Qs,F,regime, zsem,Vsem,Esem,Qsem, P = Organization_IntermValues.Surface_calculations(Vg,zins,Eg,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T)
            Vs_biasarray,F_biasarray,df_biasarray_4,dg_biasarray_4 = Organization_BuildArrays.AFM_biasarrays(Vg_array,zins,Na,Nd,epsilon_sem,T,CPD,LD,nb,pb,ni,frequency,springconst,amplitude,Qfactor,tipradius,time_AFMarray,zins_AFMarray,zinslag_AFMarray,cantheight,cantarea,timesteps,geometrybuttons)
            Vg = slider_Vg*Physics_Semiconductors.e #J
            Vg_array = np.linspace(-10,10,biassteps)*Physics_Semiconductors.e #J
            fig2.add_trace(go.Scatter(
                x = Vg_array/Physics_Semiconductors.e, y = df_biasarray_4,
                name = "FrequencyShift", mode='lines', showlegend=False,
                line_color=color_other
                ), row=1, col=2)
            fig2.add_trace(go.Scatter(
                x = Vg_array/Physics_Semiconductors.e, y = dg_biasarray_4,
                name = "Excitation", mode='lines', showlegend=False,
                line_color=color_other
                ), row=2, col=2)  
            
            slider_amplitude = 10  
            Vg,zins,Eg,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T,sampletype,biassteps,zinssteps,Vg_array,zins_array=Organization_IntermValues.Surface_inputvalues(slider_Vg,slider_zins,slider_alpha,slider_Eg,slider_epsilonsem,slider_WFmet,slider_EAsem,slider_donor,slider_acceptor,slider_emass,slider_hmass,slider_T,slider_biassteps,slider_zinssteps)
            amplitude,frequency,lag,timesteps,tipradius,cantheight,cantarea,time_AFMarray,zins_AFMarray,zinslag_AFMarray=Organization_IntermValues.AFM1_inputvalues(slider_amplitude,slider_resfreq,slider_lag,slider_timesteps,slider_tipradius,slider_cantheight,slider_cantarea, zins)
            springconst,Qfactor=Organization_IntermValues.AFM2_inputvalues(slider_springconst,slider_Qfactor)
            NC,NV,Ec,Ev,Ei,Ef,no,po,ni,nb,pb,CPD,LD,Vs,Es,Qs,F,regime, zsem,Vsem,Esem,Qsem, P = Organization_IntermValues.Surface_calculations(Vg,zins,Eg,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T)
            Vs_biasarray,F_biasarray,df_biasarray_6,dg_biasarray_6 = Organization_BuildArrays.AFM_biasarrays(Vg_array,zins,Na,Nd,epsilon_sem,T,CPD,LD,nb,pb,ni,frequency,springconst,amplitude,Qfactor,tipradius,time_AFMarray,zins_AFMarray,zinslag_AFMarray,cantheight,cantarea,timesteps,geometrybuttons)
            Vg = slider_Vg*Physics_Semiconductors.e #J
            Vg_array = np.linspace(-10,10,biassteps)*Physics_Semiconductors.e #J
            fig2.add_trace(go.Scatter(
                x = Vg_array/Physics_Semiconductors.e, y = df_biasarray_6,
                name = "FrequencyShift", mode='lines', showlegend=False,
                line_color=color_other
                ), row=1, col=2)
            fig2.add_trace(go.Scatter(
                x = Vg_array/Physics_Semiconductors.e, y = dg_biasarray_6,
                name = "Excitation", mode='lines', showlegend=False,
                line_color=color_other
                ), row=2, col=2)          


        '''
        Data_Vg = np.genfromtxt ('Data/Data_Vg.csv', delimiter=",")
        Data_df_A = np.genfromtxt ('Data/Data_df_A.csv', delimiter=",")
        Data_df_B = np.genfromtxt ('Data/Data_df_B.csv', delimiter=",")
        Data_df_C = np.genfromtxt ('Data/Data_df_C.csv', delimiter=",")
        Data_df_D = np.genfromtxt ('Data/Data_df_D.csv', delimiter=",")
        Data_df_E = np.genfromtxt ('Data/Data_df_E.csv', delimiter=",")

        fig2.add_trace(go.Scatter(
            x = Data_Vg, y = Data_df_A+1.38,
            name = "df_A", mode='lines', showlegend=False,
            line_color=color_indicator
            ), row=1, col=2)
        fig2.add_trace(go.Scatter(
            x = Data_Vg, y = Data_df_B+1.69,
            name = "df_B", mode='lines', showlegend=False,
            line_color=color_Ev
            ), row=1, col=2)
        fig2.add_trace(go.Scatter(
            x = Data_Vg, y = Data_df_C+1.69,
            name = "df_C", mode='lines', showlegend=False,
            line_color=color_Ec
            ), row=1, col=2)
        fig2.add_trace(go.Scatter(
            x = Data_Vg, y = Data_df_D+1.35,
            name = "df_D", mode='lines', showlegend=False,
            line_color=color_Ei
            ), row=1, col=2)
        fig2.add_trace(go.Scatter(
            x = Data_Vg, y = Data_df_E+1.35,
            name = "df_E", mode='lines', showlegend=False,
            line_color=color_Ef
            ), row=1, col=2)
        '''


    #######################

        if len(experimentbuttons)==0:

            fig2.add_trace(go.Scatter(
                x = Vg_array/Physics_Semiconductors.e, y = df_biasarray,
                name = "FrequencyShift", mode='lines', showlegend=False,
                line_color=color_other
                ), row=1, col=2)
            fig2.add_trace(go.Scatter(
                x = Vg_array/Physics_Semiconductors.e, y = dg_biasarray,
                name = "Excitation", mode='lines', showlegend=False,
                line_color=color_other
                ), row=2, col=2)    

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


    fig2.update_layout(transition_duration=300, height=600,margin=dict(t=0),showlegend=False)

    fig2.update_yaxes(row=1, col=1, title_text= "Contact Potential (eV)")
    fig2.update_yaxes(row=2, col=1, title_text= "Force (pN/nm^2)")
    fig2.update_yaxes(row=1, col=2, title_text = "Frequency Shift (Hz)")
    fig2.update_yaxes(row=2, col=2, title_text = "Dissipation (meV / cycle)")

    fig2.update_xaxes(row=1, col=1, showticklabels=True)
    fig2.update_xaxes(row=2, col=1, title_standoff=5, title_text= "Gate Bias (eV)")
    fig2.update_xaxes(row=1, col=2, showticklabels=True)
    fig2.update_xaxes(row=2, col=2, title_standoff=5, title_text= "Gate Bias (eV)")

    return fig2


################################################################################
################################################################################
# READOUTS

def readouts_AFM(slider_timesteps, slider_amplitude, slider_lag, slider_resfreq, slider_springconst, slider_Qfactor, slider_tipradius, slider_cantheight, slider_cantarea, slider_pulsetimesteps, slider_delaysteps):
    readout_timesteps = '{0:.0f}'.format(slider_timesteps)
    readout_amplitude = '{0:.1f}'.format(slider_amplitude)
    readout_lag = '{0:.0f}'.format(slider_lag)
    readout_resfreq = '{0:.0f}'.format(slider_resfreq)
    readout_springconst = '{0:.0f}'.format(slider_springconst)
    readout_Qfactor = '{0:.0f}'.format(slider_Qfactor)
    readout_tipradius = '{0:.3f}'.format(slider_tipradius)
    readout_cantheight = '{0:.3f}'.format(slider_cantheight)
    readout_cantarea = '{0:.0f}'.format(slider_cantarea)
    readout_pulsetimesteps = '{0:.0f}'.format(slider_pulsetimesteps)
    readout_delaysteps = '{0:.0f}'.format(slider_delaysteps)
    return readout_timesteps, readout_amplitude, readout_lag, readout_resfreq, readout_springconst, readout_Qfactor, readout_tipradius, readout_cantheight, readout_cantarea, readout_pulsetimesteps, readout_delaysteps


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

color_0 = '#d04443'
color_1 = '#ff922f'
color_2 = '#f2ac00'
color_3 = '#2ca02c'
color_4 = '#296329'
color_5 = '#224e6d'
color_6 = '#1f77b4'
color_7 = '#1e727a'
color_8 = '#6f518a'
color_9 = '#9467bd'