import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_daq as daq

################################################################################
################################################################################
# ncAFM cards

AFM_Card1 = dbc.Card([
    dbc.Row([
        dbc.Button("Calculate", id="AFMbutton_Calculate", color="secondary", className="mr-1", style={'fontSize': 14, 'width':300}),
    ], style={'padding': 10}, justify="center"),
],style={"width": "400px"})

AFM_Card2 = dbc.Card([
    dbc.FormGroup([
        dbc.Row([
            dbc.Col(dbc.Label("Gate Bias (eV)", id="AFMText_Vglabel", style={"margin-left": "10px", "margin-top": "20px"}), md=8),
            dbc.Col(html.Div(id='AFMText_Vg', style = {'text-align': 'right', "margin-right": "10px", "margin-top": "20px"}), md=4),
        ], justify="between"),
        dbc.Row([
            dbc.Col(dcc.Slider(id='AFMSlider_Vg', min=-10, max=10, step=0.1, value=0,), md=12),
        ]),
        dbc.Row([
            dbc.Col(dbc.Label("Insulator Thickness (nm)", id="AFMText_zinslabel", style={"margin-left": "10px"}), md=8),
            dbc.Col(html.Div(id='AFMText_zins', style = {'text-align': 'right', "margin-right": "10px"}), md=4),
        ], justify="between"),
        dbc.Row([
            dbc.Col(dcc.Slider(id='AFMSlider_zins', min=1, max=25, step=1, value=5,), md=12),
        ]),
        dbc.Row([
            dbc.Col(dbc.Label("Amplitude (nm)", id="AFMText_amplitudelabel", style={"margin-left": "10px"}), md=8),
            dbc.Col(html.Div(id='AFMText_amplitude', style = {'text-align': 'right', "margin-right": "10px"}), md=4),
        ], justify="between"),
        dbc.Row([
            dbc.Col(dcc.Slider(id='AFMSlider_amplitude', min=1, max=20, step=1, value=6,), md=12),
        ]),
    ]),
],style={"width": "400px"})


AFM_Card3 = dbc.Card([
    dbc.Row([
        dbc.Col(html.Div(id='AFMText_semiconducting'),  md=3),
        dbc.Col(daq.ToggleSwitch(id='AFMtoggle_sampletype', value=False), md=6),
        dbc.Col(html.Div(id='AFMText_metallic'),  md=3),
    ], style={'padding': 10}),
],style={"width": "400px"}),

AFM_Cards1 = [dbc.Col(AFM_Card1), dbc.Col(AFM_Card2), dbc.Col(AFM_Card3)]


################################################################################
################################################################################
# Bias experiment cards

AFM_Card1 = dbc.Card([
    dbc.Row([
        dbc.Button("Calculate", id="AFMbutton_CalculateBiasExp", color="secondary", className="mr-1", style={'fontSize': 14, 'width':300}),
    ], style={'padding': 10}, justify="center"),
],style={"width": "400px"})


AFM_Card2 = dbc.Card([
    dbc.FormGroup([
        dbc.Row([
            dbc.Col(dbc.Label("Resonant Frequency (Hz)", id="AFMText_resfreqlabel", style={"margin-left": "10px", "margin-top": "20px"}), md=8),
            dbc.Col(html.Div(id='AFMText_resfreq', style = {'text-align': 'right', "margin-right": "10px", "margin-top": "20px"}), md=4),
        ], justify="between"),
        dbc.Row([
            dbc.Col(dcc.Slider(id='AFMSlider_resfreq', min=200000, max=400000, step=10000, value=300000,), md=12),
        ]),
        dbc.Row([
            dbc.Col(dbc.Label("Spring Constant (N/m)", id="AFMText_springconstlabel", style={"margin-left": "10px"}), md=8),
            dbc.Col(html.Div(id='AFMText_springconst', style = {'text-align': 'right', "margin-right": "10px"}), md=4),
        ], justify="between"),
        dbc.Row([
            dbc.Col(dcc.Slider(id='AFMSlider_springconst', min=30, max=50, step=1, value=42,), md=12),
        ]),
        dbc.Row([
            dbc.Col(dbc.Label("Q factor", id="AFMText_Qfactorlabel", style={"margin-left": "10px"}), md=8),
            dbc.Col(html.Div(id='AFMText_Qfactor', style = {'text-align': 'right', "margin-right": "10px"}), md=4),
        ], justify="between"),
        dbc.Row([
            dbc.Col(dcc.Slider(id='AFMSlider_Qfactor', min=200, max=30000, step=100, value=20000,), md=12),
        ]),
        dbc.Row([
            dbc.Col(dbc.Label("Tip Radius (nm)", id="AFMText_tipradiuslabel", style={"margin-left": "10px"}), md=8),
            dbc.Col(html.Div(id='AFMText_tipradius', style = {'text-align': 'right', "margin-right": "10px"}), md=4),
        ], justify="between"),
        dbc.Row([
            dbc.Col(dcc.Slider(id='AFMSlider_tipradius', min=1, max=20, step=1, value=2,), md=12),
        ]),
    ]),
],style={"width": "400px"})

AFM_Cards2 = [dbc.Col(AFM_Card1), dbc.Col(AFM_Card2)]
