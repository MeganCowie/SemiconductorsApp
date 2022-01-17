import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_daq as daq

################################################################################
################################################################################

# Distributions controls
Distributions = dbc.Card([
    dbc.FormGroup([
        dbc.Row([
            dbc.Col(dbc.Label("Fermi Energy (eV)", id="DistributionText_Eflabel"), md=8),
            dbc.Col(html.Div(id='DistributionsText_Ef', style = {'text-align': 'right'}), md=4),
        ], justify="between"),
        dbc.Row([
            dbc.Col(dcc.Slider(id='DistributionsSlider_Ef', min=0, max=1, step=0.00001, value=0.5,), md=12),
        ]),
    ]),
    dbc.FormGroup([
        dbc.Row([
            dbc.Col(dbc.Label("Temperature (K)", id="DistributionText_Tlabel"), md=8),
            dbc.Col(html.Div(id='DistributionsText_T', style = {'text-align': 'right'}), md=4),
        ], justify="between"),
        dbc.Row([
            dbc.Col(dcc.Slider(id='DistributionsSlider_T', min=0, max=1000, step=1, value=300,), md=12),
        ]),
    ]),
], body=True,)

# CarrierIntegrals controls
CarrierIntegrals = dbc.Card([
    dbc.FormGroup([
        dbc.Row([
            dbc.Col(dbc.Label("Fermi Energy (eV)", id="CarrierIntegralsText_Eflabel"), md=8),
            dbc.Col(html.Div(id='CarrierIntegralsText_Ef', style = {'text-align': 'right'}), md=4),
        ], justify="between"),
        dbc.Row([
            dbc.Col(dcc.Slider(id='CarrierIntegralsSlider_Ef', min=0, max=1, step=0.00001, value=0.5,), md=12),
        ]),
    ]),
    dbc.FormGroup([
        dbc.Row([
            dbc.Col(dbc.Label("Temperature (K)", id="CarrierIntegralsText_Tlabel"), md=8),
            dbc.Col(html.Div(id='CarrierIntegralsText_T', style = {'text-align': 'right'}), md=4),
        ], justify="between"),
        dbc.Row([
            dbc.Col(dcc.Slider(id='CarrierIntegralsSlider_T', min=0, max=1000, step=1, value=300,), md=12),
        ]),
    ]),
], body=True,)


# Carrier controls
Bulk_Card1 = dbc.Card([
    dbc.Row([
        dbc.Col(html.Div(id='BulkText_typen'),  md=3),
        dbc.Col(daq.ToggleSwitch(id='BulkToggle_type', value=False), md=6),
        dbc.Col(html.Div(id='BulkText_typep'),  md=3),
    ]),
],body=True),

Bulk_Card2 = dbc.Card([
    dbc.FormGroup([
        dbc.Row([
            dbc.Col(dbc.Label("Ionized Donors (cm^-3)", id="BulkText_donorlabel"), md=8),
            dbc.Col(html.Div(id='BulkText_donor', style = {'text-align': 'right'}), md=4),
        ], justify="between"),
        dbc.Row([
            dbc.Col(dcc.Slider(id='BulkSlider_donor', min=0, max=19, step=1, value=0,), md=12),
        ]),
        ]),
    dbc.FormGroup([
        dbc.Row([
            dbc.Col(dbc.Label("Ionized Acceptors (cm^-3)", id="BulkText_acceptorlabel"), md=8),
            dbc.Col(html.Div(id='BulkText_acceptor', style = {'text-align': 'right'}), md=4),
        ], justify="between"),
        dbc.Row([
            dbc.Col(dcc.Slider(id='BulkSlider_acceptor',  min=0, max=19, step=1, value=0,), md=12),
        ]),
    ]),
    dbc.FormGroup([
        dbc.Row([
            dbc.Col(dbc.Label("Temperature (K)", id="BulkText_Tlabel"), md=8),
            dbc.Col(html.Div(id='BulkText_T', style = {'text-align': 'right'}), md=4),
        ], justify="between"),
        dbc.Row([
            dbc.Col(dcc.Slider(id='BulkSlider_T', min=1, max=1000, step=1, value=300,), md=12),
        ]),
    ]),
],body=True)

Bulk_Card3 = dbc.Card([
dbc.Row([
    dbc.Col([
        dbc.FormGroup([
            dbc.Row([
                dbc.Col(dbc.Label("Electron Effective Mass", id="BulkText_emasslabel", style={'fontSize': 12}), md=9),
                dbc.Col(html.Div(id='BulkText_emass',style={'fontSize': 12}), md=3),
            ], justify="between"),
            dbc.Row([
                dbc.Col(dcc.Slider(id='BulkSlider_emass', min=0.1, max=1, step=0.1, value=0.2,)),
            ]),
        ]),
    ], md=6),
    dbc.Col([
        dbc.FormGroup([
            dbc.Row([
                dbc.Col(dbc.Label("Hole Effective Mass", id="BulkText_hmasslabel", style={'fontSize': 12}), md=9),
                dbc.Col(html.Div(id='BulkText_hmass',style={'fontSize': 12}), md=3),
            ], justify="between"),
            dbc.Row([
                dbc.Col(dcc.Slider(id='BulkSlider_hmass', min=0.1, max=1, step=0.1, value=0.5,)),
            ]),
        ]),
    ], md=6)
])
],body=True),
Bulk_Cards = [dbc.Col(Bulk_Card1), dbc.Col(Bulk_Card2), dbc.Col(Bulk_Card3)]
