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
import PresetsSurface

###### important for latex ######
import dash_defer_js_import as dji

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

###### important for latex ######
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            <script type="text/x-mathjax-config">
            MathJax.Hub.Config({
                tex2jax: {
                inlineMath: [ ['$','$']],
                processEscapes: true
                }
            });
            </script>
            {%renderer%}
        </footer>
    </body>
</html>
'''

Distributions_text = open("Text_Distributions.md", "r").read()
ElectronicStructure_text = open("Text_ElectronicStructure.md", "r").read()
CarrierStatistics1_text = open("Text_CarrierStatistics1.md", "r").read()
CarrierStatistics2_text = open("Text_CarrierStatistics2.md", "r").read()
ElectricalGating_text = open("Text_ElectricalGating.md", "r").read()

axis_latex_script = dji.Import(src="https://cdn.jsdelivr.net/gh/yueyericardo/simuc@master/apps/dash/resources/redraw.js")
mathjax_script = dji.Import(src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.7/latest.js?config=TeX-AMS-MML_SVG")


################################################################################
################################################################################
# LAYOUT

app.layout = dbc.Container(
    [
        #html.Hr(),
        #html.Br(),
        #dbc.Row([
        #    dbc.Col(dcc.Markdown(ElectronicStructure_text, dangerously_allow_html=True), md=12),
        #], align="top",),
        #html.Br(),
        #html.Br(),
        #dbc.Row([
        #    dbc.Col(dcc.Markdown(Distributions_text, dangerously_allow_html=True), md=12),
        #], align="top",),
        #html.Br(),
        #dbc.Row([
        #    dbc.Col(ControlsBulk.Distributions, md=3),
        #    dbc.Col(html.Div(id="DistributionsGraph"), md=9),

        #], align="top",),
        #html.Br(),
        #dbc.Row([
        #    dbc.Col(dcc.Markdown(CarrierStatistics1_text, dangerously_allow_html=True), md=12),
        #], align="top",),
        #html.Br(),
        #dbc.Row([
        #    dbc.Col(ControlsBulk.CarrierIntegrals, md=3),
        #    dbc.Col(html.Div(id="CarrierIntegralsGraph"), md=9),
        #], align="top",),
        #html.Br(),
        #dbc.Row([
        #    dbc.Col(dcc.Markdown(CarrierStatistics2_text, dangerously_allow_html=True), md=12),
        #], align="top",),
        #html.Br(),
        #dbc.Row([
        #    dbc.Col(ControlsBulk.Bulk_Card, md=3),
        #    dbc.Col(dcc.Graph(id="BulkGraph"), md=9),
        #], align="top",),
        #html.Hr(),
        #html.Br(),
        #dbc.Row([
        #    dbc.Col(dcc.Markdown(ElectricalGating_text, dangerously_allow_html=True), md=12),
        #], align="top",),
        dbc.Row([
            dbc.Col(ControlsSurface.Surface_Cards, md=3),
            dbc.Col([dcc.Graph(id="SurfaceGraph"),dcc.Graph(id="SurfaceGraphSupp")], md=9),
        ], align="top",),

        html.Hr(),
        html.H1(children='fm-AFM Oscillations'),
        html.Br(),
        dbc.Row([
            dbc.Col(ControlsAFM.AFM_Cards1, md=3),
            dbc.Col(dcc.Graph(id="AFMGraph1"), md=9),
        ], align="top",),
        html.Hr(),
        html.H1(children='Bias Sweep Experiment'),
        html.Br(),
        dbc.Row([
            dbc.Col(ControlsAFM.AFM_Cards2, md=3),
            dbc.Col(dcc.Graph(id="AFMGraph2"), md=9),
        ], align="top",),
        #html.Hr(),
        #html.H1(children='Time Trace Experiment'),
        #html.Br(),
        #dbc.Row([
            #dbc.Col(ControlsAFM.AFM_Cards3, md=3),
            #dbc.Col(dcc.Graph(id="AFMGraph3"), md=9),
        #], align="top",),
        html.Hr(),
        html.H1(children='Delay Sweep Experiment'),
        html.Br(),
        dbc.Row([
            dbc.Col(ControlsAFM.AFM_Cards4, md=3),
            dbc.Col(dcc.Graph(id="AFMGraph4"), md=9),
        ], align="top",),
        html.Hr(),

    ###### important for latex ######
    axis_latex_script,
    mathjax_script,

    ],
    fluid=True,
)




################################################################################################################################################################
################################################################################################################################################################
# BULK

# probability distributions figure
#@app.callback(
#    Output('DistributionsGraph', 'children'),
#    [Input('DistributionsSlider_Ef', 'value'),
#     Input('DistributionsSlider_T', 'value')])
#def update_figure(slider_Ef, slider_T):
#     fig = CallbacksBulk.fig_probabilitydistributions(slider_Ef, slider_T)
#     return dcc.Graph(figure=fig)

# carrier integrals figure
#@app.callback(
#    Output('CarrierIntegralsGraph', 'children'),
#    [Input('CarrierIntegralsSlider_Ef', 'value'),
#     Input('CarrierIntegralsSlider_T', 'value'),
#     Input('CarrierIntegralsSlider_gc', 'value'),
#     Input('CarrierIntegralsSlider_gv', 'value')])
#def update_figure(slider_Ef, slider_T,slider_gc,slider_gv):
#     fig = CallbacksBulk.fig_carrierintegrals(slider_Ef, slider_T,slider_gc,slider_gv)
#     return dcc.Graph(figure=fig)

# carriers figure
#@app.callback(
#    Output('BulkGraph', 'figure'),
#    [Input('BulkSlider_donor', 'value'),
#     Input('BulkSlider_acceptor', 'value'),
#     Input('BulkSlider_T', 'value'),
#     Input('BulkSlider_emass', 'value'),
#     Input('BulkSlider_hmass', 'value'),
#     Input('BulkToggle_type', 'value')])
#def update_figure(slider_donor, slider_acceptor, slider_T, slider_emass, slider_hmass, toggle_type):
#    fig = CallbacksBulk.fig_carriers(slider_donor, slider_acceptor, slider_T, slider_emass, slider_hmass, toggle_type)
#    return fig

## probability distributions readouts
#@app.callback(
#    [Output('DistributionsText_Ef', 'children'),
#     Output('DistributionsText_T', 'children')],
#    [Input('DistributionsSlider_Ef', 'value'),
#     Input('DistributionsSlider_T', 'value')])
#def update_output(slider_Ef, slider_T):
#    readout_Ef, readout_T = CallbacksBulk.readouts_probabilitydistributions(slider_Ef, slider_T)
#    return readout_Ef, readout_T

# carriers readouts
#@app.callback(
#    [Output('BulkText_donor', 'children'),
#     Output('BulkText_acceptor', 'children'),
#     Output('BulkText_T', 'children'),
#     Output('BulkText_emass', 'children'),
#     Output('BulkText_hmass', 'children')],
#    [Input('BulkSlider_donor', 'value'),
#     Input('BulkSlider_acceptor', 'value'),
#     Input('BulkSlider_T', 'value'),
#     Input('BulkSlider_emass', 'value'),
#     Input('BulkSlider_hmass', 'value')])
#def update_output(slider_donor, slider_acceptor, slider_T, slider_emass, slider_hmass):
#    readout_donor, readout_acceptor, readout_T, readout_emass, readout_hmass = CallbacksBulk.readouts_carriers(slider_donor, slider_acceptor, slider_T, slider_emass, slider_hmass)
#    return readout_donor, readout_acceptor, readout_T, readout_emass, readout_hmass

# toggle functionality
#@app.callback(
#    [Output('BulkText_typen', 'style'),
#     Output('BulkText_typep', 'style'),
#     Output('BulkSlider_donor', 'disabled'),
#     Output('BulkSlider_acceptor', 'disabled'),
#     Output('BulkSlider_donor', 'value'),
#     Output('BulkSlider_acceptor', 'value'),
#     Output('BulkText_typen', 'children'),
#     Output('BulkText_typep', 'children')],
#    [Input('BulkToggle_type', 'value')])
#def update_output(toggle):
#    stylen, stylep, disabledn, disabledp, valuen, valuep,  = CallbacksBulk.togglefunctions(toggle)
#    return stylen, stylep, disabledn, disabledp, valuen, valuep, 'n-type', 'p-type'



################################################################################################################################################################
################################################################################################################################################################
# SURFACE PHYSICS

# surface figure
@app.callback(
    [Output('SurfaceGraph', 'figure'),
     Output('SurfaceGraphSupp', 'figure'),
     Output('SurfaceText_regime', 'children'),
     Output('SurfaceText_ni', 'children'),
     Output('SurfaceText_LD', 'children'),
     Output('SurfaceText_zQ', 'children')],
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
     Input('SurfaceSlider_T', 'value'),
     Input('SurfaceSlider_alpha', 'value')])
def update_figure(slider_Vg, slider_zins, slider_bandgap, slider_epsilonsem, slider_WFmet, slider_EAsem, slider_donor, slider_acceptor, slider_emass, slider_hmass, slider_T, slider_alpha):
    fig, figsupp, regime, ni, LD, zQ = CallbacksSurface.fig_surface(slider_Vg, slider_zins, slider_bandgap, slider_epsilonsem, slider_WFmet, slider_EAsem, slider_donor, slider_acceptor, slider_emass, slider_hmass, slider_T, slider_alpha)
    return fig, figsupp, regime, ni, LD, zQ

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
     Output('SurfaceText_T', 'children'),
     Output('SurfaceText_alpha', 'children')],
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
     Input('SurfaceSlider_T', 'value'),
     Input('SurfaceSlider_alpha', 'value')])
def update_output(slider_Vg, slider_zins, slider_bandgap, slider_epsilonsem, slider_WFmet, slider_EAsem, slider_donor, slider_acceptor, slider_emass, slider_hmass, slider_T, slider_alpha):
    readout_Vg, readout_zins, readout_bandgap, readout_epsilonsem, readout_WFmet, readout_EAsem, readout_donor, readout_acceptor, readout_emass, readout_hmass, readout_T, readout_alpha = CallbacksSurface.readouts_surface(slider_Vg, slider_zins, slider_bandgap, slider_epsilonsem, slider_WFmet, slider_EAsem, slider_donor, slider_acceptor, slider_emass, slider_hmass, slider_T, slider_alpha)
    return readout_Vg, readout_zins, readout_bandgap, readout_epsilonsem, readout_WFmet, readout_EAsem, readout_donor, readout_acceptor, readout_emass, readout_hmass, readout_T, readout_alpha


# surface presets
@app.callback(
    [Output('SurfaceToggle_type', 'value'),
     Output('SurfaceSlider_Vg', 'value'),
     Output('SurfaceSlider_zins', 'value'),
     Output('SurfaceSlider_bandgap', 'value'),
     Output('SurfaceSlider_epsilonsem', 'value'),
     Output('SurfaceSlider_WFmet', 'value'),
     Output('SurfaceSlider_EAsem', 'value'),
     Output('SurfaceSlider_donor', 'value'),
     Output('SurfaceSlider_acceptor', 'value'),
     Output('SurfaceSlider_emass', 'value'),
     Output('SurfaceSlider_hmass', 'value'),
     Output('SurfaceSlider_T', 'value'),
     Output('SurfaceSlider_alpha', 'value'),
     Output('SurfaceButtons_presets', 'value'),
     Output('SurfaceText_typen', 'style'),
     Output('SurfaceText_typep', 'style'),
     Output('SurfaceSlider_donor', 'disabled'),
     Output('SurfaceSlider_acceptor', 'disabled'),
     Output('SurfaceText_typen', 'children'),
     Output('SurfaceText_typep', 'children')],
    [Input('SurfaceButtons_presets', 'value'),
     Input('SurfaceSlider_Vg', 'value'),
     Input('SurfaceSlider_zins', 'value'),
     Input('SurfaceSlider_bandgap', 'value'),
     Input('SurfaceSlider_epsilonsem', 'value'),
     Input('SurfaceSlider_WFmet', 'value'),
     Input('SurfaceSlider_EAsem', 'value'),
     Input('SurfaceSlider_donor', 'value'),
     Input('SurfaceSlider_acceptor', 'value'),
     Input('SurfaceSlider_emass', 'value'),
     Input('SurfaceSlider_hmass', 'value'),
     Input('SurfaceSlider_T', 'value'),
     Input('SurfaceSlider_alpha', 'value'),
     Input('SurfaceToggle_type', 'value')])
def presets(button_presets,slider_Vg, slider_zins, slider_bandgap, slider_epsilonsem, slider_WFmet, slider_EAsem, slider_donor, slider_acceptor, slider_emass, slider_hmass, slider_T, slider_alpha, toggle_type):

    button_presets_og = button_presets

    # Somehow writing this as an or statement doesn't work, so for now it looks like this.
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if 'SurfaceToggle_type' in changed_id:
        button_presets = 4
    elif 'SurfaceSlider_Vg' in changed_id:
        button_presets = 4
    elif 'SurfaceSlider_zins' in changed_id:
        button_presets = 4
    elif 'SurfaceSlider_bandgap' in changed_id:
        button_presets = 4
    elif 'SurfaceSlider_epsilonsem' in changed_id:
        button_presets = 4
    elif 'SurfaceSlider_WFmet' in changed_id:
        button_presets = 4
    elif 'SurfaceSlider_EAsem' in changed_id:
        button_presets = 4
    elif 'SurfaceSlider_donor' in changed_id:
        button_presets = 4
    elif 'SurfaceSlider_acceptor' in changed_id:
        button_presets = 4
    elif 'SurfaceSlider_emass' in changed_id:
        button_presets = 4
    elif 'SurfaceSlider_hmass' in changed_id:
        button_presets = 4
    elif 'SurfaceSlider_T' in changed_id:
        button_presets = 4
    elif 'SurfaceSlider_alpha' in changed_id:
        button_presets = 4
    else:
        button_presets = button_presets

    toggle_type, slider_Vg, slider_zins, slider_bandgap, slider_epsilonsem, slider_WFmet, slider_EAsem, slider_donor, slider_acceptor, slider_emass, slider_hmass, slider_T, slider_alpha, button_presets, stylen, stylep, disabledn, disabledp = PresetsSurface.presets_surface(button_presets, toggle_type, slider_Vg, slider_zins, slider_bandgap, slider_epsilonsem, slider_WFmet, slider_EAsem, slider_donor, slider_acceptor, slider_emass, slider_hmass, slider_T, slider_alpha)

    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if 'SurfaceSlider_Vg' in changed_id:
        button_presets = button_presets_og
    elif 'SurfaceSlider_zins' in changed_id:
        button_presets = button_presets_og
    elif 'SurfaceSlider_T' in changed_id:
        button_presets = button_presets_og
    else:
        button_presets = button_presets

    return toggle_type, slider_Vg, slider_zins, slider_bandgap, slider_epsilonsem, slider_WFmet, slider_EAsem, slider_donor, slider_acceptor, slider_emass, slider_hmass, slider_T, slider_alpha, button_presets, stylen, stylep, disabledn, disabledp, 'n-type', 'p-type'

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
#@app.callback(
#    Output('AFMGraph3', 'figure'),
#    [Input('AFMSlider_Vg', 'value'),
#     Input('AFMSlider_zins', 'value'),
#     Input('SurfaceSlider_bandgap', 'value'),
#     Input('SurfaceSlider_epsilonsem', 'value'),
#     Input('SurfaceSlider_WFmet', 'value'),
#     Input('SurfaceSlider_EAsem', 'value'),
#     Input('SurfaceSlider_donor', 'value'),
#     Input('SurfaceSlider_acceptor', 'value'),
#     Input('SurfaceSlider_emass', 'value'),
#     Input('SurfaceSlider_hmass', 'value'),
#     Input('SurfaceSlider_T', 'value'),
#     Input('AFMSlider_amplitude', 'value'),
#     Input('AFMSlider_resfreq', 'value'),
#     Input('AFMSlider_springconst', 'value'),
#     Input('AFMSlider_tipradius', 'value'),
#     Input('AFMSlider_Qfactor', 'value'),
#     Input('AFMbutton_CalculateTimeExp', 'n_clicks'),
#     Input('AFMtoggle_sampletype', 'value'),
#     Input('AFMSlider_hop', 'value'),
#     Input('AFMSlider_lag', 'value')])
#def update_figure(slider_Vg,slider_zins,slider_bandgap,slider_epsilonsem,slider_WFmet,slider_EAsem,slider_donor,slider_acceptor,slider_emass,slider_hmass,slider_T, slider_amplitude,slider_resfreq,slider_springconst,slider_tipradius,slider_Qfactor,calculatebutton,toggle_sampletype,slider_hop,slider_lag):
#    fig = CallbacksAFM.fig_AFM3(slider_Vg,slider_zins,slider_bandgap,slider_epsilonsem,slider_WFmet,slider_EAsem,slider_donor,slider_acceptor,slider_emass,slider_hmass,slider_T, slider_amplitude,slider_resfreq,slider_springconst,slider_tipradius,slider_Qfactor,calculatebutton,toggle_sampletype,slider_hop,slider_lag)
#    return fig

# Delay experiment figure
@app.callback(
    Output('AFMGraph4', 'figure'),
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
     Input('AFMbutton_CalculateDelayExp', 'n_clicks'),
     Input('AFMtoggle_sampletype', 'value'),
     Input('AFMSlider_hop', 'value'),
     Input('AFMSlider_lag', 'value')])
def update_figure(slider_Vg, slider_zins, slider_bandgap, slider_epsilonsem, slider_WFmet, slider_EAsem, slider_donor, slider_acceptor, slider_emass, slider_hmass, slider_T, slider_amplitude, slider_resfreq, slider_springconst, slider_tipradius, slider_Qfactor, calculatebutton, toggle_sampletype, slider_hop,slider_lag):
    fig = CallbacksAFM.fig_AFM4(slider_Vg, slider_zins, slider_bandgap, slider_epsilonsem, slider_WFmet, slider_EAsem, slider_donor, slider_acceptor, slider_emass, slider_hmass, slider_T, slider_amplitude, slider_resfreq, slider_springconst, slider_tipradius, slider_Qfactor, calculatebutton, toggle_sampletype, slider_hop,slider_lag)
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
