from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
import dash_daq as daq

################################################################################
################################################################################

Surface_Card0 = dbc.Card([
        dbc.Row([
            dbc.Col(dbc.Label("Presets", id="SurfaceText_Presets", style = {'textAlign': 'right', "marginLeft": "10px", "marginTop": "10px",'fontSize': 18}), md=8),
        ], justify="between"),
        dbc.Row([dbc.Col(dcc.RadioItems(id="SurfaceButtons_presets", options=[
            {'label': '   MoSe2', 'value': 1},
            {'label': '   Silicon', 'value': 2},
            {'label': '   Pentacene', 'value': 3},
            {'label': '   Other', 'value': 4}
            ],value=2,labelStyle={"width": '50%','display': 'inline-block'},
            ), style={"marginLeft": "50px", "marginTop": "0px",'fontSize': 18},width="auto")
        ]),
], color='#eaeaea',style={"border":"#eaeaea"})



Surface_Card1 = dbc.Card([
        dbc.Row([
            dbc.Col(html.Div(id='SurfaceText_regime', style = {'textAlign': 'center', 'color': '#57c5f7', 'fontSize': 18, "marginRight": "10px", "marginTop": "20px","marginBottom": "10px"}), md=12),
        ], justify="between"),
        dbc.Row([
            dbc.Col(dbc.Label("Gate Bias (eV)", id="SurfaceText_Vglabel", style={"marginLeft": "10px"}), md=8),
            dbc.Col(html.Div(id='SurfaceText_Vg', style = {'textAlign': 'right', "marginRight": "10px"}), md=4),
        ], justify="between"),
        dbc.Row([
            dbc.Col(dcc.Slider(id='SurfaceSlider_Vg', marks=None, min=-10, max=10, step=0.1, value=-1.4,), md=12),
        ]),
        dbc.Row([
            dbc.Col(dbc.Label("Alpha", id="SurfaceText_alphalabel", style={"marginLeft": "10px"}), md=8),
            dbc.Col(html.Div(id='SurfaceText_alpha', style = {'textAlign': 'right', "marginRight": "10px"}), md=4),
        ], justify="between"),
        dbc.Row([
            dbc.Col(dcc.Slider(id='SurfaceSlider_alpha', marks=None, min=0, max=1, step=0.01, value=0,), md=12),
        ]),
        dbc.Row([
            dbc.Col(dbc.Label("Insulator Thickness (nm)", id="SurfaceText_zinslabel", style={"marginLeft": "10px"}), md=8),
            dbc.Col(html.Div(id='SurfaceText_zins', style = {'textAlign': 'right', "marginRight": "10px"}), md=4),
        ], justify="between"),
        dbc.Row([
            dbc.Col(dcc.Slider(id='SurfaceSlider_zins', marks=None, min=1, max=25, step=1, value=5.2,), style={"marginBottom":"-20px"}, md=12),
        ]),
])

