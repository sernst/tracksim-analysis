# {{ TRACKWAY_NAME }} Gauge Quantization

A look at how an uncertainty-weighted analysis affects the 
outcome a trackway gauge analysis for the {{ TRACKWAY_NAME }}
trackway within the A16 data set.

We calculate the gauge for every pes track within the trackway using the most 
simple and geometrically objective construct available. This requires the use
of the two opposing pes limb tracks that appear sequentially before and after
the track for which we wish to calculate the gauge.

For any possible arrangement of these three tracks, it is possible to reduce 
the gauge measurement to a 1 dimensional problem with a simple linear algebra
transformation, $$ M_{RT} $$, that repositions the coordinate axis so that the
first of the opposing limb's tracks resides at the origin, $$ (0, 0) $$, and 
the second of the opposing limb's tracks resides on the y-axis at some 
distance, $$ d $$, from the origin, $$ (0, d) $$. The track of interest will
then be located within this localized coordinate system at the coordinate 
$$ (x, y) $$. The simple geometric gauge value within this localized coordinate
system is just the value of x, which is conceptually the distance between the 
y-axis and the track. This may appear trivial, but the y-axis is coincident 
with the stride line of the opposing limb's track-pairing.

This gauge value can then be plotted for each pes track in the trackway as a
function of the geometric distance of the track from the beginning of the 
trackway. The resulting graph for the {{ TRACKWAY_NAME }} trackway is shown
below.


