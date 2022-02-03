import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_daq as daq

################################################################################
################################################################################

Surface_Card0 = dbc.Card([
    dbc.FormGroup([
        dbc.Row([
            dbc.Col(dbc.Label("Presets", id="SurfaceText_Presets", style = {'text-align': 'right', "margin-left": "10px", "margin-top": "10px"}), md=8),
        ], justify="between"),
        dbc.Row([dbc.Col(dcc.RadioItems(id="SurfaceButtons_presets", options=[
            {'label': '   MoSe2', 'value': 1},
            {'label': '   Silicon', 'value': 2},
            {'label': '   Pentacene', 'value': 3},
            {'label': '   Other', 'value': 4}
            ],value=1,labelStyle={"width": '50%','display': 'inline-block'},
            ), style={"margin-left": "50px", "margin-top": "0px"},width="auto")
        ], justify="center"),]),
], style={"width": "325px"})


Surface_Card1 = dbc.Card([
    dbc.FormGroup([
        dbc.Row([
            dbc.Col(dbc.Label("Gate Bias (eV)", id="SurfaceText_Vglabel", style={"margin-left": "10px", "margin-top": "20px"}), md=8),
            dbc.Col(html.Div(id='SurfaceText_Vg', style = {'text-align': 'right', "margin-right": "10px", "margin-top": "20px"}), md=4),
        ], justify="between"),
        dbc.Row([
            dbc.Col(dcc.Slider(id='SurfaceSlider_Vg', min=-10, max=10, step=0.1, value=-1.4,), md=12),
        ]),
        dbc.Row([
            dbc.Col(dbc.Label("Insulator Thickness (nm)", id="SurfaceText_zinslabel", style={"margin-left": "10px"}), md=8),
            dbc.Col(html.Div(id='SurfaceText_zins', style = {'text-align': 'right', "margin-right": "10px"}), md=4),
        ], justify="between"),
        dbc.Row([
            dbc.Col(dcc.Slider(id='SurfaceSlider_zins', min=1, max=25, step=1, value=5.2,), style={"margin-bottom":"-20px"}, md=12),
        ]),
    ]),
], style={"width": "325px"})

