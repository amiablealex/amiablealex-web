---
title: Chess Storyteller
category: Web app
accent: teal
summary: "A web app that transforms chess games into calm, descriptive narratives by 
feeding a chess PGN file through an LLM API."
date: 2026-04
featured: false
cover: chess-storyteller/cover.png
links:
  - label: "GitHub"
    url: "https://github.com/amiablealex/chess-storyteller"
    icon: brand-github
tech: [Python, Flask, API, Prompt Engineering, LLM]
---


## What this is

A self-hosted web app that transforms chess games into calm, descriptive narratives. Feed 
it a chess PGN file and stockfish analyses the game, then an LLM weaves the evaluation into 
a human narrative / storytelling script with rich positional language and creative descriptions. 

## Architecture

- Deliberate evaluation / creative separation: Stockfish integrated into the app and runs locally for deterministic analysis (the same output every time). The LLM does only the creative writing because it is probabilistic and can sometimes be wrong.
- From testing different AI models, Claude Sonnet came out as the best for creative voice quality, also happens to be fairly cost efficient.
- Codebase structure has prompt templates stored as plain text files and editable without touching the application code. Ended up being very useful as prompt iteration became the main development activity.

## Prompt Engineering

### Problem: LLMs can't keep track of board state

The LLM processes the game as text; it doesn't know exactly where all the pieces are at move 27. Sometimes it would fabricate, e.g a queen "captures a rook" when it didn't. Ocassionally the story would recall events in the wrong sequence and moves would get reordered. After exchanges of pieces, the LLM would invent what's left on the board.

Giving key moves in the analysis obvious and human-readable text flags hugely improved the quality and accuracy: "THIS IS A CAPTURE", "THIS GIVES CHECK", "GAME ENDS (checkmate)". This significantly reduced LLM hallucination; it was basically trying to guess the common areas the LLM would be likely to make something up and 'tagging' these moments with the correct information. e.g adding material snapshots after every capture "White now has 2 rooks, 1 knight, 5 pawns | Black now has 1 queen, 1 bishop". A useful prompt addition: *"it is better to describe a move vaguely than to describe it with incorrect tactical detail."*

### Problem: bishops and perspective

The LLM kept getting bishop colours wrong, for example "we move our light-squared bishop to b2" (b2 is always a dark square and so it must have been the dark-squared bishop that moved there). The LLM can't determine square colour from a grid reference, so it seemed to just guess a colour when it wanted to weave it into the story context. The fix was adding a function that calculates bishop colour from coordinates and labels each one as LIGHT-SQUARED or DARK-SQUARED in the data. Capitalising the labels also seemed to make the LLM more likely to respect the label. Even so, it occasionally overrides explicit labels with its own wrong reasoning.

The perspective problem was similar. PGN files don't say who exported them, so I had to add functionality to tell the storyteller which side to narrate from. I did it by auto-detecting based on player usernames against a configured username list, and then a manual override in the UI to choose which perspective to analyse from (black or white).

### Problem: leading the witness

This was the most recurring issue and the most instructive.

Every time there was example language in the prompt to inspire and guide the creativity angle, the LLM leaned on those exact words. For example, "A pawn chain is a wall, a fortress, a spine" resulted in every pawn chain always being described as a wall or a fortress. "A knight on the rim is lonely, exiled" meant that every rim knight was described as lonely and exiled. Fixed personality archetypes for pieces meant every knight was restless, every bishop was patient, in every game.

The fix was to be a lot more generic and vague in the prompt descriptions, and making the brief much more open e.g *"draw from unexpected places"*. And repurposing any explicit metaphor examples to things along the lines of "you should find your own language for this each time."

The premise ended up being to never dictate creative vocabulary, and only constrain what must be factually accurate.

### Problem: confident nonsense about missed moves

The stockfish engine can flag bad moves as a 'mistake', which can be useful for the storytelling context. But when this happened, the LLM would acknowledge the mistake and then invent what the better move was. e.g *"the queen should have recaptured"* when the queen wasn't even in range.

The LLM doesn't understand chess positions well enough to reason about alternatives, so the fix was to constrain it and not let it try. i.e when a move is flagged as a mistake, direct instruction to only say that "a better path existed", and to never expand further on what the better move was (which piece or where). 

### Summary

There's a balance between accuracy and creativity. Strict rules prevent hallucination and factual inaccuracies but constrain the creative voice.
