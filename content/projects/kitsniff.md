---
title: KitSniff Ingredient Guesser
category: Web app
accent: teal
summary: "A daily social puzzle - guess the mystery ingredient by its colour, flavour, and food group. Unlock recipes, provenance stories, achievements, and culinary trivia."
date: 2025-05
featured: true
order: 1
cover: kitsniff/cover.png
links:
  - label: Live
    url: "https://kitsniff.com"
    icon: external-link
  - label: GitHub
    url: "https://github.com/amiablealex/kitsniff"
    icon: brand-github
  - label: X
    url: "https://x.com/KitchenSniffle"
    icon: brand-x
tech: [Python, Flask, PostgreSQL, Prompt Engineering, LLM]
---

## What this is

Wordle-style daily puzzle for the kitchen - each day a new mystery ingredient is selected. Players guess ingredients and receive feedback on properties - Colour, Flavour, and Food Group.
Puzzle solves unlock recipes, provenance stories, and culinary trivia. Achievements, leaderboards, and a culinary exploration atlas track progress.

This idea particularly appealed to me because the kitchen / food angle is so relatable - everyone has some grasp of culinary knowledge from their daily lives making this game accessible and relevant to a wide community of friends and family. 

Each of ~300 ingredients carries carefully curated provenance (cultural and historical origin stories), nutritional tags, superfood status, geographic locations. And a post-game popup turns each solve into a little piece of culinary storytelling.

## Engineering Story

- **The power of a well-organised database** - the engine behind all the app's features.
- **Moving from local Pi to cloud hosting** - the magic of zero-downtime deployments and local development freedom. The necessity and power of environment variables, and an ephemeral deployment "detecting its environment".
- **Automated social pipeline** - SQL script pulls detailed statistics about the game's recent history and user behaviour. Feeds into LLM which has been given enough context to generate engaging posts for socials.

## Stuff that i found particularly interesting

- **Horseradish"". Of all the ingredients Horseradish is special - it's the only case where a player tends to submit the same phrase to mean more than one thing. i.e Horseradish Root and Horseradish Sauce (both are in the game, one as a vegetable and one as a condiment). Of course there are other similar instances (e.g Chilli and Chilli powder), but in these cases it is usually obvious which one the user intends. This resulted in some particularly interesting logic especially for Horseradish.
  - If the user has 'vegetable' property as confirmed and submits 'Horseradish', then accept the guess as 'Horseradish root'.
  - If the user has 'condiment' property as confirmed and submits 'Horseradish', then accept the guess as 'Horseradish Sauce'.
  - If the user has neither property confirmed and submits 'Horseradish', then fire a popup to ask the user whether they meant the root or the sauce.
    
- **The Basil origin story** - players independently converging on Basil as best opening guess. Resulted in building the Basil welcome messages, "how to detect a serial basil-guesser", and the Basilisk acccolade. The accolade resulting in people more likely to be exposed to the separate welcome messages feature was a particularly fun dynamic. A good example of features interacting with each other (accolade incentivising easter-egg discovery).
- **The Larder** - Including obscure ingredients and flagging as not selectable (borrowed from Wordle). These exist so a player's obscure guess gets accepted gracefully. Including these as selectable for the daily puzzle would result in frustration if a really obscure thing gets chosen as the puzzle of the day.
- **Algorithm to select the daily ingredient** i.e truly random wasnt a good user experience (lots of repeat ingredients).
- **Assigning each ingredient a 'difficulty' rating** - equal-N buckets & the stats involved. Certain methods would not be very good i.e all ingredients in the middle buckets and none at the extremes.
- **How an ingredient is assigned its colour property** - i.e no one-rule-fits-all. closest rule was 'if you eat the skin the its the colour of the skin, otherwise its the colour of the inside'. but this doesnt work for a few, e.g banana, apple. so i kind of settled on the colour being "what you would most assosiate to that ingredient". i.e kiwi = green, not brown.
-**Balancing the 'recipes'** to be actually achievable - i.e ratatouille recipe could have 6 ingredients to align to tradition but then noone would ever achieve it - balancing to reduce number of ingredients, increase chance of unlock, and remain somewhat aligned to tradition.
- **Complexity of the entire fuzzy matching / spell check flow** (i.e all 8 steps of checking for aliases, etc...) and turning bugs into features (the easter-egg philosophy). i.e Custard Conundrum — fuzzy matching would "correct" custard to mustard, so instead of fixing it I made it an achievement.
- **User experience popup for colour mismatch** - i.e adapting what happens when a user makes an ambiguous guess depending on what information they already have. e.g if user knows the answer is green and guesses 'apple', the game detects that apple can be green, and that the user is expecting the answer to be green. so a popup fires showing "we know apples can be green, but we've stored it as red. do you still want to submit it as a guess?". and it even goes further - apple is assigned with 'secondary colours': the game is intelligent of when to fire the popup. if the user guesses "green apple" they always get the popup. if they guess just "apple" they only get the popup depending on what information they have available. I quite enjoy this detailed design for enhanced user experience. The implemented logic goes along the lines of:
  - If the user guesses 'green apple' (i.e an 'ingredient' prefixed with any colour except what that ingredient is actually assigned in the database) then always fire a popup telling them that apples are stored as 'red' and ask them if they still want to submit it as a guess.
  - If the user has 'green' property confirmed as colour and then guesses 'apple' - apple has 'green' assigned as a secondary colour, so fire the same popup telling them that apples are stored as 'red' and ask them if they still want to submit it as a guess.
  - If the user has no colour property information confirmed yet and guesses just 'apple' then accept the guess without popup. Even if they were expecting it to be green and it pops up as red, it is of no detriment to their game
- **Introducing proper accounts** and the associated complex logic e.g transferring guesses if users decide to create an account mid-game. The ultimate complex case is if a signed-in user plays the puzzle, signs out, plays the puzzle again (partially or full-solve) and then decides to sign in. Pretty sure this has never happened and will never, but the game can handle it. It's all about the learning experience.
