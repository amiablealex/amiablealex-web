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
  - label: Write-up
    url: "[ optional: link to a longer write-up, or remove this link ]"
    icon: file-text
tech: [Fusion 360, A1 Mini, "3D printing"]
---


## What it is

A 24-hour wall clock with a single hand, two markers that track sunrise
and sunset times throughout the year. Midnight at the 6 o'clock position, noon at top. 

The hour hand reads as a 'how far through the daylight' indicator - the arc between the two markers is today's daylight.

![Face](/static/img/projects/sunriseclock/Face.png)

## How it works

- Standard 12-hour quartz movement with two independant chains
- 24h chain: 2:1 reduction (15T → 30T), turns 12h into 24h.
- Annual chain: Six 3:1 stages ( 15T → 45T, \3^6 = 729:1\ ), 12h becomes 8748h (close enough to the true 8760 hours in a year).
- Progressive height-stacking of the reduction gears so the big gears don't collide 
- The year-rotation drives the CAMs which are shaped to the profile of annual sunrise / sunset variation at a given location
- Each CAM gives a throw to the corresponding follower-arm-sector piece, producing a rotation at the sector mesh
- Small gear at the clock centre (meshed with the sector) amplifies the sector rotation to achieve desired Sunrise / Sunset indicator sweep.  

![Square-on](/static/img/projects/sunriseclock/square-on.png)

## Cam to Indicator - The Maths

### Follower swing
### Hand sweep
### Worked Sunrise
### Worked Sunset
### The One Assumption 
Arm rides roughly horizontal on top of the cam, so arm contact point rise ≈ cam's radial change; valid because arm (80 mm) ≫ throw (~20 mm), ≈2% error.