Surface_Card2 = dbc.Card([
dbc.Row([
    dbc.Row([
        dbc.Col(dbc.Row(html.Div(id='SurfaceText_typen'),justify="center"),  md=4),
        dbc.Col(dbc.Row(daq.ToggleSwitch(id='SurfaceToggle_type', size=50, value=True, style={'width':'100%'},), justify="center"), md=4),
        dbc.Col(dbc.Row(html.Div(id='SurfaceText_typep'),justify="center"), md=4),
    ],justify="evenly"),
], style={"marginTop":"30px","marginBottom":"10px","marginLeft":"10px","marginRight":"10px"}),
dbc.Row([
    dbc.Row([
        dbc.Col(dbc.Label("Band Gap (eV)", id="SurfaceText_Eglabel", style={"marginLeft": "10px", "marginTop": "20px"}), md=8),
        dbc.Col(html.Div(id='SurfaceText_Eg', style = {'textAlign': 'right', "marginRight": "10px", "marginTop": "20px"}), md=4),
    ], justify="between"),
    dbc.Row([
        dbc.Col(dcc.Slider(id='SurfaceSlider_Eg', marks=None, min=0.1, max=3, step=0.01, value=1.5), md=12),
    ]),
    dbc.Row([
        dbc.Col(dbc.Label("Rel. Permittivity (S)", id="SurfaceText_epsilonsemlabel", style={"marginLeft": "10px"}), md=8),
        dbc.Col(html.Div(id='SurfaceText_epsilonsem', style = {'textAlign': 'right', "marginRight": "10px"}), md=4),
    ], justify="between"),
    dbc.Row([
        dbc.Col(dcc.Slider(id='SurfaceSlider_epsilonsem', marks=None, min=0.01, max=22, step=0.01, value=5.9), md=12),
    ]),
    dbc.Row([
        dbc.Col(dbc.Label("Work Func. (M) (eV)", id="SurfaceText_WFmetlabel", style={"marginLeft": "10px"}), md=8),
        dbc.Col(html.Div(id='SurfaceText_WFmet', style = {'textAlign': 'right', "marginRight": "10px"}), md=4),
    ], justify="between"),
    dbc.Row([
        dbc.Col(dcc.Slider(id='SurfaceSlider_WFmet', marks=None, min=0.1, max=8, step=0.1, value=4.1), md=12),
    ]),
    dbc.Row([
        dbc.Col(dbc.Label("Elec. Affinity (S) (eV)", id="SurfaceText_EAsemlabel", style={"marginLeft": "10px"}), md=8),
        dbc.Col(html.Div(id='SurfaceText_EAsem', style = {'textAlign': 'right', "marginRight": "10px"}), md=4),
    ], justify="between"),
    dbc.Row([
        dbc.Col(dcc.Slider(id='SurfaceSlider_EAsem', marks=None, min=0.1, max=5, step=0.1, value=3.5), md=12),
    ]),
    dbc.Row([
        dbc.Col(dbc.Label("Donors (cm-3)", id="SurfaceText_donorlabel", style = {'textAlign': 'right', "marginLeft": "10px"}), md=8),
        dbc.Col(html.Div(id='SurfaceText_donor',style={'textAlign': 'right', "marginLeft": "-10px", "marginRight": "10px"}), md=4),
    ], justify="between"),
    dbc.Row([
        dbc.Col(dcc.Slider(id='SurfaceSlider_donor', marks=None, min=25, max=35, step=0.1, value=30)),
    ]),
    dbc.Row([
        dbc.Col(dbc.Label("Acceptors (cm-3)", id="SurfaceText_acceptorlabel", style = {'textAlign': 'right', "marginLeft": "10px"}), md=8),
        dbc.Col(html.Div(id='SurfaceText_acceptor',style={'textAlign': 'right', "marginLeft": "-10px", "marginRight": "10px"}), md=4),
    ], justify="between"),
    dbc.Row([
        dbc.Col(dcc.Slider(id='SurfaceSlider_acceptor', marks=None, min=25, max=35, step=0.1, value=0, disabled=True)),
    ]),
    dbc.Row([
        dbc.Col([
                dbc.Row([
                    dbc.Col(dbc.Label("Elec. Eff. Mass (me)", id="SurfaceText_emasslabel", style={'fontSize': 10, "marginLeft": "10px", "marginRight": "-10px"}), md=8),
                    dbc.Col(html.Div(id='SurfaceText_emass',style={'fontSize': 10, 'textAlign': 'right'}), md=4),
                ], justify="between"),
                dbc.Row([
                    dbc.Col(dcc.Slider(id='SurfaceSlider_emass', marks=None, min=0.1, max=2, step=0.1, value=1.0,)),
                ]),
        ], md=6),
        dbc.Col([
                dbc.Row([
                    dbc.Col(dbc.Label("Hole Eff. Mass (me)", id="SurfaceText_hmasslabel", style={'fontSize': 10}), md=8),
                    dbc.Col(html.Div(id='SurfaceText_hmass',style={'fontSize': 12, 'textAlign': 'right', "marginRight": "10px"}), md=4),
                ], justify="between"),
                dbc.Row([
                    dbc.Col(dcc.Slider(id='SurfaceSlider_hmass', marks=None, min=0.1, max=2, step=0.1, value=1.0,), md=12),
                ]),
        ], md=6)
    ]),
    dbc.Row([
        dbc.Col(dbc.Label("Temperature (K)", id="SurfaceText_Tlabel", style = {'textAlign': 'right', "marginLeft": "10px"}), md=8),
        dbc.Col(html.Div(id='SurfaceText_T', style = {'textAlign': 'right', "marginRight": "10px"}), md=4),
    ], justify="between"),
    dbc.Row([
        dbc.Col(dcc.Slider(id='SurfaceSlider_T', marks=None, min=200, max=500, step=1, value=300,), style={"marginBottom":"-20px"}, md=12),
    ]),
]),

]),

Surface_Card3 = dbc.Card([
        dbc.Row([
            dbc.Col(dbc.Label("Readouts", id="SurfaceText_Readouts", style = {'textAlign': 'right', "marginLeft": "10px", "marginTop": "10px"}), md=8),
        ], justify="between"),
        dbc.Row([
            dbc.Col(dbc.Label("Intrinsic Density (cm-3)", id="SurfaceText_nilabel", style={"marginLeft": "18px"}), md=8),
            dbc.Col(html.Div(id='SurfaceText_ni', style = {'textAlign': 'right', "marginRight": "10px"}), md=4),
        ], justify="between"),
        dbc.Row([
            dbc.Col(dbc.Label("Debye Length (nm)", id="SurfaceText_LDlabel", style={"marginLeft": "18px"}), md=8),
            dbc.Col(html.Div(id='SurfaceText_LD', style = {'textAlign': 'right', "marginRight": "10px"}), md=4),
        ], justify="between"),
        dbc.Row([
            dbc.Col(dbc.Label("Spacecharge Width (nm)", id="SurfaceText_zQlabel", style={"marginLeft": "18px"}), md=8),
            dbc.Col(html.Div(id='SurfaceText_zQ', style = {'textAlign': 'right', "marginRight": "10px"}), md=4),
        ], justify="between"),
    dbc.Row([
        dbc.Col(dbc.Label("Gate Bias Precision", id="SurfaceText_biasstepslabel", style={"marginLeft": "10px", "marginTop": "20px"}), md=8),
        dbc.Col(html.Div(id='SurfaceText_biassteps', style = {'textAlign': 'right', "marginRight": "10px", "marginTop": "20px"}), md=4),
    ], justify="between"),
    dbc.Row([
        dbc.Col(dcc.Slider(id='SurfaceSlider_biassteps', marks=None, min=128, max=1024, step=56, value=56), md=12),
    ]),
    dbc.Row([
        dbc.Col(dbc.Label("Insulator Thickness Precision", id="SurfaceText_zinsstepslabel", style={"marginLeft": "10px"}), md=8),
        dbc.Col(html.Div(id='SurfaceText_zinssteps', style = {'textAlign': 'right', "marginRight": "10px"}), md=4),
    ], justify="between"),
    dbc.Row([
        dbc.Col(dcc.Slider(id='SurfaceSlider_zinssteps', marks=None, min=128, max=1024, step=56, value=56), md=12),
    ]),
]),



Surface_Cards = [dbc.Col(Surface_Card0), dbc.Col(Surface_Card1), dbc.Col(Surface_Card2), dbc.Col(Surface_Card3)]
