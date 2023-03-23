#############################################################################
# INITIALIZE

import dash
from dash import dcc, html
import dash_bootstrap_components as dbc 
from dash.dependencies import Input, Output

from __main__ import *
import Controls_Bulk
import Controls_Surface
import Controls_AFM
import Callbacks_Bulk
import Callbacks_Surface
import Callbacks_AFM
import Presets

###### important for latex ######
import dash_defer_js_import as dji


app = dash.Dash(
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1"}
    ])


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
CarrierIntegrals_text = open("Text_CarrierIntegrals.md", "r").read()
BulkCarrierStatistics_text = open("Text_BulkCarrierStatistics.md", "r").read()
SurfaceCarrierStatistics_text = open("Text_SurfaceCarrierStatistics.md", "r").read()

axis_latex_script = dji.Import(src="https://cdn.jsdelivr.net/gh/yueyericardo/simuc@master/apps/dash/resources/redraw.js")
mathjax_script = dji.Import(src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.7/latest.js?config=TeX-AMS-MML_SVG")


################################################################################
################################################################################
# LAYOUT

app.layout = dbc.Container(
    [
        html.Hr(),
        html.Br(),
        html.Button('Electronic Structure', className='toggle-label', n_clicks=0, id='header_ElectronicStructure'), html.Br(),
        html.Div(dcc.Markdown(ElectronicStructure_text, dangerously_allow_html=True), hidden=True, id='display_ElectronicStructuretext'),

        html.Button('Distributions', className='toggle-label', n_clicks=0, id='header_Distributions'),
        html.Div([
            html.Br(),
            Controls_Bulk.Distributions,
            html.Div(dcc.Graph(id="DistributionsGraph"), className='graph', hidden=True, id='display_Distributionsgraph'),
            ], className='controlsgraph'), 
        html.Div(dcc.Markdown(Distributions_text, dangerously_allow_html=True), hidden=True, id='display_Distributionstext'),

        html.Button('Carrier Integrals', className='toggle-label', n_clicks=0, id='header_CarrierIntegrals'),
        html.Div([
            html.Br(),
            Controls_Bulk.CarrierIntegrals,
            html.Div(dcc.Graph(id="CarrierIntegralsGraph"), className='graph', hidden=True, id='display_CarrierIntegralsgraph'),
            ], className='controlsgraph'), 
        html.Div(dcc.Markdown(CarrierIntegrals_text, dangerously_allow_html=True), hidden=True, id='display_CarrierIntegralstext'),

        html.Button('Bulk Carrier Statistics', className='toggle-label', n_clicks=0, id='header_BulkCarrierStatistics'),
        html.Div([
            html.Br(),
            Controls_Bulk.Bulk_Card,
            html.Div(dcc.Graph(id="BulkGraph"), className='graph', hidden=True, id='display_BulkCarrierStatisticsgraph'),
            ], className='controlsgraph'), 
        html.Div(dcc.Markdown(BulkCarrierStatistics_text, dangerously_allow_html=True), hidden=True, id='display_BulkCarrierStatisticstext'),

        html.Button('Surface Carrier Statistics', className='toggle-label', n_clicks=1, id='header_SurfaceCarrierStatistics'),
        html.Div([
            html.Br(),
            Controls_Surface.Surface_Card, 
            html.Div(dcc.Graph(id="SurfaceGraph"), className='graph', hidden=True, id='display_SurfaceCarrierStatisticsgraph'),
            ], className='controlsgraph'), 
        html.Div(dcc.Markdown(SurfaceCarrierStatistics_text, dangerously_allow_html=True), hidden=True, id='display_SurfaceCarrierStatisticstext'),

        html.Button('fm-AFM Oscillations', className='toggle-label', n_clicks=0, id='header_fmAFMoscillations'),
        html.Div([
            html.Br(),
            Controls_AFM.AFM_Card1, 
            html.Div(dcc.Graph(id="AFMGraph1"), className='graph', hidden=True, id='display_fmAFMoscillationsgraph'),
            ], className='controlsgraph'), 

        html.Button('Bias Sweep Experiment', className='toggle-label', n_clicks=1, id='header_BiasSweepExperiment'), 
        html.Div([
            html.Br(),
            Controls_AFM.AFM_Card2, 
            html.Div(dcc.Graph(id="AFMGraph2"), className='graph', hidden=True, id='display_BiasSweepExperimentgraph'),
            ], className='controlsgraph'), 

        html.Button('Time Trace Experiment', className='toggle-label', n_clicks=0, id='header_TimeTraceExperiment'), html.Br(),
        html.Div([dbc.Col(Controls_AFM.AFM_Card3, md=3), dcc.Graph(id="AFMGraph3")], hidden=True, id='display_TimeTraceExperimentgraph'), 

        html.Button('Delay Sweep Experiment', className='toggle-label', n_clicks=0, id='header_DelaySweepExperiment'), html.Br(),
        html.Div([dbc.Col(Controls_AFM.AFM_Card4, md=3), dcc.Graph(id="AFMGraph4")], hidden=True, id='display_DelaySweepExperimentgraph'), 


    ###### important for latex ######
    axis_latex_script,
    mathjax_script,

    ],
    fluid=True,
)

################################################################################################################################################################
################################################################################################################################################################
# Display

# Show and hide Divs
# If n_clicks is even, it's hidden and if it's odd, it's shown
@app.callback(
    [Output('display_ElectronicStructuretext', 'hidden'),
     Output('display_Distributionstext', 'hidden'),
     Output('display_Distributionscontrols', 'hidden'),
     Output('display_Distributionsgraph', 'hidden'),
     Output('display_CarrierIntegralstext', 'hidden'),
     Output('display_CarrierIntegralscontrols', 'hidden'),
     Output('display_CarrierIntegralsgraph', 'hidden'),
     Output('display_BulkCarrierStatisticstext', 'hidden'),
     Output('display_BulkCarrierStatisticscontrols', 'hidden'),
     Output('display_BulkCarrierStatisticsgraph', 'hidden'),
     Output('display_SurfaceCarrierStatisticstext', 'hidden'),
     Output('display_SurfaceCarrierStatisticscontrols', 'hidden'),
     Output('display_SurfaceCarrierStatisticsgraph', 'hidden'),
     Output('display_fmAFMoscillationscontrols', 'hidden'),
     Output('display_fmAFMoscillationsgraph', 'hidden'),
     Output('display_BiasSweepExperimentcontrols', 'hidden'),
     Output('display_BiasSweepExperimentgraph', 'hidden')],
    [Input('header_ElectronicStructure', 'n_clicks'),
     Input('header_Distributions', 'n_clicks'),
     Input('header_CarrierIntegrals', 'n_clicks'),
     Input('header_BulkCarrierStatistics', 'n_clicks'),
     Input('header_SurfaceCarrierStatistics', 'n_clicks'),
     Input('header_fmAFMoscillations', 'n_clicks'),
     Input('header_BiasSweepExperiment', 'n_clicks')])
def update_display(click_electronicstructure,click_distributions,click_carrierintegrals,click_bulkcarrierstatistics,click_surfacecarrierstatistics,click_fmAFMoscillations,click_biassweepexperiment):
    hide_electronicstructure = True
    hide_distributions = True   
    hide_carrierintegrals = True   
    hide_bulkcarrierstatistics = True   
    hide_surfacecarrierstatistics = True   
    hide_fmAFMoscillations = True   
    hide_biassweepexperiment = True   
    if (click_electronicstructure % 2) != 0:
        hide_electronicstructure = False
    if (click_distributions % 2) != 0:
        hide_distributions = False
    if (click_carrierintegrals % 2) != 0:
        hide_carrierintegrals = False
    if (click_bulkcarrierstatistics % 2) != 0:
        hide_bulkcarrierstatistics = False
    if (click_surfacecarrierstatistics % 2) != 0:
        hide_surfacecarrierstatistics = False
    if (click_fmAFMoscillations % 2) != 0:
        hide_fmAFMoscillations = False
    if (click_biassweepexperiment% 2) != 0:
        hide_biassweepexperiment = False
    return hide_electronicstructure, hide_distributions,hide_distributions,hide_distributions, hide_carrierintegrals,hide_carrierintegrals,hide_carrierintegrals, hide_bulkcarrierstatistics,hide_bulkcarrierstatistics,hide_bulkcarrierstatistics, hide_surfacecarrierstatistics,hide_surfacecarrierstatistics,hide_surfacecarrierstatistics, hide_fmAFMoscillations,hide_fmAFMoscillations, hide_biassweepexperiment,hide_biassweepexperiment


################################################################################################################################################################
################################################################################################################################################################
# BULK

# probability distributions figure
@app.callback(
    Output('DistributionsGraph', 'figure'),
    [Input('DistributionsSlider_Ef', 'value'),
     Input('DistributionsSlider_T', 'value')])
def update_figure(slider_Ef, slider_T):
     fig = Callbacks_Bulk.fig_probabilitydistributions(slider_Ef, slider_T)
     return fig

# carrier integrals figure
@app.callback(
    Output('CarrierIntegralsGraph', 'figure'),
    [Input('CarrierIntegralsSlider_Ef', 'value'),
     Input('CarrierIntegralsSlider_T', 'value'),
     Input('CarrierIntegralsSlider_gc', 'value'),
     Input('CarrierIntegralsSlider_gv', 'value')])
def update_figure(slider_Ef, slider_T,slider_gc,slider_gv):
     fig = Callbacks_Bulk.fig_carrierintegrals(slider_Ef, slider_T,slider_gc,slider_gv)
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
    fig = Callbacks_Bulk.fig_carriers(slider_donor, slider_acceptor, slider_T, slider_emass, slider_hmass, toggle_type)
    return fig

# probability distributions readouts
@app.callback(
    [Output('DistributionsText_Ef', 'children'),
     Output('DistributionsText_T', 'children')],
    [Input('DistributionsSlider_Ef', 'value'),
     Input('DistributionsSlider_T', 'value')])
def update_output(slider_Ef, slider_T):
    readout_Ef, readout_T = Callbacks_Bulk.readouts_probabilitydistributions(slider_Ef, slider_T)
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
    readout_donor, readout_acceptor, readout_T, readout_emass, readout_hmass = Callbacks_Bulk.readouts_carriers(slider_donor, slider_acceptor, slider_T, slider_emass, slider_hmass)
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
    stylen, stylep, disabledn, disabledp, valuen, valuep,  = Callbacks_Bulk.togglefunctions(toggle)
    return stylen, stylep, disabledn, disabledp, valuen, valuep, 'n-type', 'p-type'



###############################################################################################################################################################
###############################################################################################################################################################
# SURFACE PHYSICS

# surface figure
@app.callback(
    [Output('SurfaceGraph', 'figure'),
     Output('SurfaceText_regime', 'children'),
     Output('SurfaceText_ni', 'children'),
     Output('SurfaceText_LD', 'children'),
     Output('SurfaceText_zQ', 'children')],
    [Input('SurfaceSlider_Vg', 'value'),
     Input('SurfaceSlider_zins', 'value'),
     Input('SurfaceSlider_Eg', 'value'),
     Input('SurfaceSlider_epsilonsem', 'value'),
     Input('SurfaceSlider_WFmet', 'value'),
     Input('SurfaceSlider_EAsem', 'value'),
     Input('SurfaceSlider_donor', 'value'),
     Input('SurfaceSlider_acceptor', 'value'),
     Input('SurfaceSlider_emass', 'value'),
     Input('SurfaceSlider_hmass', 'value'),
     Input('SurfaceSlider_T', 'value'),
     Input('SurfaceSlider_alpha', 'value'),
     Input('SurfaceSlider_biassteps', 'value'),
     Input('SurfaceSlider_zinssteps', 'value')])
def update_figure(slider_Vg, slider_zins, slider_Eg, slider_epsilonsem, slider_WFmet, slider_EAsem, slider_donor, slider_acceptor, slider_emass, slider_hmass, slider_T, slider_alpha, slider_biassteps, slider_zinssteps):
    fig0, regime, ni, LD, zQ = Callbacks_Surface.fig0_surface(slider_Vg, slider_zins, slider_Eg, slider_epsilonsem, slider_WFmet, slider_EAsem, slider_donor, slider_acceptor, slider_emass, slider_hmass, slider_T, slider_alpha, slider_biassteps, slider_zinssteps)
    return fig0, regime, ni, LD, zQ

# surface readouts
@app.callback(
    [Output('SurfaceText_Vg', 'children'),
     Output('SurfaceText_zins', 'children'),
     Output('SurfaceText_Eg', 'children'),
     Output('SurfaceText_epsilonsem', 'children'),
     Output('SurfaceText_WFmet', 'children'),
     Output('SurfaceText_EAsem', 'children'),
     Output('SurfaceText_donor', 'children'),
     Output('SurfaceText_acceptor', 'children'),
     Output('SurfaceText_emass', 'children'),
     Output('SurfaceText_hmass', 'children'),
     Output('SurfaceText_T', 'children'),
     Output('SurfaceText_alpha', 'children'),
     Output('SurfaceText_biassteps', 'children'),
     Output('SurfaceText_zinssteps', 'children')],
    [Input('SurfaceSlider_Vg', 'value'),
     Input('SurfaceSlider_zins', 'value'),
     Input('SurfaceSlider_Eg', 'value'),
     Input('SurfaceSlider_epsilonsem', 'value'),
     Input('SurfaceSlider_WFmet', 'value'),
     Input('SurfaceSlider_EAsem', 'value'),
     Input('SurfaceSlider_donor', 'value'),
     Input('SurfaceSlider_acceptor', 'value'),
     Input('SurfaceSlider_emass', 'value'),
     Input('SurfaceSlider_hmass', 'value'),
     Input('SurfaceSlider_T', 'value'),
     Input('SurfaceSlider_alpha', 'value'),
     Input('SurfaceSlider_biassteps', 'value'),
     Input('SurfaceSlider_zinssteps', 'value')])
def update_output(slider_Vg, slider_zins, slider_Eg, slider_epsilonsem, slider_WFmet, slider_EAsem, slider_donor, slider_acceptor, slider_emass, slider_hmass, slider_T, slider_alpha, slider_biassteps, slider_zinssteps):
    readout_Vg, readout_zins, readout_Eg, readout_epsilonsem, readout_WFmet, readout_EAsem, readout_donor, readout_acceptor, readout_emass, readout_hmass, readout_T, readout_alpha, readout_biassteps, readout_zinssteps = Callbacks_Surface.readouts_surface(slider_Vg, slider_zins, slider_Eg, slider_epsilonsem, slider_WFmet, slider_EAsem, slider_donor, slider_acceptor, slider_emass, slider_hmass, slider_T, slider_alpha, slider_biassteps, slider_zinssteps)
    return readout_Vg, readout_zins, readout_Eg, readout_epsilonsem, readout_WFmet, readout_EAsem, readout_donor, readout_acceptor, readout_emass, readout_hmass, readout_T, readout_alpha, readout_biassteps, readout_zinssteps


# surface presets
@app.callback(
    [Output('SurfaceToggle_type', 'value'),
     Output('SurfaceSlider_Vg', 'value'),
     Output('SurfaceSlider_zins', 'value'),
     Output('SurfaceSlider_Eg', 'value'),
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
     Input('SurfaceSlider_Eg', 'value'),
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
def presets(button_presets,slider_Vg, slider_zins, slider_Eg, slider_epsilonsem, slider_WFmet, slider_EAsem, slider_donor, slider_acceptor, slider_emass, slider_hmass, slider_T, slider_alpha, toggle_type):

    button_presets_og = button_presets

    # Somehow writing this as an or statement doesn't work, so for now it looks like this.
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if 'SurfaceToggle_type' in changed_id:
        button_presets = 0
    elif 'SurfaceSlider_Vg' in changed_id:
        button_presets = 0
    elif 'SurfaceSlider_zins' in changed_id:
        button_presets = 0
    elif 'SurfaceSlider_Eg' in changed_id:
        button_presets = 0
    elif 'SurfaceSlider_epsilonsem' in changed_id:
        button_presets = 0
    elif 'SurfaceSlider_WFmet' in changed_id:
        button_presets = 0
    elif 'SurfaceSlider_EAsem' in changed_id:
        button_presets = 0
    elif 'SurfaceSlider_donor' in changed_id:
        button_presets = 0
    elif 'SurfaceSlider_acceptor' in changed_id:
        button_presets = 0
    elif 'SurfaceSlider_emass' in changed_id:
        button_presets = 0
    elif 'SurfaceSlider_hmass' in changed_id:
        button_presets = 0
    elif 'SurfaceSlider_T' in changed_id:
        button_presets = 0
    elif 'SurfaceSlider_alpha' in changed_id:
        button_presets = 0
    else:
        button_presets = button_presets_og

    toggle_type, slider_Vg, slider_zins, slider_Eg, slider_epsilonsem, slider_WFmet, slider_EAsem, slider_donor, slider_acceptor, slider_emass, slider_hmass, slider_T, slider_alpha, button_presets, stylen, stylep, disabledn, disabledp = Presets.presets_surface(button_presets, toggle_type, slider_Vg, slider_zins, slider_Eg, slider_epsilonsem, slider_WFmet, slider_EAsem, slider_donor, slider_acceptor, slider_emass, slider_hmass, slider_T, slider_alpha)

    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if 'SurfaceSlider_Vg' in changed_id:
        button_presets = button_presets_og
    elif 'SurfaceSlider_zins' in changed_id:
        button_presets = button_presets_og
    elif 'SurfaceSlider_T' in changed_id:
        button_presets = button_presets_og
    else:
        button_presets = button_presets

    return toggle_type, slider_Vg, slider_zins, slider_Eg, slider_epsilonsem, slider_WFmet, slider_EAsem, slider_donor, slider_acceptor, slider_emass, slider_hmass, slider_T, slider_alpha, button_presets, stylen, stylep, disabledn, disabledp, 'n-type', 'p-type'



################################################################################################################################################################
################################################################################################################################################################
# AFM

# ncAFM oscillations figure
@app.callback(
    Output('AFMGraph1', 'figure'),
    [Input('SurfaceSlider_Vg', 'value'),
     Input('SurfaceSlider_zins', 'value'),
     Input('SurfaceSlider_Eg', 'value'),
     Input('SurfaceSlider_epsilonsem', 'value'),
     Input('SurfaceSlider_WFmet', 'value'),
     Input('SurfaceSlider_EAsem', 'value'),
     Input('SurfaceSlider_donor', 'value'),
     Input('SurfaceSlider_acceptor', 'value'),
     Input('SurfaceSlider_emass', 'value'),
     Input('SurfaceSlider_hmass', 'value'),
     Input('SurfaceSlider_T', 'value'),
     Input('SurfaceSlider_alpha', 'value'),
     Input('SurfaceSlider_biassteps', 'value'),
     Input('SurfaceSlider_zinssteps', 'value'),
     Input('AFMSlider_timesteps', 'value'),
     Input('AFMSlider_amplitude', 'value'),
     Input('AFMSlider_resfreq', 'value'),
     Input('AFMSlider_lag', 'value'),
     Input('AFMbutton_Calculate', 'n_clicks')])
def update_figure(slider_Vg, slider_zins, slider_Eg, slider_epsilonsem, slider_WFmet, slider_EAsem, slider_donor, slider_acceptor, slider_emass, slider_hmass, slider_T, slider_alpha, slider_biassteps,slider_zinssteps, slider_timesteps, slider_amplitude, slider_resfreq, slider_lag, calculatebutton):
    fig1 = Callbacks_AFM.fig1_AFM(slider_Vg, slider_zins, slider_Eg, slider_epsilonsem, slider_WFmet, slider_EAsem, slider_donor, slider_acceptor, slider_emass, slider_hmass, slider_T, slider_alpha, slider_biassteps,slider_zinssteps, slider_timesteps, slider_amplitude, slider_resfreq, slider_lag, calculatebutton)
    return fig1

# Bias experiment figure
@app.callback(
    Output('AFMGraph2', 'figure'),
    [Input('SurfaceSlider_Vg', 'value'),
     Input('SurfaceSlider_zins', 'value'),
     Input('SurfaceSlider_Eg', 'value'),
     Input('SurfaceSlider_epsilonsem', 'value'),
     Input('SurfaceSlider_WFmet', 'value'),
     Input('SurfaceSlider_EAsem', 'value'),
     Input('SurfaceSlider_donor', 'value'),
     Input('SurfaceSlider_acceptor', 'value'),
     Input('SurfaceSlider_emass', 'value'),
     Input('SurfaceSlider_hmass', 'value'),
     Input('SurfaceSlider_T', 'value'),
     Input('SurfaceSlider_alpha', 'value'),
     Input('SurfaceSlider_biassteps', 'value'),
     Input('SurfaceSlider_zinssteps', 'value'),
     Input('AFMSlider_timesteps', 'value'),
     Input('AFMSlider_amplitude', 'value'),
     Input('AFMSlider_resfreq', 'value'),
     Input('AFMSlider_springconst', 'value'),
     Input('AFMSlider_tipradius', 'value'),
     Input('AFMSlider_cantheight', 'value'),
     Input('AFMSlider_cantarea', 'value'),
     Input('AFMSlider_Qfactor', 'value'),
     Input('AFMbutton_CalculateBiasExp', 'n_clicks'),
     Input('AFMSlider_lag', 'value')])
def update_figure(slider_Vg, slider_zins, slider_Eg, slider_epsilonsem, slider_WFmet, slider_EAsem, slider_donor, slider_acceptor, slider_emass, slider_hmass, slider_T,slider_alpha,slider_biassteps,slider_zinssteps, slider_timesteps,slider_amplitude, slider_resfreq, slider_springconst, slider_tipradius, slider_cantheight, slider_cantarea, slider_Qfactor, calculatebutton, slider_lag):
    fig2 = Callbacks_AFM.fig2_AFM(slider_Vg, slider_zins, slider_Eg, slider_epsilonsem, slider_WFmet, slider_EAsem, slider_donor, slider_acceptor, slider_emass, slider_hmass, slider_T,slider_alpha,slider_biassteps,slider_zinssteps, slider_timesteps,slider_amplitude, slider_resfreq, slider_springconst, slider_tipradius, slider_cantheight, slider_cantarea, slider_Qfactor, calculatebutton, slider_lag)
    return fig2


# afm presets
@app.callback(
    [Output('AFMSlider_timesteps', 'value'),
     Output('AFMSlider_amplitude', 'value'),
     Output('AFMSlider_resfreq', 'value'),
     Output('AFMSlider_lag', 'value'),
     Output('AFMSlider_springconst', 'value'),
     Output('AFMSlider_tipradius', 'value'),
     Output('AFMSlider_cantheight', 'value'),
     Output('AFMSlider_cantarea', 'value'),
     Output('AFMSlider_Qfactor', 'value')],
     [Input('AFMButtons_presets', 'value'),
     Input('AFMSlider_timesteps', 'value'),
     Input('AFMSlider_amplitude', 'value'),
     Input('AFMSlider_resfreq', 'value'),
     Input('AFMSlider_lag', 'value'),
     Input('AFMSlider_springconst', 'value'),
     Input('AFMSlider_tipradius', 'value'),
     Input('AFMSlider_cantheight', 'value'),
     Input('AFMSlider_cantarea', 'value'),
     Input('AFMSlider_Qfactor', 'value')])
def presets(button_presets,slider_timesteps, slider_amplitude, slider_resfreq, slider_lag, slider_springconst, slider_tipradius, slider_cantheight, slider_cantarea, slider_Qfactor):

    button_presets_og = button_presets

    # Somehow writing this as an or statement doesn't work, so for now it looks like this.
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if 'SurfaceToggle_type' in changed_id:
        button_presets = 0
    elif 'AFMSlider_timesteps' in changed_id:
        button_presets = 0
    elif 'AFMSlider_amplitude' in changed_id:
        button_presets = 0
    elif 'AFMSlider_resfreq' in changed_id:
        button_presets = 0
    elif 'AFMSlider_lag' in changed_id:
        button_presets = 0
    elif 'AFMSlider_springconst' in changed_id:
        button_presets = 0
    elif 'AFMSlider_tipradius' in changed_id:
        button_presets = 0
    elif 'AFMSlider_cantheight' in changed_id:
        button_presets = 0
    elif 'AFMSlider_cantarea' in changed_id:
        button_presets = 0
    elif 'AFMSlider_Qfactor' in changed_id:
        button_presets = 0
    else:
        button_presets = button_presets_og

    slider_timesteps, slider_amplitude, slider_resfreq, slider_lag, slider_springconst, slider_tipradius, slider_cantheight, slider_cantarea, slider_Qfactor = Presets.presets_afm(button_presets, slider_timesteps, slider_amplitude, slider_resfreq, slider_lag, slider_springconst, slider_tipradius, slider_cantheight, slider_cantarea, slider_Qfactor)

    return slider_timesteps, slider_amplitude, slider_resfreq, slider_lag, slider_springconst, slider_tipradius, slider_cantheight, slider_cantarea, slider_Qfactor


























'''
# Time trace experiment figure
@app.callback(
    Output('AFMGraph3', 'figure'),
    [Input('AFMbutton_CalculateTimeExp', 'n_clicks'),
     Input('AFMSlider_sigma', 'value'),
     Input('AFMSlider_RTS1mag', 'value'),
     Input('AFMSlider_RTS1per', 'value'),
     Input('AFMSlider_RTS2mag', 'value'),
     Input('AFMSlider_RTS2per', 'value'),
     Input('AFMSlider_RTS3mag', 'value'),
     Input('AFMSlider_RTS3per', 'value'),
     Input('AFMSlider_RTS4mag', 'value'),
     Input('AFMSlider_RTS4per', 'value'),
     Input('AFMSlider_RTS5mag', 'value'),
     Input('AFMSlider_RTS5per', 'value'),
     Input('AFMSlider_f0y', 'value'),
     Input('AFMSlider_f1y', 'value'),
     Input('AFMSlider_f2y', 'value'),])
def update_figure(calculatebutton, slider_sigma,slider_RTS1mag,slider_RTS1per,slider_RTS2mag,slider_RTS2per,slider_RTS3mag,slider_RTS3per,slider_RTS4mag,slider_RTS4per,slider_RTS5mag,slider_RTS5per,slider_f0y,slider_f1y,slider_f2y):
    fig3 = Callbacks_AFM.fig3_AFM(calculatebutton, slider_sigma,slider_RTS1mag,slider_RTS1per,slider_RTS2mag,slider_RTS2per,slider_RTS3mag,slider_RTS3per,slider_RTS4mag,slider_RTS4per,slider_RTS5mag,slider_RTS5per,slider_f0y,slider_f1y,slider_f2y)
    return fig3

# Delay experiment figure
@app.callback(
    Output('AFMGraph4', 'figure'),
    [Input('SurfaceSlider_Vg', 'value'),
     Input('SurfaceSlider_zins', 'value'),
     Input('SurfaceSlider_Eg', 'value'),
     Input('SurfaceSlider_epsilonsem', 'value'),
     Input('SurfaceSlider_WFmet', 'value'),
     Input('SurfaceSlider_EAsem', 'value'),
     Input('SurfaceSlider_donor', 'value'),
     Input('SurfaceSlider_acceptor', 'value'),
     Input('SurfaceSlider_emass', 'value'),
     Input('SurfaceSlider_hmass', 'value'),
     Input('SurfaceSlider_T', 'value'),
     Input('SurfaceSlider_alpha', 'value'),
     Input('AFMSlider_timesteps', 'value'),
     Input('AFMSlider_amplitude', 'value'),
     Input('AFMSlider_resfreq', 'value'),
     Input('AFMSlider_springconst', 'value'),
     Input('AFMSlider_tipradius', 'value'),
     Input('AFMSlider_Qfactor', 'value'),
     Input('AFMbutton_CalculateDelayExp', 'n_clicks'),
     Input('AFMtoggle_sampletype', 'value'),
     Input('AFMSlider_hop', 'value'),
     Input('AFMSlider_lag', 'value'),
     Input('AFMSlider_pulsetimesteps', 'value'),
     Input('AFMSlider_delaysteps', 'value')])
def update_figure(slider_Vg, slider_zins, slider_Eg, slider_epsilonsem, slider_WFmet, slider_EAsem, slider_donor, slider_acceptor, slider_emass, slider_hmass, slider_T,slider_alpha, slider_timesteps, slider_amplitude, slider_resfreq, slider_springconst, slider_tipradius, slider_Qfactor, calculatebutton, toggle_sampletype, slider_hop,slider_lag,slider_pulsetimesteps,slider_delaysteps):
    fig4 = Callbacks_AFM.fig4_AFM(slider_Vg, slider_zins, slider_Eg, slider_epsilonsem, slider_WFmet, slider_EAsem, slider_donor, slider_acceptor, slider_emass, slider_hmass, slider_T,slider_alpha, slider_timesteps, slider_amplitude, slider_resfreq, slider_springconst, slider_tipradius, slider_Qfactor, calculatebutton, toggle_sampletype, slider_hop,slider_lag,slider_pulsetimesteps,slider_delaysteps)
    return fig4
'''
# AFM readouts
@app.callback(
    [Output('AFMText_timesteps', 'children'),
     Output('AFMText_amplitude', 'children'),
     Output('AFMText_lag', 'children'),
     Output('AFMText_resfreq', 'children'),
     Output('AFMText_springconst', 'children'),
     Output('AFMText_Qfactor', 'children'),
     Output('AFMText_tipradius', 'children'),
     Output('AFMText_cantheight', 'children'),
     Output('AFMText_cantarea', 'children'),
     Output('AFMText_delaysteps', 'children'),
     Output('AFMText_pulsetimesteps', 'children')],
    [Input('AFMSlider_timesteps', 'value'),
     Input('AFMSlider_amplitude', 'value'),
     Input('AFMSlider_lag', 'value'),
     Input('AFMSlider_resfreq', 'value'),
     Input('AFMSlider_springconst', 'value'),
     Input('AFMSlider_Qfactor', 'value'),
     Input('AFMSlider_tipradius', 'value'),
     Input('AFMSlider_cantheight', 'value'),
     Input('AFMSlider_cantarea', 'value'),
     Input('AFMSlider_pulsetimesteps', 'value'),
     Input('AFMSlider_delaysteps', 'value')])
def update_output(slider_timesteps,slider_amplitude, slider_lag, slider_resfreq, slider_springconst, slider_Qfactor, slider_tipradius, slider_cantheight, slider_cantarea, slider_delaysteps, slider_pulsetimesteps):
    readout_timesteps, readout_amplitude, readout_lag, readout_resfreq, readout_springconst, readout_Qfactor, readout_tipradius, readout_cantheight, readout_cantarea, readout_pulsetimesteps, readout_delaysteps = Callbacks_AFM.readouts_AFM(slider_timesteps, slider_amplitude, slider_lag, slider_resfreq, slider_springconst, slider_Qfactor, slider_tipradius, slider_cantheight, slider_cantarea, slider_pulsetimesteps, slider_delaysteps)
    return readout_timesteps, readout_amplitude, readout_lag, readout_resfreq, readout_springconst, readout_Qfactor, readout_tipradius, readout_cantheight, readout_cantarea, readout_pulsetimesteps, readout_delaysteps


################################################################################################################################################################
################################################################################################################################################################
# RUN ON SERVER

if __name__ == '__main__':
    app.run_server(debug=True)
