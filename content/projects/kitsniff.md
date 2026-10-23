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
tech: [Python, Flask, PostgreSQL, LLM]
---

## What this is

Daily ingredient-guessing puzzle for the kitchen - each day a new mystery ingredient is selected. Players guess ingredients and receive feedback on properties - Colour, Flavour, and Food Group.
Puzzle solves unlock recipes, provenance stories, and culinary trivia. Achievements, leaderboards, and a culinary exploration atlas track progress.

This idea particularly appealed to me because the kitchen / food angle is so relatable - everyone has some grasp of culinary knowledge from their daily lives making this game accessible and relevant to a wide community of friends and family. 

![post-game](/static/img/projects/kitsniff/post-game.png?v=1)

## Part one: the daily sniff
 
### The guess
- Four properties per guess: ✅ right, ❌ wrong, 🟨 right food group but wrong type ("a warm clue — you're in the right part of the kitchen").
- New puzzle at 03:05 UTC. Same answer for everyone.
![feedback](/static/img/projects/kitsniff/feedback.png?v=1)
### Hints
- Unlock after five guesses. Each one reveals the next letter. Reveal the last letter and you've given up.
### The poison
- Every day one ingredient is secretly poisoned by "mischievous kitchen gnomes". Guess it and the screen shakes, the colours turn, and they stay turned until you finish.
- Purely cosmetic. Your leaderboard row wears a ☠️ "as a badge of questionable honour".
![poisoned](/static/img/projects/kitsniff/poisoned.png?v=1)
### Crowns and spoons
- Best hint-free solve wins the day's 👑 (ties go to whoever got there first). Last place takes the 🥄 wooden spoon.
- Announced the next morning: "Master of the Maison!" / "A lesson in humility!"
- The Hall of Fame on the Community page.
### The greeting
- A welcome line chosen by time of day: "Rise and sniff," "The sauce is splitting," "Where is the lamb sauce,"
- Some players get a different greeting entirely (→ see *Everyone opens with Basil*).
### The share
- The emoji grid for the group chat, ending in a deliberately bare link.
![share](/static/img/projects/kitsniff/share.png?v=1)
  
---
 
## Part two: after the solve
 
### The card stack
- Every solve deals a stack of cards: the ingredient, any recipes you cooked, any places you discovered.
- Ingredient card anatomy: collector number ("Ingredient · No. 070"), difficulty pips, the origin story, "Rich in…", where it comes from, what it's used in, your history with it.
![ingredient-card](/static/img/projects/kitsniff/ingredient-card.png?v=1)
### Difficulty, in seven words
- A Doddle · Bread and Butter · Worth a Sniff · Some Stirring Required · Cause for Pause · Devilish · Fiendish.
- Until an ingredient has been solved enough times: "Yet to reveal itself". (→ deep dive in Kitchen Notes)
### Cards like a trading card game
- Three things a card can tell you, never mixed up: what *type* it is (ingredient / recipe / place), how *rare* it is (gold for Superfoods and mastered places, with a shine), and its *state* (dashed for locked, parchment for the Larder).
- Every name on a card is a door to that card.
![card-types](/static/img/projects/kitsniff/card-types.png?v=1)

---
 
## Part three: the collection
 
### The Pantry
- Every ingredient you've solved. Ingredients you've guessed but never had as the answer show as *Sniffed*.
![pantry](/static/img/projects/kitsniff/pantry.png?v=1)
### The Larder
- The back shelf: ingredients you can guess but that will never be the answer. Too obscure to be fair, or "pure nuisance" — "This kitchen has never once told Mace from Mache from Matcha."
- Found by accident, the first time you guess one. Marmite lives here.
### The Cookbook
- Recipes unlock from everything you guess in a game you solve — the wrong guesses count too.
- Three kinds: dishes you have to hunt (Minestrone, Ratatouille), ones you stumble into (Banana Bread, Bollywood), and the silly ones (Paddington, Mermaid's Tears, Vampire Repellant, Mr. T's Nut Mix, Barbie — any three pink things).
- Every menu description is written by an over-earnest critic. Lemsip: "infused with paracetamol".
- A locked recipe gives away one clue: "One of them is **Egg**. The rest is up to you."
- Pin one to your prep list to hunt it deliberately.
### The Atlas
- Every ingredient has a place in the world. Continents, countries, regions — and trade routes: The Silk Road, The Spice Trade, The Columbian Exchange, The Viking Trade Network, The Road to Al-Andalus, The Manila Galleons ("1565–1815 · Manila › Acapulco").
- Discover a place by solving one of its ingredients; master it by solving all of them.
![atlas](/static/img/projects/kitsniff/atlas.png?v=1)
### The Résumé
- What the game has learnt about you: a Palate Profile radar, your Opening Gambit, your Nemesis (slowest solve) and Sidekick (fastest).
![palate](/static/img/projects/kitsniff/palate.png?v=1)

