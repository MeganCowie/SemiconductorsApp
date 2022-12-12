from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
import dash_daq as daq

################################################################################
################################################################################

# Distributions controls
Distributions = html.Div([
    html.Div([
        html.Div([
            html.Div("Fermi Energy (eV)", className='label_name', id="DistributionText_Eflabel"),
            html.Div(id='DistributionsText_Ef', className='label_value'),
        ], className='label_container'),
        dcc.Slider(id='DistributionsSlider_Ef', className='slider', marks=None, min=0, max=1, step=0.00001, value=0.5),
        
        html.Div([
            html.Div("Temperature (K)", className='label_name', id="DistributionText_Tlabel"),
            html.Div(id='DistributionsText_T', className='label_value'),
        ], className='label_container'),
        dcc.Slider(id='DistributionsSlider_T', className='slider', marks=None, min=0, max=1000, step=1, value=300),
    ], className= 'controls_container'),
], className='controls', hidden=True, id='display_Distributionscontrols')

# CarrierIntegrals controls
CarrierIntegrals = html.Div([
    html.Div([
        html.Div([
            html.Div("Fermi Energy (eV)", className='label_name', id="CarrierIntegralsText_Eflabel"),
            html.Div(id='CarrierIntegralsText_Ef', className='label_value'),
        ], className='label_container'),
        dcc.Slider(id='CarrierIntegralsSlider_Ef', className='slider', marks=None, min=0, max=1, step=0.00001, value=0.5),

        html.Div([
            html.Div("Temperature (K)", className='label_name', id="CarrierIntegralsText_Tlabel"),
            html.Div(id='CarrierIntegralsText_T', className='label_value'),
        ], className='label_container'),
        dcc.Slider(id='CarrierIntegralsSlider_T', className='slider', marks=None, min=0, max=1000, step=1, value=300),

        html.Div([
            html.Div("DOS: Conduction Band", className='label_name', id="CarrierIntegralsText_gclabel"),
            html.Div(id='CarrierIntegralsText_gc', className='label_value'),
        ], className='label_container'),
        dcc.Slider(id='CarrierIntegralsSlider_gc', className='slider', marks=None, min=0, max=5, step=0.1, value=2),

        html.Div([
            html.Div("DOS: Valence Band", className='label_name', id="CarrierIntegralsText_gvlabel"),
            html.Div(id='CarrierIntegralsText_gv', className='label_value'),
        ], className='label_container'),
        dcc.Slider(id='CarrierIntegralsSlider_gv', className='slider', marks=None, min=0, max=5, step=0.1, value=2),
    ], className= 'controls_container'),
], className='controls', hidden=True, id='display_CarrierIntegralscontrols')


# Carrier controls
Bulk_Card = html.Div([
    html.Div([
        html.Div([
            html.Div(id='BulkText_typen',className='toggle-left'),
            daq.ToggleSwitch(id='BulkToggle_type',className='toggle-switch', value=True),
            html.Div(id='BulkText_typep', className='toggle-right'),
        ], className='toggle_container'),

        html.Div([
            html.Div("Donors (cm-3)", className='label_name', id="BulkText_donorlabel"),
            html.Div(id='BulkText_donor', className='label_value'),
        ], className='label_container'),
        dcc.Slider(id='BulkSlider_donor', className='slider', marks=None, min=25, max=35, step=0.1, value=0, disabled=True),

        html.Div([
            html.Div("Acceptors (cm-3)", className='label_name', id="BulkText_acceptorlabel"),
            html.Div(id='BulkText_acceptor', className='label_value'),
        ], className='label_container'),
        dcc.Slider(id='BulkSlider_acceptor', className='slider', marks=None, min=25, max=35, step=0.1, value=0),

        html.Div([
            html.Div("Elec. Eff. Mass (me)", className='label_name', id="BulkText_emasslabel"),
            html.Div(id='BulkText_emass', className='label_value'),
        ], className='label_container'),
        dcc.Slider(id='BulkSlider_emass', className='slider', marks=None, min=0.1, max=2, step=0.1, value=1.0),

        html.Div([
            html.Div("Hole Eff. Mass (me)", className='label_name', id="BulkText_hmasslabel"),
            html.Div(id='BulkText_hmass', className='label_value'),
        ], className='label_container'),
        dcc.Slider(id='BulkSlider_hmass', className='slider', marks=None, min=0.1, max=2, step=0.1, value=1.0),

        html.Div([
            html.Div("Temperature (K)", className='label_name', id="BulkText_Tlabel"),
            html.Div(id='BulkText_T', className='label_value'),
        ], className='label_container'),
        dcc.Slider(id='BulkSlider_T', className='slider', marks=None, min=100, max=1000, step=1, value=300),
    ], className= 'controls_container'),
], className='controls', hidden=True, id='display_BulkCarrierStatisticscontrols')
