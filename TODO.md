
Figure out a better numerical solution method
(Currently have runtime warnings from SurfacepotForce fsolve.)
(Might be able to get rid of it by rewriting Vs equation to get rid of large #s)

Check units for Efield and Charge

Check units for bulk - shouldn't need the division in CallbacksBulk

converting between n-type to p-type is a mess: I need a toggle like the bulk
situation which forces one or the other to zero.

Dissipation and freqshift prefactors are wrong.

Add save buttons everywhere.
Or at least organize saving better.

Rephrase "hop" units and the RTN stuff is almost outdated.
