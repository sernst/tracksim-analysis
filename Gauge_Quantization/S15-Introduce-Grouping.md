## Grouping Segments

Now that we have arrived at a scientifically rigorous segmentation, we want to
cluster segments into groups of distinct values to ascertain how many 
distinctly different gauge values were observed within the trackway. We employ
the same statistical significance and precision ordering here to a final group
clustering algorithm. It works the same way that the segmentation algorithms
did except that it does not rely on contiguous values, but instead compares
each segment globally to the other segments when assigning groups.

This is trivial for the idealized shrinking gauge track above because the three
regions are distinct within the trackway already. It's the more complicated 
cases in real track data, especially long trackways, where this reduces
a potentially large number of segments to the statistically significant minimum.
