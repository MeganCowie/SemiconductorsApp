from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
import dash_daq as daq

################################################################################
################################################################################
# ncAFM cards

AFM_Card1 = dbc.Card([
    dbc.Row([
        dbc.Button("Calculate", id="AFMbutton_Calculate", color="secondary", className="mr-1", style={'fontSize': 14, 'width':300}),
    ], style={'padding': 10}, justify="center"),
    dbc.Row([
        dbc.Col(dbc.Label("zins(t) Precision", id="AFMText_timestepslabel", style={"margin-left": "10px", "margin-top": "20px"}), md=8),
        dbc.Col(html.Div(id='AFMText_timesteps', style = {'text-align': 'right', "margin-right": "10px", "margin-top": "20px"}), md=4),
    ], justify="between"),
    dbc.Row([
        dbc.Col(dcc.Slider(id='AFMSlider_timesteps', marks=None, min=10, max=50, step=10, value=10), md=12),
    ]),
])

AFM_Card2 = dbc.Card([
        dbc.Row([
            dbc.Col(dbc.Label("Amplitude (nm)", id="AFMText_amplitudelabel", style={"margin-left": "10px", "margin-top": "20px"}), md=8),
            dbc.Col(html.Div(id='AFMText_amplitude', style = {'text-align': 'right', "margin-right": "10px", "margin-top": "20px"}), md=4),
        ], justify="between"),
        dbc.Row([
            dbc.Col(dcc.Slider(id='AFMSlider_amplitude', marks=None, min=1, max=20, step=1, value=6), md=12),
        ]),
        dbc.Row([
            dbc.Col(dbc.Label("Resonant Frequency (Hz)", id="AFMText_resfreqlabel", style={"margin-left": "10px"}), md=8),
            dbc.Col(html.Div(id='AFMText_resfreq', style = {'text-align': 'right', "margin-right": "10px"}), md=4),
        ], justify="between"),
        dbc.Row([
            dbc.Col(dcc.Slider(id='AFMSlider_resfreq', marks=None, min=200000, max=400000, step=10000, value=300000), md=12),
        ]),
])


AFM_Card3 = dbc.Card([
    dbc.Row([
        dbc.Col(dbc.Label("Lag (ns)", id="AFMText_laglabel", style={"margin-left": "10px", "margin-top": "20px"}), md=8),
        dbc.Col(html.Div(id='AFMText_lag', style = {'text-align': 'right', "margin-right": "10px", "margin-top": "20px"}), md=4),
    ], justify="between"),
    dbc.Row([
        dbc.Col(dcc.Slider(id='AFMSlider_lag', marks=None, min=0, max=100, step=5, value=30,), md=12),
    ]),
    dbc.Row([
        dbc.Col(dbc.Label("Hop", id="AFMText_hoplabel", style={"margin-left": "10px"}), md=8),
        dbc.Col(html.Div(id='AFMText_hop', style = {'text-align': 'right', "margin-right": "10px"}), md=4),
    ], justify="between"),
    dbc.Row([
        dbc.Col(dcc.Slider(id='AFMSlider_hop', marks=None, min=0, max=1, step=0.01, value=0.05,), md=12),
    ]),
    dbc.Row([
        dbc.Col(html.Div(id='AFMText_RTNoff'),  md=4),
        dbc.Col(daq.ToggleSwitch(id='AFMtoggle_RTN', value=False), md=4),
        dbc.Col(html.Div(id='AFMText_RTNon',style={"margin-bottom": "20px"}),  md=4),
    ], style={'padding': 5}),
    dbc.Row([
        dbc.Col(html.Div(id='AFMText_semiconducting'),  md=4),
        dbc.Col(daq.ToggleSwitch(id='AFMtoggle_sampletype', value=False, style={ "margin-bottom": "20px"}), md=4),
        dbc.Col(html.Div(id='AFMText_metallic'),  md=4),
    ], style={'padding': 5}),
]),

AFM_Cards1 = [dbc.Col(AFM_Card1), dbc.Col(AFM_Card2), dbc.Col(AFM_Card3)]


################################################################################
################################################################################
# Bias experiment cards

AFM_Card1 = dbc.Card([
    dbc.Row([
        dbc.Button("Calculate", id="AFMbutton_CalculateBiasExp", color="secondary", className="mr-1", style={'fontSize': 14, 'width':300}),
    ], style={'padding': 10}, justify="center"),
])


