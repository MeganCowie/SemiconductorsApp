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

def fig1_AFM(slider_Vg, slider_zins, slider_Eg, slider_epsilonsem, slider_WFmet, slider_EAsem, slider_donor, slider_acceptor, slider_emass, slider_hmass, slider_T, slider_alpha, slider_biassteps,slider_zinssteps, slider_timesteps, slider_amplitude, slider_resfreq, slider_lag, calculatebutton):

    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if 'AFMbutton_Calculate' in changed_id:

        # Input values and arrays
        Vg,zins,Eg,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T,sampletype,biassteps,zinssteps,Vg_array,zins_array=Organization_IntermValues.Surface_inputvalues(slider_Vg,slider_zins,slider_alpha,slider_Eg,slider_epsilonsem,slider_WFmet,slider_EAsem,slider_donor,slider_acceptor,slider_emass,slider_hmass,slider_T,slider_biassteps,slider_zinssteps)
        amplitude,frequency,lag,timesteps,time_AFMarray,zins_AFMarray,zinslag_AFMarray=Organization_IntermValues.AFM1_inputvalues(slider_amplitude,slider_resfreq,slider_lag,slider_timesteps,  zins)

        # Calculations and results
        NC,NV,Ec,Ev,Ei,Ef,no,po,ni,CPD,LD,Vs,Es,Qs,F,regime, zsem,Vsem,Esem,Qsem, P = Organization_IntermValues.Surface_calculations(Vg,zins,Eg,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T)
        Vs_biasarray,F_biasarray,Es_biasarray,Qs_biasarray,P_biasarray = Organization_BuildArrays.Surface_biasarrays(Vg_array,zins,Na,Nd,epsilon_sem,T,CPD,LD,no,po,ni)
        Vs_zinsarray,F_zinsarray,Es_zinsarray,Qs_zinsarray,P_zinsarray = Organization_BuildArrays.Surface_zinsarrays(zins_array,Vg,Na,Nd,epsilon_sem,T,CPD,LD,no,po,ni)
        Vs_AFMarray, F_AFMarray, P_AFMarray = Organization_BuildArrays.AFM_timearrays(zinslag_AFMarray,Vg,zins,Na,Nd,epsilon_sem,T,CPD,LD,no,po,ni)
        zsem_AFMarray,Vsem_AFMarray,zgap_AFMarray,Vgap_AFMarray,zvac_AFMarray,Vvac_AFMarray,zmet_AFMarray,Vmet_AFMarray = Organization_BuildArrays.AFM_banddiagrams(zins_AFMarray,Vg,T,Nd,Na,WFmet,EAsem,epsilon_sem, ni,no,po,Vs,Ec,Ev,Ef,CPD)

        # Account for alpha
        Vg = slider_Vg*Physics_Semiconductors.e #J
        Vg_array = np.linspace(-10,10,biassteps)*Physics_Semiconductors.e #J

    
        # Stack arrays to show two periods
        time_AFMarray = np.hstack((time_AFMarray,time_AFMarray[1:]+2*np.pi))
        zins_AFMarray = np.hstack((zins_AFMarray,zins_AFMarray[1:]))
        zinslag_AFMarray = np.hstack((zinslag_AFMarray,zinslag_AFMarray[1:]))
        Vs_AFMarray = np.hstack((Vs_AFMarray,Vs_AFMarray[1:]))
        F_AFMarray = np.hstack((F_AFMarray,F_AFMarray[1:]))
        zsem_AFMarray_steps = np.vstack((zsem_AFMarray,zsem_AFMarray[1:]))
        Vsem_AFMarray_steps = np.vstack((Vsem_AFMarray,Vsem_AFMarray[1:]))
        zgap_AFMarray_steps = np.vstack((zgap_AFMarray,zgap_AFMarray[1:]))
        Vgap_AFMarray_steps = np.vstack((Vgap_AFMarray,Vgap_AFMarray[1:]))
        zvac_AFMarray_steps = np.vstack((zvac_AFMarray,zvac_AFMarray[1:]))
        Vvac_AFMarray_steps = np.vstack((Vvac_AFMarray,Vvac_AFMarray[1:]))
        zmet_AFMarray_steps = np.vstack((zmet_AFMarray,zmet_AFMarray[1:]))
        Vmet_AFMarray_steps = np.vstack((Vmet_AFMarray,Vmet_AFMarray[1:]))
    
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
        fig1.add_trace(go.Scatter(
            x = time_AFMarray, y = F_AFMarray*(1e-9)**2*1e12,
            name = "Force", mode='lines', showlegend=False,
            line_color=color_other
            ), row=3, col=2)
        fig1.add_trace(go.Scatter(
            x = [time_AFMarray[0]], y = [F_AFMarray[0]*(1e-9)**2*1e12],
            name = "Force", mode='markers',
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
    fig1.update_xaxes(row=1, col=2, title_text= "Time", showticklabels=False, range=[0, 4*np.pi])
    fig1.update_xaxes(row=2, col=2, title_text= "Time", showticklabels=False, range=[0, 4*np.pi])
    fig1.update_xaxes(row=3, col=2, title_text= "Time", showticklabels=False, range=[0, 4*np.pi])

    return fig1


################################################################################
################################################################################
# FIGURE: Bias sweep experiment

def fig2_AFM(slider_Vg,slider_zins,slider_Eg,slider_epsilonsem,slider_WFmet,slider_EAsem,slider_donor,slider_acceptor,slider_emass,slider_hmass,slider_T,slider_alpha,slider_biassteps,slider_zinssteps, slider_timesteps,slider_amplitude,slider_resfreq,slider_springconst,slider_tipradius,slider_Qfactor,calculatebutton,slider_lag):

    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if 'AFMbutton_CalculateBiasExp' in changed_id:

        # Input values and arrays
        Vg,zins,Eg,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T,sampletype,biassteps,zinssteps,Vg_array,zins_array=Organization_IntermValues.Surface_inputvalues(slider_Vg,slider_zins,slider_alpha,slider_Eg,slider_epsilonsem,slider_WFmet,slider_EAsem,slider_donor,slider_acceptor,slider_emass,slider_hmass,slider_T,slider_biassteps,slider_zinssteps)
        amplitude,frequency,lag,timesteps,time_AFMarray,zins_AFMarray,zinslag_AFMarray=Organization_IntermValues.AFM1_inputvalues(slider_amplitude,slider_resfreq,slider_lag,slider_timesteps,  zins)
        springconst,Qfactor,tipradius=Organization_IntermValues.AFM2_inputvalues(slider_springconst,slider_Qfactor,slider_tipradius)

        # Calculations and results
        NC,NV,Ec,Ev,Ei,Ef,no,po,ni,CPD,LD,Vs,Es,Qs,F,regime, zsem,Vsem,Esem,Qsem, P = Organization_IntermValues.Surface_calculations(Vg,zins,Eg,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T)
        Vs_biasarray,F_biasarray,df_biasarray,dg_biasarray = Organization_BuildArrays.AFM_biasarrays(Vg_array,zins,Na,Nd,epsilon_sem,T,CPD,LD,no,po,ni,frequency,springconst,amplitude,Qfactor,tipradius,time_AFMarray,zinslag_AFMarray)

        # Account for alpha
        Vg = slider_Vg*Physics_Semiconductors.e #J
        Vg_array = np.linspace(-10,10,biassteps)*Physics_Semiconductors.e #J

        # Plot data
        Data_Vg = np.genfromtxt ('Data_Vg.csv', delimiter=",")
        Data_df_A = np.genfromtxt ('Data_df_A.csv', delimiter=",")
        Data_df_B = np.genfromtxt ('Data_df_B.csv', delimiter=",")
        Data_df_C = np.genfromtxt ('Data_df_C.csv', delimiter=",")
        Data_df_D = np.genfromtxt ('Data_df_D.csv', delimiter=",")
        Data_df_E = np.genfromtxt ('Data_df_E.csv', delimiter=",")

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
        fig2.add_trace(go.Scatter(
            x = Vg_array/Physics_Semiconductors.e, y = df_biasarray,
            name = "FrequencyShift", mode='lines', showlegend=False,
            line_color=color_other
            ), row=1, col=2)
        fig2.add_trace(go.Scatter(
            x = Data_Vg, y = Data_df_A+1.38,
            name = "FrequencyShiftData", mode='lines', showlegend=False,
            line_color=color_indicator
            ), row=1, col=2)
        fig2.add_trace(go.Scatter(
            x = Data_Vg, y = Data_df_B+1.38,
            name = "FrequencyShiftData", mode='lines', showlegend=False,
            line_color=color_Ev
            ), row=1, col=2)
        fig2.add_trace(go.Scatter(
            x = Data_Vg, y = Data_df_C+1.38,
            name = "FrequencyShiftData", mode='lines', showlegend=False,
            line_color=color_Ec
            ), row=1, col=2)
        fig2.add_trace(go.Scatter(
            x = Vg_array/Physics_Semiconductors.e, y = dg_biasarray,
            name = "Dissipation", mode='lines', showlegend=False,
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

'''
################################################################################
################################################################################
# FIGURE: Time trace experiment
# NOT DONE YET

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
'''

################################################################################
################################################################################
# READOUTS

def readouts_AFM(slider_timesteps, slider_amplitude, slider_lag, slider_resfreq, slider_springconst, slider_Qfactor, slider_tipradius, slider_pulsetimesteps, slider_delaysteps):
    readout_timesteps = '{0:.0f}'.format(slider_timesteps)
    readout_amplitude = '{0:.1f}'.format(slider_amplitude)
    readout_lag = '{0:.0f}'.format(slider_lag)
    readout_resfreq = '{0:.0f}'.format(slider_resfreq)
    readout_springconst = '{0:.0f}'.format(slider_springconst)
    readout_Qfactor = '{0:.0f}'.format(slider_Qfactor)
    readout_tipradius = '{0:.1f}'.format(slider_tipradius)
    readout_pulsetimesteps = '{0:.0f}'.format(slider_pulsetimesteps)
    readout_delaysteps = '{0:.0f}'.format(slider_delaysteps)
    return readout_timesteps, readout_amplitude, readout_lag, readout_resfreq, readout_springconst, readout_Qfactor, readout_tipradius, readout_pulsetimesteps, readout_delaysteps


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
