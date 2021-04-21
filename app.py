#############################################################################
# INITIALIZE

import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output, State

from __main__ import *
import ControlsBulk
import ControlsSurface
import ControlsAFM
import CallbacksBulk
import CallbacksSurface
import CallbacksAFM

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])


################################################################################
################################################################################
# LAYOUT

app.layout = dbc.Container(
    [
    dcc.Tabs([

    dcc.Tab(label='Bulk Physics', children=[
        html.Hr(),
        html.H1(children='Probability Distributions'),
        html.Br(),
        dbc.Row([
        dbc.Col(ControlsBulk.Distributions, md=4),
        dbc.Col(dcc.Graph(id="DistributionsGraph"), md=8),
        ], align="top",),
        html.Hr(),
        html.H1(children='Carrier Statistics'),
        html.Br(),
        dbc.Row([
        dbc.Col(ControlsBulk.Bulk_Cards, md=4),
        dbc.Col(dcc.Graph(id="BulkGraph"), md=8),
        ], align="top",),
        html.Hr(),
        ]),

    dcc.Tab(label='Surface Physics', children=[
        html.Hr(),
        html.H1(children='The MIS Capacitor'),
        html.Br(),
        dbc.Row([
            dbc.Col(ControlsSurface.Surface_Cards, md=3),
            dbc.Col(dcc.Graph(id="SurfaceGraph"), md=9),
        ], align="top",),
        html.Hr(),
        ]),

    dcc.Tab(label='Surface Measurements', children=[
        html.Hr(),
        html.H1(children='ncAFM Oscillations'),
        html.Br(),
        dbc.Row([
        dbc.Col(ControlsAFM.AFM_Cards1, md=4),
        dbc.Col(dcc.Graph(id="AFMGraph1"), md=8),
        ], align="top",),
        html.Hr(),
        html.H1(children='Bias Sweep Experiment'),
        html.Br(),
        dbc.Row([
        dbc.Col(ControlsAFM.AFM_Cards2, md=4),
        dbc.Col(dcc.Graph(id="AFMGraph2"), md=8),
        ], align="top",),
        html.Hr(),
        html.H1(children='Time Trace Experiment'),
        html.Br(),
        dbc.Row([
        dbc.Col(ControlsAFM.AFM_Cards3, md=4),
        dbc.Col(dcc.Graph(id="AFMGraph3"), md=8),
        ], align="top",),
        html.Hr(),
        ]),
    ])],
    fluid=True,
)

################################################################################################################################################################
################################################################################################################################################################
# BULK

# probability distributions figure
@app.callback(
    Output('DistributionsGraph', 'figure'),
    [Input('DistributionsSlider_Ef', 'value'),
     Input('DistributionsSlider_T', 'value')])
def update_figure(slider_Ef, slider_T):
     fig = CallbacksBulk.fig_probabilitydistributions(slider_Ef, slider_T)
     return fig

# carriers figure
@app.callback(
    Output('BulkGraph', 'figure'),
    [Input('BulkSlider_donor', 'value'),
     Input('BulkSlider_acceptor', 'value'),
     Input('BulkSlider_T', 'value'),
     Input('BulkSlider_emass', 'value'),
     Input('BulkSlider_hmass', 'value'),
     Input('BulkToggle_type', 'value')])
def update_figure(slider_donor, slider_acceptor, slider_T, slider_emass, slider_hmass, toggle_type):
    fig = CallbacksBulk.fig_carriers(slider_donor, slider_acceptor, slider_T, slider_emass, slider_hmass, toggle_type)
    return fig

# probability distributions readouts
@app.callback(
    [Output('DistributionsText_Ef', 'children'),
     Output('DistributionsText_T', 'children')],
    [Input('DistributionsSlider_Ef', 'value'),
     Input('DistributionsSlider_T', 'value')])
def update_output(slider_Ef, slider_T):
    readout_Ef, readout_T = CallbacksBulk.readouts_probabilitydistributions(slider_Ef, slider_T)
    return readout_Ef, readout_T

# carriers readouts
@app.callback(
    [Output('BulkText_donor', 'children'),
     Output('BulkText_acceptor', 'children'),
     Output('BulkText_T', 'children'),
     Output('BulkText_emass', 'children'),
     Output('BulkText_hmass', 'children')],
    [Input('BulkSlider_donor', 'value'),
     Input('BulkSlider_acceptor', 'value'),
     Input('BulkSlider_T', 'value'),
     Input('BulkSlider_emass', 'value'),
     Input('BulkSlider_hmass', 'value')])
