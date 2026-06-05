---
title: Sunrise Clock
category: "Hardware · 3D"
accent: clay
summary: "Mechanical Sunrise Sunset Clock - 24-hour sweeping hand plus sunrise and sunset indicators that change throughout the year"
date: 2025-12
featured: true
order: 2
cover: sunriseclock/cover.png
links:
  - label: MakerWorld
    url: "https://makerworld.com/en/models/2465134-mechanical-sunrise-clock#profileId-2705952"
    icon: printer
tech: [Fusion 360, A1 Mini, "3D printing"]
---


## What it is

A 24-hour wall clock with a single hand, plus two indicators that track sunrise
and sunset times throughout the year. Midnight at the 6 o'clock position, noon at top. 

The hour hand reads as a 'how far through the daylight' indicator - the arc between the two markers is today's daylight.

![Face](/static/img/projects/sunriseclock/Face.png)

## How it works

The clock is driven by a standard 12-hour quartz movement. From it, two independent gear chains do separate jobs.
The first drives the hour hand (one revolution in 24h). A single 2:1 reduction (15T → 30T) turns the 12h drive into 24h, 
with an idler gear to make sure the hour hand rotates clockwise.

![24h-chain-annotated](/static/img/projects/sunriseclock/24h-chain.png)

The second chain drives the year rotation. Six 3:1 stages (15T → 45T) multiply to \(3^6 = 729{:}1\), turning the 12h input 
to 8748h - within half a day of the true 8760 hours in a year.

![annual-chain](/static/img/projects/sunriseclock/annual-chain.png)

Two cams are mounted on a shaft fixed to the annual rotation, each shaped to the exact sunrise or sunset curve for the 
clock's location. As the cam rotates, its variable radius raises and lowers a follower arm. A sector gear at the arm's 
pivot meshes with a small gear in the centre, amplifying that small angular rotation into the full desired 
sweep of the indicators. 

![cam-arm-indicator-flow](/static/img/projects/sunriseclock/cam-arm-indicator.png?v=1)

## Astronomy behind the cam shapes

Sunrise and sunset times change throughout the year - long days in summer, short in winter. This seasonal effect is because the 
Earth is tilted on its spinning axis by \(23.4^\circ\). On its own this effect is straightforward and predictable: daylight 
hours would vary smoothly and symmetrically through the year, and a regular oval cam would reproduce it perfectly.

However, **the sunrise and sunset curves aren't symmetric**. The shortest day is the winter solstice, around 21 December. 
But that isn't the day the sun sets earliest or rises latest. In the UK the earliest sunset is around 12 December, and the 
latest sunrise around 30 December. So for two weeks before Christmas the evenings are already on their way towards spring 
while the mornings are still darkening.[^evenings]

