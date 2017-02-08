## Precision Windowing

So far we've relied on forward-windowing for clustering gauges into segments,
but this is still a somewhat arbitrary choice. It actually becomes more 
arbitrary with the addition of uncertainty because values with higher 
uncertainty increase variance and allow the cluster to grow more greedily. 
Under the right circumstances this behavior is desired, but forward-windowing
is not the right one.

Instead we change the windowing algorithm to preference higher precision 
gauge values first. The way it works is that instead of starting at the 
beginning of the trackway, the windowing algorithm starts with the highest
precision (lowest uncertainty) value in the trackway. It then clusters
around that highest precision value in both the forward and reverse
directions always comparing the cluster median value against the forward or 
reverse value with the higher precision. The result is that the clustering
process preserves the maximum statistical precision from the underlining gauge 
values and eliminates the arbitrary biasing of the forward-windowing approach.