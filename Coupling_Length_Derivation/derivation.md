Derivation
==========

The midpoint, $$@gamma$$, between a pair pes or manus locators is given as,

$$$
    @gamma = @left(
        @frac{x_l + x_r} {2},
        @frac{y_l + y_r} {2}
    @right)      
$$$

and the coupling length, $$C@!L$$, is the distance two midpoints, one for the 
pes locators and one for the manus locators.

$$$
    C@!L = @sqrt{
        @left( x_{@gamma,pes} - x_{@gamma,manus} @right) ^ 2
        @left( y_{@gamma,pes} - y_{@gamma,manus} @right) ^ 2
    }
$$$

Applying those computations to the locators in the example trackway from above 
yields:

![Example Calculation](assets/trackway_coupling_length.svg)

So far the coupling length calculation appears to be identical to the 
gleno-acetabular distance (GAD) calculation. The differences begin when trying
to compute gait and duty cycle combinations without a four-limb support phase. 
In these cases, one or more position locators will always be in transition 
between tracks, which is not addressed by GAD. To calculate the coupling length
for such cases, the locator position for transitioning limbs is calculated 
using linear interpolation between the previous, 
$$ @left( x_{prev}, y_{prev} @right) $$ 
and upcoming, 
$$ @left( x_{next}, y_{next} @right) $$
track center positions,

$$$
    @Upsilon = @left( 
    @begin{array}{ c c }
        x_{prev} + @alpha @left( x_{next} - x_{prev} @right), @@
        y_{prev} + @alpha @left( y_{next} - y_{prev} @right)
    @end{array}    
    @right)
$$$

The $$@alpha$$ parameter represents a relative phase in the interval 
$$ @left[0, 1 @right] $$ and depends upon choice of gait and duty cycle. We 
restrict ourselves to non-aerial gaits where the duty cycle is greater than or 
equal to 50%. We adopt a pes-centric view and choose to measure the coupling 
length only when both pes are in support. For a duty cycle of 50%, this will 
occur only at 0% and 50% in the gait cycle when one pes makes ground contact 
while the other lifts off.

A Walk
------

In a symmetric walking gait, the left manus lifts off from the ground 
+25% after the left pes, the right manus -25% before the left pes and the right
pes 50% after the left pes. For a duty cycle of 50% the right manus will be
halfway through a transition as the left manus ends its support phase and the 
other two limbs are in support. Similarly the left manus will be halfway through 
its transition when the right pes ends its support phase and the other two limbs 
remain in support. For a walking gait with a duty cycle of 50%, 
$$ @alpha_{walk} @left( 50@% @right) = 0.5 $$. 

Longer duty cycles lead to higher $$ @alpha $$ values because the transition
phases of the cycle are shortened. This generalizes in a walk to,

$$$
    @alpha_{walk} = @frac { 0.25 } { 1.0 - DC }
$$$

where $$ DC $$ is the duty cycle. If the duty cycle is greater than or equal
to 75%, the transition for either manus will be over before the pes lifts off, 
such that $$ @alpha = 1 $$, and the solution reduces to the four-limb support 
case outlined above.

Generalized
-----------

The numerator in the $$ @alpha_{walk} $$ is called the &alpha;-phase and 
represents the relative phase between the in-transition manus and the pes that 
is about to enter its transition phase when the coupling length measurement is 
made. The general equation for $$ @alpha $$ is,

$$$
    @alpha @left( @phi_@alpha, DC @right) = @left@{
        @begin{array}{cl}
            1 & @text{if } @phi_@alpha @geq 1.0 - DC @@
            @frac { @phi_@alpha } { 1.0 - DC } & @text{otherwise}
         @end{array}
        @right.
$$$

For walking gaits the in-transition manus is contralateral to the reference 
pes ending its support phase and the &alpha;-phases are:

* **G1 Pacing Walk:** 0.375
* **G2 Walk:** 0.25
* **G3 Walking Trot:** 0.125 

For ambling gaits the in-transition manus is ipsilateral to the reference pes
ending its support phase and the &alpha;-phases are:

* **G5 Trotting Amble:** 0.375
* **G6 Amble:** 0.25
* **G7 Ambling Pace:** 0.125

The midpoint equation for the manus can be generalized in terms of track 
centers and phase, $$@alpha$$.

$$$
    @gamma_{manus} = @left(
        @frac{
            x_{@Upsilon1} + 
            x_{@Upsilon2,prev} + 
            @alpha @left( x_{@Upsilon2,next} - x_{@Upsilon2,prev} @right)
        } {2},
        @frac{
            y_{@Upsilon1} + 
            y_{@Upsilon1,prev} + 
            @alpha @left( y_{@Upsilon1,next} - y_{@Upsilon1,prev} @right)
        } {2}
    @right),
$$$

The track centers 
$$ @left( x_{@Upsilon1}, y_{@Upsilon1} @right) $$ and
$$ @left( x_{@Upsilon2}, y_{@Upsilon2} @right) $$ 
could be assigned to right or left tracks depending on the selected 
configuration. This formula reduces to the original midpoint 
formula if $$@alpha$$ is 0 or 1.

At this point it should be clear that coupling length is a discretely-sampled, 
periodic value within a trackway. It can be measured twice per gait cycle each
time a pes support cycle ends.