Surface_Card2 = dbc.Card([
dbc.FormGroup([
    dbc.Row([
        dbc.Col(html.Div(id='SurfaceText_typen'),  md=3),
        dbc.Col(daq.ToggleSwitch(id='SurfaceToggle_type', value=True), md=6),
        dbc.Col(html.Div(id='SurfaceText_typep'),  md=3),
    ]),
], style={"margin-top":"20px","margin-bottom":"20px","margin-left":"10px","margin-right":"20px"}),
dbc.Row([
    dbc.Col([
        dbc.FormGroup([
            dbc.Row([
                dbc.Col(dbc.Label("Band Gap (eV)", id="SurfaceText_bandgaplabel", style={'fontSize': 10, "margin-left": "10px", "margin-right": "-10px", "margin-top": "10px"}), md=8),
                dbc.Col(html.Div(id='SurfaceText_bandgap',style={'fontSize': 10, 'text-align': 'right',"margin-top": "10px"}), md=4),
            ], justify="between"),
            dbc.Row([
                dbc.Col(dcc.Slider(id='SurfaceSlider_bandgap', min=0.1, max=5, step=0.01, value=1.5,), md=12),
            ]),
        ]),
    ], style={"margin-bottom":"-20px"}, md=6),
    dbc.Col([
        dbc.FormGroup([
            dbc.Row([
                dbc.Col(dbc.Label("Rel. Permittivity (S)", id="SurfaceText_epsilonsemlabel", style={'fontSize': 10, "margin-top": "10px", "margin-left": "-10px"}), md=8),
                dbc.Col(html.Div(id='SurfaceText_epsilonsem',style={'fontSize': 10, 'text-align': 'right', "margin-right": "10px", "margin-top": "10px"}), md=4),
            ], justify="between"),
            dbc.Row([
                dbc.Col(dcc.Slider(id='SurfaceSlider_epsilonsem', min=0.01, max=22, step=0.01, value=5.9)),
            ]),
        ]),
    ], md=6),
]),
dbc.Row([
    dbc.Col([
        dbc.FormGroup([
            dbc.Row([
                dbc.Col(dbc.Label("Work Func. (M) (eV)", id="SurfaceText_WFmetlabel", style={'fontSize': 10, "margin-left": "10px", "margin-right": "-10px"}), md=8),
                dbc.Col(html.Div(id='SurfaceText_WFmet',style={'fontSize': 10, 'text-align': 'right'}), md=4),
            ], justify="between"),
            dbc.Row([
                dbc.Col(dcc.Slider(id='SurfaceSlider_WFmet', min=0.1, max=8, step=0.1, value=4.1)),
            ]),
        ]),
    ], md=6),
    dbc.Col([
        dbc.FormGroup([
            dbc.Row([
                dbc.Col(dbc.Label("Elec. Affinity (S) (eV)", id="SurfaceText_EAsemlabel", style={'fontSize': 10, "margin-left": "-10px"}), md=8),
                dbc.Col(html.Div(id='SurfaceText_EAsem',style={'fontSize': 10, 'text-align': 'right', "margin-right": "10px"}), md=4),
            ], justify="between"),
            dbc.Row([
                dbc.Col(dcc.Slider(id='SurfaceSlider_EAsem', min=0.1, max=5, step=0.1, value=3.5)),
            ]),
        ]),
    ], md=6)
]),
dbc.Row([
    dbc.Col([
        dbc.FormGroup([
            dbc.Row([
                dbc.Col(dbc.Label("Elec. Eff. Mass (me)", id="SurfaceText_emasslabel", style={'fontSize': 10, "margin-left": "10px", "margin-right": "-10px"}), md=8),
                dbc.Col(html.Div(id='SurfaceText_emass',style={'fontSize': 10, 'text-align': 'right'}), md=4),
            ], justify="between"),
            dbc.Row([
                dbc.Col(dcc.Slider(id='SurfaceSlider_emass', min=0.1, max=2, step=0.1, value=1.0,)),
            ]),
        ]),
    ], md=6),
    dbc.Col([
        dbc.FormGroup([
            dbc.Row([
                dbc.Col(dbc.Label("Hole Eff. Mass (me)", id="SurfaceText_hmasslabel", style={'fontSize': 10}), md=8),
                dbc.Col(html.Div(id='SurfaceText_hmass',style={'fontSize': 12, 'text-align': 'right', "margin-right": "10px"}), md=4),
            ], justify="between"),
            dbc.Row([
                dbc.Col(dcc.Slider(id='SurfaceSlider_hmass', min=0.1, max=2, step=0.1, value=1.0), md=12),
            ]),
        ]),
    ], md=6)
]),
    dbc.FormGroup([
        dbc.Row([
            dbc.Col(dbc.Label("Donors (cm-3)", id="SurfaceText_donorlabel", style = {'text-align': 'right', "margin-left": "10px"}), md=8),
            dbc.Col(html.Div(id='SurfaceText_donor',style={'fontSize': 10, 'text-align': 'right', "margin-left": "-10px", "margin-right": "10px"}), md=4),
        ], justify="between"),
        dbc.Row([
            dbc.Col(dcc.Slider(id='SurfaceSlider_donor', min=17, max=20, step=0.1, value=0, disabled=True)),
        ]),
    ]),
    dbc.FormGroup([
        dbc.Row([
            dbc.Col(dbc.Label("Acceptors (cm-3)", id="SurfaceText_acceptorlabel", style = {'text-align': 'right', "margin-left": "10px"}), md=8),
            dbc.Col(html.Div(id='SurfaceText_acceptor',style={'fontSize': 10, 'text-align': 'right', "margin-left": "-10px", "margin-right": "10px"}), md=4),
        ], justify="between"),
        dbc.Row([
            dbc.Col(dcc.Slider(id='SurfaceSlider_acceptor', min=17, max=20, step=0.1, value=18.8)),
        ]),
    ]),
    dbc.FormGroup([
        dbc.Row([
            dbc.Col(dbc.Label("Temperature (K)", id="SurfaceText_Tlabel", style = {'text-align': 'right', "margin-left": "10px"}), md=8),
            dbc.Col(html.Div(id='SurfaceText_T', style = {'text-align': 'right', "margin-right": "10px"}), md=4),
        ], justify="between"),
        dbc.Row([
            dbc.Col(dcc.Slider(id='SurfaceSlider_T', min=1, max=1000, step=1, value=300,), style={"margin-bottom":"-20px"}, md=12),
        ]),
    ]),

],style={"width": "325px"}),

Surface_Card3 = dbc.Card([
    dbc.FormGroup([
        dbc.Row([
            dbc.Col(dbc.Label("Readouts", id="SurfaceText_Readouts", style = {'text-align': 'right', "margin-left": "10px", "margin-top": "10px"}), md=8),
        ], justify="between"),
        dbc.Row([
            dbc.Col(dbc.Label("Intrinsic Density (cm-3)", id="SurfaceText_nilabel", style={"margin-left": "18px"}), md=8),
            dbc.Col(html.Div(id='SurfaceText_ni', style = {'text-align': 'right', "margin-right": "10px"}), md=4),
        ], justify="between"),
        dbc.Row([
            dbc.Col(dbc.Label("Depletion Width (nm)", id="SurfaceText_zDlabel", style={"margin-left": "18px"}), md=8),
            dbc.Col(html.Div(id='SurfaceText_zD', style = {'text-align': 'right', "margin-right": "10px"}), md=4),
        ], justify="between"),
    ]),
], style={"width": "325px"}),



Surface_Cards = [dbc.Col(Surface_Card0), dbc.Col(Surface_Card1), dbc.Col(Surface_Card2), dbc.Col(Surface_Card3)]