[^evenings]: The latest sunrise / earliest sunset divergence around the solstice is particularly well explained 
in [The evenings are drawing out already](https://explainingscience.org/2019/12/13/the-evenings-are-drawing-out-already-2/), 
Explaining Science (2019).

This is because there is another astronomical phenomenon also contributing to the time that the sun rises and sets - 
**The Equation of Time**: the deviation of the Sun from regular clock-time. The Sun runs slightly fast or slow 
against the clock depending on the season, coming from the Earth's tilt and elliptical orbit acting together. Because the 
Earth's orbit is an ellipse, the Earth speeds up as it orbits closer to the Sun in January and slows as it orbits further 
from the Sun in July - **Kepler's Second Law**. 

<object type="image/svg+xml" data="/static/img/projects/sunriseclock/kepler-viz.svg?v=1"
        width="100%" class="cam-viz"
        style="display:block; max-width:170px; margin-inline:auto; aspect-ratio:420 / 320;"
        aria-label="Kepler's Second Law: a planet moving faster near the Sun and slower when far away">
  <img src="/static/img/projects/sunriseclock/fallback-image.png" alt="An elliptical orbit with the Sun at one focus">
</object>

The equation of time emerges because each day the Earth must turn slightly more than a full \(360^\circ\) to bring the sun 
back to the same point in the sky. The amount of extra rotation needed each day depends on the orbital speed, which 
in turn depends on which part of the orbit the Earth is in. So the equation of time varies throughout the seasons.

```
Day 1:  Earth at position A
        🌍 → rotates 360°
        Sun appears at noon
        
Day 2:  Earth has moved in orbit
        🌍 → must rotate 360° + 1° to get sun back to noon
        (The extra 1° depends on orbital speed)
```   

When Earth is moving *fast* (January - perihelion), the Earth travels further along orbit each day and must rotate *more* to bring sun back to noon; Solar day is *longer* than average and Sunrise/sunset times relative to the clock drift *later* with each passing day. When Earth is moving *slow* (July - aphelion): the Earth travels less far along orbit each day and needs less extra rotation to get back to noon. The solar day is *shorter* than average and Sunrise/sunset times relative to the clock drift *earlier* with each passing day.

Add together this contribution from the equation of time and the seasonal variation from axial tilt, and you get two 
independent astronomical phenomena combining in complex ways. **Axial tilt sets how long the day is (symmetric), and the 
equation of time shifts where it sits on a fixed clock (the asymmetry)**. The resulting observation is that, for the same 
clock time each day of the year, the Sun never sits in quite the same spot; instead it traces a distorted figure-of-eight. 
That shape is the **analemma**: the equation of time made visible, etched into the sky. 

The shapes below represent the Sun's position at noon across a one-year period. Up–down is how high the Sun climbs in the sky, 
rising and falling once a year (high in summer, low in winter). The central vertical line on each diagram is due south - 
**solar noon**; the Sun perfectly in sync with clock-time would always appear due south at exactly 12:00pm. Therefore any 
side-to-side variation away from the centre line (left-right) represents the solar noon being ahead of or behind the clock noon.  

![analemma-decomposition](/static/img/projects/sunriseclock/analemma-decomposition.svg?v=1)

- Axial tilt makes the Sun run fast at the solstices and slow at the equinoxes: *fast, slow, fast, slow*, twice a year. That
  twice-yearly period draws a clean, symmetric figure-8.
- The elliptical orbit speeds the Sun up and slows it down just once a year: *fast, slow* (Kepler's Second Law), tracing a
  single slim, tilted loop.
- Added together, Kepler's elliptical orbit loop reinforces the symmetric figure-8 on one side of the year and cancels out on
  the other. One figure-8 loop swells and the other shrinks. That lopsided figure-of-8 is the analemma we actually see in the
  sky:

<figure markdown="1">
![analemma-real](/static/img/projects/sunriseclock/analemma-real.png)
<figcaption>The Sun photographed at the same time of day for one year, via the Vatican Observatory's
<a href="https://www.vaticanobservatory.org/sacred-space-astronomy/the-analemma-and-the-darkest-evening/">The Analemma and the 
  Darkest Evening</a>.</figcaption>
</figure>

The complex interaction of these effects are also what pushes the earliest sunset and latest sunrise to *opposite* sides of 
the solstice. Sunrise and sunset sit on opposite sides of *solar* midday (not the clock 12:00pm), and solar midday is still 
drifting later through the end of December.

<details><summary>Further explanation</summary>
  After the winter solstice the days are lengthening, so sunrise <em>should</em> start getting earlier; but the second factor - 
  the equation of time - is still dragging solar noon later even after the solstice.   That wins for another week, holding 
  sunrise back until its latest point around 30 December. The same interaction works the other way at dusk, the equation of 
  time turning sunset around before the solstice, near 12 December.
</details> 

**This is where the cam shapes come in**. The profiles are generated from a year of real sunrise and sunset data, each cam 
tailored to a specific location. So the axial tilt, the equation of time, Kepler's Second Law, and the analemma are all programmed 
into the shape.

<img src="/static/img/projects/sunriseclock/camshapes-translucent.png?v=1"
     alt="cam shapes"
     class="bare"
     style="display:block; max-width:260px; margin-inline:auto;">

<details><summary>A short history</summary>
<ul>
<li><strong>c. 150 CE — Ptolemy.</strong> Noticed the Sun didn't keep even time and
gave the first method to convert sundial time into steady clock time. He could correct
for the wobble without knowing its cause.</li>
<li><strong>c. 1000 CE — Islamic astronomers.</strong> Ibn Yunus, in Cairo, sharpened
Ptolemy's solar tables and corrected his figures. Still no explanation.</li>
<li><strong>1609 — Kepler.</strong> Arrives with the "why." His <em>Astronomia Nova</em>
showed the orbit is an ellipse and that Earth speeds up as it nears the Sun - his
first and second laws - explaining the once-a-year part of the wobble. The
twice-a-year part, from the axial tilt, had been geometry since antiquity.</li>
<li><strong>1656 — Huygens.</strong> Built the pendulum clock: the first timekeeper
steady enough to make the Sun drift against it. Up to about a quarter-hour over
the year - plainly visible.</li>
</ul>
</details>

## Design Story

![design-photo](/static/img/projects/sunriseclock/design1.png?v=1)

To accurately reproduce the daylight hours, the cam shape has to carry all of the astronomical 
effects from the previous section. Although, you don't actually need to understand any of 
the astronomy to arrive at the correct shape. It follows a two-step process:

1. Size the mechanism: work backwards from the clock face to find the cam throw that gives the indicator its correct sweep
1. Generate the profile: sample a year of real sunrise times and turn each into a radius
   
### Working backwards from the clock face

Four properties describe the mechanism - the arm length \(L\), the cam's **throw** \(t\)
(the difference between its largest and smallest radius), the gear ratio \(G\) (sector
teeth ÷ centre teeth), and the indicator's **sweep** \(S\). The design problem is to pick each property so the indicator sweeps exactly the right amount. 
The key is to work backwards, starting from the desired indicator sweep and tracing the mechanism back to work 
out the necessary cam throw.

[image]

Take the year's absolute earliest and latest sunrise. For example, sunrise at 03:35 and 08:16 GMT,
i.e. decimal time of 3.58 and 8.27[^decimal] - the indicator must sweep across that spread. Expressed as a fraction
of the full 24-hour dial, the sunrise indicator's total rotation over the year needs to 
be \(70.3^\circ\):

[^decimal]: Converting times to decimal format e.g 3:45am → 3.75 makes doing calculations much easier 

\[S = \frac{8.27 - 3.58}{24}\times 360^\circ = \approx 70.3^\circ\]

A gear ratio between the sector and the centre amplifies the sector's rotation, so the sector itself only needs to 
turn a fraction of the indicator's full sweep. The higher the ratio, the less the cam has to lift.[^ratios]  At 4:1, the sunrise sector 
only needs to rotate (17.6^\circ) to drive the full (70.3^\circ) at the centre:

[^ratios]: Some trial and error landed on 4:1 for sunrise and 6:1 for sunset, which gave sensible cam dimensions. Having different ratios means the sector pivots can be fixed at different points, avoiding 
having to design the support frame with complicated overlaps.

\[\theta = \frac{S}{G} = \frac{70.3^\circ}{4} \approx 17.6^\circ\]

For the sector arm to rotate, it must be fixed at one end and lifted at the other. To achieve the
\(17.6^\circ\) rotation at the pivot point, the 80mm arm needs to raised by 25.3mm:

<object type="image/svg+xml" data="/static/img/projects/sunriseclock/lift-viz.svg?v=1"
        width="100%" class="cam-viz"
        style="display:block; max-width:420px; margin-inline:auto; aspect-ratio:480 / 340;"
        aria-label="The follower arm lifting: throw t equals arm length times tangent of theta">
  <img src="/static/img/projects/sunriseclock/fallback-image.png" alt="A right triangle showing the follower arm lifting through angle theta">
</object>

\[t = L\tan\theta = 80\,\text{mm}\times\tan 17.6^\circ \approx 25.3\,\text{mm}\]

Finally, the **throw** is the difference between the cam's largest and smallest radius. It's what determines how much 
the follower arm resting on the cam raises and lowers by - and we know the arm needs to be raised
by \(t = 25.3mm\). The largest radius \(R_{\max}\) is set by the space available for the cam in the mechanism 
(about 41 mm). For a 25.3mm throw, the minimum radius has to be 15.7mm:

\[R_{\min} = R_{\max} - t \approx 41\,\text{mm} - 25.3\,\text{mm} \approx 15.7\,\text{mm}\]

Sunset runs through the same steps; its annual spread is slightly wider (about 4.8 h → \(72^\circ\)), 
and its 6:1 ratio needs a smaller throw to achieve the same sweep:

\[\begin{aligned}
\theta &= \frac{72^\circ}{6} = 12^\circ \\[9pt]
t &= 80\,\text{mm}\times\tan 12^\circ \approx 17.0\,\text{mm} \\[9pt]
R_{\min} &\approx 24\,\text{mm}
\end{aligned}\]

<details markdown="1"><summary>The one assumption</summary>
  
The follower's contact point on the cam is assumed to rise by exactly the cam's change in radius, staying a fixed 
80 mm from the pivot. It doesn't, quite: as the arm swings up the contact point creeps inside 80 mm, and as it 
swings down, outside. But with an 80 mm arm against a ~20 mm throw, the angle stays small, and the error is only a 
few percent.
</details>

### Generating the cam profile

With the cam's minimum and maximum radii determined, what's left is to plot the cam's actual shape. The cam is mounted onto a shaft that rotates
once per year, so the year maps onto a \(360^\circ\) circle. Sample at 24 equal points, about 15 days apart \(365.25/24 = 15.21\text{ days}\), 
and set the summer solstice (21 June) as the starting point. The method is then simply:

1. Look up the real sunrise (or sunset) time at each of the 24 dates.
1. Turn each time into a radius, with latest sunrise = min radius, earliest = max
   **(and the reverse for sunset)**.
1. Fit a smooth spline through the 24 radii. That curve is the cam edge.

<object type="image/svg+xml" data="/static/img/projects/sunriseclock/build-viz.svg?v=2"
        width="100%" class="cam-viz"
        style="display: block; max-width:400px; margin-inline:auto; aspect-ratio: 640 / 600;"
        aria-label="Building the cam from 24 samples and a spline">
  <img src="/static/img/projects/sunriseclock/fallback-image.png" alt="The sunrise cam shape, built from 24 sampled points">
</object>

Because every radius comes from a *real* sunrise time, the cam inherits every effect from the astronomy section. 
You don't actually need to understand any of the astronomy; the data already contains it.

<object type="image/svg+xml" data="/static/img/projects/sunriseclock/sweep-viz.svg?v=2"
        width="100%" class="cam-viz"
        style="display: block; aspect-ratio: 1000 / 470;"
        aria-label="A year of sunrise times, wrapped onto the cam">
  <img src="/static/img/projects/sunriseclock/fallback-image.png" alt="A year of sunrise times wrapped onto the cam">
</object>

One detail comes out of this - the June 21 solstice was deliberately plotted at \(0^\circ\), and the winter solstice at \(180^\circ\). But the 
maximum cam radius was defined as the *earliest sunrise* and the min radius as the *latest sunrise*. The latest sunrise 
happens *after* the winter solstice - you can see it on the cams here:

[image]

The cam's fattest point sits slightly off \(0^\circ\), and its narrowest just past the \(180^\circ\) position. That small offset frozen into the
shape, is the **equation of time made physical** - the same lopsidedness from the analemma, now in the cam's silhouette.

The sunset cam follows the same process, just with a slightly different min & max radius range. 24 sunset times, 
each converted to a radius, draw a spline through the points.  With one difference I didn't spot...
 
### What I got wrong

Through the year the two hands have to move in **opposite** directions - toward summer, sunrise gets earlier (indicator anticlockwise) while sunset gets later (indicator clockwise). But both cams are fixed to the same shaft, turning the same direction, and a growing cam radius always pushes its follower the same way. But at first I built both cams the same way: setting the largest radius at the summer solstice. After assembling the clock, I set the cam positions to the winter solstice, set the sunrise and sunset indicators at about the right times, and wound the year forward. The sunrise indicator started at about 8am and moved slowly back (correctly) to 7:30am, 7am.... The sunset indicator started at about 4pm and also started slowly moving backwards, to 3pm, 2pm, 1pm.... !
  
The fix was to invert the sunset cam: put its **minimum** radius at the summer solstice instead of its maximum. Now as the shaft turns toward summer the sunrise cam's radius grows while the sunset cam's shrinks, and the indicators sweep in the correct directions. The rule is *earlier in the day → larger cam radius*. Applied correctly, the earliest sunrise (June) and the earliest sunset (December) sit on **opposite sides of the year**. So the sunrise cam's largest radius should be at the \(0^\circ\) position and the sunset cam's at the \(180^\circ\) position.

---
My intention was always to ignore the clocks-change (British Summer Time), as a smooth cam profile could never cause the follower to 'jump' 1 hour at an instantaneous point. But when generating the cam profiles, I obtained sunrise and sunset data in the local time and forgot to convert the summer times to GMT. I didn't notice until 6 months after that both indicators were now ~1 hour ahead of where they should be. The fix was to redesign and replace the two cams, this time converting the summer times to GMT so that the full cam shape  is programmed to a consistent time zone.

My solution for the daylight savings time is simply to treat the 12'o'clock position as the 'middle of the daylight'. Therefore in BST the top of the clock indicates 1pm, and in GMT it indicates 12pm. That way, the clock can be left alone and the only necessary adjustment is how to read it.

And for a clock with numerical labels, here's my solution:

   [image]
   
## Make Your Own

- Makerworld Link
- Calculator spreadsheet / app
- Hardware List
- Assembly Guide

![side-on](/static/img/projects/sunriseclock/side-on.png?v=1)