def update_output(slider_donor, slider_acceptor, slider_T, slider_emass, slider_hmass):
    readout_donor, readout_acceptor, readout_T, readout_emass, readout_hmass = CallbacksBulk.readouts_carriers(slider_donor, slider_acceptor, slider_T, slider_emass, slider_hmass)
    return readout_donor, readout_acceptor, readout_T, readout_emass, readout_hmass

# toggle functionality
@app.callback(
    [Output('BulkText_typen', 'style'),
     Output('BulkText_typep', 'style'),
     Output('BulkSlider_donor', 'disabled'),
     Output('BulkSlider_acceptor', 'disabled'),
     Output('BulkSlider_donor', 'value'),
     Output('BulkSlider_acceptor', 'value'),
     Output('BulkText_typen', 'children'),
     Output('BulkText_typep', 'children')],
    [Input('BulkToggle_type', 'value')])
def update_output(toggle):
    stylen, stylep, disabledn, disabledp, valuen, valuep,  = CallbacksBulk.togglefunctions(toggle)
    return stylen, stylep, disabledn, disabledp, valuen, valuep, 'n-type', 'p-type'



################################################################################################################################################################
################################################################################################################################################################
# SURFACE PHYSICS

# surface figure
@app.callback(
    [Output('SurfaceGraph', 'figure'),
     Output('SurfaceText_ni', 'children')],
    [Input('SurfaceSlider_Vg', 'value'),
     Input('SurfaceSlider_zins', 'value'),
     Input('SurfaceSlider_bandgap', 'value'),
     Input('SurfaceSlider_epsilonsem', 'value'),
     Input('SurfaceSlider_WFmet', 'value'),
     Input('SurfaceSlider_EAsem', 'value'),
     Input('SurfaceSlider_donor', 'value'),
     Input('SurfaceSlider_acceptor', 'value'),
     Input('SurfaceSlider_emass', 'value'),
     Input('SurfaceSlider_hmass', 'value'),
     Input('SurfaceSlider_T', 'value')])
def update_figure(slider_Vg, slider_zins, slider_bandgap, slider_epsilonsem, slider_WFmet, slider_EAsem, slider_donor, slider_acceptor, slider_emass, slider_hmass, slider_T):
    fig, ni = CallbacksSurface.fig_surface(slider_Vg, slider_zins, slider_bandgap, slider_epsilonsem, slider_WFmet, slider_EAsem, slider_donor, slider_acceptor, slider_emass, slider_hmass, slider_T)
    return fig, ni

# surface readouts
@app.callback(
    [Output('SurfaceText_Vg', 'children'),
     Output('SurfaceText_zins', 'children'),
     Output('SurfaceText_bandgap', 'children'),
     Output('SurfaceText_epsilonsem', 'children'),
     Output('SurfaceText_WFmet', 'children'),
     Output('SurfaceText_EAsem', 'children'),
     Output('SurfaceText_donor', 'children'),
     Output('SurfaceText_acceptor', 'children'),
     Output('SurfaceText_emass', 'children'),
     Output('SurfaceText_hmass', 'children'),
     Output('SurfaceText_T', 'children')],
    [Input('SurfaceSlider_Vg', 'value'),
     Input('SurfaceSlider_zins', 'value'),
     Input('SurfaceSlider_bandgap', 'value'),
     Input('SurfaceSlider_epsilonsem', 'value'),
     Input('SurfaceSlider_WFmet', 'value'),
     Input('SurfaceSlider_EAsem', 'value'),
     Input('SurfaceSlider_donor', 'value'),
     Input('SurfaceSlider_acceptor', 'value'),
     Input('SurfaceSlider_emass', 'value'),
     Input('SurfaceSlider_hmass', 'value'),
     Input('SurfaceSlider_T', 'value')])
def update_output(slider_Vg, slider_zins, slider_bandgap, slider_epsilonsem, slider_WFmet, slider_EAsem, slider_donor, slider_acceptor, slider_emass, slider_hmass, slider_T):
    readout_Vg, readout_zins, readout_bandgap, readout_epsilonsem, readout_WFmet, readout_EAsem, readout_donor, readout_acceptor, readout_emass, readout_hmass, readout_T = CallbacksSurface.readouts_surface(slider_Vg, slider_zins, slider_bandgap, slider_epsilonsem, slider_WFmet, slider_EAsem, slider_donor, slider_acceptor, slider_emass, slider_hmass, slider_T)
    return readout_Vg, readout_zins, readout_bandgap, readout_epsilonsem, readout_WFmet, readout_EAsem, readout_donor, readout_acceptor, readout_emass, readout_hmass, readout_T



