# Semiconductors App

## Note: This code became a bit of a labyrinth and needs to be re-worked. For now, a simple self-contained script to plot the MIS capacitor is at MIScapacitor.py. 

This is an app to visualize semiconductor physics in the bulk and at the
surface of a material, and in particular what we measure in an ncAFM experiment.

It contains four parts:
1) app.py
2) Controls.py
3) Callbacks.py
4) Physics.py

![image](https://user-images.githubusercontent.com/78166226/137530831-f0839dd7-0b16-4b0a-bd7e-f58d1dd25bc6.png)

app.py is the hub. This is the script that runs the app (so to run the app, run
app.py). It sets the layout (set in Controls.py) and calls Callbacks (set in
Callbacks.py). The layout defines appearance of the app, and the callbacks
define how the app updates with user interaction.

Controls.py defines the initial values, appearance, and layout of the controls
(e.g. buttons / sliders) in the app. The script itself is called in the layout
section of app.py, but each separate control is also called by callbacks in
app.py.

Callbacks.py defines what to do when a user interacts with the controls. The
script itself is called in the callbacks section of app.py.

Physics scripts contain all of the actual physics behind the app. Some physics
scripts are very fundamental (e.g. semiconductor equations) while others are
more applied (e.g. how to draw a band diagram). Any calculation that needs to be
called in a Callback must be inside a function so that the calculation is
re-done every time the Callback is called (by updating a control). Below is the 
dependency order of the Physics scripts:
1. Semiconductors
2. SurfacepotForce
3. BandDiagram
4. AFMoscillation
5.  FreqshiftDissipation

This app contains multiple tabs. I let each tab have its own Controls.py and
Callbacks.py scripts, for their own tab-specific functions. Separating things
out this way introduces a lot of redundancy in the code (as does writing the
callbacks in Callbacks.py instead of app.py), but I find this improves
readability.

Note that in Physics functions, I included all available slider values as inputs
even if they aren't needed in the function. This just helped me keep things
(e.g. order of variables in functions) consistent and in my head it's neater and
easier to read, though it's probably slower.


