import numpy as np

def presets_surface(button_presets, toggle_type, slider_Vg, slider_zins, slider_Eg, slider_epsilonsem, slider_WFmet, slider_EAsem, slider_donor, slider_acceptor, slider_emass, slider_hmass, slider_T, slider_alpha):
    if button_presets == 1: #MoSe2
        toggle_type = True
        slider_Vg = -1.4
        slider_zins = 5.2
        slider_Eg = 1.5
        slider_epsilonsem = 5.9
        slider_WFmet = 4.1
        slider_EAsem = 3.5
        slider_emass = 1
        slider_hmass = 1
        slider_donor = 0
        slider_acceptor = 32.8
        slider_T = 300
        slider_alpha = 0
        stylen = {'color': '#7f7f7f'}
        stylep = {'color': '#57c5f7'}
        disabledn = True
        disabledp = False
    elif button_presets == 2: #Si
        toggle_type = False
        slider_Vg = 0
        slider_zins = 6
        slider_Eg = 1.1
        slider_epsilonsem = 11.7
        slider_WFmet = 4.5
        slider_EAsem = 4.5#4.05
        slider_emass = 1.08
        slider_hmass = 0.56
        slider_donor = 32.7
        slider_acceptor = 0
        slider_T = 300
        slider_alpha = 0#0.3
        stylen = {'color': '#57c5f7'}
        stylep = {'color': '#7f7f7f'}
        disabledn = False
        disabledp = True
    elif button_presets == 3: #Pentacene
        toggle_type = False
        slider_Vg = -1.4
        slider_zins = 6
        slider_Eg = 2.2
        slider_epsilonsem = 11.8
        slider_WFmet = 3.4
        slider_EAsem = 2.9
        slider_emass = 1
        slider_hmass = 1
        slider_donor = 17.4
        slider_acceptor = 0
        slider_T = 300
        slider_alpha = 0.8
        stylen = {'color': '#57c5f7'}
        stylep = {'color': '#7f7f7f'}
        disabledn = False
        disabledp = True
    elif button_presets == 4: #Figure_ntype
        toggle_type = False
        slider_Vg = 0
        slider_zins = 1
        slider_Eg = 1
        slider_epsilonsem = 1
        slider_WFmet = 1.3
        slider_EAsem = 0.8
        slider_emass = 1
        slider_hmass = 1
        slider_donor = 33
        slider_acceptor = 0
        slider_T = 300
        slider_alpha = 0
        stylen = {'color': '#57c5f7'}
        stylep = {'color': '#7f7f7f'}
        disabledn = False
        disabledp = True
    elif button_presets == 5: #Figure_ptype
        toggle_type = True
        slider_Vg = 0
        slider_zins = 1
        slider_Eg = 1
        slider_epsilonsem = 1
        slider_WFmet = 1.3
        slider_EAsem = 0.8
        slider_emass = 1
        slider_hmass = 1
        slider_donor = 0
        slider_acceptor = 33
        slider_T = 300
        slider_alpha = 0
        stylen = {'color': '#57c5f7'}
        stylep = {'color': '#7f7f7f'}
        disabledn = True
        disabledp = False
    else:
        toggle_type = toggle_type
        slider_Vg = slider_Vg
        slider_zins = slider_zins
        slider_Eg = slider_Eg
        slider_epsilonsem = slider_epsilonsem
        slider_WFmet = slider_WFmet
        slider_EAsem = slider_EAsem
        slider_emass = slider_emass
        slider_hmass = slider_hmass
        slider_donor = slider_donor
        slider_acceptor = slider_acceptor
        slider_T = slider_T
        slider_alpha = slider_alpha
        if toggle_type == True: #p-type
            stylen = {'color': '#7f7f7f'}
            stylep = {'color': '#57c5f7'}
            disabledn = True
            disabledp = False
            if slider_acceptor == 0:
                slider_acceptor = slider_donor
            else:
                slider_acceptor = slider_acceptor
            slider_donor = 0
        elif toggle_type == False: #n-type
            stylen = {'color': '#57c5f7'}
            stylep = {'color': '#7f7f7f'}
            disabledn = False
            disabledp = True
            if slider_donor == 0:
                slider_donor = slider_acceptor
            else:
                slider_donor = slider_donor
            slider_acceptor = 0
    return toggle_type, slider_Vg, slider_zins, slider_Eg, slider_epsilonsem, slider_WFmet, slider_EAsem, slider_donor, slider_acceptor, slider_emass, slider_hmass, slider_T, slider_alpha, button_presets, stylen, stylep, disabledn, disabledp

def presets_afm(button_presets,slider_timesteps, slider_amplitude, slider_resfreq, slider_lag, slider_springconst, slider_tipradius, slider_cantheight, slider_cantarea, slider_Qfactor):

    if button_presets == 1: #Figure
        slider_timesteps = 30
        slider_amplitude = 6
        slider_resfreq = 300000
        slider_lag = 0
        slider_springconst = 42
        slider_tipradius = 5
        slider_cantheight = 5
        slider_cantarea = 3750
        slider_Qfactor = 18000
    else:
        slider_timesteps = slider_timesteps
        slider_amplitude = slider_amplitude
        slider_resfreq = slider_resfreq
        slider_lag = slider_lag
        slider_springconst = slider_springconst
        slider_tipradius = slider_tipradius
        slider_cantheight = slider_cantheight
        slider_cantarea = slider_cantarea
        slider_Qfactor = slider_Qfactor
    return slider_timesteps, slider_amplitude, slider_resfreq, slider_lag, slider_springconst, slider_tipradius, slider_cantheight, slider_cantarea, slider_Qfactor



def togglefunctions(toggle_type, slider_donor, slider_acceptor):
    if toggle_type == True: #p-type
        stylen = {'color': '#7f7f7f'}
        stylep = {'color': '#57c5f7'}
        disabledn = True
        disabledp = False
        slider_donor = 0
        slider_acceptor = slider_acceptor
    elif toggle_type == False: #n-type
        stylen = {'color': '#57c5f7'}
        stylep = {'color': '#7f7f7f'}
        disabledn = False
        disabledp = True
        slider_donor = slider_donor
        slider_acceptor = 0
    return stylen, stylep, disabledn, disabledp, slider_donor, slider_acceptor

