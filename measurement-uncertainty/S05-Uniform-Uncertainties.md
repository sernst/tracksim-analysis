## Uniformity of Relative Uncertainties

Standard statistical methods require that the measurements used must 
have similar relative uncertainties. What constitutes _similar_ depends 
on the specific problem in question and requires further investigation 
as it pertains to inchnology.

### Relative Uncertainty Spread

The relative uncertainty for a measurement, $$m @pm @sigma_m$$, is
defined as the ratio of absolute uncertainty and value:

$$$
    @sigma_{/_m} = @frac { @sigma_m } { m } 
$$$

Relative uncertainties can be calculated for any measurement and are
bounded to the range $$ (0, @infty) $$. They approach zero as
absolute uncertainties approach zero but can never be zero given that 
all  physical measurements have some amount of uncertainty. While there 
is no physically imposed upper boundary on this range, values that 
approach or exceed one must be handled with additional care.

As statistics deals with sets of measurements, we vectorize the relative 
uncertainty definition from above:
 
$$$
    @sigma_{/_M} = 
        @langle 
            @frac{ @sigma_{m,i} } { m_i } 
        @rangle
$$$

to describe the element-wise equation in terms of a measurement 
ensemble consisting of $$ N $$ measurements where:

$$$
    M = @langle m_i @rangle
$$$

The range of relative uncertainty values for an ensemble, 
$$ @vec{X} $$, can be quantified in terms of its spread:

$$$
    @Delta_{M} = max(M) - min(M)
$$$

The range of potential values for spreads is $$ [0, @infty) $$. A zero 
value indicates that all measurements in the ensemble, $$ @vec{X} $$, 
have identical relative uncertainties. The larger the spread
value, the less likely standard statistical methodologies can be used
to describe the ensemble.

We apply spread to the fundamental spatial measurements of track 
length and width. For each trackway in the A16 data set consisting of 
at least 10 tracks, we compute the relative uncertainty spread for the 
length and width measurements. We also reduce the two spreads by 
taking the larger one, 

$$$
    @Delta_{max} = max(@Delta_{length}, @Delta_{width})
$$$