AFM_Card2 = dbc.Card([
        dbc.Row([
            dbc.Col(dbc.Label("Spring Constant (N/m)", id="AFMText_springconstlabel", style={"margin-left": "10px", "margin-top": "20px"}), md=8),
            dbc.Col(html.Div(id='AFMText_springconst', style = {'text-align': 'right', "margin-right": "10px", "margin-top": "20px"}), md=4),
        ], justify="between"),
        dbc.Row([
            dbc.Col(dcc.Slider(id='AFMSlider_springconst', marks=None, min=30, max=50, step=1, value=42,), md=12),
        ]),
        dbc.Row([
            dbc.Col(dbc.Label("Q factor", id="AFMText_Qfactorlabel", style={"margin-left": "10px"}), md=8),
            dbc.Col(html.Div(id='AFMText_Qfactor', style = {'text-align': 'right', "margin-right": "10px"}), md=4),
        ], justify="between"),
        dbc.Row([
            dbc.Col(dcc.Slider(id='AFMSlider_Qfactor', marks=None, min=200, max=30000, step=100, value=23000,), md=12),
        ]),
        dbc.Row([
            dbc.Col(dbc.Label("Tip Radius (nm)", id="AFMText_tipradiuslabel", style={"margin-left": "10px"}), md=8),
            dbc.Col(html.Div(id='AFMText_tipradius', style = {'text-align': 'right', "margin-right": "10px"}), md=4),
        ], justify="between"),
        dbc.Row([
            dbc.Col(dcc.Slider(id='AFMSlider_tipradius', marks=None, min=1, max=25, step=1, value=10,), md=12),
        ]),
])

AFM_Cards2 = [dbc.Col(AFM_Card1), dbc.Col(AFM_Card2)]

################################################################################
################################################################################
# Time trace experiment cards

AFM_Card1 = dbc.Card([
    dbc.Row([
        dbc.Button("Calculate", id="AFMbutton_CalculateTimeExp", color="secondary", className="mr-1", style={'fontSize': 14, 'width':300}),
    ], style={'padding': 10}, justify="center"),
])

AFM_Card2 = dbc.Card([
    dbc.Row([
        dbc.Col(dbc.Label("Sigma", id="AFMText_sigmalabel", style={"margin-left": "10px", "margin-top": "20px"}), md=8),
        dbc.Col(html.Div(id='AFMText_sigma', style = {'text-align': 'right', "margin-right": "10px", "margin-top": "20px"}), md=4),
    ], justify="between"),
    dbc.Row([
        dbc.Col(dcc.Slider(id='AFMSlider_sigma', marks=None, min=0, max=2, step=0.01, value=0.05), md=12),
    ]),
])

