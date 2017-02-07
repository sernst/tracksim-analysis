# Introduce Uncertainty

Next we add uncertainty to the gauge values and plot the results for the
same {{ TRACKWAY_NAME }} trackway.

To calculate the uncertainty for a given gauge value, we need to make
sure that we properly include the contributing uncertainties for all three 
tracks used in determining a particular gauge value. While it may seem valid
to use the x-position uncertainty for the track by itself, this is incorrect.
It ignores the fact that there is uncertainty in the positions of the two
tracks of the opposing limb. Those two positions are used to carry out the
transformation into the localized coordinate systems needed to ascertain gauge
values. We must, therefore, properly include those uncertainties as well.

To do that we use the generalized formula for the distance between a point and
a line defined by two points, which is:

$$$
    d = @frac
        { @big| x @cdot (y_2 - y_1) - y @cdot (x_2 - x_1) + x_2 y_1 - y_2 x_1 @big| }
        { @sqrt{ (y_2 - y_1)^2 + (x_2 - x_1)^2 } }
$$$

where $$ (x_1, y_1) $$ and $$ (x_2, y_2) $$ are the positions the opposing 
limb's tracks that define the stride line and $$ (x, y) $$ is the position of
the track on which we are calculating the gauge. The error in distance can
then be calculated using standard error propagation techinques as:

$$$
    @delta d = @Big| @frac{ @partial d } { @partial x } @delta x @Big| +
        @Big| @frac{ @partial d } { @partial y } @delta y @Big| +
        @Big| @frac{ @partial d } { @partial x_1 } @delta x_1 @Big| +
        @Big| @frac{ @partial d } { @partial y_1 } @delta y_1 @Big| +
        @Big| @frac{ @partial d } { @partial x_2 } @delta x_2 @Big| +
        @Big| @frac{ @partial d } { @partial y_2 } @delta y_2 @Big|
$$$

where $$ @delta d $$, $$ @delta x $$, $$ @delta y $$, $$ @delta x_1 $$, 
$$ @delta y_1 $$, $$ @delta x_2$$ and $$ @delta y_2 $$ are the uncertainties
in each of their respective values. These uncertainty values can then be
calculated from the uncertainties in the positions of tracks to yield an
uncertainty in that gauge value. Rather than dwell on the mathematical 
derivation of the general uncertainty equation, we will look at visualizing
the uncertainties as an example.
