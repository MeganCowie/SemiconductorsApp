from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
import dash_daq as daq

################################################################################
################################################################################

# Distributions controls
Distributions = dbc.Card([
        dbc.Row([
            dbc.Col(dbc.Label("Fermi Energy (eV)", id="DistributionText_Eflabel"), md=8),
            dbc.Col(html.Div(id='DistributionsText_Ef', style = {'text-align': 'right'}), md=4),
        ], justify="between"),
        dbc.Row([
            dbc.Col(dcc.Slider(id='DistributionsSlider_Ef', marks=None, min=0, max=1, step=0.00001, value=0.5,), md=12),
        ]),
        dbc.Row([
            dbc.Col(dbc.Label("Temperature (K)", id="DistributionText_Tlabel"), md=8),
            dbc.Col(html.Div(id='DistributionsText_T', style = {'text-align': 'right'}), md=4),
        ], justify="between"),
        dbc.Row([
            dbc.Col(dcc.Slider(id='DistributionsSlider_T', marks=None, min=0, max=1000, step=1, value=300,), style={"margin-bottom":"-20px"}, md=12),
        ]),
], body=True,)

# CarrierIntegrals controls
CarrierIntegrals = dbc.Card([
        dbc.Row([
            dbc.Col(dbc.Label("Fermi Energy (eV)", id="CarrierIntegralsText_Eflabel"), md=8),
            dbc.Col(html.Div(id='CarrierIntegralsText_Ef', style = {'text-align': 'right'}), md=4),
        ], justify="between"),
        dbc.Row([
            dbc.Col(dcc.Slider(id='CarrierIntegralsSlider_Ef', marks=None, min=0, max=1, step=0.00001, value=0.5,), md=12),
        ]),
        dbc.Row([
            dbc.Col(dbc.Label("Temperature (K)", id="CarrierIntegralsText_Tlabel"), md=8),
            dbc.Col(html.Div(id='CarrierIntegralsText_T', style = {'text-align': 'right'}), md=4),
        ], justify="between"),
        dbc.Row([
            dbc.Col(dcc.Slider(id='CarrierIntegralsSlider_T', marks=None, min=0, max=1000, step=1, value=300,), md=12),
        ]),
        dbc.Row([
            dbc.Col(dbc.Label("Density of States: Conduction Band", id="CarrierIntegralsText_gclabel"), md=8),
            dbc.Col(html.Div(id='CarrierIntegralsText_gc', style = {'text-align': 'right'}), md=4),
        ], justify="between"),
        dbc.Row([
            dbc.Col(dcc.Slider(id='CarrierIntegralsSlider_gc', marks=None, min=0, max=5, step=0.1, value=2,), md=12),
        ]),
        dbc.Row([
            dbc.Col(dbc.Label("Density of States: Valence Band", id="CarrierIntegralsText_gvlabel"), md=8),
            dbc.Col(html.Div(id='CarrierIntegralsText_gv', style = {'text-align': 'right'}), md=4),
        ], justify="between"),
        dbc.Row([
            dbc.Col(dcc.Slider(id='CarrierIntegralsSlider_gv', marks=None, min=0, max=5, step=0.1, value=2,), style={"margin-bottom":"-20px"}, md=12),
        ]),
], body=True,)


# Carrier controls
Bulk_Card = dbc.Card([
    dbc.Row([
        dbc.Row([
            dbc.Col(dbc.Row(html.Div(id='BulkText_typen'),justify="center"),  md=4),
            dbc.Col(dbc.Row(daq.ToggleSwitch(id='BulkToggle_type', size=50, value=True, style={'width':'100%'},), justify="center"), md=4),
            dbc.Col(dbc.Row(html.Div(id='BulkText_typep'),justify="center"), md=4),
        ],justify="evenly"),
    ], style={"margin-top":"30px","margin-bottom":"10px","margin-left":"10px","margin-right":"10px"}),

    dbc.Row([
    dbc.Row([
        dbc.Col(dbc.Label("Donors (cm-3)", id="BulkText_donorlabel", style = {'text-align': 'right', "margin-left": "10px","margin-top": "20px"}), md=8),
        dbc.Col(html.Div(id='BulkText_donor',style={'text-align': 'right', "margin-left": "-10px", "margin-right": "10px","margin-top": "20px"}), md=4),
    ], justify="between"),
    dbc.Row([
        dbc.Col(dcc.Slider(id='BulkSlider_donor', marks=None, min=17, max=20, step=0.1, value=0, disabled=True)),
    ]),
    dbc.Row([
        dbc.Col(dbc.Label("Acceptors (cm-3)", id="BulkText_acceptorlabel", style = {'text-align': 'right', "margin-left": "10px"}), md=8),
        dbc.Col(html.Div(id='BulkText_acceptor',style={'text-align': 'right', "margin-left": "-10px", "margin-right": "10px"}), md=4),
    ], justify="between"),
    dbc.Row([
        dbc.Col(dcc.Slider(id='BulkSlider_acceptor', marks=None, min=17, max=20, step=0.1, value=0)),
    ]),
    dbc.Row([
        dbc.Col([
                dbc.Row([
                    dbc.Col(dbc.Label("Elec. Eff. Mass (me)", id="BulkText_emasslabel", style={'fontSize': 10, "margin-left": "10px", "margin-right": "-10px"}), md=8),
                    dbc.Col(html.Div(id='BulkText_emass',style={'fontSize': 10, 'text-align': 'right'}), md=4),
                ], justify="between"),
                dbc.Row([
                    dbc.Col(dcc.Slider(id='BulkSlider_emass', marks=None, min=0.1, max=2, step=0.1, value=1.0,)),
                ]),
        ], md=6),
        dbc.Col([
                dbc.Row([
                    dbc.Col(dbc.Label("Hole Eff. Mass (me)", id="BulkText_hmasslabel", style={'fontSize': 10}), md=8),
                    dbc.Col(html.Div(id='BulkText_hmass',style={'fontSize': 12, 'text-align': 'right', "margin-right": "10px"}), md=4),
                ], justify="between"),
                dbc.Row([
                    dbc.Col(dcc.Slider(id='BulkSlider_hmass', marks=None, min=0.1, max=2, step=0.1, value=1.0,), md=12),
                ]),
        ], md=6)
    ], style={"margin-bottom":"-20px"},),
    dbc.Row([
        dbc.Col(dbc.Label("Temperature (K)", id="BulkText_Tlabel", style = {'text-align': 'right', "margin-left": "10px"}), md=8),
        dbc.Col(html.Div(id='BulkText_T', style = {'text-align': 'right', "margin-right": "10px"}), md=4),
    ], justify="between"),
    dbc.Row([
        dbc.Col(dcc.Slider(id='BulkSlider_T', marks=None, min=100, max=1000, step=1, value=300,), style={"margin-bottom":"-10px"}, md=12),
    ]),
    ]),
]),