AFM_Card3 = dbc.Card([
    dbc.Row([
        dbc.Col([
                dbc.Row([
                    dbc.Col(dbc.Label("RTS 1 mag", id="AFMText_RTS1maglabel", style={'fontSize': 14, "margin-left": "10px", "margin-right": "-10px", "margin-top": "20px"}), md=8),
                    dbc.Col(html.Div(id='AFMText_RTS1mag',style={'fontSize': 14, 'text-align': 'right', "margin-top": "20px"}), md=4),
                ], justify="between"),
                dbc.Row([
                    dbc.Col(dcc.Slider(id='AFMSlider_RTS1mag', marks=None, min=0, max=10, step=0.1, value=0,)),
                ]),
        ], md=6),
        dbc.Col([
                dbc.Row([
                    dbc.Col(dbc.Label("RTS 1 period", id="AFMText_RTS1perlabel", style={'fontSize': 14, "margin-left": "10px", "margin-right": "-10px", "margin-top": "20px"}), md=8),
                    dbc.Col(html.Div(id='AFMText_RTS1per',style={'fontSize': 14, 'text-align': 'right', "margin-top": "20px"}), md=4),
                ], justify="between"),
                dbc.Row([
                    dbc.Col(dcc.Slider(id='AFMSlider_RTS1per', marks=None, min=0, max=1, step=0.01, value=0,)),
                ]),
        ], md=6)
    ]),
    dbc.Row([
        dbc.Col([
                dbc.Row([
                    dbc.Col(dbc.Label("RTS 2 mag", id="AFMText_RTS2maglabel", style={'fontSize': 14, "margin-left": "10px", "margin-right": "-10px", "margin-top": "20px"}), md=8),
                    dbc.Col(html.Div(id='AFMText_RTS2mag',style={'fontSize': 14, 'text-align': 'right', "margin-top": "20px"}), md=4),
                ], justify="between"),
                dbc.Row([
                    dbc.Col(dcc.Slider(id='AFMSlider_RTS2mag', marks=None, min=0, max=10, step=0.1, value=0,)),
                ]),
        ], md=6),
        dbc.Col([
                dbc.Row([
                    dbc.Col(dbc.Label("RTS 2 period", id="AFMText_RTS2perlabel", style={'fontSize': 14, "margin-left": "10px", "margin-right": "-10px", "margin-top": "20px"}), md=8),
                    dbc.Col(html.Div(id='AFMText_RTS2per',style={'fontSize': 14, 'text-align': 'right', "margin-top": "20px"}), md=4),
                ], justify="between"),
                dbc.Row([
                    dbc.Col(dcc.Slider(id='AFMSlider_RTS2per', marks=None, min=0, max=1, step=0.01, value=0,)),
                ]),
        ], md=6)
    ]),
    dbc.Row([
        dbc.Col([
                dbc.Row([
                    dbc.Col(dbc.Label("RTS 3 mag", id="AFMText_RTS3maglabel", style={'fontSize': 14, "margin-left": "10px", "margin-right": "-10px", "margin-top": "20px"}), md=8),
                    dbc.Col(html.Div(id='AFMText_RTS3mag',style={'fontSize': 14, 'text-align': 'right', "margin-top": "20px"}), md=4),
                ], justify="between"),
                dbc.Row([
                    dbc.Col(dcc.Slider(id='AFMSlider_RTS3mag', marks=None, min=0, max=10, step=0.1, value=0,)),
                ]),
        ], md=6),
        dbc.Col([
                dbc.Row([
                    dbc.Col(dbc.Label("RTS 3 period", id="AFMText_RTS3perlabel", style={'fontSize': 14, "margin-left": "10px", "margin-right": "-10px", "margin-top": "20px"}), md=8),
                    dbc.Col(html.Div(id='AFMText_RTS3per',style={'fontSize': 14, 'text-align': 'right', "margin-top": "20px"}), md=4),
                ], justify="between"),
                dbc.Row([
                    dbc.Col(dcc.Slider(id='AFMSlider_RTS3per', marks=None, min=0, max=1, step=0.01, value=0,)),
                ]),
        ], md=6)
    ]),
    dbc.Row([
        dbc.Col([
                dbc.Row([
                    dbc.Col(dbc.Label("RTS 4 mag", id="AFMText_RTS4maglabel", style={'fontSize': 14, "margin-left": "10px", "margin-right": "-10px", "margin-top": "20px"}), md=8),
                    dbc.Col(html.Div(id='AFMText_RTS4mag',style={'fontSize': 14, 'text-align': 'right', "margin-top": "20px"}), md=4),
                ], justify="between"),
                dbc.Row([
                    dbc.Col(dcc.Slider(id='AFMSlider_RTS4mag', marks=None, min=0, max=10, step=0.1, value=0,)),
                ]),
        ], md=6),
        dbc.Col([
                dbc.Row([
                    dbc.Col(dbc.Label("RTS 4 period", id="AFMText_RTS4perlabel", style={'fontSize': 14, "margin-left": "10px", "margin-right": "-10px", "margin-top": "20px"}), md=8),
                    dbc.Col(html.Div(id='AFMText_RTS4per',style={'fontSize': 14, 'text-align': 'right', "margin-top": "20px"}), md=4),
                ], justify="between"),
                dbc.Row([
                    dbc.Col(dcc.Slider(id='AFMSlider_RTS4per', marks=None, min=0, max=1, step=0.01, value=0,)),
                ]),
        ], md=6)
    ]),
    dbc.Row([
        dbc.Col([
                dbc.Row([
                    dbc.Col(dbc.Label("RTS5 mag", id="AFMText_RTS5maglabel", style={'fontSize': 14, "margin-left": "10px", "margin-right": "-10px", "margin-top": "20px"}), md=8),
                    dbc.Col(html.Div(id='AFMText_RTS5mag',style={'fontSize': 14, 'text-align': 'right', "margin-top": "20px"}), md=4),
                ], justify="between"),
                dbc.Row([
                    dbc.Col(dcc.Slider(id='AFMSlider_RTS5mag', marks=None, min=0, max=10, step=0.1, value=0,)),
                ]),
        ], md=6),
        dbc.Col([
                dbc.Row([
                    dbc.Col(dbc.Label("RTS5 period", id="AFMText_RTS5perlabel", style={'fontSize': 14, "margin-left": "10px", "margin-right": "-10px", "margin-top": "20px"}), md=8),
                    dbc.Col(html.Div(id='AFMText_RTS5per',style={'fontSize': 14, 'text-align': 'right', "margin-top": "20px"}), md=4),
                ], justify="between"),
                dbc.Row([
                    dbc.Col(dcc.Slider(id='AFMSlider_RTS5per', marks=None, min=0, max=1, step=0.01, value=0,)),
                ]),
        ], md=6)
    ]),
])