### Rotational-vs-linear-follower subtlety
Because the arm pivots and the roller sits on top, the cam's push is nearly perpendicular to the arm → near-zero pressure angle → efficient. 
(A nice "why horizontal is actually optimal" footnote — went back and forth on this and it's genuinely counterintuitive.)

### Why a 10-tooth centre gear is fine despite being near the undercut limit
- Total swing (~140°) is set by how much day length changes; a symmetric world splits it evenly.
- The actual lopsided split (~55° sunrise vs ~85° sunset) is the equation-of-time-plus-longitude fingerprint: solar noon wanders, so morning and evening don't shift equally.
- Real sunrise range is ~55°, but the build rounds to 52° for clean 4:1 gearing.

## Why the two hands sweep different angles

## What the cam shape encodes
- Two effects: axial tilt 23.4° (the smooth swing — alone it'd give a plain ellipse) + orbital eccentricity (the bump).
- Kepler's 2nd law: Earth moves faster near the Sun → the Day-1/Day-2 over-rotation diagram.
- The November bump — sunrise creeping earlier while days still shorten — "weird thing"
- The January turnaround: latest sunrise is late December, not the solstice.
- Longitude offset: 4 min per degree west; Belfast worked example (solar midpoint ~12:37).
- The analemma figure-8
**The cam shape programs every contributing effect into a single physical curve.**
"How we worked this out" history aside: Hipparchus → Ptolemy → Ibn Yunus (equation-of-time tables, ~1000 CE) → Kepler (ellipses, 1609) → Huygens
(the pendulum clock, 1656, finally accurate enough to measure the effect). Perfect for <details>.

## Designing the profile
- Year = 360° of cam rotation, sampled at 24 equal points (~15 days).
- Why 24: started at 12, doubled it to catch the November plateau and January turnaround without overloading the spline.
- The interval correction: 365.25/12, not a round 30 days, so the points land true.
- The inverted sunset cam — max radius at the winter solstice — so the hand turns the right way. A funny mistake! That had to be fixed.
- One throw value drives the whole 24-row table, so the profile re-targets to any latitude.
- Differing CAMs between locations - (53.2°N) and (51.27°N). Summer sunrise ~15 min later, winter near-identical. Strong proof of the parameterisation.
- Roller compensation (cam surface vs roller-centre radius, 4 mm) and the 40.3 mm radius cap to clear the drive-gear support pin — build-accuracy.

## Make Your Own
- Makerworld Link
- Calculator spreadsheet / app
- Hardware List
- Assembly Guide

## Design Journey
-  Centre concentric hands chosen over a perimeter ring. The ring's mass/friction would have stalled the quartz movement and needed multi-stage amplification.
-  Gravity-loaded follower instead of a spring — the **low friction** is the reason a feeble quartz movement can drive the whole train. "how does a quartz movement turn all that?"
-  Nested brass tubes for the concentric hand shafts rather than 3D-printed thin shafts (too weak to print).

## Interesting things about sunrise / sunset

### Why sunrise and sunset are not centered exactly around mid-day
- The geographic offset - for every degree of longitude you move west from the meridian, solar noon is delayed by about
  4 minutes, pushing the true 'middle-of-the-day' later.
- The astronomical offset (*The Equation of Time*) - Even if you are standing exactly on the Prime Meridian in
  Greenwich, the sun still won't be at its peak at exactly 12:00 PM today. This is due to the Equation of Time, which is
  the difference between "Clock Time" and "Sun Time." Two things cause the sun to be "fast" or "slow" relative to our 24-hour clocks:
  - **The Earth’s Elliptical Orbit**: The Earth doesn't move at a constant speed around the sun. It moves faster when it's closer
    to the sun (January) and slower when it's farther away (July).  
  - **The Earth’s Axial Tilt**: Because the Earth is tilted at \(23.5^\circ\), the sun's apparent path across the sky changes speed
    throughout the year.
    
*An example>: On February 27th - Equation of Time pushes the solar midpoint about 13 minutes later (12:13 PM). Longitude
(e.g Belfast) pushes the midpoint another 24 minutes later. The cumulative effect is that Belfast sees sunrise and sunset centered
around approx. 12:37 PM. Sunrise and sunset times appear asymmetrical - the afternoon feels "longer" than the morning.*
  
### The bump in the shape of the CAMs and The Analemma Effect
Sunrise and sunset times are controlled by two independent astronomical phenomena that combine in complex ways:
1. Earth's axis is tilted 23.4° relative to its orbital plane. This creates the PRIMARY pattern: Smooth variation from early to late
   throughout the year. Would create a perfect elliptical cam if this were the ONLY effect.
2. Orbital Eccentricity - The "Bump" Effect. Earth's orbit is not a perfect circle - it's an ellipse. Key insight: Earth moves FASTER
   when closer to the sun (Kepler's Second Law). Earth must rotate slightly MORE than 360° to bring the sun back to the same position,
   because Earth has moved along its orbit.

```
   Day 1:  Earth at position A
           🌍 → rotates 360°
           Sun appears at noon
        
   Day 2:  Earth has moved in orbit
           🌍 → must rotate 360° + 1° to get sun back to noon
           (The extra 1° depends on orbital speed)
```
   
When Earth moves FAST (January - perihelion):
- Earth travels further along orbit each day.
- Must rotate MORE to bring sun back to noon.
- Solar day is LONGER than average.
- Sunrise/sunset times drift LATER

When Earth moves SLOW (July - aphelion):
- Earth travels less far along orbit each day
- Needs less extra rotation for noon
- Solar day is SHORTER than average
- Sunrise/sunset times drift EARLIER
      
Why the "Bump" Appears in the Sunrise Cam:
November is EARLIER than October. Why this seems weird: Days are getting shorter (winter solstice approaching). You'd expect sunrise to get 
progressively LATER every day. But it doesn't.
The Detailed Explanation - From October to November:
- Axial tilt effect (dominant):
  - Northern hemisphere tilting away from sun
  - Pushes sunrise LATER by ~40 minutes

- Equation of Time effect (secondary):
  - Earth approaching perihelion (January)
  - Orbital speed increasing
  - Equation of Time goes from ~16 minutes fast (early Nov) to ~10 minutes fast (late Nov)
  - This makes sunrise EARLIER by ~6 minutes

But these effects apply ASYMMETRICALLY to sunrise vs sunset. For sunrise: The Equation of Time causes the "mean sunrise" to drift. But axial 
tilt is also changing the "earliest possible sunrise". These combine in complex ways. The result: Late October → Early November: Sunrise gets 
slightly EARLIER. This creates the "bump" on your cam (radius increases from Oct to Nov).

**The shape of the cam effectively programs all the effects that contribute to the sunrise / sunset variation into a single physical shape**.
