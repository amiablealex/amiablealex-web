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

A 24-hour wall clock with a single hand, plus two markers that track sunrise
and sunset times throughout the year. Midnight at the 6 o'clock position, noon at top. 

The hour hand reads as a 'how far through the daylight' indicator - the arc between the two markers is today's daylight.

![Face](/static/img/projects/sunriseclock/Face.png)

## How it works

The clock is driven by a standard 12-hour quartz movement. From it, two independent gear chains do separate jobs.
The first drives the time hand (one revolution in 24h). A single 2:1 reduction (15T → 30T) turns the 12h drive into 24h, 
with an idler gear to make sure the hour hand rotates clockwise.

![24h-chain-annotated](/static/img/projects/sunriseclock/24h-chain.png)

The second chain drives the year rotation. Six 3:1 stages (15T → 45T) multiply to \(3^6 = 729{:}1\), turning the 12h input 
to 8748h - within half a day of the true 8760 hours in a year.

![annual-chain](/static/img/projects/sunriseclock/annual-chain.png)

Two CAMs are mounted on a shaft fixed to the annual rotation, each shaped to the exact sunrise or sunset curve for the 
clock's location. As the CAM rotates, its variable radius raises and lowers a follower arm. A sector gear at the arm's 
pivot meshes with a small gear in the centre, amplifying that small angular rotation into the full desired 
sweep of the indicators. 

![cam-arm-indicator-flow](/static/img/projects/sunriseclock/cam-arm-indicator.png)

## Astronomy behind the cam shapes

This project aims to indicate the variation of sunrise and sunset mechanically on a 24-hour clock face. 

**Daylight hours change throughout the seasons** - long days in summer, short in winter. The effect is mostly due to the 
Earth being tilted on its spinning axis (23.4°) - on its own this effect is straightforward and predictable: daylight 
hours would vary smoothly and symmetrically through the year, and a regular oval cam would reproduce it perfectly.

However, **the sunrise and sunset curves aren't symmetric**. The shortest day is the winter solstice, around 21 December. 
But that isn't the day the sun sets earliest or rises latest. In the UK the earliest sunset is around 12 December, and the 
latest sunrise around 30 December. So for two weeks before Christmas the evenings are already on their way towards spring 
while the mornings are still darkening.[^evenings] Mechanically reproducing the annual cycle is becoming more complicated. 