AFM_Card4 = dbc.Card([
    dbc.Row([
        dbc.Col(dbc.Label("1/f^0 y-intercept", id="AFMText_f0ylabel", style={"margin-left": "10px", "margin-top": "20px"}), md=8),
        dbc.Col(html.Div(id='AFMText_f0y', style = {'text-align': 'right', "margin-right": "10px", "margin-top": "20px"}), md=4),
    ], justify="between"),
    dbc.Row([
        dbc.Col(dcc.Slider(id='AFMSlider_f0y', marks=None, min=-10, max=10, step=0.1, value=0), md=12),
    ]),
    dbc.Row([
        dbc.Col(dbc.Label("1/f^1 y-intercept", id="AFMText_f1ylabel", style={"margin-left": "10px", "margin-top": "20px"}), md=8),
        dbc.Col(html.Div(id='AFMText_f1y', style = {'text-align': 'right', "margin-right": "10px", "margin-top": "20px"}), md=4),
    ], justify="between"),
    dbc.Row([
        dbc.Col(dcc.Slider(id='AFMSlider_f1y', marks=None, min=-10, max=10, step=0.1, value=0), md=12),
    ]),
    dbc.Row([
        dbc.Col(dbc.Label("1/f^2 y-intercept", id="AFMText_f2ylabel", style={"margin-left": "10px", "margin-top": "20px"}), md=8),
        dbc.Col(html.Div(id='AFMText_f2y', style = {'text-align': 'right', "margin-right": "10px", "margin-top": "20px"}), md=4),
    ], justify="between"),
    dbc.Row([
        dbc.Col(dcc.Slider(id='AFMSlider_f2y', marks=None, min=-10, max=10, step=0.1, value=0), md=12),
    ]),
])

AFM_Cards3 = [dbc.Col(AFM_Card1),dbc.Col(AFM_Card2),dbc.Col(AFM_Card3),dbc.Col(AFM_Card4)]

################################################################################
################################################################################
# Delay sweep experiment cards

AFM_Card1 = dbc.Card([
    dbc.Row([
        dbc.Button("Calculate", id="AFMbutton_CalculateDelayExp", color="secondary", className="mr-1", style={'fontSize': 14, 'width':300}),
    ], style={'padding': 10}, justify="center"),
    dbc.Row([
        dbc.Col(dbc.Label("Pulse Precision", id="AFMText_pulsetimestepslabel", style={"margin-left": "10px", "margin-top": "20px"}), md=8),
        dbc.Col(html.Div(id='AFMText_pulsetimesteps', style = {'text-align': 'right', "margin-right": "10px", "margin-top": "20px"}), md=4),
    ], justify="between"),
    dbc.Row([
        dbc.Col(dcc.Slider(id='AFMSlider_pulsetimesteps', marks=None, min=50, max=1000, step=50, value=100), md=12),
    ]),
    dbc.Row([
        dbc.Col(dbc.Label("Delay Precision", id="AFMText_delaystepslabel", style={"margin-left": "10px"}), md=8),
        dbc.Col(html.Div(id='AFMText_delaysteps', style = {'text-align': 'right', "margin-right": "10px"}), md=4),
    ], justify="between"),
    dbc.Row([
        dbc.Col(dcc.Slider(id='AFMSlider_delaysteps', marks=None, min=50, max=1000, step=50, value=100), md=12),
    ]),
])


AFM_Cards4 = [dbc.Col(AFM_Card1)]
