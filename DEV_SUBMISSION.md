---
title: "Shade Ledger: A Local AI That Sends You Outside to Notice Neighborhood Shade"
published: false
tags: devchallenge, hf26challenge, ai, opensource
---

*This is a submission for the [Hacktoberfest Open-Source AI Challenge Week 1: Touch Grass](https://dev.to/challenges/hacktoberfest-week1-2026-10-05)*

## What I Built

**Shade Ledger** is a small fieldwork companion that tries to get out of your way. Most outdoor apps turn a walk into more screen time: step counts, GPS trails, notifications. Shade Ledger does the opposite. It asks a locally running open-weight model to design a short, personalized outdoor mission, tells you to close your laptop, and then waits for you to come back with a few observations about your neighborhood.

You pick how long you have (5–30 minutes), where you can go, how you'll explore (walking, a slow stroll, a wheelchair-friendly route, or seated observation), what you want to notice (shade and urban heat, trees and biodiversity, rainwater and drainage, urban nature, or public-space care), your pace, and a rough climate context. The model returns a mission with three steps, three things to notice, and one question to think about later.

When you get back, you fill in a 60-second **field receipt**: how many stops you made, how many felt shaded, how many planted or permeable surfaces and drainage features you spotted, and how being outside felt. It's saved to a local ledger so you can compare visits over time.

It's for anyone who wants a gentle reason to step outside and pay attention, and especially for people curious about how city design shapes everyday comfort. Shade and greenery aren't just nice to look at; they're worth noticing. To be clear about what it isn't: the "shade share" is a simple count of the stops you chose, **not** a measurement of temperature, canopy cover, or environmental impact.

## Demo

Shade Ledger is designed for local inference and local storage, so there's no hosted version. These screenshots are from the app running on my machine against the local Qwen2.5 model:

**A mission generated locally by Qwen2.5 1.5B via Ollama:**

![Shade Ledger generating an outdoor mission with a local model](https://raw.githubusercontent.com/ryuuseiwa/shade-ledger/main/docs/02-mission.png)

**The field receipt you fill in when you come back (shown with example values):**

![Shade Ledger field receipt showing a 50% observed shade share](https://raw.githubusercontent.com/ryuuseiwa/shade-ledger/main/docs/03-field-receipt.png)

To run it yourself, setup takes a few minutes and is described in the README.

## Code

{% github ryuuseiwa/shade-ledger %}

## How I Built It

- **Model:** [Qwen2.5 1.5B Instruct](https://ollama.com/library/qwen2.5:1.5b-instruct), an Apache-2.0 open-weight model, running locally through **Ollama**.
- **Inference:** a plain HTTP call to Ollama's local `/api/generate` endpoint at `127.0.0.1:11434`, using Ollama's JSON mode for structured output. On my desktop (AMD RX 7900 GRE), a mission comes back in about 3 seconds.
- **Prompting:** `engine.py` builds a safety-constrained, mobility-aware prompt from your choices. It tells the model to keep you in public, accessible areas, never to suggest entering roads, trespassing, touching unknown plants or animals, or going out in unsafe weather, and not to invent routes, species, temperatures, or safety conditions.
- **Validation:** the response is parsed and checked against a strict schema (a title, a mission, exactly three steps, exactly three things to notice, and a reflection question). Anything malformed is rejected with a clear error.
- **No fake fallback:** if the model isn't available, the app says so. There's no hardcoded list of canned missions pretending to be AI.
- **UI and storage:** Streamlit for the interface; field receipts are appended to a local JSONL file that's git-ignored, viewable in the app, and exportable as JSON.
- **Tests:** unit tests cover the schema validation, the scoring, and the prompt builder.

The whole flow is: **your preferences → prompt → local Qwen model → validated mission → go outside → local field receipt.** No account, GPS, paid API, or cloud database.

## Why Does Open Innovation Matter?

Where you walk and what you notice about your own neighborhood is personal. With an open-weight model running on my own machine, none of that leaves my computer. Once the model is downloaded, mission generation works with Wi-Fi off.

Open weights also make the project adaptable. Anyone can swap in a different Ollama model from the sidebar, rewrite the prompt, or run it on smaller hardware, without asking a vendor or paying per request. Because the prompt, validation, and scoring are all plain, inspectable Python, the same idea could be reshaped into a campus accessibility walk, a stormwater observation log, or a neighborhood green-space journal.

A closed API would have meant an account, a key, a per-mission cost, and sending people's reflections about their surroundings to a third party. For an app whose whole point is *less* screen and *more* attention, keeping the AI small, local, and open felt like the right fit.
