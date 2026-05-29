---
title: KitSniff Ingredient Guesser
category: Web app
accent: teal
summary: "A daily social puzzle - guess the mystery ingredient by its colour, flavour, and food group. Unlock recipes, provenance stories, achievements, and culinary trivia."
date: 2025-05
featured: true
cover: kitsniff/cover.png
links:
  - label: Live
    url: "https://kitsniff.com"
    icon: external-link
  - label: GitHub
    url: "https://github.com/amiablealex/kitsniff"
    icon: brand-github
tech: [Python, Flask, PostgreSQL]   # [ adjust to the real stack ]
---

## What this is

Wordle-style daily puzzle for the kitchen - each day a new mystery ingredient is selected. Players guess ingredients and receive feedback on properties - Colour, Flavour, and Food Group.
Puzzle solves unlock recipes, provenance stories, and culinary trivia. Achievements, leaderboards, and a culinary exploration atlas track progress.

## Why I made it

Had the idea one day and quickly realised nothing like it existed. It particularly appealed to me because the kitchen / food angle is so relatable. Everyone has some grasp of culinary knowledge from their daily lives - making this game accessible and relevant to a wide community of friends and family.  

## Puzzle Intelligence

-including ingredients and flagging as not selectable (borrowed from Wordle) - these exist only so a player's obscure guess gets accepted gracefully. Including these as selectable for the daily puzzle would result in frustration if a really obscure thing gets chosen as the puzzle of the day. Side note, needing to deliberately exclude unselectable from the progress-ring denominators since they can never be the daily answer - counting them would make 100% progress literally unreachable. Same "make the goal actually attainable" instinct as the recipe balancing.
-The algorithm to select the daily ingredient and how it evolved from completely random. i.e truly random wasnt a good user experience. i'd explain how the actual algorithm works with the weighting, never-selected weights, same-property penalisers etc.
-Assigning each ingredient a 'difficulty' - settling on the equal-N buckets, the stats involved, and how certain methods would not be very good i.e all ingredients in the middle buckets and none at the extremes.
-How an ingredient is assigned its colour property - i.e no one-rule-fits-all. closest rule was 'if you eat the skin the its the colour of the skin, otherwise its the colour of the inside'. but this doesnt work for a few, e.g banana, apple. so i kind of settled on the colour being "what you would most assosiate to that ingredient". i.e kiwi = green, not brown.
-balancing the 'recipes' to be actually achievable - i.e ratatouille recipe could have 6 ingredients to align to tradition but then noone would ever achieve it - balancing to reduce number of ingredients, increase chance of unlock, and remain somewhat aligned to tradition.
-the complexity of the entire fuzzy matching / spell check (i.e all 8 steps of checking for aliases, etc...) and turning bugs into features (the easter-egg philosophy). i.e Custard Conundrum — fuzzy matching would "correct" custard to mustard, so instead of fixing it became an achievement.
-the logic to throw a popup for colour mismatch - i.e when a user already has certain information (e.g the answer is green), then user guesses apple. game detects that apple can be green, and that the user is expecting the answer to be green. so we throw a popup to saw "we know apples can be green, but we've stored it as red. do you still want to submit it as a guess?. and this even goes further, apple is assigned with 'secondary colours': the game is very intelligent of when to throw the popup. if the user guesses "green apple" they always get the popup. if they guess just "apple" they only get the popup depending on if they have already recieved the feedback that the answer is green. if not, the 'apple' guess just submits with no popup. I quite enjoy this user interaction.
-The poison mechanic — the original hue-rotate(45deg) filter quietly shifted the yellow feedback pills to look almost identical to the green "confirmed" pills — actively misleading players mid-game. Landing on hue-rotate(180deg) (yellow→blue, green→magenta) to keep feedback legible, plus the barely-perceptible poison-breathe scale animation, resulting in "a visual effect that mustn't corrupt the actual game".
-Introducing proper accounts and dealing with the complex logic e.g transferring guesses if users decide to create an account mid-game.

## Personality Layer

-The Basil origin story - family independently converging on Basil as best opening guess — i.e  the "best Wordle starting word" logic. Resulting in building the teasing Basil welcome messages. And the dynamic of the Basilisk achievement ending up incentivising users to start guessing basil, resulting in more users being exposed to the teasing welcome messages. Perfectly captures my whole game development ethos: small community, watching how they play, the game quietly responding.
-Birthday

## Culinary / Education Layer

-The culinary layer — KitSniff as a teaching tool, smuggling in education. Each of ~300 ingredients carries hand-curated provenance (cultural and historical origin stories), nutritional tags, superfood flags, and geographic locations, and the post-game modal turns each solve into a little piece of food storytelling. 

## Engineering Story

- Migrating to SQL database early (within 5 days of initial launch) with cleanly organised and structured data was the number one best decision made for the project. Resulting in entire history of user data being captured and accumulating from the get-go.
-Growing up from a Pi hobby to cloud production - the magic of zero-downtime deployments and local development freedom. PostgreSQL's strictness vs SQLite's loose typing caused many nuisance during the migration phase (e.g is_active column stored as 0/1 integers clashing with a native boolean 'won' column). This is where i learnt the necessity and power of environment variables - an ephemeral deployment detecting its environment.
-The automated social pipeline - because the selection algorithm deliberately favours never-picked ingredients, debuts are the norm — yet the AI kept leading every single day with "first-ever appearance!" And near-miss property matches were so tempting that no amount of prompt instruction stopped it calling them "heartbreaking". Eventually had to delete the data from the SQL entirely. That tension between what the data invites and what's actually interesting is a sharp, true story about both prompt engineering and the algorithm's design.

{#[ The interesting part. Pick two or three things that were genuinely tricky or
satisfying to solve. For example: the ingredient-weighting logic, the move to a
hosted Postgres database, or keeping the game fair day-to-day. Write a few
sentences on each. ]#}
