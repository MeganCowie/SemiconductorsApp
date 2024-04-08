from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
import dash_daq as daq

################################################################################
################################################################################

Surface_Card = html.Div([

    html.Div([
        html.Div(id='SurfaceText_regime', className = 'readout_large'),

        html.Div([
            html.Div("Gate Bias (eV)", className='label_name', id="SurfaceText_Vglabel"),
            html.Div(id='SurfaceText_Vg', className='label_value'),
        ], className='label_container'),
        dcc.Slider(id='SurfaceSlider_Vg', className='slider', marks=None, min=-10, max=10, step=0.1, value=-1.4),

        html.Div([
            html.Div("Alpha", className='label_name', id="SurfaceText_alphalabel"),
            html.Div(id='SurfaceText_alpha', className='label_value'),
        ], className='label_container'),
        dcc.Slider(id='SurfaceSlider_alpha', className='slider', marks=None, min=0, max=1, step=0.01, value=0),

        html.Div([
            html.Div("Insulator Thickness (nm)", className='label_name', id="SurfaceText_zinslabel"),
            html.Div(id='SurfaceText_zins', className='label_value'),
        ], className='label_container'),
        dcc.Slider(id='SurfaceSlider_zins', className='slider', marks=None, min=0.001, max=100, step=0.1, value=5.2),
    ], className= 'controls_container'),

    html.Div([
        html.Div([
            html.Div(id='SurfaceText_typen',className='toggle-left'),
            daq.ToggleSwitch(id='SurfaceToggle_type',className='toggle-switch', value=True),
            html.Div(id='SurfaceText_typep', className='toggle-right'),
        ], className='toggle_container'),

        html.Div([
            html.Div("Band Gap (eV)", className='label_name', id="SurfaceText_Eglabel"),
            html.Div(id='SurfaceText_Eg', className='label_value'),
        ], className='label_container'),
        dcc.Slider(id='SurfaceSlider_Eg', className='slider', marks=None, min=0.1, max=12, step=0.1, value=1.5),

        html.Div([
            html.Div("Rel. Permittivity (S)", className='label_name', id="SurfaceText_epsilonsemlabel"),
            html.Div(id='SurfaceText_epsilonsem', className='label_value'),
        ], className='label_container'),
        dcc.Slider(id='SurfaceSlider_epsilonsem', className='slider', marks=None, min=0.1, max=22, step=0.1, value=5.9),

        html.Div([
            html.Div("Work Func. (M) (eV)", className='label_name', id="SurfaceText_WFmetlabel"),
            html.Div(id='SurfaceText_WFmet', className='label_value'),
        ], className='label_container'),
        dcc.Slider(id='SurfaceSlider_WFmet', className='slider', marks=None, min=0.1, max=8, step=0.01, value=4.1),

        html.Div([
            html.Div("Elec. Affinity (S) (eV)", className='label_name', id="SurfaceText_EAsemlabel"),
            html.Div(id='SurfaceText_EAsem', className='label_value'),
        ], className='label_container'),
        dcc.Slider(id='SurfaceSlider_EAsem', className='slider', marks=None, min=0.1, max=5, step=0.01, value=3.5),

        html.Div([
            html.Div("Donors (cm-3)", className='label_name', id="SurfaceText_donorlabel"),
            html.Div(id='SurfaceText_donor', className='label_value'),
        ], className='label_container'),
        dcc.Slider(id='SurfaceSlider_donor', className='slider', marks=None, min=25, max=40, step=0.001, value=30),

        html.Div([
            html.Div("Acceptors (cm-3)", className='label_name', id="SurfaceText_acceptorlabel"),
            html.Div(id='SurfaceText_acceptor', className='label_value'),
        ], className='label_container'),
        dcc.Slider(id='SurfaceSlider_acceptor', className='slider', marks=None, min=25, max=40, step=0.001, value=0, disabled=True),

        html.Div([
            html.Div("Elec. Eff. Mass (me)", className='label_name', id="SurfaceText_emasslabel"),
            html.Div(id='SurfaceText_emass', className='label_value'),
        ], className='label_container'),
        dcc.Slider(id='SurfaceSlider_emass', className='slider', marks=None, min=0.1, max=2, step=0.1, value=1.0),

        html.Div([
            html.Div("Hole Eff. Mass (me)", className='label_name', id="SurfaceText_hmasslabel"),
            html.Div(id='SurfaceText_hmass', className='label_value'),
        ], className='label_container'),
        dcc.Slider(id='SurfaceSlider_hmass', className='slider', marks=None, min=0.1, max=2, step=0.1, value=1.0),

        html.Div([
            html.Div("Temperature (K)", className='label_name', id="SurfaceText_Tlabel"),
            html.Div(id='SurfaceText_T', className='label_value'),
        ], className='label_container'),
        dcc.Slider(id='SurfaceSlider_T', className='slider', marks=None, min=10, max=500, step=1, value=300),
    ], className= 'controls_container'),

    html.Div([
        html.Div([
            html.Div([
                html.Div("Intrinsic Density (cm-3)", id="SurfaceText_nilabel", className='readout_name'),
                html.Div(id='SurfaceText_ni', className = 'readout_value'),
            ], className = 'readout_container'),
            html.Div([
                html.Div("Debye Length (nm)", id="SurfaceText_LDlabel", className='readout_name'),
                html.Div(id='SurfaceText_LD', className = 'readout_value'),
            ], className = 'readout_container'),
            html.Div([
                html.Div("Spacecharge Width (nm)", id="SurfaceText_zQlabel", className='readout_name'),
                html.Div(id='SurfaceText_zQ', className = 'readout_value'),
            ], className = 'readout_container'),
        ], className= 'readout_small'),
    ], className= 'controls_container'),

    html.Div([
        html.Div([
            html.Div("Presets", id="SurfaceText_Presets"),
            dcc.RadioItems(id="SurfaceButtons_presets", options=[
                {'label': '   Silicon_A', 'value': 2},
                {'label': '   Figure_ntype', 'value': 8},
                {'label': '   Silicon_B', 'value': 3},
                {'label': '   Figure_ptype', 'value': 9},
                {'label': '   Silicon_C', 'value': 4},
                {'label': '   MoSe2', 'value': 1},
                {'label': '   Silicon_D', 'value': 5},
                {'label': '   Pentacene', 'value': 7},
                {'label': '   Silicon_E', 'value': 6},
                {'label': '   Other', 'value': 0}
                ]
            ,value=2, labelStyle={"width": '50%','display': 'inline-block'}),
        ], className='presets_container'),

        html.Div([
            html.Div("Gate Bias Precision", className='label_name', id="SurfaceText_biasstepslabel"),
            html.Div(id='SurfaceText_biassteps', className='label_value'),
        ], className='label_container'),
        dcc.Slider(id='SurfaceSlider_biassteps', className='slider', marks=None, min=56, max=1024, step=56, value=56),

        html.Div([
            html.Div("Insulator Thickness Precision", className='label_name', id="SurfaceText_zinsstepslabel"),
            html.Div(id='SurfaceText_zinssteps', className='label_value'),
        ], className='label_container'),
        dcc.Slider(id='SurfaceSlider_zinssteps', className='slider', marks=None, min=56, max=1024, step=56, value=56), 
    ], className= 'controls_container'),


], className='controls', hidden=True, id='display_SurfaceCarrierStatisticscontrols')