[^evenings]: I found the latest sunrise / earliest sunset divergence around the solstice to be particularly well explained 
in [The evenings are drawing out already](https://explainingscience.org/2019/12/13/the-evenings-are-drawing-out-already-2/), 
Explaining Science (2019).

This is because there is another mechanic also contributing its own effect to the daylight hours - an astronomical 
phenomenon called **The Equation of Time**: the gap between sun-time and clock-time. The Sun runs slightly fast or slow 
against the clock depending on the season, coming from the Earth's tilt and elliptical orbit acting together. Because the 
Earth's orbit is an ellipse, the Earth speeds up as it orbits closer to the Sun in January and slows as it orbits further 
from the Sun in July - **Kepler's second law**. 

<object type="image/svg+xml" data="/static/img/projects/sunriseclock/kepler-viz.svg?v=1"
        width="100%" class="cam-viz"
        style="display:block; max-width:170px; margin-inline:auto; aspect-ratio:420 / 320;"
        aria-label="Kepler's second law: a planet moving faster near the Sun and slower when far away">
  <img src="/static/img/projects/sunriseclock/fallback-image.png" alt="An elliptical orbit with the Sun at one focus">
</object>

The equation of time emerges because each day the Earth must turn slightly 
more than a full 360° to bring the sun back to the same point in the sky. The amount of extra rotation needed each day 
depends on the orbital speed, which in turn depends on which part of the orbit the Earth is in. So the equation of time 
varies throughout the seasons.

```
Day 1:  Earth at position A
        🌍 → rotates 360°
        Sun appears at noon
        
Day 2:  Earth has moved in orbit
        🌍 → must rotate 360° + 1° to get sun back to noon
        (The extra 1° depends on how far Earth has moved around its orbit since Day 1)
```   

When Earth is moving *fast* (January - perihelion):

- Earth travels further along orbit each day
- Must rotate *more* to bring sun back to noon
- Solar day is *longer* than average
- Sunrise/sunset times relative to the clock drift *later* with each passing day

When Earth is moving *slow* (July - aphelion):

- Earth travels less far along orbit each day
- Needs less extra rotation to get back to noon
- Solar day is *shorter* than average
- Sunrise/sunset times relative to the clock drift *earlier* with each passing day

Add together this contribution from the equation of time and the seasonal variation from axial tilt, and what you get is two 
independent astronomical phenomena combining in complex ways. The result is that - for the same clock time each day of the
year - the Sun never sits in quite the same spot; instead it traces a distorted figure-of-eight. That shape is the 
**analemma**: the equation of time made visible, etched into the sky. 

The shapes below show the Sun's position at noon across a one-year period. Up–down is how high the Sun climbs in the sky, 
rising and falling once a year. Any side-to-side variation (left-right) is showing the Sun being ahead of or behind the clock 
noon. The central vertical line on each diagram is due south - **solar noon** - the Sun perfectly in sync with clock-time 
would always appear due south at exactly 12:00pm. 

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
<figcaption>The Sun photographed at 12:00pm for one year, via the Vatican Observatory's
<a href="https://www.vaticanobservatory.org/sacred-space-astronomy/the-analemma-and-the-darkest-evening/">The Analemma and the 
  Darkest Evening</a>.</figcaption>
</figure>

Those two contributing factors are also what pushes the earliest sunset and latest sunrise to *opposite* sides of the solstice - 
because sunrise and sunset sit on opposite sides of *solar* midday, and solar midday is itself still drifting later through
December.

<details><summary>Further explanation</summary>
  After the winter solstice the days are lengthening, so sunrise <em>should</em> start getting earlier; but the second factor - 
  the equation of time - is still dragging solar noon later even after the solstice.   That wins for another week, holding 
  sunrise back until its latest point around 30 December. The same interaction works the other way at dusk, the equation of 
  time turning sunset around before the solstice, near 12 December.
</details> 

**This is where the cam shapes come in**. Both cam profiles are generated from a year of real sunrise and sunset data. So the 
axial tilt, the equation of time, Kepler's Second Law, and the analemma are all programmed into the shape - frozen in plastic. 
And because the individual contributions of those effects depend on where you are on the planet, every cam is tailored to a 
location.

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

The cam edge has to carry all of those interacting effects at once. The funny thing is, much
like Ptolemy in 150 AD, is that you don't need to understand the astronomy to arrive at the
correct shape. Building it is two jobs, and I'll go through it in the order I actually worked it out, because it 
makes the most logical sense for me to follow. 

1. Size the mechanism: work backwards from the dial to find the cam throw that gives the hand its correct annual sweep.
1. Generate the profile: sample a year of real sunrise times and turn each one into a radius.
   
### Working backwards from the dial

Four properties describe the mechanism - the arm length \(L\), the cam's **throw** \(t\) (its max-min radius difference), 
the gear ratio \(G\) (sector teeth ÷ centre teeth), and the resulting indicator **sweep** \(S\). The design problem is to 
pick each property so the hand sweeps exactly the right amount, and I solved it backwards: starting from the desired sweep, 
ending with the cam throw.

First, look up the year's earliest and latest sunrise for a location. To make calculations easier I converted times into
**decimal hours** - 3:45am becomes 3.75. The year's overall sunrise variation is simply latest − earliest.

\[\text{sunrise variation} = \text{latest sunrise time} - \text{earliest sunrise time}\]

For my latitude (03:35 and 08:16 UTC): 8.26 - 3.58 = 4.68 hours (4hrs 40min). On a 24-hour dial, 1 hour is 15 \(^circ\), and
so we can work out desired indicator rotation: 

\[S \approx 4.68\,\text{h} \times 15^\circ/\text{h} \approx 74.8^\circ\]

Next, it was a bit of trial and error to determine a gear ratio that would resut in a sensible-shaped cam. I settled on 4:1
for the sunrise cam and 6:1 for the sunset cam. This ratio reduces the required rotation needed at the sector:
 
\[\theta = \frac{S}{G} = \frac{74.8^\circ}{4} \approx 18.7^\circ\]

And work out how much the follower arm needs to lift to provide the desired 18.7\(^circ)\ rotation:
 
\[t = L\tan\theta = 80\,\text{mm}\times\tan 18.7^\circ \approx 27.4\,\text{mm}\]

Finally, the throw is the difference between the cam's largest and smallest radius. The largest is set by the space available 
for the cam in the mechanism (about 41 mm). To get the minimum radius of the cam:

\[R_{\min} = R_{\max} - t \approx 41\,\text{mm} - 27.4\,\text{mm} \approx 13.6\,\text{mm}\]

So the sunrise cam runs between about 14 mm and 41 mm. Sunset works out similar - 4.8 hours of annual spread, about 72\(^circ)\ 
of sweep. The one difference is the gear ratio: for a fixed sweep a higher ratio needs a smaller throw (since \(\theta = S/G\) 
shrinks), and I used 6:1 for sunset against 4:1 for sunrise:

\[\theta = \frac{72^\circ}{6} \approx 12^\circ \qquad t = 80\,\text{mm}\times\tan 12^\circ \approx 17.0\,\text{mm} \qquad R_{\min} \approx 23\,\text{mm}\]

<details markdown="1"><summary>The one assumption</summary>
The first step treats the follower's contact point as rising by exactly the cam's change in radius, staying a fixed 
80 mm from the pivot. It doesn't, quite: as the arm swings up the contact point creeps inside 80 mm, and as it 
swings down, outside. But with an 80 mm arm against a ~20 mm throw, the arm barely tilts, and the error stays 
around a couple of percent. Comfortably below what the print tolerances and gear backlash contribute anyway.
</details>


### Generating the cam profile

With the cam throw determined, what's left is to plot the cam's actual shape. The cam is mounted onto a shaft that rotates
once per year, so the year maps onto 360°. Sample that circle at 24 equal points, about 15 days apart \(365.25/24 = 15.21\text{ days}\), 
and set the summer solstice (21 June) as the reference point. The method is then simply:

1. Look up the real sunrise (or sunset) time at each of the 24 dates.
1. Fix the cam's maximum radius, determined by the space available in the mechanism.
1. Turn each time into a radius: the latest sunrise becomes the smallest radius, the earliest becomes the largest
   **(and the reverse for sunset)**.
1. Fit a smooth spline through the 24 radii. That curve is the cam edge.

<object type="image/svg+xml" data="/static/img/projects/sunriseclock/build-viz.svg?v=2"
        width="100%" class="cam-viz"
        style="display: block; max-width:400px; margin-inline:auto; aspect-ratio: 640 / 600;"
        aria-label="Building the cam from 24 samples and a spline">
  <img src="/static/img/projects/sunriseclock/fallback-image.png" alt="The sunrise cam shape, built from 24 sampled points">
</object>

Because every radius comes from a *real* sunrise time, the cam inherits every effect from the the astronomy section. 
You don't actually need to understand any of the astronomy to capture it; the data already carries it.

<object type="image/svg+xml" data="/static/img/projects/sunriseclock/sweep-viz.svg?v=2"
        width="100%" class="cam-viz"
        style="display: block; aspect-ratio: 1000 / 470;"
        aria-label="A year of sunrise times, wrapped onto the cam">
  <img src="/static/img/projects/sunriseclock/fallback-image.png" alt="A year of sunrise times wrapped onto the cam">
</object>

One detail falls out of this, and you can see it in the wrap above. I pinned the solstice at 0°, but I set the maximum radius 
to the *earliest sunrise* - and thanks to the equation of time the earliest sunrise lands a little *before* the June solstice, 
the latest a little *after* December. So the cam's fattest point sits slightly off top, and its narrowest just past the 
6 o'clock position rather than dead on it. That small offset, frozen into the spokes, is the equation of time made physical - 
the same lopsidedness from the analemma, now in the cam's silhouette.
 
The sunset cam comes from exactly the same recipe - same 24 points, same spline, same kind of radius range. With one difference I didn't spot until the clock was assembled.

### What I got wrong

I built both cams the same way: biggest radius pointing straight up at the summer solstice. The sunrise cam worked. So I set the clock to the winter solstice, parked the sunset hand at about 4 pm, and wound the year forward. The evenings should draw out - sunset creeping later through January, February, March. Instead the sunset hand marched the wrong way: 4 pm, 3 pm, 2 pm, backwards into the afternoon.
 
Here's the trap. Through the year the two hands have to move in **opposite** directions - toward summer, sunrise gets earlier (hand one way) while sunset gets later (hand the other way), and the daylight arc between them widens. But both cams ride the same shaft, turning the same direction, and a growing cam radius always pushes its follower the same way, swinging its hand in one fixed sense. Two identical cams therefore drive both hands the *same* way - so if sunrise is right, sunset is exactly backwards.
 
The fix is to invert the sunset cam: put its **minimum** radius at the summer solstice instead of its maximum. Now as the shaft turns toward summer the sunrise cam's radius grows while the sunset cam's shrinks, the two followers move oppositely, and the hands finally sweep apart as they should.
 
What clicked afterwards is that this isn't really a special-case flip at all. The rule was always *earlier in the day → larger radius*. Apply it honestly and the earliest sunrise (June) and the earliest sunset (December) sit on **opposite sides of the year** - so the sunrise cam's bulge lands at midsummer and the sunset cam's at midwinter, automatically. My mistake was thinking "big radius = summer" instead of "big radius = earliest." Get the rule right and the inversion falls out for free.
 
The second bug hid in the data. My first set of times came in local clock time - which in the UK means the summer half of the year secretly carries the extra daylight-saving hour. Baked into the cam, that one-hour summer offset faked an asymmetry between the sunrise and sunset sweeps that shouldn't exist. A simple check caught it: the midpoint between sunrise and sunset should sit near solar noon, around 12:00, all year - but in summer mine came out near 13:00, the tell-tale DST hour. The fix was to regenerate everything from true GMT, with no seasonal jump. A smooth cam couldn't reproduce the instantaneous clocks-change leap anyway, so GMT is the honest frame - and the visuals above all use it.
 
Both bugs taught the same lesson: the mechanism was never the hard part. Getting the data honest and the directions right was.

<details>
_[INSTRUCTION: the honest beats. Two of them. Frame as "caught and fixed," not disaster.
Lead with whichever you find more interesting.]_

_[BEAT 1 — the GMT / daylight-saving mix-up. In your own words: the source times secretly
had the clocks-change hour baked in, which faked an asymmetry between the sunrise and
sunset sweeps; you caught it with the solar-noon test (midpoints should sit near 12,
but summer came out near 13:00); fixing it meant regenerating the profiles in true GMT.
Optionally: the one-line takeaway that a smooth cam can't follow the DST jump anyway.]_

_[BEAT 2 — the inverted cam / direction error. In your own words: from winter to summer,
sunrise must move earlier while sunset moves later — opposite directions on the dial —
but a rising cam radius turns its hand one fixed way, so identical cams sent both hands
the same way. Fix: invert the sunset cam (minimum radius at the winter solstice instead
of maximum) so the same rising radius drives its hand the other way.]_

_[INSTRUCTION: optional closing line — what these two taught you, e.g. that the hard part
wasn't the mechanism but getting the data and the directions honest. Keep it light.]_
</details>

## Make Your Own

- Makerworld Link
- Calculator spreadsheet / app
- Hardware List
- Assembly Guide

<details><summary>Writing Notes</summary>

### Rotational-vs-linear-follower subtlety
Because the arm pivots and the roller sits on top, the cam's push is nearly perpendicular to the arm → near-zero pressure angle → efficient. 
(A nice "why horizontal is actually optimal" footnote — went back and forth on this and it's genuinely counterintuitive.)


### Why sunrise and sunset are not centered exactly around mid-day
- The geographic offset - for every degree of longitude you move west from the meridian, solar noon is delayed by about
  4 minutes, pushing the true 'middle-of-the-day' later.
- The astronomical offset (*The Equation of Time*) - Even if you are standing exactly on the Prime Meridian in
  Greenwich, the effect from the equation of time means the Sun still won't be at its peak at exactly 12:00pm.

*An example>: On February 27th - The equation of time pushes the solar noon about 13 minutes later (12:13 PM). Longitude
(e.g Belfast) pushes the midpoint another 24 minutes later. The cumulative effect is that Belfast sees sunrise and sunset centered
around approx. 12:37 PM. Sunrise and sunset times appear asymmetrical - the afternoon feels "longer" than the morning.*

</details>