################################################################################################################################################################
################################################################################################################################################################
# AFM

# ncAFM oscillations figure
@app.callback(
    Output('AFMGraph1', 'figure'),
    [Input('AFMSlider_Vg', 'value'),
     Input('AFMSlider_zins', 'value'),
     Input('SurfaceSlider_bandgap', 'value'),
     Input('SurfaceSlider_epsilonsem', 'value'),
     Input('SurfaceSlider_WFmet', 'value'),
     Input('SurfaceSlider_EAsem', 'value'),
     Input('SurfaceSlider_donor', 'value'),
     Input('SurfaceSlider_acceptor', 'value'),
     Input('SurfaceSlider_emass', 'value'),
     Input('SurfaceSlider_hmass', 'value'),
     Input('SurfaceSlider_T', 'value'),
     Input('AFMSlider_amplitude', 'value'),
     Input('AFMSlider_resfreq', 'value'),
     Input('AFMSlider_hop', 'value'),
     Input('AFMSlider_lag', 'value'),
     Input('AFMbutton_Calculate', 'n_clicks'),
     Input('AFMtoggle_sampletype', 'value'),
     Input('AFMtoggle_RTN', 'value')])
def update_figure(slider_Vg, slider_zins, slider_bandgap, slider_epsilonsem, slider_WFmet, slider_EAsem, slider_donor, slider_acceptor, slider_emass, slider_hmass, slider_T, slider_amplitude, slider_resfreq, slider_hop, slider_lag, calculatebutton, toggle_sampletype, toggle_RTN):
    fig = CallbacksAFM.fig_AFM1(slider_Vg, slider_zins, slider_bandgap, slider_epsilonsem, slider_WFmet, slider_EAsem, slider_donor, slider_acceptor, slider_emass, slider_hmass, slider_T, slider_amplitude,slider_resfreq, slider_hop, slider_lag, calculatebutton, toggle_sampletype, toggle_RTN)
    return fig

# Bias experiment figure
@app.callback(
    Output('AFMGraph2', 'figure'),
    [Input('AFMSlider_Vg', 'value'),
     Input('AFMSlider_zins', 'value'),
     Input('SurfaceSlider_bandgap', 'value'),
     Input('SurfaceSlider_epsilonsem', 'value'),
     Input('SurfaceSlider_WFmet', 'value'),
     Input('SurfaceSlider_EAsem', 'value'),
     Input('SurfaceSlider_donor', 'value'),
     Input('SurfaceSlider_acceptor', 'value'),
     Input('SurfaceSlider_emass', 'value'),
     Input('SurfaceSlider_hmass', 'value'),
     Input('SurfaceSlider_T', 'value'),
     Input('AFMSlider_amplitude', 'value'),
     Input('AFMSlider_resfreq', 'value'),
     Input('AFMSlider_springconst', 'value'),
     Input('AFMSlider_tipradius', 'value'),
     Input('AFMSlider_Qfactor', 'value'),
     Input('AFMbutton_CalculateBiasExp', 'n_clicks'),
     Input('AFMtoggle_sampletype', 'value'),
     Input('AFMSlider_hop', 'value'),
     Input('AFMSlider_lag', 'value')])
def update_figure(slider_Vg, slider_zins, slider_bandgap, slider_epsilonsem, slider_WFmet, slider_EAsem, slider_donor, slider_acceptor, slider_emass, slider_hmass, slider_T, slider_amplitude, slider_resfreq, slider_springconst, slider_tipradius, slider_Qfactor, calculatebutton, toggle_sampletype, slider_hop,slider_lag):
    fig = CallbacksAFM.fig_AFM2(slider_Vg, slider_zins, slider_bandgap, slider_epsilonsem, slider_WFmet, slider_EAsem, slider_donor, slider_acceptor, slider_emass, slider_hmass, slider_T, slider_amplitude, slider_resfreq, slider_springconst, slider_tipradius, slider_Qfactor, calculatebutton, toggle_sampletype, slider_hop,slider_lag)
    return fig

