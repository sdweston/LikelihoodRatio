Version 0.4

This is to start modifying the pipeline to deal with radio doubles and IR doubles.

The Radio Doubles can be handled as a pre-process as it doesn't use any of the LR values.
We use the region on the plot of F1/F2 vs Ang_Sep/log(F1+F2) 

F1/F2 				0.0 - 2.0
Ang_Sep/log(F1+F2)	2.0 - 20.0

These limits need to be explored and defined better.

For IR Doubles then we need the LR Reliability and Angular Separation (between IR objects), we are looking where :

LR-Rel 0.4 - 0.6
Ang_Sep is say 1" as we have a 10" search radius

We can have two IR objects with a similar LR-Rel and similar distance from the Radio Source but opposed,
to each other say one at 3" from the Radio Source at 2 O'Clock and the other at 3.1" at 6 O'Clock. So they
are clearly not related.

Need to use ATLAS_DR3 schema with normalised tables rather than the one big table:

field_cmpcat 				Full DR3 component catalogue
field_coords				DR3 component coords
field_deconv				DR3 component deconv values
field_name
field_radio_properties		DR3 component radio values
field_sindex

field_matches				DR3 working table for LR

This code runs through, still some issues:

1. cdfs it gets a value of Q0 > 1, but for elais Q0=0.752139

2. check handling of radio pairs