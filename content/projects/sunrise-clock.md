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

A 24-hour wall clock with a single hand, plus two markers that track sunrise
and sunset times throughout the year. 

Provides an interesting representation of how the seasons affect the daylight hours - it's easy to see at a glance 
how long the daylight hours are compared to the 360-degree day. 
The effect is that the hour hand becomes a 'time-of-day' indicator, communicating the current time by "how far through the 
daylight hours".


![Face](/static/img/projects/sunriseclock/4-3.png)


## How it works

- Std 12-hour quartz movement geared down 2:1 to drive the 24-hour hand
- Separate chain 729:1 (3^6 - six stages of 3:1 reduction) to gear down the 12-hour rotation to an 8748-hour rotation
  (very close to the 8760 hours in a year).
- The year-rotation drives the CAMs which are shaped to the profile of annual sunrise / sunset variation at a given location
- Each CAM gives a throw to the corresponding followr-arm-sector piece, which produces a rotation at the sector mesh
- Small gear at the clock centre (meshed with the sector) amplifies the sector rotation
- Sunrise / Sunset indicators fixed to the center gear which achieves the desired sweep of the sunrise / sunset  

![Square-on](/static/img/projects/sunriseclock/square-on.png)

## Interesting things about sunrise / sunset

### Why sunrise and sunset are not centered exactly around mid-day
- The geographic offset - for every degree of longitude you move west from the meridian, solar noon is delayed by about
  4 minutes, pushing the true 'middle-of-the-day' later.
- The astronomical offset (<em>The Equation of Time</em>) - Even if you are standing exactly on the Prime Meridian in
  Greenwich, the sun still won't be at its peak at exactly 12:00 PM today. This is due to the Equation of Time, which is
  the difference between "Clock Time" and "Sun Time." Two things cause the sun to be "fast" or "slow" relative to our 24-hour clocks:
  - **The Earth’s Elliptical Orbit**: The Earth doesn't move at a constant speed around the sun. It moves faster when it's closer
    to the sun (January) and slower when it's farther away (July).  
  - **The Earth’s Axial Tilt**: Because the Earth is tilted at $23.5°$, the sun's apparent path across the sky changes speed
    throughout the year.
    
<em>An example>: On February 27th - Equation of Time pushes the solar midpoint about 13 minutes later (12:13 PM). Longitude
(e.g Belfast) pushes the midpoint another 24 minutes later. The cumulative effect is that Belfast sees sunrise and sunset centered
around approx. 12:37 PM. Sunrise and sunset times appear asymmetrical - the afternoon feels "longer" than the morning.</em>
  
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