# Time trace experiment figure
@app.callback(
    Output('AFMGraph3', 'figure'),
    [Input('AFMSlider_Vg', 'value'),
     Input('AFMSlider_zins', 'value'),
     Input('SurfaceSlider_bandgap', 'value'),
     Input('SurfaceSlider_epsilonsem', 'value'),
     Input('SurfaceSlider_WFmet', 'value'),
     Input('SurfaceSlider_EAsem', 'value'),
     Input('SurfaceSlider_donor', 'value'),
     Input('SurfaceSlider_acceptor', 'value'),
     Input('SurfaceSlider_emass', 'value'),
     Input('SurfaceSlider_hmass', 'value'),
     Input('SurfaceSlider_T', 'value'),
     Input('AFMSlider_amplitude', 'value'),
     Input('AFMSlider_resfreq', 'value'),
     Input('AFMSlider_springconst', 'value'),
     Input('AFMSlider_tipradius', 'value'),
     Input('AFMSlider_Qfactor', 'value'),
     Input('AFMbutton_CalculateTimeExp', 'n_clicks'),
     Input('AFMtoggle_sampletype', 'value'),
     Input('AFMSlider_hop', 'value'),
     Input('AFMSlider_lag', 'value')])
def update_figure(slider_Vg,slider_zins,slider_bandgap,slider_epsilonsem,slider_WFmet,slider_EAsem,slider_donor,slider_acceptor,slider_emass,slider_hmass,slider_T, slider_amplitude,slider_resfreq,slider_springconst,slider_tipradius,slider_Qfactor,calculatebutton,toggle_sampletype,slider_hop,slider_lag):
    fig = CallbacksAFM.fig_AFM3(slider_Vg,slider_zins,slider_bandgap,slider_epsilonsem,slider_WFmet,slider_EAsem,slider_donor,slider_acceptor,slider_emass,slider_hmass,slider_T, slider_amplitude,slider_resfreq,slider_springconst,slider_tipradius,slider_Qfactor,calculatebutton,toggle_sampletype,slider_hop,slider_lag)
    return fig

# AFM readouts
@app.callback(
    [Output('AFMText_Vg', 'children'),
     Output('AFMText_zins', 'children'),
     Output('AFMText_amplitude', 'children'),
     Output('AFMText_hop', 'children'),
     Output('AFMText_lag', 'children'),
     Output('AFMText_resfreq', 'children'),
     Output('AFMText_springconst', 'children'),
     Output('AFMText_Qfactor', 'children'),
     Output('AFMText_tipradius', 'children')],
    [Input('AFMSlider_Vg', 'value'),
     Input('AFMSlider_zins', 'value'),
     Input('AFMSlider_amplitude', 'value'),
     Input('AFMSlider_hop', 'value'),
     Input('AFMSlider_lag', 'value'),
     Input('AFMSlider_resfreq', 'value'),
     Input('AFMSlider_springconst', 'value'),
     Input('AFMSlider_Qfactor', 'value'),
     Input('AFMSlider_tipradius', 'value')])
def update_output(slider_Vg, slider_zins, slider_amplitude, slider_hop, slider_lag, slider_resfreq, slider_springconst, slider_Qfactor, slider_tipradius):
    readout_Vg, readout_zins, readout_amplitude, readout_hop, readout_lag, readout_resfreq, readout_springconst, readout_Qfactor, readout_tipradius = CallbacksAFM.readouts_AFM(slider_Vg, slider_zins, slider_amplitude, slider_hop, slider_lag, slider_resfreq, slider_springconst, slider_Qfactor, slider_tipradius)
    return readout_Vg, readout_zins, readout_amplitude, readout_hop, readout_lag, readout_resfreq, readout_springconst, readout_Qfactor, readout_tipradius

# toggle functionality
@app.callback(
    [Output('AFMText_semiconducting', 'style'),
     Output('AFMText_metallic', 'style'),
     Output('AFMText_semiconducting', 'children'),
     Output('AFMText_metallic', 'children')],
    [Input('AFMtoggle_sampletype', 'value')])
def update_output(toggle):
    style_s, style_m = CallbacksAFM.togglefunctions(toggle)
    return style_s, style_m, 'Semiconducting', 'Metallic'

#@app.callback(
#    [Output('AFMText_RTNoff', 'style'),
#     Output('AFMText_RTNon', 'style'),
#     Output('AFMText_RTNoff', 'children'),
#     Output('AFMText_RTNon', 'children')],
#    [Input('AFMtoggle_RTN', 'value')])
#def update_output(toggle):
#    style_off, style_on = CallbacksAFM.togglefunctions(toggle)
#    return style_off, style_on, 'Jump off', 'Jump on'


################################################################################################################################################################
################################################################################################################################################################
# RUN ON SERVER

if __name__ == '__main__':
    app.run_server(debug=True)
