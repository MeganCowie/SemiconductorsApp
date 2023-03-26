from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
import dash_daq as daq

################################################################################
################################################################################
# ncAFM cards

AFM_Card1 = html.Div([
    html.Div([        
        html.Div([
            html.Button("Calculate", id="AFMbutton_Calculate", className='button'),
        ], className = 'button_container'),

        html.Div([
            html.Div("zins(t) Precision", className='label_name', id="AFMText_timestepslabel"),
            html.Div(id='AFMText_timesteps', className='label_value'),
        ], className='label_container'),
        dcc.Slider(id='AFMSlider_timesteps', className='slider', marks=None, min=10, max=50, step=10, value=30),

        html.Div([
            html.Div("Amplitude (nm)", className='label_name', id="AFMText_amplitudelabel"),
            html.Div(id='AFMText_amplitude', className='label_value'),
        ], className='label_container'),
        dcc.Slider(id='AFMSlider_amplitude', className='slider', marks=None, min=1, max=20, step=1, value=6),

        html.Div([
            html.Div("Resonant Frequency (Hz)", className='label_name', id="AFMText_resfreqlabel"),
            html.Div(id='AFMText_resfreq', className='label_value'),
        ], className='label_container'),
        dcc.Slider(id='AFMSlider_resfreq', className='slider', marks=None, min=100000, max=10000000, step=100000, value=300000),

        html.Div([
            html.Div("Lag (ns)", className='label_name', id="AFMText_laglabel"),
            html.Div(id='AFMText_lag', className='label_value'),
        ], className='label_container'),
        dcc.Slider(id='AFMSlider_lag', className='slider', marks=None, min=0, max=3000, step=5, value=30),
    
    ], className= 'controls_container'),
   
    html.Div([

        html.Div([
            html.Div("Presets", id="AFMText_Presets"),
            dcc.RadioItems(id="AFMButtons_presets", options=[
                {'label': '   Figure', 'value': 1},
                {'label': '   Other', 'value': 0}
                ]
            ,value=1, labelStyle={"width": '50%','display': 'inline-block'}),
        ], className='presets_container'),
        
    ], className= 'controls_container'),


], className='controls', hidden=True, id='display_fmAFMoscillationscontrols')


################################################################################
################################################################################
# Bias experiment cards

AFM_Card2 = html.Div([
    html.Div([
        html.Div([
            html.Button("Calculate", id="AFMbutton_CalculateBiasExp", className='button'),
        ], className = 'button_container'),

        html.Div([
            html.Div("Spring Constant (N/m)", className='label_name', id="AFMText_springconstlabel"),
            html.Div(id='AFMText_springconst', className='label_value'),
        ], className='label_container'),
        dcc.Slider(id='AFMSlider_springconst', className='slider', marks=None, min=30, max=50, step=1, value=42),

        html.Div([
            html.Div("Q factor", className='label_name', id="AFMText_Qfactorlabel"),
            html.Div(id='AFMText_Qfactor', className='label_value'),
        ], className='label_container'),
        dcc.Slider(id='AFMSlider_Qfactor', className='slider', marks=None, min=1000, max=30000, step=1000, value=18000),

        html.Div([
            html.Div("Tip Radius (nm)", className='label_name', id="AFMText_tipradiuslabel"),
            html.Div(id='AFMText_tipradius', className='label_value'),
        ], className='label_container'),
        dcc.Slider(id='AFMSlider_tipradius', className='slider', marks=None, min=1, max=25, step=0.01, value=6.25),

        html.Div([
            html.Div("Cantilever height (um)", className='label_name', id="AFMText_cantheightlabel"),
            html.Div(id='AFMText_cantheight', className='label_value'),
        ], className='label_container'),
        dcc.Slider(id='AFMSlider_cantheight', className='slider', marks=None, min=0, max=10, step=0.01, value=2.1),

        html.Div([
            html.Div("Cantilever area (um^2)", className='label_name', id="AFMText_cantarealabel"),
            html.Div(id='AFMText_cantarea', className='label_value'),
        ], className='label_container'),
        dcc.Slider(id='AFMSlider_cantarea', className='slider', marks=None, min=0, max=10000, step=10, value=3750),

    ], className= 'controls_container'),
], className='controls', hidden=True, id='display_BiasSweepExperimentcontrols')


################################################################################
################################################################################
# Time trace experiment cards

AFM_Card3 = dbc.Card([
    dbc.Row([
        dbc.Button("Calculate", id="AFMbutton_CalculateTimeExp", color="secondary", className="mr-1", style={'fontSize': 14, 'width':300}),
    ], style={'padding': 10}, justify="center"),

    dbc.Row([
        dbc.Col(dbc.Label("Sigma", id="AFMText_sigmalabel", style={"margin-left": "10px", "margin-top": "20px"}), md=8),
        dbc.Col(html.Div(id='AFMText_sigma', style = {'text-align': 'right', "margin-right": "10px", "margin-top": "20px"}), md=4),
    ], justify="between"),
    dbc.Row([
        dbc.Col(dcc.Slider(id='AFMSlider_sigma', marks=None, min=0, max=2, step=0.01, value=0.05), md=12),
    ]),

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


################################################################################
################################################################################
# Delay sweep experiment cards

AFM_Card4 = dbc.Card([
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
