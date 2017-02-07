# Multi-Value Quantization

What we're really looking for in a gauge analysis is a measure
of distinct gauges within the trackway. There may only be one distinct gauge
value or there may be many for any given trackway. Properly quantifying gauges
are important for this search to be sufficiently scientifically rigorous.

Given the amount of noise that occurs in quadrupedal locomotion, it is not
readily apparent looking at most gauge plots what the statistically distinct 
values reside. One way to solve this problem is to introduce a clustering
algorithm that segments successive gauge values into similar groups. Each of
these segments can then be represented by the median of the constituent
gauge values.

To cluster the gauges values we use a forward windowing algorithm that compares
a current cluster of successive gauge values with the next value in the 
trackway. This comparator determines whether or not the next value should be
clustered with its predecessors. If the next value differs too much from the
cluster of previous gauge values, a new cluster is created and populated 
initially with the gauge value rejected from the previous cluster. The result 
is a number of distinct gauge segments, $$ N_s $$, for the trackway. The number
of segments will always be less than or equal to the number of tracks in
the trackway, $$ N_s @leq N_t $$.

For a better conceptual understanding of how this forward windowing algorithm
functions let's consider a few ideal trackway cases.

---
We'll begin by quantizing using the unweighted data. In order
to do this we need to come up with a quantization tolerance
because, as you can see in the plot, a certain amount of noise
exists in the gauge values from step to step. Already we have
to be somewhat arbitrary in the analysis. There is no completely
objective way to assign a tolerance in the absence of uncertainty
values. For this analysis we'll use fractional values of the width
of the track and see how those compare.
