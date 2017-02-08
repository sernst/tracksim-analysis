## Normality

Normality describes how well a measurement ensemble conforms to a 
Normal, Gaussian distribution. A lot of standard statistics methods 
rely on this assumption the normality. And while small deviations from
normal are to be expected for real measurements, too much deviation 
suggests something in the data that cannot be adequately described by 
these standard statistical methods.

There are many ways to test for the normality of a distribution, but 
many of them are unreliable because non-normal distributions can 
exhibit attributes of normality. The most robust test of normality 
requires comparing the distribution to one created by fitting a 
Gaussian curve to that distribution.

This Guassian-fit distribution can be calculated from the mean, 
$$ @overline{M} $$, and standard deviation, 
$$ @sigma_{_{@overline{M}}} $$ of a measurement ensemble, $$ M $$, and 
applying those values to the Gaussian (Normal) function:

$$$
    f_{norm}(x, @overline{M}, @sigma_{_{@overline{M}}}) = 
        @frac 
            { 1 } 
            { @sqrt{2 @pi @sigma_{_{@overline{M}}}^2} }
        e^{
            -@frac 
                { (x - @overline{M})^2 }
                { 2 @sigma_{ _{@overline{M}} }^2 }
        }
$$$

We can determine the difference of the distribution and its Gaussian-fit
distribution by calculating the area of deviation between the two 
curves as:

$$$
    @Delta_{_A} = 
        1 -
        @frac {1} {2}
        @int_{-@infty}^{@infty} | f(x) - f_{norm}(x) | dx
$$$

If the distribution is perfectly normal, the area of deviation, 
$$ @Delta_{_A} $$, will be one. If the reverse is true, the area of 
deviation will be zero. For this to work we need to be able to describe 
the distribution in an effectively continuous manner, which is not 
possible with just discrete measurements and histograms. A Kernel 
Density Function (KDF) is needed that redefines the discrete 
distribution as a smooth, continuous one. Kernel density functions are 
defined in terms of their measurement ensemble as:

$$$
    f_{_{KDF}}(x) = 
        @frac {1} {N}
        @sum_{i=0}^N f_{kernel}(x, m_i, @sigma_{m,i}) 
$$$

where $$ @sigma_{m,i} $$ is the uncertainty in the measurement, 
$$ m_i $$. For measurements that do not specify their uncertainties, 
which is an oversight as all physical measurements have uncertainty,
the $$ @sigma_{m,i} $$ is determined using a statistical technique 
called Kernel Density Estimation (KDE) that is applied uniformly to
all measurements in the ensemble.

The Normal, Gaussian function defined above is the most commonly 
used kernel function for $$ f_{kernel} $$. It is appropriate under the 
assumption that each measurement in the ensemble was acquired without
systematic biases such that the uncertainty is due only to random 
errors.
