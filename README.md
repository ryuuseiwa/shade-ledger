# 🌿 Shade Ledger — Less scrolling. More noticing.

**An outdoor-first, privacy-first neighborhood fieldwork app powered by an open-weight model running on your laptop.** Designed for the Hacktoberfest 2026 Open-Source AI Challenge, Week 1: Touch Grass.

## What makes it different

Most outdoors apps turn a walk into more screen time, tracking, and GPS. Shade Ledger uses a **local LLM to design a 5–30 minute mini field mission**, then sends you outside to notice shade, plantings, storm drains, and other neighborhood details. On return, make a 60-second **field receipt** and learn how to compare your own observations over time. No GPS, login, paid API, location history, server database, or image upload.

**A city-planning / environmental-justice-inspired field journal, not a scientific instrument.** The app does not infer measured temperatures, carbon capture, canopy cover, or safety from observations.

## How open-source AI powers it

- **Model:** `qwen2.5:1.5b-instruct` (open-weight, Apache 2.0) running through Ollama.
- **Inference:** locally at `127.0.0.1:11434` using Ollama's `/api/generate` endpoint.
- **Generation is real:** the model builds an individual mission from mobility, minutes, theme, climate context, setting and energy. **No model = no mission** (a clear setup error, not a secretly hardcoded response).
- **Inspectable:** prompts, JSON schema validation, scoring logic and storage are plain Python; swap any installed Ollama model from the sidebar.
- **Privacy:** missions and note data are handled on your computer; data remains in `data/field_notes.jsonl`. No web or GPS calls by the app. Initial installation/model download DOES require internet. The app uses system fonts and does not load third-party fonts.

## Windows + VS Code quick start

**1. Install Ollama:** https://ollama.com/download/windows and open Ollama. In VS Code terminal (PowerShell):

```powershell
ollama pull qwen2.5:1.5b-instruct
```

This downloads ~1 GB once. Test with `ollama list`. If not running, launch Ollama. A model is required.

**2. Open this folder in VS Code** (File → Open Folder). Run:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

If script activation is blocked, run `.\.venv\Scripts\python.exe -m pip install -r requirements.txt` then `.\.venv\Scripts\python.exe -m streamlit run app.py` instead. On macOS/Linux: `python3 -m venv .venv && source .venv/bin/activate` and proceed with `python` commands.

**3. Open the local link** Streamlit shows (`http://localhost:8501`), generate a mission, go outside, return, record what you noticed.

## Demo flow (90 seconds)

1. Show the local model in `ollama list` and the app sidebar.
2. Pick **15 minutes**, **Neighborhood sidewalks**, **Shade & urban heat**, **Low-key**. Generate a mission; show its 3 actionable steps and 3 observation prompts.
3. Close the screen and physically go outside (record a 5–10-second video clip if safe).
4. Return, open **Field receipt**, log four stops with two shaded, and see 50% **observed shade share** (a stop-count proxy only).
5. Save. Open **My local ledger** and show the observation is stored and exportable without any account.
6. Disconnect Wi-Fi AFTER setup, repeat mission generation to demonstrate local inference.

## Safety / limitations

- **Always check weather/heat and local advisories independently.** No real-time weather, emergency info or street safety is provided.
- Never navigate traffic, trespass, inspect during unsafe weather, or collect/touch unknown wildlife or plants.
- AI can occasionally return an imperfect mission; review it before going outside. The model's output is JSON-validated, but safety is not guaranteed.
- The ledger is individual and exploratory, not a source of standardized environmental measurements.
- To remove personal notes, delete `data/field_notes.jsonl`. The `data/` folder is git-ignored.
- Ollama must be installed and the selected model downloaded. Streamlit runs locally; it is **not** a hosted web deployment, and no public live demo URL is provided.

## Project structure

```
shade-ledger/
├── app.py                 # Streamlit UI, receipt & ledger
├── engine.py              # Real Ollama call, structured mission schema, score
├── requirements.txt
├── .streamlit/config.toml  # Green theme
├── tests/test_engine.py   # Unit tests
├── DEV_SUBMISSION.md      # Draft DEV entry (customize after actual demo)
├── DEMO_CHECKLIST.md      # Test and recording checklist
├── .gitignore             # Prevent accidental sharing of field notes
└── README.md
```

## Run checks

```powershell
python -m unittest discover -s tests -v
python -m py_compile app.py engine.py
```

## Why not a closed API?

No key, inference fees, or transmitting the user's environment and observational reflections to a third-party model API. It also stays functional without connectivity **after installation**, and the model can be replaced and the behavioral prompt changed without asking a vendor. This is an architectural benefit, not a claim of benchmarked superiority or zero electricity/hardware cost.

## Credits / licenses

Application code: MIT (see LICENSE). Model weights: Qwen2.5 1.5B Instruct, Apache-2.0 per [Ollama model listing](https://ollama.com/library/qwen2.5:1.5b-instruct) and [Qwen license](https://huggingface.co/Qwen/Qwen2.5-1.5B/blob/main/LICENSE). Ollama and Streamlit have their own licenses. No model weights bundled.
