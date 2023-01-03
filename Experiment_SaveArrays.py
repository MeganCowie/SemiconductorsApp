# Vary the dopant concentration of n-type silicon
import Physics_Semiconductors
import Physics_BandDiagram
import Organization_IntermValues
import Organization_BuildArrays
import numpy as np
import pandas as pd
import os

fig_carrierintegrals = 0
fig_carriers = 1

################################################################################
if fig_carrierintegrals == 1:

    # Sliders
    slider_Ef = 0.54
    slider_T = 500
    slider_gc = 4
    slider_gv = 1
    

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

    # Unit conversions
    Ef_xarray = np.array([1,1])*Ef/Physics_Semiconductors.e
    Ef_yarray = np.array([min_y, max_y])
    E_Earray = E/Physics_Semiconductors.e
    fc_Earray =  fc
    gc_Earray = gc*Physics_Semiconductors.e/scaling
    gv_Earray = gv*Physics_Semiconductors.e/scaling
    Ne_Earray = Ne*Physics_Semiconductors.e/scaling
    Nh_Earray = Nh*Physics_Semiconductors.e/scaling

    # Convert to dataframes
    save_Ef_xarray = pd.DataFrame({'Ef': [str(x) for x in Ef_xarray]})
    save_Ef_yarray = pd.DataFrame({'arb': [str(x) for x in Ef_yarray]})
    save_Ef = pd.concat([save_Ef_xarray,save_Ef_yarray], axis=1, join="outer")
    save_Earray_E = pd.DataFrame({'E': [str(x) for x in E_Earray]})
    save_Earray_fc = pd.DataFrame({'fc': [str(x) for x in fc_Earray]})
    save_Earray_gc = pd.DataFrame({'gc': [str(x) for x in gc_Earray]})
    save_Earray_gv = pd.DataFrame({'gv': [str(x) for x in gv_Earray]})
    save_Earray_Ne = pd.DataFrame({'Ne': [str(x) for x in Ne_Earray]})
    save_Earray_Nh = pd.DataFrame({'Nh': [str(x) for x in Nh_Earray]})
    save_Earrays = pd.concat([save_Earray_E,save_Earray_fc,save_Earray_gc,save_Earray_gv,save_Earray_Ne,save_Earray_Nh], axis=1, join="outer")

    # Save
    thispath = "Xsave_fig_carrierintegrals_%.2f_%.2f_%.2f_%.2f/" % (slider_Ef,slider_T,slider_gc,slider_gv)
    thisname = "%.2f_%.2f_%.2f_%.2f.csv" % (slider_Ef,slider_T,slider_gc,slider_gv)

    if not os.path.exists(thispath):
        os.mkdir(thispath)

    save_Ef.to_csv(os.path.join(thispath,'_'.join(['Ef',thisname])), index=False)
    save_Earrays.to_csv(os.path.join(thispath,'_'.join(['Earrays',thisname])), index=False)

if fig_carriers == 1:

    # sliders
    toggle_type = False
    slider_donor = 32
    slider_acceptor = 0
    slider_T = 750
    slider_emass = 0.5
    slider_hmass = 2

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

    # Unit conversions
    E_Earray = E/Physics_Semiconductors.e
    fc_Earray =  fc
    fv_Earray =  fv
    gc_Earray = gc*Physics_Semiconductors.e/(1000**3)
    gv_Earray = gv*Physics_Semiconductors.e/(1000**3)
    Ne_Earray = Ne*Physics_Semiconductors.e/(1000**3)
    Nh_Earray = Nh*Physics_Semiconductors.e/(1000**3)
    
    Ef_yarray = np.array([min_x, max_x])    
    Ef_xarray = np.array([1,1])*Ef/Physics_Semiconductors.e
    Ec_xarray = np.array([1,1])*Ec/Physics_Semiconductors.e
    Ev_xarray = np.array([1,1])*Ev/Physics_Semiconductors.e
    Ei_xarray = np.array([1,1])*Ei/Physics_Semiconductors.e
    

    # Convert to dataframes
    save_Ef_yarray = pd.DataFrame({'arb': [str(x) for x in Ef_yarray]})
    save_Ef_xarray = pd.DataFrame({'Ef': [str(x) for x in Ef_xarray]})
    save_Ec_xarray = pd.DataFrame({'Ec': [str(x) for x in Ec_xarray]})
    save_Ev_xarray = pd.DataFrame({'Ev': [str(x) for x in Ev_xarray]})
    save_Ei_xarray = pd.DataFrame({'Ei': [str(x) for x in Ei_xarray]})
    save_Evalues = pd.concat([save_Ef_yarray,save_Ef_xarray,save_Ec_xarray,save_Ev_xarray,save_Ei_xarray], axis=1, join="outer")
    save_Earray_E = pd.DataFrame({'E': [str(x) for x in E_Earray]})
    save_Earray_fc = pd.DataFrame({'fc': [str(x) for x in fc_Earray]})
    save_Earray_fv = pd.DataFrame({'fv': [str(x) for x in fv_Earray]})
    save_Earray_gc = pd.DataFrame({'gc': [str(x) for x in gc_Earray]})
    save_Earray_gv = pd.DataFrame({'gv': [str(x) for x in gv_Earray]})
    save_Earray_Ne = pd.DataFrame({'Ne': [str(x) for x in Ne_Earray]})
    save_Earray_Nh = pd.DataFrame({'Nh': [str(x) for x in Nh_Earray]})
    save_Earrays = pd.concat([save_Earray_E,save_Earray_fc,save_Earray_fv,save_Earray_gc,save_Earray_gv,save_Earray_Ne,save_Earray_Nh], axis=1, join="outer")

    # Save
    thispath = "Xsave_fig_carrierstatistics_%.2f_%.2f_%.2f_%.2f_%0.2f_%0.2f/" % (toggle_type,slider_donor,slider_acceptor,slider_T,slider_emass,slider_hmass)
    thisname = "%.2f_%.2f_%.2f_%.2f_%0.2f_%0.2f.csv" % (toggle_type,slider_donor,slider_acceptor,slider_T,slider_emass,slider_hmass)

    if not os.path.exists(thispath):
        os.mkdir(thispath)

    save_Evalues.to_csv(os.path.join(thispath,'_'.join(['Evalues',thisname])), index=False)
    save_Earrays.to_csv(os.path.join(thispath,'_'.join(['Earrays',thisname])), index=False)
