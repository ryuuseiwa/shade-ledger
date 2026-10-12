---
title: "Shade Ledger: I built a local AI that sends me outside to audit neighborhood shade"
published: false
tags: devchallenge, hf26challenge, ai, opensource
---

*This is a submission for the [Hacktoberfest Open-Source AI Challenge Week 1: Touch Grass](https://dev.to/challenges/hacktoberfest-week1-2026-10-05).*

## What I Built

I built **Shade Ledger**, a small fieldwork companion that deliberately tries to get out of your way. Instead of tracking every step or asking you to keep your phone in hand, it creates a short, personalized outdoor mission and asks you to come back with a few observations about your neighborhood. The inspiration came from thinking about how city design, the environment, and everyday decisions overlap: shade and greenery aren't only nice to look at; they're things worth noticing.

Choose your time, accessible movement style, and topic (shade, biodiversity, stormwater, or public-space care). Your laptop's local AI creates three steps and three things to notice. Then you leave the screen. When you return, you can create a tiny "field receipt" and compare what you saw on future visits. Shade share is explicitly a rough count of observed stops, **not** a measured heat or canopy metric.

## Demo

**[ADD: a short screen recording/GIF of local mission generation and saved field receipt.]**

**[ADD: one real photo/video from your field test, if comfortable.]**

Local setup and demo instructions are in the README. A public hosted demo isn't available because the app is designed for local inference and local storage.

## Code

**[ADD YOUR GITHUB REPOSITORY URL AFTER PUSHING]**

## How I Built It

The interface is Streamlit; the AI engine is the **Apache-2.0-licensed Qwen2.5 1.5B Instruct** open-weight model running locally via Ollama. `engine.py` builds a safety-constrained, mobility-aware prompt and requests actual structured JSON generation via Ollama's local endpoint. Schema checks reject incomplete results. The model—not a predefined list of trips—creates the actual mission. `app.py` manages the UI and writes local JSONL observations. Small deterministic functions compute a transparently labeled shade-stop percentage.

My architecture is simple: **user preferences → Python prompt → local Ollama/Qwen model → validated mission → get outside → local observation receipt.** No account, GPS, paid API, or cloud database is necessary.

## Why Does Open Innovation Matter?

I wanted a tool that can help me pay attention to my surroundings without sending my location-related habits and reflections to an outside provider. Once I install the model, mission generation can run without internet. Open weights make it practical to change models, edit the prompting, experiment with smaller hardware requirements, and inspect how the AI is used instead of depending on a closed remote API. There's no per-mission API fee. Setup downloads and compute still have costs.

More importantly, making the fieldwork logic inspectable means the app can be adapted for a campus accessibility walk, local stormwater observations, or a neighborhood green-space journal without changing the core idea: **less screen time, more real-world attention.**

## What Happened When I Took It Outside

**[FILL IN ONLY AFTER YOU REALLY TEST OUTDOORS: date, place at a broad level, how long you spent, what you observed, what surprised you, and one thing you would change.]**

## My Agent Session

**[OPTIONAL: add a real DevRelay session embed/link if you record one.]**

## Prize Categories

**[OPTIONAL: identify only eligible categories confirmed from the official challenge page.]**
