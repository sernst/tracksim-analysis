# Trackway Measurement Comparison

There are **{{ df_tracks.shape[0] }}** sauropod tracks in the A16 data 
set. A majority of them have at least one attribute (e.g. width, 
length, stride length, etc.) that was measured both directly in the field and indirectly from maps.

Having such a large data set containing two independent measurements for the same track attributes allows us to compare the two measurement techniques. If one technique is better than the other, a comparative analysis will reveal this.

Consider a track attribute $$ x $$ that was measured directly in the field and from a map. The value that was measured in the field is $$ x_f $$ and has a measurement uncertainty of $$ @sigma_f $$. The value that was measured from a map is $$ x_m $$ and has an uncertainty of
$$ @sigma_m $$. These deviation between these two measurements is then,

$$$
    @Delta_x = @frac
        { @left| x_f - x_m @right| }
        { @sqrt{ @sigma_f^2 + @sigma_m^2 } }
$$$

where the $$ @Delta_x $$ value quantifies the amount of deviation between the two measurements with respect to their uncertainties.

The deviations for all measurements of each track in the data set can be calculated in the same way.