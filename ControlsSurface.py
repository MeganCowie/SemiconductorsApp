import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html

################################################################################
################################################################################

Surface_Card1 = dbc.Card([
    dbc.FormGroup([
        dbc.Row([
            dbc.Col(dbc.Label("Gate Bias (eV)", id="SurfaceText_Vglabel", style={"margin-left": "10px", "margin-top": "20px"}), md=8),
            dbc.Col(html.Div(id='SurfaceText_Vg', style = {'text-align': 'right', "margin-right": "10px", "margin-top": "20px"}), md=4),
        ], justify="between"),
        dbc.Row([
            dbc.Col(dcc.Slider(id='SurfaceSlider_Vg', min=-10, max=10, step=0.1, value=5,), md=12),
        ]),
        dbc.Row([
            dbc.Col(dbc.Label("Insulator Thickness (nm)", id="SurfaceText_zinslabel", style={"margin-left": "10px"}), md=8),
            dbc.Col(html.Div(id='SurfaceText_zins', style = {'text-align': 'right', "margin-right": "10px"}), md=4),
        ], justify="between"),
        dbc.Row([
            dbc.Col(dcc.Slider(id='SurfaceSlider_zins', min=1, max=25, step=1, value=10,), style={"margin-bottom":"-20px"}, md=12),
        ]),
    ]),
], style={"width": "325px"})

Surface_Card2 = dbc.Card([
dbc.Row([
    dbc.Col([
        dbc.FormGroup([
            dbc.Row([
                dbc.Col(dbc.Label("Band Gap (eV)", id="SurfaceText_bandgaplabel", style={'fontSize': 10, "margin-left": "10px", "margin-right": "-10px", "margin-top": "10px"}), md=8),
                dbc.Col(html.Div(id='SurfaceText_bandgap',style={'fontSize': 10, 'text-align': 'right',"margin-top": "10px"}), md=4),
            ], justify="between"),
            dbc.Row([
                dbc.Col(dcc.Slider(id='SurfaceSlider_bandgap', min=0.1, max=5, step=0.01, value=1.55,), md=12),
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
                dbc.Col(dcc.Slider(id='SurfaceSlider_epsilonsem', min=0.01, max=22, step=0.01, value=4.74)),
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
                dbc.Col(dcc.Slider(id='SurfaceSlider_WFmet', min=0.1, max=8, step=0.1, value=4,)),
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
                dbc.Col(dcc.Slider(id='SurfaceSlider_EAsem', min=0.1, max=5, step=0.1, value=3.5,)),
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
                dbc.Col(dcc.Slider(id='SurfaceSlider_emass', min=0.1, max=2, step=0.1, value=1.1,)),
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
                dbc.Col(dcc.Slider(id='SurfaceSlider_hmass', min=0.1, max=2, step=0.1, value=1.2), md=12),
            ]),
        ]),
    ], md=6)
]),

    dbc.FormGroup([
        dbc.Row([
            dbc.Col(dbc.Label("Donors (cm-3)", id="SurfaceText_donorlabel", style = {'text-align': 'right', "margin-left": "10px"}), md=8),
            dbc.Col(html.Div(id='SurfaceText_donor',style={'fontSize': 10, 'text-align': 'right'}), md=4),
        ], justify="between"),
        dbc.Row([
            dbc.Col(dcc.Slider(id='SurfaceSlider_donor', min=1, max=26, step=0.5, value=0,)),
        ]),
    ]),
    dbc.FormGroup([
        dbc.Row([
            dbc.Col(dbc.Label("Acceptors (cm-3)", id="SurfaceText_acceptorlabel", style = {'text-align': 'right', "margin-left": "10px"}), md=8),
            dbc.Col(html.Div(id='SurfaceText_acceptor',style={'fontSize': 10, 'text-align': 'right', "margin-left": "-10px", "margin-right": "10px"}), md=4),
        ], justify="between"),
        dbc.Row([
            dbc.Col(dcc.Slider(id='SurfaceSlider_acceptor', min=1, max=26, step=0.5, value=17,)),
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
            dbc.Col(dbc.Label("ni (cm-3)", id="SurfaceText_nilabel", style={"margin-left": "10px", "margin-top": "20px"}), md=4),
            dbc.Col(html.Div(id='SurfaceText_ni', style = {'text-align': 'right', "margin-right": "10px", "margin-top": "20px"}), md=8),
        ], justify="between"),
    ]),
], style={"width": "325px"})


Surface_Cards = [dbc.Col(Surface_Card1), dbc.Col(Surface_Card2), dbc.Col(Surface_Card3)]
