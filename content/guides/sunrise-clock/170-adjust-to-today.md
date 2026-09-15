---
title: Adjust to today's date
summary: ""
---

Earlier we set the clock to it's winter solstice position and then added the indicator hands. Before we fix the mechanism and set the hour hand, we need to run the annual part of the mechanism to get it into the correct position for today's date.

## Work out how many days the current date is past the winter solstice (21/Dec)

Here are some examples:

| Date | Days past winter solstice |
| --- | --- |
| 21st Dec | 0 |
| 3rd Feb | 44 |
| 30th May | 160 |
| 3rd Sept | 256 |
| Dec 2nd | 346 |

And you can actually just google it:
![step18 google](step18-google.png)

## Turn the annual chain to today's position 
Lets use the example of September 3rd: it is 256 days forwards from the winter solstice. This means we need to advance the clock mechanism through 256 days.

Look at the diagram below. After we fix the powered drive, the gear at position 1 will rotate anticlockwise one full turn every 12 hours (because it will mesh with the drive gear that we fixed on the clock's hour hand). So to advance the clock 256 days, this is 6,144 hours (256 x 24), and will be 512 turns of the gear at position 1 (6144 / 12).
Instead of turning the gear at position 1 512 turns, we can make it easier:

- Due to the 3:1 ratio, 512 anticlockwise turns of the gear at position 1 will mean 170.6 turns clockwise of the gear at position 2 (512 / 3).
- Also, 170.6 clockwise turns of the gear at position 2 means 56.8 turns anticlockwise of the gear at position 3.
- And 56.8 anticlockwise turns of the gear at position 3 will be 18.9 turns clockwise of the gear at position 4.

So, to advance the clock mechanism through 256 days, we just need to rotate the gear at position 4 clockwise by almost 19 full turns.

![step18 calc](step18-calc.png)

In the example in the video, I actually reduce the required rotation even further:
- Although September 3rd is 256 days forwards of the winter solstice, it is also 97 days before the next one. 
- So instead of rotating the gear at position 4 clockwise by almost 19 turns, I actually rotate it in the opposite direction (anticlockwise) by 7.2 turns (97 x 24 / 12 / 3 / 3 / 3). 
- The cams end up in the same position as if i had rotated the 19 turns clockwise.

![Step18](youtube:2Pz-NeOZCgM)
