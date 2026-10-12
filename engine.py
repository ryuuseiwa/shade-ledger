"""Local-only open-weight mission generator and deterministic field scoring."""
from __future__ import annotations
import json
import urllib.request
import urllib.error
from dataclasses import dataclass, asdict

MODEL = 'qwen2.5:1.5b-instruct'
ENDPOINT = 'http://127.0.0.1:11434/api/generate'

@dataclass
class MissionInput:
    minutes: int = 15
    environment: str = 'Neighborhood sidewalks'
    mobility: str = 'Walking'
    focus: str = 'Shade & urban heat'
    energy: str = 'Low-key'
    city_context: str = 'Warm climate'


def build_prompt(spec: MissionInput) -> str:
    return f'''You are Shade Ledger, a privacy-first outdoor micro-fieldwork guide.
Create a fresh, specific, SAFE outdoor field mission that takes {spec.minutes} minutes including observations.
Setting: {spec.environment}; movement/accessibility: {spec.mobility}; interest: {spec.focus}; energy: {spec.energy}; climate: {spec.city_context}.
Return ONLY one valid JSON object with exactly these keys:
"title" (max 9 words), "mission" (2 short sentences), "steps" (array of exactly 3 short imperative strings),
"notice" (array of exactly 3 observable, non-technical things), "reflection" (one question).
Keep it within public, accessible areas. Never recommend entering roads, trespassing, touching unknown plants/animals, collecting samples, or going outside during unsafe weather. Do not invent local routes, species, temperatures, air quality, or safety conditions. Favor observation over phone use. No buying, GPS, login, or internet required. Return JSON only.'''


def parse_mission(raw: str) -> dict:
    raw = raw.strip()
    if raw.startswith('```'):
        raw = raw.split('\n', 1)[1].rsplit('```', 1)[0].strip()
    obj = json.loads(raw)
    required = {'title': str, 'mission': str, 'steps': list, 'notice': list, 'reflection': str}
    if not isinstance(obj, dict) or any(not isinstance(obj.get(k), t) for k, t in required.items()):
        raise ValueError('Model response did not match mission schema')
    if len(obj['steps']) != 3 or len(obj['notice']) != 3 or any(not isinstance(x, str) for x in obj['steps'] + obj['notice']):
        raise ValueError('Expected three steps and three observations')
    return {k: obj[k] for k in required}


def generate_mission(spec: MissionInput, model: str = MODEL, timeout: int = 95) -> dict:
    payload = json.dumps({'model': model, 'prompt': build_prompt(spec), 'stream': False,
                          'format': 'json', 'options': {'temperature': 0.65, 'num_predict': 450}}).encode()
    request = urllib.request.Request(ENDPOINT, payload, {'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            data = json.load(response)
    except (urllib.error.URLError, TimeoutError) as exc:
        raise RuntimeError('Cannot reach Ollama locally. Start Ollama and pull the selected model first.') from exc
    return parse_mission(data.get('response', ''))


def shade_score(shaded: int, total: int) -> int | None:
    """Observational proxy, NOT temperature/carbon measurement."""
    if total <= 0 or shaded < 0 or shaded > total:
        return None
    return round(100 * shaded / total)


def local_summary(shaded: int, total: int, green: int, water: int) -> str:
    score = shade_score(shaded, total)
    if score is None:
        return 'Add at least one valid observation.'
    return (f'{shaded} of {total} observation stops felt shaded ({score}%). '
            f'You noticed {green} planted/permeable-surface areas and {water} water or drainage features. '
            'This is a personal observational snapshot, not a scientific temperature or carbon assessment.')