---
 
## Part four: the accolade wall
 
- 43 accolades, each with its own emoji. Nothing is hidden, and every one counts towards the Michelin star — so none can be too obscure for an ordinary player to earn.
- Show a dozen in a small table, grouped:
  - **Skill:** Hole in One ⛳️, Clairvoyant 🔮, Truffle Hound 🐕
  - **Habits:** Groundhog Day 🐿️, Thyme Lord ⏳ (guess tomorrow's answer today), Yesterday's News 📰
  - **Collection:** Pantry Perfectionist 📜, Master Chef 🧑‍🍳, Merchant Venturer 🧭
  - **Mischief:** Breaking the Fourth Wall 🎮, Custard Conundrum 🍮, The Idiot Sandwich 🥪, Rhubarb, Rhubarb 🎭, The Basilisk 🐍
  - **The calendar:** Sunday Roast 🍖, Shrove Tuesday 🥞 ("any Tuesday will do"), The Anniversary Dinner 🎂
![accolades](/static/img/projects/kitsniff/accolades.png?v=1)

---
 
## Part five: the Guide (the endgame)
 
### Being scouted
- The morning after a new player's first solve, a letter: "A new kitchen opened on… and served [ingredient] on its first night."
- More letters as the wall fills: *A Note from the Guide*, then *A Kitchen on the Rise*.
### The inspection
- Complete the wall and an inspector books a table. The post-game tells you they're coming; the letter arrives on your next visit, however long you've been away.
- "They booked under a name nobody believed, ate everything put in front of them, and said very little, which in our profession is high praise." Button: *Frame it.*
![guide](/static/img/projects/kitsniff/guide.png?v=1)
### The ladder
- ★ every accolade on the wall — yours for good.
- ★★ thirty hint-free solves in a row (days you play, not calendar days).
- ★★★ all of that, plus every recipe in the book.
### Losing stars
- Stars above the first can be taken away, and the letter says exactly when and why: "our inspector was seated by the pass and watched you reach for a hint." A walked-out game: "The plates were still warm."
- New recipes added under three stars arrive as *A Revised Menu*: seven services to cook them before the third star goes back in the drawer.
- Finish the wall just as a new accolade appears: *Inspection Postponed*, signed "Yours, with napkin still tucked".
### Your Post
- Every letter is kept, written as it read on the day it was sent.
---
 
## Part six: days that aren't like the others
 
- **13 May, KitSniff's birthday:** birthday greetings all day, the Anniversary Dinner accolade, and a personal Year in Review (your first ever guess, judged: "Straight for the meat. Bold.").
- **Sundays and Tuesdays:** Sunday Roast and Shrove Tuesday.
- Check: are Halloween/Christmas themed days still live? Only the birthday is in the current code.
---
 
## Kitchen notes
 
Intro: the odd corners, the special cases, and the decisions that took longer than they should have.
 
### Horseradish, the ingredient that won't pick a lane
- The only guess that genuinely means two things (Root, a vegetable; Sauce, a condiment).
- The game infers which from the clues you've already earned; if it can't, it asks.
- The disambiguation system is built to be general and has exactly one entry. The modal copy is horseradish-specific on purpose.
![horseradish](/static/img/projects/kitsniff/horseradish.png?v=1)
### Everyone opens with Basil
- Players independently converged on Basil as the best opening guess.
- The game noticed: "Basil regulars" (three of their last five games) get their own greetings ("Basil again? Groundbreaking." / "Live dangerously. Type 'Oregano'.") and flash messages ("The Basil Strategy™ — patent pending.").
- The Basilisk 🐍 for fifty Basil openers — the accolade that drags people into the easter egg. Features feeding each other.
- Basil stays unique; deliberately not expanded to other ingredients.
### Apples are red, kiwis are green
- No single colour rule works. Closest was "skin if you eat it, inside if you don't" — until bananas and apples. Settled on *the colour you'd most associate with it*.
- Then the fix for the fallout: secondary colours and the mismatch modal. Type "green apple" and you're always warned; type "apple" while you know the answer is green and you're warned; know nothing yet and it just goes through.
- "In KitSniff's pantry, apple is filed under Red. The committee was unavailable for comment."
![disambiguation](/static/img/projects/kitsniff/disambiguation.png?v=1)
### From typo to guess
- What happens between pressing Enter and getting feedback: the KitSniff easter egg, category words ("cheese is a category"), exact names, aliases, horseradish, then fuzzy matching (similarity, short-word edit distance, common typo patterns), with guards against over-eager corrections.
- Recount the stages for the piece — the code has roughly a dozen gates now.
- The bug that became a feature: fuzzy matching kept turning custard into mustard, so it became an accolade. "🍮 Custard? Mustard! Common mistake... or is it?"
- Type one letter: "You unlocked the 'Single Letter Hacker' badge. Unfortunately it does nothing."
- Guesses the game doesn't know land in an admin inbox, where they become aliases or new ingredients — players write the dictionary.
### Rhubarb, rhubarb
- The one ingredient you're allowed to guess twice ("The extras thank you for your service."). A third time: "That's quite enough rhubarb."
### Please do not fix this
- Marmite and the Larder: guess it, earn *Love It or Hate It*.
- Some accolades are swept up retroactively when you sign in. This one never is, and the code says so in a box: everyone starts fresh on their next Marmite. "The omission is the feature."
### Choosing the answer, part one: the rotation
- Truly random felt bad: repeats, and two cheeses in a row.
- Weight = days since last seen, squared. Never-seen ingredients get a boost. Nothing repeats within 90 days. Penalties for sharing a food group, colour or flavour with recent answers.
### Choosing the answer, part two: the wanted list
- The problem: Pantry Perfectionist gates the star, and a missed ingredient came back after a median of ~276 days.
- Simulations: a near-perfect player still spent a year waiting on the tail.
- The fix: players close to a full pantry make some days "wanted days", drawn from what they still need. 25% per end-game player, capped at 40%. Drift away for a week and you stop pulling.
- Result: last 2 ingredients ~227 days → ~9; last 15 ~329 → ~53. Invisible to players.
- Show the before/after table.
### How hard is Fiendish?
- Difficulty from real solve data, recomputed nightly, split into seven equal-sized buckets so every label gets used.
- Why the obvious approaches failed (everything piling into the middle).
### Recipes are a matching problem
- Recipes mix named ingredients with rules ("any cheese", "three pink things"). One guess can satisfy two lines, but it can only count once.
- The game solves it properly (a maximum matching), so your guesses always go where they're needed. Find a real recipe where a naïve check would fail.
- Balancing: a traditional Ratatouille would need six ingredients and nobody would ever cook it. Trimmed to three.
### A game that doesn't nag
- No solve streaks shown. Stars count days you play, not calendar days. Letters arrive when you come back, at most one a morning. End-game players who stop playing stop steering the puzzle.
- The design thread through the whole endgame: never punish absence.
### Kale is not Swiss chard
- The March 2026 provenance audit: origin stories had wandered between ingredients. Kale was "also known as Swiss chard, first cultivated in Sicily"; the artichoke came from the Yangtze River Delta.
- Every one fact-checked and rewritten.
### Pork is Turkish
- Tagging the Atlas: origin vs "also at home in" vs "carried by". Tomato: Mesoamerica, also at home in Italy. Pork stays on Turkey (wild boar domestication in Anatolia).
- Why a one-ingredient place (the Banda Islands) can't be "mastered", and the handwritten mark it gets instead.
---
 
## Reserve shelf
Candidates if you want more; each could be a short entry or folded into another.
 
- **Signing in halfway through lunch** — guest games carried into a new account, and late claims onto legacy accounts. The play / sign out / play again / sign in case.
- **The Idiot Sandwich** — bread, not-bread, bread.
- **Breaking the fourth wall** — guess "KitSniff": scanlines, inversion, "REALITY BREACH DETECTED".
- **Thyme Lord** — guess tomorrow's answer today. Renamed from The Time Traveler; the old name lives on in the code.
- **Forgetful Sniffer** — why only the first letter counts.
- **The trading-card principle** — type, rarity, state; collector numbers that are database ids (so the tables can never be reseeded). Doubles as the planned Reddit post.
- **@KitchenSniffle** — the daily social posts, written from yesterday's stats in the game's voice.
- **Under the bonnet** — one closing line on the stack, if anything (Flask, PostgreSQL, a Pi for dev, Railway for prod).
